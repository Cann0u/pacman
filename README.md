# pacman
the pacman project from 42 cursus 

🔴 Bloquants qu’il reste
Commentaires de config : # et // font rejeter toute la config, et le jeu retombe sur les défauts. C’est le point le plus important, car la config sera changée pendant la défense.
README.md : il contient en ce moment mon rapport collé tel quel, pas un vrai README. Il faut la 1re ligne en italique avec les logins, et les sections Description, Instructions, Resources (avec l’usage de l’IA), Configuration, Highscore, Maze Generation, Implementation, General Software Architecture et Project Management.
Dossier de gestion de projet : il n’existe pas.
Packaging et déploiement itch.io/Steam : rien n’est fait, et le .gitignore contient toujours *.spec.
Highscore sur clone propre : FileNotFoundError en fin de partie si score/ n’existe pas. Il est dans le .gitignore et rien ne crée le dossier. Ajoute un os.makedirs(..., exist_ok=True) avant d’écrire.
Lancement depuis un autre dossier : traceback FileNotFoundError: font/ARCADE_N.TTF. Il reste les chemins relatifs font/…, sprite/canvas.png et score/score.json (les sprites sont déjà corrigés via Path(__file__)).
Usage : sans argument, le jeu affiche toujours « Hello from pacman! », « To few argument » et uv run …, puis sort avec le code 0.
🟠 Non-conformités fonctionnelles qu’il reste

Config

level_max_time : 30 devient 90 sans message (le=10 dans le parser).
points_per_ghost n’est toujours pas utilisé (200 * multiplicateur en dur, pacman.py:146).
Les valeurs invalides sont remplacées sans aucun message.
Une seule erreur jette toute la config, et le message est du pydantic brut avec la faute « loding ».
Il n’y a pas de vérification de l’extension .json.

Highscore

Rejouer avec le même nom écrase le meilleur score (5000 puis 10 donne 10).
Un nom vide est accepté.
Les espaces sont ignorés dans la saisie ("a b" devient "ab").
Le backspace ne fait rien.
Le préfixe "duo " dépasse les 10 caractères.
Les noms lus dans le fichier ne sont pas validés.
Ton score.json contient des noms avec des caractères d’échappement, une chaîne vide et « merde ». Nettoie-le avant le rendu.

Écrans

L’écran de fin n’affiche toujours pas le score final, et il n’y a pas de message de félicitations.
L’écran d’instructions est faux (s = droite, d = bas) et ne mentionne ni ÉCHAP, ni C, ni P.
Les libellés du menu sont 1 PLAYER, INFO, HIGHSCORE, EXIT, alors que le sujet parle de Start Game, View Highscores, Instructions, Exit. C’est un point mineur.

Timer

Le chrono continue pendant la pause.
À la fin du temps, c’est game over en 3 frames, sans message.

Contrôles

En 1 joueur, les flèches ne marchent pas (seul WASD fonctionne), ce qui est un problème sur clavier AZERTY.

Cheat mode

C et P restent actifs en permanence, sans indicateur ni documentation, et le level skip et le ghost freeze n’existent pas.

Niveaux

Il n’y a que 42 pacgums, alors que le sujet demande « most corridors ».
Leur placement utilise random.randint non seedé (game.py:367).
La génération du labyrinthe n’est pas protégée par un try/except.
perfect=False n’est pas passé explicitement.

Bibliothèque graphique

pygame contre « MLX or similar » reste à confirmer avec le staff.
🟡 Hygiène et qualité qu’il reste
Docstrings : 1 seule sur 119 fonctions et classes, alors que le sujet les demande en PEP 257.
pydantic n’est toujours pas déclaré dans pyproject.toml.
Il n’y a toujours pas de .flake8 avec exclude (il y a --exclude dans le Makefile, mais un flake8 . lancé à la main lint ton .venv).
Les fichiers .DS_Store, arcade_ya.zip et Readme.TXT traînent à la racine.
Il reste du code mort : self.score += 10 dans eat_pacgum (pacman.py:43), pygame.RESIZABLE seul sur une ligne (render.py:18), des w_x, w_y inutilisés, et le print("Hello…").
Il n’y a aucun test (recommandé, non noté).