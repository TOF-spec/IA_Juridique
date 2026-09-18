# ⚖️ Aurore — Assistant juridique contractuel

Application Streamlit d’analyse de contrats avec Mistral, OCR des PDF et référentiel juridique interne.

## 1. Prérequis

Installer :
- Python 3.13 (ou version compatible avec les bibliothèques utilisées)
- VS Code recommandé
- Un compte Mistral avec une clé API
- Git recommandé, mais facultatif

## 2. Structure du projet

```text
aurore/
├── app.py
├── analyse_pdf.py
├── connecter_aurore.py
├── test_aurore.py
├── test_libraries.py
├── contrat_test_services.pdf
└── README.md
```

L’utilisation quotidienne de l’application se fait avec `app.py`.

## 3. Créer l’environnement virtuel

Dans PowerShell, depuis le dossier du projet :

```powershell
python -m venv .venv
```

Activer :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Pour sortir de `.venv` :

```powershell
deactivate
```

## 4. Installer les dépendances

Une fois `.venv` activé :

```powershell
python -m pip install --upgrade pip
pip install mistralai streamlit python-docx
```

- `mistralai` : API Mistral, Agents, OCR et fichiers
- `streamlit` : interface web
- `python-docx` : génération de rapports Word

## 5. Configurer la clé API Mistral

Ne jamais mettre la clé directement dans `app.py`.

Dans PowerShell :

```powershell
$env:MISTRAL_API_KEY="VOTRE_CLE_API_MISTRAL"
```

Vérifier sa présence sans afficher la clé :

```powershell
if ($env:MISTRAL_API_KEY) { "API key présente" } else { "API key absente" }
```

Cette variable est valable pour la session PowerShell en cours.

## 6. Configuration Mistral

L’application utilise actuellement :

- Agent : **Aurore**
- Agent ID :
```text
ag_01a0a05ef1347680b9297f3dff763223
```
- Modèle : `mistral-medium-latest`
- OCR : `mistral-ocr-latest`

L’agent Aurore doit avoir accès au référentiel juridique interne.

Bibliothèque :

```text
Référentiel juridique interne
```

Document de test actuel :

```text
politique_responsabilite.txt
```

## 7. Lancer l’application

Activer `.venv` :

```powershell
.\.venv\Scripts\Activate.ps1
```

Puis :

```powershell
streamlit run app.py
```

Si nécessaire :

```powershell
python -m streamlit run app.py
```

L’application est généralement accessible sur :

```text
http://localhost:8501
```

## 8. Utilisation

1. Ouvrir l’application.
2. Importer un contrat PDF.
3. Cliquer sur **Analyser le contrat**.
4. Aurore extrait le texte via OCR puis analyse le contrat.
5. Poser ensuite des questions dans la zone de discussion.

Exemple :

```text
Que dit le référentiel interne concernant la responsabilité ?
```

L’analyse porte notamment sur :
- responsabilité
- résiliation
- pénalités
- confidentialité
- propriété intellectuelle
- données
- incohérences
- ambiguïtés
- écarts au référentiel interne
- informations manquantes
- propositions de rédaction

## 9. Principes de l’analyse

Aurore doit distinguer :

**Contrat** : ce qui est effectivement écrit.

**Référentiel interne** : politiques, cibles, standards ou préférences internes.

**Analyse** : identification et explication des risques ou écarts.

**Recommandation** : proposition destinée à aider le juriste.

Une cible interne ne doit pas être présentée comme une obligation légale.

Si une information manque :

```text
Information non disponible.
```

Si aucune règle interne pertinente n’est identifiée :

```text
Aucune règle interne identifiée.
```

En cas d’incertitude :

```text
À confirmer par le juriste.
```

Les nouvelles rédactions proposées par Aurore doivent être présentées comme des propositions d’Aurore et non comme des extraits du référentiel.

## 10. Niveaux de risque

```text
CRITIQUE
ÉLEVÉ
MOYEN
FAIBLE
```

Ces niveaux sont une aide à l’analyse et ne remplacent pas la validation juridique humaine.

## 11. Fichiers générés

Le script d’analyse peut générer :

```text
rapport_analyse_aurore.docx
```

## 12. Dépannage

### Module manquant

Exemple :

```text
ModuleNotFoundError: No module named 'streamlit'
```

Activer `.venv` puis :

```powershell
pip install mistralai streamlit python-docx
```

### Clé API absente

```powershell
if ($env:MISTRAL_API_KEY) { "API key présente" } else { "API key absente" }
```

Puis, si nécessaire :

```powershell
$env:MISTRAL_API_KEY="VOTRE_CLE_API_MISTRAL"
```

### Streamlit ne démarre pas

```powershell
python -m streamlit run app.py
```

### `(.venv)` apparaît dans le terminal

C’est normal : l’environnement virtuel est actif.

Pour le quitter :

```powershell
deactivate
```

## 13. Commandes utiles

Activer :

```powershell
.\.venv\Scripts\Activate.ps1
```

Quitter :

```powershell
deactivate
```

Installer :

```powershell
pip install mistralai streamlit python-docx
```

Mettre à jour :

```powershell
pip install --upgrade mistralai streamlit python-docx
```

Lancer :

```powershell
streamlit run app.py
```

## 14. Sécurité

Pour de vrais contrats :

- Ne jamais mettre la clé Mistral dans le code.
- Ne jamais committer une clé API dans Git.
- Ne pas versionner les contrats confidentiels.
- Contrôler les droits d’accès au référentiel interne.
- Utiliser une gestion sécurisée des secrets en production.
- Maintenir une validation humaine pour les analyses sensibles.

## 15. `.gitignore` recommandé

Créer `.gitignore` à la racine :

```gitignore
.venv/
__pycache__/
*.pyc
.env
*.env
.streamlit/secrets.toml

# Documents confidentiels
*.pdf
*.docx

# Rapport généré
rapport_analyse_aurore.docx
```

Adapter cette liste si certains fichiers doivent être versionnés.

## 16. Installation rapide sur une nouvelle machine

```powershell
python -m venv .venv

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install mistralai streamlit python-docx

$env:MISTRAL_API_KEY="VOTRE_CLE_API_MISTRAL"

streamlit run app.py
```

## 17. État actuel du projet

- [x] Import d’un PDF
- [x] OCR du contrat
- [x] Analyse par Aurore
- [x] Utilisation du référentiel juridique interne
- [x] Identification des risques
- [x] Questions/réponses sur le contrat
- [x] Génération de rapport Word via le script d’analyse
- [ ] Interface juridique avancée
- [ ] Tableau de risques interactif
- [ ] Comparaison avec des modèles internes
- [ ] Gestion de plusieurs référentiels
- [ ] Authentification
- [ ] Gestion des droits d’accès
- [ ] Déploiement sécurisé en entreprise

## 18. Avertissement

Aurore est un assistant d’analyse contractuelle. Ses résultats constituent une aide au travail du service juridique.

Les points sensibles, interprétations incertaines et propositions de modification doivent être validés par un juriste avant utilisation ou communication à une contrepartie.
