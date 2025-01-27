import pandas as pd
from datetime import datetime, timedelta
nascar_data = pd.read_csv('/Users/mlittle20/Downloads/updated_nascar_data.csv')

# Clean up the column names by stripping leading/trailing spaces
nascar_data.columns = nascar_data.columns.str.strip()

# Function to suggest NASCAR races based on the user's stay dates
def suggest_nascar_races_v2(start_date, end_date, location):
    race_year = start_date.year
    nascar_data['Full Date'] = pd.to_datetime(nascar_data['Date'], errors='coerce').apply(lambda x: x.replace(year=race_year) if pd.notnull(x) else None)
    
    suggested_races = []
    for index, race in nascar_data.iterrows():
        race_date = race['Full Date']
        race_location = race['Location'].lower()  # Normalize the location to lowercase
        location_normalized = location.lower()  # Normalize the user input location
        
        # Filter races by date and location
        if race_date and start_date <= race_date <= end_date and location_normalized in race_location:
            suggested_races.append({
                'Race Name': race['Race Name'],
                'Location': race['Location'],
                'City': race['City'],
                'State': race['State'],
                'Date': race_date.strftime('%B %d')
            })
    
    return suggested_races

    race_year = start_date.year
    # Let pandas infer the date format instead of specifying one
    nascar_data['Date'] = pd.to_datetime(nascar_data['Date'], errors='coerce')
    nascar_data['Full Date'] = nascar_data['Date'].apply(lambda x: x.replace(year=race_year) if pd.notnull(x) else None)
    
    suggested_races = []
    for index, race in nascar_data.iterrows():
        race_date = race['Full Date']
        if race_date and start_date <= race_date <= end_date:
            suggested_races.append({
                'Race Name': race['Race Name'],
                'Location': race['Location'],
                'City': race['City'],
                'State': race['State'],
                'Date': race_date.strftime('%B %d')
            })
    
    return suggested_races
