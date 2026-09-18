import os
import streamlit as st
from mistralai.client import Mistral


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Aurore – Assistant juridique",
    page_icon="⚖️",
    layout="wide",
)

API_KEY = os.environ["MISTRAL_API_KEY"]

AGENT_ID = "ag_01a0a05ef1347680b9297f3dff763223"


# ============================================================
# CONNEXION MISTRAL
# ============================================================

client = Mistral(
    api_key=API_KEY
)


# ============================================================
# MÉMOIRE DE L'APPLICATION
# ============================================================

if "texte_contrat" not in st.session_state:
    st.session_state.texte_contrat = None

if "nom_contrat" not in st.session_state:
    st.session_state.nom_contrat = None

if "rapport" not in st.session_state:
    st.session_state.rapport = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# INTERFACE
# ============================================================

st.title("⚖️ Aurore")
st.subheader("Assistant juridique contractuel")

st.write(
    "Analysez un contrat et interrogez Aurore directement "
    "sur son contenu."
)

st.divider()


# ============================================================
# IMPORT DU CONTRAT
# ============================================================

fichier = st.file_uploader(
    "📄 Déposer votre contrat",
    type=["pdf"],
)


# ============================================================
# NOUVEAU CONTRAT
# ============================================================

if fichier is not None:

    if (
        st.session_state.nom_contrat != fichier.name
    ):

        st.session_state.texte_contrat = None
        st.session_state.rapport = None
        st.session_state.messages = []

        st.session_state.nom_contrat = fichier.name


    st.success(
        f"Contrat sélectionné : {fichier.name}"
    )

    st.write(
        f"Taille : {fichier.size / 1024:.1f} Ko"
    )


    # ========================================================
    # BOUTON ANALYSE
    # ========================================================

    if st.button(
        "🔍 Analyser le contrat",
        type="primary",
    ):

        try:

            with st.status(
                "Analyse du contrat en cours...",
                expanded=True
            ) as status:

                # ------------------------------------------------
                # UPLOAD
                # ------------------------------------------------

                st.write(
                    "📄 Envoi du contrat..."
                )

                uploaded_file = client.files.upload(
                    file={
                        "file_name": fichier.name,
                        "content": fichier.getvalue(),
                    },
                    purpose="ocr",
                )


                # ------------------------------------------------
                # OCR
                # ------------------------------------------------

                st.write(
                    "🔎 Extraction du texte..."
                )

                ocr_response = client.ocr.process(
                    model="mistral-ocr-latest",
                    document={
                        "type": "file",
                        "file_id": uploaded_file.id,
                    },
                )


                texte_contrat = ""

                for page in ocr_response.pages:

                    if hasattr(page, "markdown"):

                        texte_contrat += page.markdown
                        texte_contrat += "\n\n"


                if not texte_contrat.strip():

                    raise Exception(
                        "Aucun texte n'a été extrait."
                    )


                st.session_state.texte_contrat = texte_contrat


                st.write(
                    f"✅ {len(texte_contrat):,} caractères extraits"
                )


                # ------------------------------------------------
                # ANALYSE AURORE
                # ------------------------------------------------

                st.write(
                    "⚖️ Analyse juridique par Aurore..."
                )


                question = f"""
Tu es Aurore, assistant juridique interne chargé
de la revue de contrats.

Analyse le contrat ci-dessous en utilisant le
Référentiel juridique interne disponible dans ta
bibliothèque.

============================================================
CONTRAT
============================================================

{texte_contrat}

============================================================
RÈGLES
============================================================

Distingue strictement :

A. TEXTE DU CONTRAT
Uniquement ce qui est écrit.

B. RÉFÉRENTIEL INTERNE
Uniquement les règles réellement présentes dans
le référentiel.

C. ANALYSE
Ton analyse.

D. RECOMMANDATION
Les actions proposées.

Ne transforme jamais une cible interne en obligation
juridique.

N'invente aucune règle interne.

N'invente aucune information absente du contrat.

Si une information est absente :

"Information non disponible."

Si aucune règle interne ne s'applique :

"Aucune règle interne identifiée."

Distingue :
- risque juridique ;
- écart au référentiel ;
- point de négociation.

Utilise uniquement les niveaux :

CRITIQUE
ÉLEVÉ
MOYEN
FAIBLE

============================================================
RAPPORT
============================================================

# 1. SYNTHÈSE EXÉCUTIVE

- Parties
- Objet
- Durée
- Montant annuel
- Conditions de paiement
- Droit applicable
- Nombre de points nécessitant une attention particulière

# 2. MATRICE DES RISQUES

Pour chaque risque :

## Article X – [Titre]

**Niveau de risque :**

**Extrait du contrat :**

**Constat contractuel :**

**Référentiel interne :**

**Écart au référentiel :**

**Analyse :**

**Certitude :**

**Conséquence pour le Client :**

**Recommandation :**

**Rédaction alternative :**

# 3. ÉCARTS AU RÉFÉRENTIEL INTERNE

| Article | Règle interne | Écart constaté | Risque |

# 4. CLAUSES MANQUANTES OU INSUFFISAMMENT PRÉCISES

# 5. POINTS À NÉGOCIER

# 6. PROPOSITIONS DE RÉDACTION

# 7. INFORMATIONS MANQUANTES

# 8. AVERTISSEMENT

Cette analyse constitue une assistance à la revue
contractuelle. Elle ne remplace pas la validation
d'un juriste.
"""


                response = client.beta.conversations.start(
                    agent_id=AGENT_ID,
                    inputs=[
                        {
                            "role": "user",
                            "content": question,
                        }
                    ],
                )


                rapport = ""

                for output in response.outputs:

                    if hasattr(output, "content"):

                        rapport += output.content


                if not rapport.strip():

                    raise Exception(
                        "Aurore n'a retourné aucun résultat."
                    )


                st.session_state.rapport = rapport


                status.update(
                    label="✅ Analyse terminée",
                    state="complete",
                    expanded=False
                )


        except Exception as erreur:

            st.error(
                "Une erreur est survenue."
            )

            st.exception(erreur)


