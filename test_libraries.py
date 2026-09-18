import os
from mistralai.client import Mistral

client = Mistral(
    api_key=os.environ["MISTRAL_API_KEY"]
)

libraries = client.beta.libraries.list().data

print("Nombre de bibliothèques visibles :", len(libraries))

for library in libraries:
    print("Nom :", library.name)
    print("ID  :", library.id)
    print("Docs:", library.nb_documents)
    print()