
import pandas as pd
import json
import os
import plotly.express as px
import requests
import subprocess
import plotly.graph_objects as go
from IPython.display import display
import psycopg2
import numpy as np
import streamlit as st

host = 'xxx'
port = 'yyy'
database = 'zzz'
username = 'aaa'
password = 'zzz'

eta = psycopg2.connect(host=host, port=port, database=database, user=username, password=password)
cursor=eta.cursor()

!git clone https://github.com/PhonePe/pulse.git

#1
path="data/aggregated/transaction/country/india/state"
Agg_state_list=os.listdir(path)
clm={'State':[], 'Year':[],'Quarter':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}
for i in Agg_state_list:
    p_i=path+"/"+i
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+"/"+j
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
          p_k=p_j+"/"+k
          Data=open(p_k, 'r')
          A = json.load(Data)
          for z in A['data']['transactionData']:
            Name=z['name']
            count=z['paymentInstruments'][0]['count']
            amount=z['paymentInstruments'][0]['amount']
            clm['Transaction_type'].append(Name)
            clm['Transaction_count'].append(count)
            clm['Transaction_amount'].append(amount)
            clm['State'].append(i)
            clm['Year'].append(j)
            clm['Quarter'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Agg_Trans=pd.DataFrame(clm)
Agg_Trans['State'] = Agg_Trans['State'].str.replace('andaman-&-nicobar-islands', 'Andaman & Nicobar')
Agg_Trans['State'] = Agg_Trans['State'].str.replace('---', ' & ')
Agg_Trans['State'] = Agg_Trans['State'].str.replace('-', ' ')
Agg_Trans['State'] = Agg_Trans['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')

Agg_Trans['State'] = Agg_Trans['State'].str.title()


#2
path2="data/aggregated/user/country/india/state/"
user_list = os.listdir(path2)
col2 = {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'Transaction_Count': [],'Percentage': []}
for i in user_list:
    p_i = path2 + "/"+ i
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + "/"+ j
        Agg_yr_list = os.listdir(p_j)
        for k in Agg_yr_list:
          p_k = os.path.join(p_j, k)
          if os.path.isfile(p_k):# Check if the file exists before attempting to open it
              with open(p_k, 'r') as Data2:
                B = json.load(Data2)
                try:
                  for z in B['data']['usersByDevice']:
                    Brand=z['brand']
                    Count=z['count']
                    Percentage=z['percentage']
                    col2['Brands'].append(Brand)
                    col2['Transaction_Count'].append(Count)
                    col2['Percentage'].append(Percentage)
                    col2['State'].append(i)
                    col2['Year'].append(j)
                    col2['Quarter'].append(int(k.strip('.json')))
                except:
                  pass
Agg_user=pd.DataFrame(col2)
Agg_user['State'] = Agg_user['State'].str.replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')
Agg_user['State'] = Agg_user['State'].str.replace('---', ' & ')
Agg_user['State'] = Agg_user['State'].str.replace('-', ' ')
Agg_user['State'] = Agg_user['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')

Agg_user['State'] = Agg_user['State'].str.title()


#3
path3="data/map/transaction/hover/country/india/state/"

hover_list = os.listdir(path3)

col3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Transaction_count': [],
        'Transaction_amount': []}
for i in hover_list:
    p_i = path3 + "/"+ i
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + "/"+ j
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j +"/" +k
            Data = open(p_k, 'r')
            C = json.load(Data)
            for x in C["data"]["hoverDataList"]:
                District = x["name"]
                count = x["metric"][0]["count"]
                amount = x["metric"][0]["amount"]
                col3["District"].append(District)
                col3["Transaction_count"].append(count)
                col3["Transaction_amount"].append(amount)
                col3['State'].append(i)
                col3['Year'].append(j)
                col3['Quarter'].append(int(k.strip('.json')))
map_trans = pd.DataFrame(col3)
map_trans['State'] = map_trans['State'].str.replace('---', ' & ')
map_trans['State'] = map_trans['State'].str.replace('-', ' ')
map_trans['State'] = map_trans['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')
map_trans['State'] = map_trans['State'].str.replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')
map_trans['State'] = map_trans['State'].str.title()


#4
path4="data/map/user/hover/country/india/state"
col4={'State':[],'Year':[],'Quarter':[],'District':[],'RegisteredUsers':[],'AppOpens':[]}
map_user=os.listdir(path4)
for i in map_user:
  p_i=path4+"/"+i
  year=os.listdir(p_i)
  for j in year:
    p_j=p_i+"/"+j
    year_lst=os.listdir(p_j)
    for k in year_lst:
      p_k = os.path.join(p_j, k)
      if os.path.isfile(p_k):# Check if the file exists before attempting to open it
          with open(p_k, 'r') as Data4:
            E = json.load(Data4)
            for z in E['data']['hoverData'].items():
              District=z[0]
              RegisteredUser=z[1]['registeredUsers']
              AppOpens=z[1]['appOpens']
              col4['District'].append(District)
              col4['RegisteredUsers'].append(RegisteredUser)
              col4['AppOpens'].append(AppOpens)
              col4['State'].append(i)
              col4['Year'].append(j)
              col4['Quarter'].append(int(k.strip('.json')))