# ============================================================
# AFFICHAGE DE L'ANALYSE
# ============================================================

if st.session_state.rapport:

    st.divider()

    st.header("📋 Analyse juridique")

    st.markdown(
        st.session_state.rapport
    )


# ============================================================
# CHAT JURIDIQUE
# ============================================================

if st.session_state.texte_contrat:

    st.divider()

    st.header("💬 Questionner le contrat")

    st.write(
        "Posez une question à Aurore sur le contrat analysé."
    )


    # --------------------------------------------------------
    # HISTORIQUE
    # --------------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    question_utilisateur = st.chat_input(
        "Exemple : Quel est le plafond de responsabilité ?"
    )


    if question_utilisateur:

        # ----------------------------------------------------
        # AFFICHAGE QUESTION
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question_utilisateur,
            }
        )


        with st.chat_message("user"):

            st.markdown(
                question_utilisateur
            )


        # ----------------------------------------------------
        # QUESTION À AURORE
        # ----------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Aurore analyse votre question..."
            ):

                question_aurore = f"""
Tu es Aurore, assistant juridique interne.

Tu dois répondre à la question de l'utilisateur
en analysant le contrat fourni ci-dessous.

Tu peux utiliser le Référentiel juridique interne
disponible dans ta bibliothèque.

============================================================
CONTRAT
============================================================

{st.session_state.texte_contrat}

============================================================
QUESTION
============================================================

{question_utilisateur}

============================================================
RÈGLES
============================================================

1. Réponds uniquement à la question posée.

2. Base-toi d'abord sur le texte du contrat.

3. Lorsque tu utilises le référentiel interne,
distingue clairement celui-ci du contrat.

4. Ne transforme jamais une cible interne en
obligation juridique.

5. N'invente aucune information.

6. Si l'information n'est pas présente :

"Information non disponible."

7. Si aucune règle interne ne s'applique :

"Aucune règle interne identifiée."

8. Lorsque c'est pertinent, cite l'article
du contrat concerné.

9. Si tu proposes une rédaction, précise qu'il
s'agit d'une proposition d'Aurore.

10. Reste factuel et prudent.

11. Termine par une mention de validation humaine
uniquement lorsque la question nécessite une
appréciation juridique.

"""


                try:

                    response = client.beta.conversations.start(
                        agent_id=AGENT_ID,
                        inputs=[
                            {
                                "role": "user",
                                "content": question_aurore,
                            }
                        ],
                    )


                    reponse = ""

                    for output in response.outputs:

                        if hasattr(output, "content"):

                            reponse += output.content


                    if not reponse.strip():

                        reponse = (
                            "Aurore n'a retourné aucune réponse."
                        )


                    st.markdown(
                        reponse
                    )


                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": reponse,
                        }
                    )


                except Exception as erreur:

                    st.error(
                        "Erreur lors de la réponse d'Aurore."
                    )

                    st.exception(erreur)