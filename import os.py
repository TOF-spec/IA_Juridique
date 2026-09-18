import os

from mistralai.client import Mistral


# Connexion à Mistral
client = Mistral(
    api_key=os.environ["MISTRAL_API_KEY"]
)


# Question envoyée à l'Agent
question = """
Analyse la clause suivante :

"En cas de manquement à ses obligations,
le Prestataire pourra être tenu responsable
de l'intégralité des dommages subis par le Client,
sans limitation de montant."

Je veux que tu identifies :

1. Le niveau de risque
2. Le problème juridique
3. Les conséquences pour le Client
4. Les points à négocier
5. Une proposition de rédaction alternative

Réponds de manière structurée et concise.
"""


# Envoi à ton Agent juridique
response = client.beta.conversations.start(
    agent_id="ag_01a0a05ef1347680b9297f3dff763223",
    inputs=[
        {
            "role": "user",
            "content": question
        }
    ],
)


# Affichage uniquement de la réponse de l'Agent
print("\n==============================")
print("       ANALYSE JURIDIQUE")
print("==============================\n")

for output in response.outputs:
    if hasattr(output, "content"):
        print(output.content)