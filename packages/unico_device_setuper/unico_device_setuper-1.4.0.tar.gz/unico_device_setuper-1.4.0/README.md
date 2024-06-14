### How 2 install ?

-   Avoir un mac
-   Ouvrir un terminal
-   Installer <a href="https://brew.sh" class="external-link" target="_blank">Homebrew</a>:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

-   Vérifier l'installation de Homebrew:

```bash
brew --version
```

-   Installer <a href="https://pipx.pypa.io/stable/" class="external-link" target="_blank">Pipx</a>:

```bash
brew install pipx
```

-   Vérifier l'installation de Pipx:

```bash
pipx --version
```

-   Mettre à jour le path:

```bash
pipx ensurepath
```

-   Ouvrir un nouveau terminal

-   Installer <a href="https://gitlab.com/unico-dev/device-setuper" class="external-link" target="_blank">device-setuper</a>:

```bash
pipx install unico_device_setuper
```

-   Vérifier l'installation device-setuper:

```bash
device-setup --version
```

---

### How 2 mettre à jour ?

```bash
pipx upgrade unico_device_setuper
```

---

### Utilisation

-   Ouvrir un terminal

```bash
device-setup
```

-   Se laisser guider 🧑‍🦯‍➡️

---

### Faire tourner en local

-   Suivre les étapes <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ" class="external-link" target="_blank">plus haut</a> pour installer Pipx
-   Installer <a href="https://python-poetry.org" class="external-link" target="_blank">Poetry</a>:

```bash
pipx install poetry
```

-   Clone le répo:

```bash
git clone git@gitlab.com:unico-dev/device-setuper.git && cd device-setuper
```

-   Installer les dépendances:

```bash
poetry install --with dev
```

-   Créer puis (probablement me demander pour) remplir le fichier d'environement:

```bash
touch config.toml
```

-   Pour lancer le backend:

```bash
device-setuper-backend
```

-   Pour lancer la cli:

```bash
device-setup
```
