# MEDIQ – Crash Cart Intelligent

MEDIQ est un projet logiciel conçu dans le cadre d’un défi d’ingénierie biomédicale visant à réduire les erreurs médicamenteuses lors des situations de réanimation intra-hospitalière.

Le projet propose un **logiciel d’analyse clinique** capable de lire un fichier CSV contenant les signes vitaux et les médicaments administrés à des patients fictifs, puis de **détecter automatiquement des erreurs médicamenteuses potentielles**.  
L’objectif est de soutenir un **chariot de réanimation intelligent (crash cart)** en signalant rapidement les incohérences entre le médicament administré, la dose et l’état physiologique du patient. :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

---
## Captures d’écran
<p align="center">
  <img src="https://github.com/user-attachments/assets/4519802c-b83e-499f-955c-74815186123b" alt="Capture d’écran MEDIQ - alerte critique" width="49%" />
  <img src="https://github.com/user-attachments/assets/665aec94-8731-446f-972f-a8d564149c41" alt="Capture d’écran MEDIQ - aucune alerte" width="49%" />
</p>

<p align="center">
  <em>À gauche : détection d’une erreur critique. À droite : administration conforme sans alerte.</em>
</p>


## Aperçu du projet

MEDIQ analyse les administrations médicamenteuses à partir de données cliniques structurées et identifie deux grands types de problèmes :

- **erreurs de dosage**
- **contre-indications selon les signes vitaux**

Le système attribue ensuite un **score de gravité** et une **catégorie d’alerte** :

- **Normal**
- **Inhabituel**
- **Erreur critique**

Une **interface web de monitoring** permet aussi de visualiser les résultats sous forme de simulation chronologique avec alertes visuelles et sonores.

---

## Fonctionnalités principales

- Lecture automatique d’un fichier CSV clinique
- Normalisation des colonnes pour l’analyse
- Détection d’erreurs de dose selon le médicament et la voie d’administration
- Détection de contre-indications selon les signes vitaux :
  - fréquence cardiaque
  - tension artérielle
  - fréquence respiratoire
  - saturation
  - température
- Attribution d’un score de risque par administration
- Génération de fichiers JSON pour l’interface
- Affichage d’une interface de surveillance en direct
- Alertes critiques avec signal sonore

---

## Structure du projet

```bash
MEDIQ-main/
│
├── main.py
├── analyzer.py
├── TEST.csv
├── EVALUATION.csv
│
├── rules/
│   ├── __init__.py
│   ├── dose_rules.py
│   ├── vitals_rules.py
│   └── output/
│       ├── interface.html
│       ├── script.js
│       ├── style.css
│       ├── alert.mp3
│       ├── results.json
│       └── timeline_results.json
