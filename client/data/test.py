import numpy as np
import json

# Générer une matrice 100x100 avec des couleurs RGB aléatoires
matrice = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8).tolist()

# Sauvegarde dans un fichier JSON
data = matrice

with open("project.json", "w") as f:
    json.dump(data, f, indent=4)
