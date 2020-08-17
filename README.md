# Recommendations data.gouv.fr manuelles

Ce dépôt permet de définir des recommendations manuellement sur data.gouv.fr à l'aide du plugin [udata-recommendations](https://github.com/opendatateam/udata-recommendations).

Vous pouvez définir des recommendations en éditant le fichier YAML [recommendations.yml](recommendations.yml).

## URL

Les recommendations de ce dépôt sont disponibles en JSON à l'adresse https://etalab.github.io/recommendations-edito/recommendations.json

## Exemple

Vous souhaitez voir apparaitre 2 recommendations sur le jeu de données https://www.data.gouv.fr/fr/datasets/jours-feries-en-france/. Vous pouvez indiquer ces 2 autres jeux de données de la manière suivante.

```yaml
-
  source: https://www.data.gouv.fr/fr/datasets/jours-feries-en-france/
  recommendations:
    -
      id: https://www.data.gouv.fr/fr/datasets/repertoire-national-des-certifications-professionnelles-et-repertoire-specifique/
      score: 50
    -
      id: https://www.data.gouv.fr/fr/datasets/municipales-2020-resultats-2nd-tour/
      score: 50
```
