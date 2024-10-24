# Importing Required Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium 
#%matplotlib inline
import io
import requests
import datetime as dt


URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv"

# Realiza la solicitud HTTP para obtener el archivo CSV
response = requests.get(URL)

# Verifica si la solicitud fue exitosa (código 200)
if response.status_code == 200:
    # Convierte el contenido en bytes y luego en un DataFrame de pandas
    text = io.BytesIO(response.content)
    df = pd.read_csv(text)
    print('Data read into a pandas dataframe!')
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
    
print(df.head())

df['Year'] = pd.to_datetime(df['Date']).dt.year
df['Month'] = pd.to_datetime(df['Date']).dt.month

print(df.head())