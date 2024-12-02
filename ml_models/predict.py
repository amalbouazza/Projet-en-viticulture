# predict.py
import joblib
import pandas as pd

def load_model(filename="ml_models/type_travail_model.pkl"):
    return joblib.load(filename)

def predict(model, data):
    return model.predict(data)

if __name__ == "__main__":
    # Charger le modèle
    model = load_model()
    print("Modèle chargé avec succès !")
    
    # Exemple de nouvelles données à prédire
    new_data = pd.DataFrame({'duree': [5, 8], 'ouvrier': [1, 2]})
    predictions = predict(model, new_data)
    print("Prédictions :", predictions)
