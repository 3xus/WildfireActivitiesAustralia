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
    

df['Year'] = pd.to_datetime(df['Date']).dt.year
df['Month'] = pd.to_datetime(df['Date']).dt.month

## Let's try to understand the change in average estimated fire area over time
plt.figure(figsize=(12,6))

# Grouping the data by 'Year' and calculating the mean of Estimated_fire_area
df_new = df.groupby('Year')['Estimated_fire_area'].mean()

#Plotting the data
df_new.plot(x = df_new.index, y=df_new.values)
plt.xlabel('Year')
plt.ylabel('Average Estimated Fire Area (km^2)')
plt.title('Estimated Fire Area over Time')
plt.show()

#Task 1.2. You can notice the peak in the plot between 2010 to 2013. Let's plot
# the estimated fire area for year grouped together with month
df_month_year = df.groupby(['Year', 'Month'])['Estimated_fire_area'].mean()
#df_month_year

# Plotting
df_month_year.plot(x = df_month_year.index, y = df_month_year.values)
plt.xticks(rotation = 90)
plt.xlabel('Year, Month')
plt.ylabel('Average Estimated Fire Area (km^2)')
plt.title('Estimated Fire Area Over Time')
plt.show()

# Task 1.3. Let's have an insight on the distribution of mean estimated fire brightness 
# across the regions use the functionality of seaborn to develop a barplot
df['Region'].unique()