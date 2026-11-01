# Archives des coupes de robotique

Archive des éditions de la Coupe de France de Robotique / Eurobot : règlements, plans, vinyles, modèles 3D,
images et texte des pages de présentation. Le but : garder une copie au cas où les sources disparaissent.

Chaque dossier `<année>-<thème>` contient un `README.md` (fichiers, origine, empreinte SHA-256, texte de la page source),
un dossier `fichiers/` et un dossier `images/`.

## Éditions

| Édition | Thème | Fichiers | Images | Taille |
|---|---|---|---|---|
| [1994](1994-sumo/) | Sumo | 0 | 1 | 823 Ko |
| [1995](1995-balloon-attack/) | Balloon Attack | 0 | 1 | 897 Ko |
| [1996](1996-gold-rush/) | Gold Rush | 0 | 1 | 454 Ko |
| [1997](1997-basket-ball/) | Basket-ball | 0 | 1 | 533 Ko |
| [1998](1998-le-football/) | Le football | 1 | 2 | 676 Ko |
| [1999](1999-castles/) | Castles | 1 | 2 | 182 Ko |
| [2000](2000-la-fete-foraine/) | La fête foraine | 1 | 2 | 2.4 Mo |
| [2001](2001-l-odyssee-de-l-espace/) | L'odyssée de l'espace | 1 | 16 | 1.9 Mo |
| [2002](2002-le-billard-aerien/) | Le billard aérien | 1 | 6 | 655 Ko |
| [2003](2003-pile-ou-face/) | Pile ou face | 1 | 13 | 1.7 Mo |
| [2004](2004-coconut-rugby/) | Coconut Rugby | 1 | 11 | 3.8 Mo |
| [2005](2005-le-bowling/) | Le bowling | 1 | 1 | 2.1 Mo |
| [2006](2006-funny-golf/) | Funny Golf | 1 | 1 | 2.9 Mo |
| [2007](2007-robot-tri-party/) | Robot Tri Party | 1 | 10 | 1.1 Mo |
| [2008](2008-mission-to-mars/) | Mission to Mars | 1 | 8 | 3.0 Mo |
| [2009](2009-temples-en-atlantide/) | Temples en Atlantide | 1 | 16 | 2.6 Mo |
| [2010](2010-feed-the-world/) | Feed the World | 1 | 19 | 11.2 Mo |
| [2011](2011-chess-up/) | Chess'Up | 1 | 26 | 2.8 Mo |
| [2012](2012-treasure-island/) | Treasure Island | 1 | 16 | 3.0 Mo |
| [2013](2013-happy-birthday/) | Happy Birthday | 1 | 10 | 5.2 Mo |
| [2014](2014-prehistobot/) | Prehistobot | 1 | 18 | 3.9 Mo |
| [2015](2015-robomovies/) | Robomovies | 1 | 14 | 4.6 Mo |
| [2016](2016-the-beachbots/) | The Beachbots | 1 | 12 | 10.8 Mo |
| [2017](2017-moon-village/) | Moon Village | 1 | 79 | 6.3 Mo |
| [2018](2018-robot-cities/) | Robot Cities | 4 | 35 | 18.1 Mo |
| [2019](2019-atom-factory/) | Atom Factory | 1 | 43 | 21.8 Mo |
| [2020](2020-sail-the-world/) | Sail the World | 3 | 2 | 22.0 Mo |
| [2021](2021-sail-the-world/) | Sail the World | 6 | 28 | 51.9 Mo |
| [2022](2022-age-of-bots/) | Age of Bots | 9 | 7 | 262.0 Mo |
| [2023](2023-the-cherry-on-the-cake/) | The Cherry on the Cake | 10 | 8 | 29.5 Mo |
| [2024](2024-farming-mars/) | Farming Mars | 5 | 4 | 72.5 Mo |
| [2025](2025-the-show-must-go-on/) | The Show Must Go On | 5 | 4 | 11.5 Mo |
| [2026](2026-winter-is-coming/) | Winter is Coming | 9 | 0 | 63.5 Mo |
| [2027](2027-the-legend-of-camelot/) | The Legend of Camelot | 9 | 0 | 57.0 Mo |

Total : 683.4 Mo.

## Sources

- [PM-ROBOTIX, les tables de jeux](https://www.pm-robotix.eu/accueil/les-tables-de-jeux/) : 1994 à 2025, fichiers sur leur site et leur Google Drive.
- [Eurobot](https://www.eurobot.org/) et [Coupe de France de Robotique](https://www.coupederobotique.fr/) : règlements officiels 2026 et 2027.

## Droits

Le texte cité des pages sources est repris tel quel. Les documents restent la propriété de leurs auteurs : Planète Sciences, Eurobot, PM-ROBOTIX.
Ce dépôt ne fait que les conserver, avec un lien vers leur origine.

## Outils

`outils/archive.py` refait l'archive à partir des pages HTML sauvegardées dans `sources/pm-robotix/`, `outils/index.py` régénère ce README.
