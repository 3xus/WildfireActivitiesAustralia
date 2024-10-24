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

# Creating a bar plot using seaborn to visualize the distribution of mean estimated fire 
# brightness across regions
plt.figure(figsize=(10,6))

# Using seaborn's barplot function to create the plot
sns.barplot(data = df, x='Region', y='Mean_estimated_fire_brightness')
plt.xlabel('Region')
plt.ylabel('Mean Estimated Fire Brightness (Kelvin)')
plt.title('Distribution of Mean Estimated Fire Brightness across Region')
plt.show()

# Task 1.4: Let's find the portion of count of pixels for presumed vegetation fires 
# vary across regions we will develop a pie chart for this
region_count = df.groupby('Region')['Count'].sum()

# Creating a pie chart to visualize the portion of count of pixels for presumed 
# vegetation fires across regions
plt.figure(figsize=(10,6))
plt.pie(region_counts, labels = region_count.index)
plt.title('Percentage of Pixels for Presumed Vegetation Fires by Region')
plt.legend([(i,round(k/region_counts.sum()*100,2)) for i,k in zip(region_counts.index, region_counts)])
plt.axis('equal')
plt.show()

# Task 1.6: Let's try to develop a histogram of the mean estimated fire 
# brightness. Using Matplotlib to create the histogram
plt.figure(figsize=(10,6))
plt.hist(x=df['Mean_estimated_fire_brightness'], bins=20)
plt.xlabel('Mean Estimated Fire Brightness (Kelvin)')
plt.ylabel('Count')
plt.title('Histogram of Mean Estimated Fire Brightness')
plt.show()

# Creating a histogram to visualize the distribution of mean estimated fire brightness across regions using Seaborn
# Using sns.histplot to create the histogram
# Specifying the DataFrame (data=df) and the column for the x-axis (x='Mean_estimated_fire_brightness')
# Adding hue='Region' to differentiate the distribution across regions
sns.histplot(data=df, x='Mean_estimated_fire_brightness', hue='Region', multiple='stack')
plt.show()

# Task 1.8. Let's try to find of there is any correlation between mean estimated fire
# radiative power and mean confidence level
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='Mean_confidence', y='Mean_estimated_fire_radiative_power')
plt.xlabel('Mean Estimated Fire Radiative Power (MW)')
plt.ylabel('Mean Confidence')
plt.title('Mean Estimated Fire Radiative Power vs. Mean Confidence')
plt.show()

## Task 1.9. Let's mark these seven regions on the Map of Australia Usinf Folium
region_data = {'region':['NSW','QL','SA','TA','VI','WA','NT'], 'Lat':[-31.8759835,-22.1646782,-30.5343665,-42.035067,-36.5986096,-25.2303005,-19.491411], 
               'Lon':[147.2869493,144.5844903,135.6301212,146.6366887,144.6780052,121.0187246,132.550964]}
reg=pd.DataFrame(region_data)
## reg

# Instantiate a feature group
aus_reg = folium.map.FeatureGroup()

# Map centered on Australia
Aus_map = folium.Map(location = [-25,135], zoom_start=4)

# Loop through the region and add to feature group
for lat, lng, lab in zip(reg.Lat, reg.Lon, reg.region):
    aus_reg.add_child(
        folium.features.CircleMarker(
            [lat,lng],
            popup = lab,
            radius = 5,
            color = 'red',
            fill = True,
            fill_color = 'blue',
            fill_opacity=0.6            
        )
    )
    
Aus_map.add_child(aus_reg)