Map_user=pd.DataFrame(col4)
Map_user['State'] = Map_user['State'].str.replace('---', ' & ')
Map_user['State'] = Map_user['State'].str.replace('-', ' ')
Map_user['State'] = Map_user['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')
Map_user['State'] = Map_user['State'].str.replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')
Map_user['State'] = Map_user['State'].str.title()


#5
path5="data/top/transaction/country/india/state"
col5={'State':[],'Year':[],"Quarter":[],'Pincode':[],'Transaction_Count':[],'Transaction_Amount':[]}
top_transaction=os.listdir(path5)
for i in top_transaction:
  p_i=path5+"/"+i
  year=os.listdir(p_i)
  for j in year:
    p_j=p_i+"/"+j
    year_list=os.listdir(p_j)
    for k in year_list:
      p_k = os.path.join(p_j, k)
      if os.path.isfile(p_k):# Check if the file exists before attempting to open it
          with open(p_k, 'r') as Data5:
            F = json.load(Data5)
            for z in F['data']['pincodes']:
              Pincode=z['entityName']
              count=z['metric']['count']
              amount=z['metric']['amount']
              col5['Pincode'].append(Pincode)
              col5['Transaction_Count'].append(count)
              col5['Transaction_Amount'].append(amount)
              col5['State'].append(i)
              col5['Year'].append(j)
              col5['Quarter'].append(int(k.strip('.json')))
top_trans=pd.DataFrame(col5)
top_trans['State'] = top_trans['State'].str.replace('---', ' & ')
top_trans['State'] = top_trans['State'].str.replace('-', ' ')
top_trans['State'] = top_trans['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')
top_trans['State'] = top_trans['State'].str.replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')
top_trans['State'] = top_trans['State'].str.title()


#6
path6="data/top/user/country/india/state"
top_user=os.listdir(path6)
col6={'State':[],'Year':[],'Quarter':[],'Pincode':[],'RegisteredUsers':[]}
for i in top_user:
  p_i=path6+"/"+i
  year=os.listdir(p_i)
  for j in year:
    p_j=p_i+"/"+j
    year_list=os.listdir(p_j)
    for k in year_list:
      p_k = os.path.join(p_j, k)
      if os.path.isfile(p_k):# Check if the file exists before attempting to open it
          with open(p_k, 'r') as Data6:
            G = json.load(Data6)
            for z in G['data']['pincodes']:
              Pincode=z['name']
              RegisteredUser=z['registeredUsers']
              col6['Pincode'].append(Pincode)
              col6['RegisteredUsers'].append(RegisteredUser)
              col6['State'].append(i)
              col6['Year'].append(j)
              col6['Quarter'].append(int(k.strip('.json')))
Top_user=pd.DataFrame(col6)
Top_user['State'] = Top_user['State'].str.replace('---', ' & ')
Top_user['State'] = Top_user['State'].str.replace('-', ' ')
Top_user['State'] = Top_user['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')
Top_user['State'] = Top_user['State'].str.replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')
Top_user['State'] = Top_user['State'].str.title()


cursor.execute('''create table if not exists Aggregate_Transaction(State varchar(50),
           Year int, 
           Quarter int, 
           Transaction_type varchar(50),
           Transaction_count bigint,
           Transaction_amount bigint)'''
           )
eta.commit()
for _, row in Agg_Trans.iterrows():
            insert_query = '''
                INSERT INTO Aggregate_Transaction (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount)
                VALUES (%s, %s, %s, %s, %s, %s)

            '''
            values = (
                row['State'],
                row['Year'],
                row['Quarter'],
                row['Transaction_type'],
                row['Transaction_count'],
                row['Transaction_amount']
            )
            cursor.execute(insert_query,values)
eta.commit()     


cursor.execute('''create table if not exists Aggregate_User(State varchar(50),
           Year int, 
           Quarter int, 
           Brands varchar(20),
           Transaction_Count bigint,
           Percentage float)'''
           )
eta.commit()
for _, row in Agg_user.iterrows():
            insert_query = '''
                INSERT INTO Aggregate_User (State, Year, Quarter, Brands, Transaction_Count, Percentage)
                VALUES (%s, %s, %s, %s, %s, %s)

            '''
            values = (
                row['State'],
                row['Year'],
                row['Quarter'],
                row['Brands'],
                row['Transaction_Count'],
                row['Percentage']
            )
            cursor.execute(insert_query,values)
eta.commit()


#Map_Transaction
cursor.execute('''create table if not exists Map_Transaction(State varchar(50),
           Year int, 
           Quarter int, 
           District varchar(50),
           Transaction_count bigint,
           Transaction_amount float)'''
           )
