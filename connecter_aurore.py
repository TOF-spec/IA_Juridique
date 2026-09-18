import os

from mistralai.client import Mistral


client = Mistral(
    api_key=os.environ["MISTRAL_API_KEY"]
)


# 1. Récupérer la bibliothèque juridique
libraries = client.beta.libraries.list().data

bibliotheque = None

for library in libraries:
    if library.name == "Référentiel juridique interne":
        bibliotheque = library
        break


if bibliotheque is None:
    raise Exception("Bibliothèque juridique introuvable")


print("Bibliothèque trouvée :", bibliotheque.name)
print("ID :", bibliotheque.id)


# 2. Mettre à jour l'agent Aurore
agent_id = "ag_01a0a05ef1347680b9297f3dff763223"

agent = client.beta.agents.update(
    agent_id=agent_id,
    tools=[
        {
            "type": "document_library",
            "library_ids": [bibliotheque.id]
        }
    ]
)


print()
print("================================")
print("AGENT AURORE MIS À JOUR")
print("================================")
print("Nom :", agent.name)
print("ID  :", agent.id)
print("Bibliothèque connectée :", bibliotheque.name)