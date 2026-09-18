import os

from mistralai.client import Mistral


client = Mistral(
    api_key=os.environ["MISTRAL_API_KEY"]
)


question = """
Analyse cette clause contractuelle :

"En cas de manquement à ses obligations,
le Prestataire pourra être tenu responsable
de l'intégralité des dommages subis par le Client,
sans limitation de montant."

Utilise obligatoirement le Référentiel juridique interne
mis à ta disposition.

Je veux une analyse structurée avec :

1. Niveau de risque
2. Problème identifié
3. Écart éventuel avec la politique interne
4. Conséquences pour le Client
5. Point(s) à négocier
6. Proposition de rédaction alternative

Indique explicitement les règles du référentiel interne
que tu as utilisées.
"""


response = client.beta.conversations.start(
    agent_id="ag_01a0a05ef1347680b9297f3dff763223",
    inputs=[
        {
            "role": "user",
            "content": question
        }
    ],
)


print("\n==============================")
print("       ANALYSE D'AURORE")
print("==============================\n")

for output in response.outputs:
    if hasattr(output, "content"):
        print(output.content)