eta.commit()
for _, row in map_trans.iterrows():
            insert_query = '''
                INSERT INTO Map_Transaction (State, Year, Quarter, District, Transaction_count, Transaction_amount)
                VALUES (%s, %s, %s, %s, %s, %s)

            '''
            values = (
                row['State'],
                row['Year'],
                row['Quarter'],
                row['District'],
                row['Transaction_count'],
                row['Transaction_amount']
            )
            cursor.execute(insert_query,values)
eta.commit()         


#4th table
cursor.execute('''create table if not exists Map_User(State varchar(50),
           Year int, 
           Quarter int, 
           District varchar(50),
           RegisteredUsers bigint,
           AppOpens bigint)'''
           )
eta.commit()
for _, row in Map_user.iterrows():
            insert_query = '''
                INSERT INTO Map_User (State, Year, Quarter, District, RegisteredUsers, AppOpens)
                VALUES (%s, %s, %s, %s, %s, %s)

            '''
            values = (
                row['State'],
                row['Year'],
                row['Quarter'],
                row['District'],
                row['RegisteredUsers'],
                row['AppOpens']
            )
            cursor.execute(insert_query,values)
eta.commit()   


#5
cursor.execute('''create table if not exists Top_trans(State varchar(50),
           Year int, 
           Quarter int, 
           Pincode int,
           Transaction_Count bigint,
           Transaction_Amount bigint)'''
           )
eta.commit()
for _, row in top_trans.iterrows():
            insert_query = '''
                INSERT INTO Top_trans (State, Year, Quarter, Pincode, Transaction_Count, Transaction_Amount)
                VALUES (%s, %s, %s, %s, %s, %s)

            '''
            values = (
                row['State'],
                row['Year'],
                row['Quarter'],
                row['Pincode'],
                row['Transaction_Count'],
                row['Transaction_Amount']
            )
            cursor.execute(insert_query,values)
eta.commit()         


#6
cursor.execute('''create table if not exists Top_user(State varchar(50),
           Year int, 
           Quarter int, 
           Pincode int,
           RegisteredUsers bigint)'''
           )
eta.commit()
for _, row in Top_user.iterrows():
            insert_query = '''
                INSERT INTO Top_user (State, Year, Quarter, Pincode, RegisteredUsers)
                VALUES (%s, %s, %s, %s, %s)

            '''
            values = (
                row['State'],
                row['Year'],
                row['Quarter'],
                row['Pincode'],
                row['RegisteredUsers']
            )
            cursor.execute(insert_query,values)
eta.commit()         


def page1():
    st.title('Page 1')
    st.write('Welcome to Page 1!')
    #page 1
    #animated transaction count
    # Load the GeoJSON data
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
    state_names_tra.sort()

    # Create a DataFrame with the state names column
    df_state_names_tra = pd.DataFrame({'State': state_names_tra})

    # Initialize an empty list to store the frames
    frames = []

    # Iterate through each year and quarter
    for year in Agg_Trans['Year'].unique():
        for quarter in Agg_Trans['Quarter'].unique():
            # Filter the DataFrame for the current year and quarter
            at1 = Agg_Trans[(Agg_Trans['Year'] == year) & (Agg_Trans['Quarter'] == quarter)]
            atf1 = at1[['State', 'Transaction_count']]
            atf1 = atf1.sort_values(by='State')
            # Add 'Year' and 'Quarter' columns to match animation frames
            atf1['Year'] = year
            atf1['Quarter'] = quarter
            # Append the current frame to the list
            frames.append(atf1)

    # Concatenate all frames into a single DataFrame
    merged_df = pd.concat(frames)

    # Define the choropleth map figure with animation_frame set to 'Year' and 'Quarter'
    fig_tra = px.choropleth(
        merged_df, 
        geojson=data1, 
        locations='State', 
        featureidkey='properties.ST_NM', 
        color='Transaction_count',
        color_continuous_scale='Sunsetdark',
        hover_name='State',
        title='Transaction Analysis',
        animation_frame='Year',  # Specify the column representing the years for animation
        animation_group='Quarter',  # Specify the column representing the quarters for animation
        height=800
    )

    # Adjust the map layout and display it
    fig_tra.update_geos(fitbounds="locations", visible=False)
    fig_tra.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
    #fig_tra.show()
    st.plotly_chart(fig_tra)
    tab1, tab2 = st.tabs(['Transaction Analysis','User'])

    # -------------------------       /     All India Transaction        /        ------------------ #
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            in_tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='in_tr_yr')
        with col2:
            in_tr_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='in_tr_qtr')


def page2():
    st.title('Page 2')
    st.write('Welcome to Page 2!')
    # Add your content for page 2 here

def main():
    st.sidebar.title('Navigation')
    selected_page = st.sidebar.radio('Go to:', ['Page 1', 'Page 2'])

    if selected_page == 'Page 1':
        page1()
    elif selected_page == 'Page 2':
        page2()

if __name__ == "__main__":
    main()





