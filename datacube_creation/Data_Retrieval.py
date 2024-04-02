import numpy as np
import pandas as pd
import geopandas as gpdç
from shapely.geometry import Point
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO
from datetime import datetime, date
from isoweek import Week


##### These functions fetch the data from APIs and websites  ########

######## FETCH UPDATED ACLED DATA #############

def fetch_latest_ACLED():

    key = ''
    email = 'jomataha@uv.es'

    params = {
                    "key": key,
                    "email": email,
                    "first_event_date": '2006-01-01',
                    "last_event_date": str(date.today()),
                    "limit":100000000000000, # No limit
                    "country": 'Somalia',
                }

    res = requests.get("https://api.acleddata.com/acled/read", params=params)
    data_json = res.json()['data']
    ACLED_df = pd.json_normalize(data_json)

    print('ACLED data retreived succesfully')
    ACLED_df.to_csv('ACLED_df.csv', index  = False)

    return ACLED_df


######## FETCH UPDATED FSNAU DATA #############

def fetch_latest_FSNAU_data(current_year, path):


    ######## FETCH LAST FSNAU DATA (CURRENT MONTH) #############

    login_url = 'https://fsnau.org/ids/index.php'
    dashboard_url = 'https://fsnau.org/ids/dashboard.php'
    data_export_url = 'https://fsnau.org/ids/exportdata/index.php'

    # Login details
    username = 'jomataha'
    password = ''

    # Create a session
    session = requests.Session()

    # Perform login
    response = session.get(login_url)

    # Parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the username and password fields
    username_field = soup.find('input', {'name': 'username'})
    password_field = soup.find('input', {'name': 'password'})

    # Check if the fields were found
    if not username_field or not password_field:
        print('Failed to find the username or password field.')
        exit()

    # Set the values for the username and password fields
    username_field['value'] = username
    password_field['value'] = password

    # Find the submit button within the form
    submit_button = soup.find('input', {'type': 'submit'})

    # Check if the submit button was found
    if not submit_button:
        print('Failed to find the submit button.')
        exit()

    # Click the submit button by submitting the login form
    response = session.post(login_url, data={username_field['name']: username, password_field['name']: password, submit_button['name']: submit_button['value']})

    # Check if login was successful
    if response.status_code != 200:
        print('Failed to log in. Status code:', response.status_code)
        exit()

    # Check if we are redirected to the dashboard page
    if response.url == dashboard_url:
        print('Login successful. Redirected to the dashboard page.')

        # Navigate to the data export page
        response = session.get(data_export_url)

        # Check if navigation was successful
        if response.status_code != 200:
            print('Failed to navigate to the data export page. Status code:', response.status_code)
            exit()

        # Check if we have successfully accessed the data export page
        if response.url == data_export_url:
            print('Successfully accessed the data export page.')
        else:
            print('Failed to access the data export page.')

    else:
        print('Login failed. Not redirected to the dashboard page.')

        
    # Find the "Fetch Data" button on the data export page
    soup = BeautifulSoup(response.content, 'html.parser')
    form_element = soup.find('form', id='frmExporter')

    # Check if the form element was found
    if not form_element:
        print('Failed to find the form element.')
        exit()

    # Extract the form action URL
    form_action = form_element['action']

    # Construct the absolute URL
    base_url = 'https://fsnau.org/ids/exportdata/'
    form_action_url = urljoin(base_url, form_action)

    # Define the form data
    form_data = {
        'criteria': 'year_range',
        'start_year': current_year,   # May
        'year': current_year,
        'btnExport': 'Fetch Data'
    }

    # Send the POST request to retrieve the Excel data
    response = session.post(form_action_url, data=form_data)

    # Check if the request was successful
    if response.status_code == 200:
        # Assuming the response contains the Excel file
        excel_data = response.content

        # Save the Excel file
        with open(path, 'wb') as file:
            file.write(excel_data)

        print('Excel data saved successfully.')
    else:
        print('Failed to retrieve the Excel data.')

###########################################################################



######## FETCH PRMN DATA #############

def collect_PRMN_IDP(url):

