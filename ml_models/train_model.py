import pymysql
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.utils import resample  # Pour le rééchantillonnage
import joblib  # Pour sauvegarder le modèle

# 1. Charger les données depuis MySQL
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

# 2. Préparer les données
def preprocess_data(data):
    # Créer la colonne "ouvrier" en combinant le prénom et nom
    data['ouvrier'] = data['nom'] + " " + data['prenom']
    data = data.drop(columns=['nom', 'prenom'])
    
    # Convertir "type_travail" en codes numériques
    data['type_travail'] = data['type_travail'].astype('category').cat.codes
    data['ouvrier'] = data['ouvrier'].astype('category').cat.codes
    
    X = data[['duree', 'ouvrier']]  # Features
    y = data['type_travail']        # Target
    
    # Rééchantillonnage (ici on fait un sur-échantillonnage de la classe minoritaire)
    X_upsampled, y_upsampled = resample(X, y, 
                                        replace=True, 
                                        n_samples=len(X), 
                                        random_state=42)
    # Diviser les données en ensembles d'entraînement et de test
    return train_test_split(X_upsampled, y_upsampled, test_size=0.3, random_state=42)

# 3. Entraîner le modèle
def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=200, max_depth=50, random_state=42, class_weight='balanced')  # Ajout de max_depth et class_weight
    model.fit(X_train, y_train)
    return model

# 4. Sauvegarder le modèle
def save_model(model, filename="ml_models/type_travail_model.pkl"):
    joblib.dump(model, filename)
    print(f"Modèle sauvegardé sous : {filename}")

# 5. Évaluer le modèle
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print("Rapport de classification :")
    print(classification_report(y_test, y_pred, zero_division=1))  # Ajout de zero_division=1

# Pipeline principal
if __name__ == "__main__":
    # Charger les données
    data = load_data()
    print("Données chargées avec succès !")
    
    # Préparer les données
    X_train, X_test, y_train, y_test = preprocess_data(data)
    print("Données préparées avec succès !")
    
    # Entraîner le modèle
    model = train_model(X_train, y_train)
    print("Modèle entraîné avec succès !")
    
    # Évaluer le modèle
    evaluate_model(model, X_test, y_test)
    
    # Sauvegarder le modèle
    save_model(model)
