from sqlalchemy import create_engine
import pandas as pd

# Remplacez par votre URL de base de données MySQL
DATABASE_URL = "mysql+pymysql://root:@localhost/viticulture"

# Créer un moteur SQLAlchemy pour se connecter à la base de données
engine = create_engine(DATABASE_URL)

# Exemple de requête
query = "SELECT * FROM travaux"
df = pd.read_sql(query, engine)

# Affichage des résultats
print(df)
