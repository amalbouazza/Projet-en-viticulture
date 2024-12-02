import joblib
import pymysql
import pandas as pd

# Charger le modèle pré-entraîné
def load_model():
    return joblib.load('ml_models/ml_models/type_travail_model.pkl')

# Charger les données depuis MySQL
def load_data():
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='viticulture'
    )
    query = """
        SELECT 
            travaux.duree, travaux.date_travail, ouvriers.nom, ouvriers.prenom, travaux.type_travail 
        FROM 
            travaux 
        JOIN 
            ouvriers 
        ON 
            travaux.ouvrier_id = ouvriers.id;
    """
    data = pd.read_sql(query, connection)
    connection.close()
    return data

# Préparer les données (même préparation que lors de l'entraînement)
def preprocess_data(data):
    data['ouvrier'] = data['nom'] + " " + data['prenom']
    data = data.drop(columns=['nom', 'prenom'])
    data['type_travail'] = data['type_travail'].astype('category').cat.codes
    data['ouvrier'] = data['ouvrier'].astype('category').cat.codes
    X = data[['duree', 'ouvrier']]  # Features
    return X

# Faire une prédiction avec le modèle
def predict(model, data):
    # Préparer les données pour la prédiction
    X = preprocess_data(data)
    
    # Faire la prédiction
    predictions = model.predict(X)
    return predictions

# Exemple d'utilisation dans votre application
if __name__ == "__main__":
    # Charger le modèle
    model = load_model()
    print("Modèle chargé avec succès !")
    
    # Charger les nouvelles données à partir de la base de données
    data = load_data()
    print("Données chargées avec succès !")
    
    # Faire des prédictions sur les données
    predictions = predict(model, data)
    print("Prédictions :", predictions)
    
    # Vous pouvez maintenant utiliser ces prédictions comme bon vous semble dans votre application
