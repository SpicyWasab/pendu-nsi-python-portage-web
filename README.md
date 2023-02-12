# Portage du pendu sur le web

Pour rendre le projet plus accessible, j'ai eu l'idée d'utiliser [pyscript](https://pyscript.net/) pour porter ce jeu sur le web.

La page web tourne une version **non modifiée** du code original.

Cependant, j'ai dû mettre en place quelques lignes de code en plus, à part, pour faire en sorte que cela fonctionne.

## Difficultés

### mots.txt

Web oblige, pyscript ne pouvait pas lire le fichier `mots.txt` car il n'avait pas connaissance de son existence.  
En effet, pyscript dispose d'un système de fichier MEMFS reprenant une partie de la structure des systèmes de fichiers linux. Le dossier utilisateur, dans lequel on se trouve au départ, est par défaut vide.  
Le jeu ne fonctionne donc pas. Il a donc fallu récupérer son contenu avec JavaScript, et le rendre accessible à pyscript comme suit :

```js
    globalThis.words = await fetch('mots.txt')
        .then(res => res.text());
```

Dans ces deux lignes, on récupère le contenu de "mots.txt", et on le place dans le contexte global (`globalThis`, équivalent de `window`). Cela est nécessaire car pyscript permet d'importer n'importe quel élément du contexte global dans le contexte python grâce à l'instruction `import js`.

On peut donc ensuite créer le fichier avec pyscript :

```py
    from js import words

    file = open('mots.txt', 'w') # crée et ouvre le fichier
    file.write(words) # écrit dans le fichier
    file.close() # ferme le fichier
```

Le fichier est désormais accessible.

### print et input

Par défaut, les messages de `print` sont affichés dans le corps de la page, alors que la fonction `input` affiche une popup, similaire au `prompt` de JavaScript.  
En revanche, cela interrompt le programme. On ne voit donc pas les affichages de print sur le corps de la page.  
De plus, `input` ne montre pas le message spécifié à l'utilisateur.

J'ai donc décidé de surcharger les fonctions `print` et `input` pour pallier à ces problèmes. `print` utilise la fonction javascript `alert`, alors qu'`input` utilise la fonction `prompt`, en affichant le message :

```py
# on importe les fonctions JavaScript alert et prompt
from js import alert, prompt

def print(*args):
    # print doit accepter plusieurs arguments, et les concaténer.
    message = ' '.join(str(e) for e in args)

    alert(message)

def input(message):
    answer = prompt(message)

    return answer
```

### Faire tourner le fichier python d'origine

À l'origine, le code était copié collé tel quel dans une balise `<py-script>`. Cependant, en faisant quelques ajustements mineurs dans le code, je me suis rendu compte que ça allait être ennuyeux à mettre à jour. J'ai donc fait en sorte que le code soit récupéré directement du fichier, et ajouté à la page :

```js
// on récupère le code
const pythonCode = await fetch('pendu.py')
            .then(res => res.text());

// on crée un élément <py-script>
const pyscriptElement = document.createElement('py-script')
// on le remplit avec le code
pyscriptElement.textContent = pythonCode;

// on l'ajoute à la page
document.body.appendChild(pyscriptElement);

console.log(pyscriptElement)
```

Ça a pris environ 3 minutes, mais je trouve que c'est beaucoup mieux et que ça rend l'idée beaucoup plus *cool* de faire tourner le code directement depuis le fichier python d'origine.

## Limitations

Les affichages de `print` se font les uns à la suite des autres à travers des popups, ce qui peut désorienter l'utilisateur.  
J'ai donc pris la liberté d'ajouter quelques prints supplémentaires dans le code pour plus de clarté. (par exemple, dire que l'utilisateur a bien trouvé le bon caractère, ce qui était implicite avec les étoiles et l'affichage du pendu)