################## a) Collect NEW DATA from PRMN website ########################

    response = requests.get(url)

    if response.status_code == 200:
        
        data = requests.get(url).content
        PRMN_data = pd.read_excel(BytesIO(data), engine='openpyxl')
        print("PRMN file downloaded successfully.")

    else:
        print("Failed to download the PRMN file.")

    # Convert Year Week to DATE
    PRMN_data['Arrival'] = pd.to_datetime(PRMN_data['Year Week'].astype(str) + '-1', format='%Y%W-%w')

    # Select columns
    PRMN_data.rename(columns = {'Arrival': 'Date', 'Previous (Departure) District': 'District', 'Number of Individuals':'IDP','Previous (Departure) Region': 'Region'}, inplace = True)
    PRMN_data = PRMN_data[['Date', 'Region', 'District', 'Reason', 'IDP']]

    # Drought
    new_drought = PRMN_data[PRMN_data['Reason'] == 'Drought related'].drop('Reason', axis = 1)
    new_drought.rename(columns = {'IDP':'IDP_Drought'}, inplace = True)

    # Conflict
    new_conflict = PRMN_data[PRMN_data['Reason'] == 'Conflict/Insecurity'].drop('Reason', axis = 1)
    new_conflict.rename(columns = {'IDP':'IDP_Conflict'}, inplace = True)

    PRMN_data_IDP = pd.merge(new_drought, new_conflict, on=['Date', 'Region', 'District'], how='outer')

    return PRMN_data_IDP



######## COLLECT NDA DATA AND CLEAN LABELS AND REASONS #############


from Data_Aggregation_Functions import correct_districts

########### Select Drought Season + Possible causes of droughts in NDA data ################ possible upgrade with chat-gpt

def collect_NDA_IDP(old_df):

    old_df.rename(columns={'PreviousDistrict': 'District', 'PreviousRegion': 'Region'}, inplace=True)
    old_df = old_df[['Arrival','Reason', 'Region', 'District', 'IDP', 'PreviousSettlement', 'PartnerComments']]

    # Helper function to extract reasons and partner comments: input a set of reasons and a set of words that must match    
    def select_reasons(df, reason_list, check_list, certain_list):
        is_in = []

        for i, row in df.iterrows():
            reason = row['Reason']
            comment = row['PartnerComments']

            if reason in certain_list:
                is_in.append(i)
            else:
                if reason in reason_list:
                    if any(word in str(comment) for word in check_list):
                        is_in.append(i)
        return df[df.index.isin(is_in)]  

    # Drought
    drought_check_list = {'Drought', 'drought', 'Drough', 'drough', 'Pastoralist', 'pastoralist', 'rain', 'Rain', 'farm', 'agriculture', 'rainfall', 'grazing', 'Pasture', 'livestock', 'pastoralists', 'water', 'pasture', 'Water', 'Food', 'food', 'dry', 'Dry', 'posture', 'cultivated', 'farms', 'Agro-pastoralist'}
    drought_reason_list = ['Lack of livelihood', 'Access to humanitarian assistance', 'Could not afford to stay in the previous location (if IDP) or country (if cross border)', 'Lack of Livelihoods - Other']
    certain_drought_list = ['Drought']

    old_drought = select_reasons(old_df, drought_reason_list, drought_check_list, certain_drought_list)
    old_drought.rename(columns={'IDP': 'IDP_Drought'}, inplace=True)
    old_drought.Arrival = pd.to_datetime(old_drought.Arrival)

    # Conflict
    conflict_check_list = {'insecurity', 'protection', 'shelter', 'military', 'AS', 'recruit', 'offences', 'Military', 'operation', 'alshabaab', 'training', 'conflict', 'clans', 'clan', 'tension', 'al shabab', 'taxation', 'war', 'Al-shabaab', 'security', 'fight', 'insecurit', 'confilect', 'insecuritythere', 'fighting', 'As', 'soldiers', 'al-shabab', 'soldieries', 'force', 'troops', 'forces', 'militant', 'fleeing', 'fled', 'fear', 'Alshabab', 'stability', 'recruiting', 'recruited', 'recruit', 'Insecurity', 'militia', 'weapon', 'protection', 'fears', 'threating', 'Al- shabaab', 'Protection', 'solders', 'attack', 'offensive'}
    conflict_reason_list = ['Insecurity - Other Insecurity', 'Insecurity']
    certain_conflict_list = ['Insecurity - Military Offensive', 'Clan Conflict']

    old_df.District = correct_districts(old_df.District)
    old_conflict = select_reasons(old_df, conflict_reason_list, conflict_check_list, certain_conflict_list)
    old_conflict.rename(columns={'IDP': 'IDP_Conflict'}, inplace=True)
    old_conflict.Arrival = pd.to_datetime(old_conflict.Arrival)

    NDA_data_IDP = pd.merge(old_drought[['Arrival', 'Region', 'District', 'PreviousSettlement', 'IDP_Drought']], old_conflict[['Arrival', 'Region', 'District','PreviousSettlement', 'IDP_Conflict']], on=['Arrival', 'Region', 'District', 'PreviousSettlement'], how='outer')

    NDA_data_IDP.rename(columns = {'PreviousSettlement': 'Settlement', 'Arrival': 'Date'}, inplace = True)

    return NDA_data_IDP