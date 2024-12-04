import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

# Chargement du jeu de données Iris
data = load_iris()
X = data.data  # Les caractéristiques (sepal_length, sepal_width, petal_length, petal_width)
y = data.target  # Les labels (0: setosa, 1: versicolor, 2: virginica)

# Diviser les données en ensembles d'entraînement et de test (80% entraînement, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Création et entraînement du modèle
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Sauvegarde du modèle dans un fichier
with open('ml_models/ml_models/type_travail_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

print("Modèle sauvegardé avec succès dans 'ml_models/ml_models/type_travail_model.pkl'")


import pickle
from sklearn.metrics import accuracy_score

# Chargement du modèle sauvegardé
with open('ml_models/ml_models/type_travail_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Exemple de prédiction avec des données d'entrée
y_pred = loaded_model.predict(X_test)  # Remplacez X_test par de nouvelles données si nécessaire

# Affichage de la précision du modèle chargé
print(f"Précision du modèle chargé : {accuracy_score(y_test, y_pred) * 100:.2f}%")