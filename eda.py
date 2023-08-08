
import pandas as pd
import json
import os
import plotly.express as px
import requests
import subprocess
import plotly.graph_objects as go
from IPython.display import display
import psycopg2
import streamlit as st
from PIL import Image as PILImage

#Enter your the port, database 
#Enter your password
host = 'xxx'
port = 'yyy'
database = 'zzz'
username = 'aaa'
password = 'kkk'

st.set_page_config(layout='wide')

eta = psycopg2.connect(host=host, port=port, database=database, user=username, password=password)
cursor=eta.cursor()


cursor.execute("select * from Aggregate_transaction;")
eta.commit()
t1=cursor.fetchall()
Agg_Trans=pd.DataFrame(t1, columns=['State', 'Year', 'Quarter', 'Transaction_type', 'Transaction_count', 'Transaction_amount'])


cursor.execute("select * from Aggregate_user;")
eta.commit()
t2=cursor.fetchall()
Agg_user=pd.DataFrame(t2, columns=['State', 'Year', 'Quarter', 'Brands', 'Transaction_Count', 'Percentage'])


cursor.execute("select * from map_transaction;")
eta.commit()
t3=cursor.fetchall()
map_trans=pd.DataFrame(t3, columns=['State', 'Year', 'Quarter', 'District', 'Transaction_count', 'Transaction_amount'])


cursor.execute("select * from map_user;")
eta.commit()
t4=cursor.fetchall()
map_user=pd.DataFrame(t4, columns=['State', 'Year', 'Quarter', 'District', 'RegisteredUsers', 'AppOpens'])


cursor.execute("select * from top_trans;")
eta.commit()
t5=cursor.fetchall()
top_trans=pd.DataFrame(t5, columns=['State', 'Year', 'Quarter', 'Pincode', 'Transaction_Count', 'Transaction_Amount'])


cursor.execute("select * from top_user;")
eta.commit()
t6=cursor.fetchall()
top_user=pd.DataFrame(t6, columns=['State', 'Year', 'Quarter', 'Pincode', 'RegisteredUsers'])

#*******************************************************************************************************************************************

def animate_all():
    
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
        range_color=(0,500000000),
        hover_name='State',
        title='TRANSACTION COUNT',
        animation_frame='Year',  # Specify the column representing the years for animation
        animation_group='Quarter',  # Specify the column representing the quarters for animation
        height=600
    )

    # Adjust the map layout and display it
    fig_tra.update_geos(fitbounds="locations", visible=False)
    fig_tra.update_layout(width=600, height=700)
    fig_tra.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
    st.plotly_chart(fig_tra)
#=======================================================================================================================================

def animate_all_amount():
    
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
    for year in map_user['Year'].unique():
        for quarter in Agg_Trans['Quarter'].unique():
            # Filter the DataFrame for the current year and quarter
            at1 = Agg_Trans[(Agg_Trans['Year'] == year) & (Agg_Trans['Quarter'] == quarter)]
            atf1 = at1[['State', 'Transaction_amount']]
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
        color='Transaction_amount',
        color_continuous_scale='Sunsetdark',
        range_color=(0-1,200000000000),
        hover_name='State',
        title='TRANSACTION AMOUNT',
        animation_frame='Year',  # Specify the column representing the years for animation
        animation_group='Quarter',  # Specify the column representing the quarters for animation
        height=600
    )

    # Adjust the map layout and display it
    fig_tra.update_geos(fitbounds="locations", visible=False)
    fig_tra.update_layout(width=600, height=700)
    fig_tra.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
    st.plotly_chart(fig_tra)
    
def Trans_amount(yr):
    year=int(yr)
    at=Agg_Trans[['State','Year','Quarter','Transaction_amount']]
    at1=at.loc[(at['Year']==year)]

    atf1=at1[['State','Transaction_amount']]
    atf1=atf1.sort_values(by='State')

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
    state_names_tra.sort()
    # Create a DataFrame with the state names column
    df_state_names_tra = pd.DataFrame({'State': state_names_tra})
    merged_df = df_state_names_tra.merge(atf1, on='State')


    # Merge the two DataFrames on the 'State' column
    merged_df = df_state_names_tra.merge(atf1, on='State')
    merged_df.to_csv('State_trans.csv', index=False)
    # Read csv
    df_tra = pd.read_csv('State_trans.csv')
    fig_tra = px.choropleth(
                df_tra,
                         geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                
        featureidkey='properties.ST_NM',
        locations='State',color='Transaction_amount',
        title='TRANSACTION AMOUNT',
        color_continuous_scale='Sunsetdark',
        range_color=(0,145000000000)
    )
    fig_tra.update_geos(fitbounds="locations", visible=False)
    fig_tra.update_layout(width=600, height=700)
    fig_tra.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
    st.plotly_chart(fig_tra)

    
    
    
def Trans_count(yr):
    year=int(yr)
    at=Agg_Trans[['State','Year','Quarter','Transaction_count']]
    at1=at.loc[(at['Year']==year)]

    atf1=at1[['State','Transaction_count']]
    atf1=atf1.sort_values(by='State')

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
    state_names_tra.sort()
    # Create a DataFrame with the state names column
    df_state_names_tra = pd.DataFrame({'State': state_names_tra})
    merged_df = df_state_names_tra.merge(atf1, on='State')


    # Merge the two DataFrames on the 'State' column
    merged_df = df_state_names_tra.merge(atf1, on='State')
    merged_df.to_csv('State_trans.csv', index=False)
    # Read csv
    df_tra = pd.read_csv('State_trans.csv')
    fig_tra = px.choropleth(
                df_tra,
                         geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                
        featureidkey='properties.ST_NM',
        locations='State',
        color='Transaction_count',
        title='TRANSACTION COUNT',
        color_continuous_scale='Sunsetdark',
        range_color=(0,250000000)
    )
    fig_tra.update_geos(fitbounds="locations", visible=False)
    # Customize the size (width and height) of the choropleth map
    fig_tra.update_layout(width=600, height=700)
    fig_tra.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
    st.plotly_chart(fig_tra)
    
    
    
def Payment_count():
    attype=Agg_Trans[['Transaction_type','Transaction_count']]
    att1=attype.groupby('Transaction_type')['Transaction_count'].sum()
    att1_df= pd.DataFrame(att1).reset_index()
    fig=px.bar(att1_df, x='Transaction_type',y='Transaction_count',
               title='TRANSACTION TYPE vs TRANSACTION COUNT',
               color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(width=500, height=400)
    
    return st.plotly_chart(fig)

def Payment_amount():
    attype=Agg_Trans[['Transaction_type','Transaction_amount']]
    att1=attype.groupby('Transaction_type')['Transaction_amount'].sum()
    att1_df= pd.DataFrame(att1).reset_index()
    fig=px.bar(att1_df,x='Transaction_type',y='Transaction_amount',
                title='TRANSACTION TYPE vs TRANSACTION AMOUNT',
               color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(width=500, height=400)
    return st.plotly_chart(fig)
    
def payment_count_y(year):
    yr=int(year)
    attype=Agg_Trans[['Year','Transaction_type','Transaction_count']]
    att1=attype.loc[(attype['Year']==yr)]

    att1=att1.groupby('Transaction_type')['Transaction_count'].sum()
    #att1_df=pd.DataFrame(att1)
    att1_df= pd.DataFrame(att1).reset_index()
    fig=px.bar(att1_df,x='Transaction_type',y='Transaction_count', 
                title='TRANSACTION TYPE vs TRANSACTION COUNT',
               color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(width=500, height=400)
    return st.plotly_chart(fig)

def payment_amount_y(year):
    yr=int(year)
    attype=Agg_Trans[['Year','Transaction_type','Transaction_amount']]
    att1=attype.loc[(attype['Year']==yr)]

    att1=att1.groupby('Transaction_type')['Transaction_amount'].sum()
    #att1_df=pd.DataFrame(att1)
    att1_df= pd.DataFrame(att1).reset_index()
    fig=px.bar(att1_df,x='Transaction_type',y='Transaction_amount', 
                title='TRANSACTION TYPE vs TRANSACTION AMOUNT',
               color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(width=500, height=400)
    return st.plotly_chart(fig)


def reg_state_all(state):
    mu=map_user[['State','District','RegisteredUsers']]
    mu1=mu.loc[(mu['State']==state)]
    mu2=mu1.groupby('District')['RegisteredUsers'].sum()
    bt = pd.DataFrame(mu2).reset_index()
    fig = px.bar(bt, x='District', y='RegisteredUsers',
                 title="REGISTERED USERS IN EACH DISTRICTS",
                 color_discrete_sequence=px.colors.sequential.Agsunset)
    fig.update_layout(width=1300, height=400)
    return st.plotly_chart(fig)

def reg_state(state,year):
    yr=int(year)
    mu=map_user[['State','Year','District','RegisteredUsers']]
    mu1=mu.loc[(mu['State']==state)&(mu['Year']==yr)]
    mu2=mu1.groupby('District')['RegisteredUsers'].sum()
    bt = pd.DataFrame(mu2).reset_index()
    fig = px.bar(bt, x='District', y='RegisteredUsers',
                 title="REGISTERED USERS IN EACH DISTRICTS",
                 color_discrete_sequence=px.colors.sequential.Agsunset)
    fig.update_layout(width=1300, height=400)
    return st.plotly_chart(fig)
    


#preprossed for animation
def ani():
    ag=Agg_Trans
    #Convert integer columns to strings
    ag['Year'] = ag['Year'].astype(str)
    ag['Quarter'] = ag['Quarter'].astype(str)

    # Merge columns using a hyphen ("-") as separator
    ag['Year-Q'] = ag.apply(lambda row: '-'.join([row['Year'], row['Quarter']]), axis=1)

    # Drop the original columns if needed
    ag.drop(columns=['Year', 'Quarter'], inplace=True)
    
    
#*************************************************Queries********************************************************************************** 

def one():
    au=Agg_user[['Brands','Transaction_Count']]
    brand_transaction_counts = au.groupby('Brands')['Transaction_Count'].sum()
    bt = pd.DataFrame(brand_transaction_counts).reset_index()


    fig= px.pie(bt, values='Transaction_Count',
                 names='Brands',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig)
    
def two():
    ag1 = Agg_Trans[['State','Transaction_amount']]
    ag1 = ag1.groupby('State')['Transaction_amount'].sum()
    ag1 = ag1.sort_values()

    agi = ag1.head(10)
    fig = px.bar(agi, x=agi.index, y='Transaction_amount',color_discrete_sequence=px.colors.sequential.RdBu)  
    st.plotly_chart(fig)
    
def three():
    mt = map_trans[['District', 'Transaction_amount']]
    mt = mt.groupby('District')['Transaction_amount'].sum()
    mt1 = mt.sort_values(ascending=False).head(10).reset_index()  # Reset the index to get 'District' as a column
    fig = px.bar(mt1, x='District', y='Transaction_amount', color='District', color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig)
    
def four():
    mt = map_trans[['District', 'Transaction_count']]
    mt = mt.groupby('District')['Transaction_count'].sum()
    mt1 = mt.sort_values(ascending=False).head(10).reset_index()  # Reset the index to get 'District' as a column
    fig = px.bar(mt1, x='District', y='Transaction_count', color='District', color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig)
    
def five():
    mu=map_user[["State",'AppOpens']]
    mu1=mu.groupby('State')['AppOpens'].sum()
    bt = pd.DataFrame(mu1).reset_index()
    bt=bt.sort_values(by='AppOpens')
    bt1=bt.head(10)
    fig=px.bar(bt1, x='State', y='AppOpens',color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig)
    
def six():
    mu=map_user[["State",'AppOpens']]
    mu1=mu.groupby('State')['AppOpens'].sum()
    bt = pd.DataFrame(mu1).reset_index()
    bt=bt.sort_values(by='AppOpens')
    bt1=bt.tail(10)
    fig=px.bar(bt1, x='State', y='AppOpens',color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig) 
def seven():
    ag1 = Agg_Trans[['State','Transaction_count']]
    ag1 = ag1.groupby('State')['Transaction_count'].sum()
    ag1 = ag1.sort_values()
    agi = ag1.head(10)
    fig = px.bar(agi, x=agi.index, y='Transaction_count',color_discrete_sequence=px.colors.sequential.RdBu)  
    st.plotly_chart(fig)

def eight():
    ag1 = Agg_Trans[['State','Transaction_count']]
    ag1 = ag1.groupby('State')['Transaction_count'].sum()
    ag1 = ag1.sort_values()
    agi = ag1.tail(10)
    fig = px.bar(agi, x=agi.index, y='Transaction_count',color_discrete_sequence=px.colors.sequential.RdBu)  
    st.plotly_chart(fig)
    
def nine():
    ag1 = Agg_Trans[['State','Transaction_amount']]
    ag1 = ag1.groupby('State')['Transaction_amount'].sum()
    ag1 = ag1.sort_values()
    agi = ag1.tail(10)
    fig = px.bar(agi, x=agi.index, y='Transaction_amount',color_discrete_sequence=px.colors.sequential.RdBu)  
    st.plotly_chart(fig)
    
def ten():
    mt = map_trans[['District', 'Transaction_amount']]
    mt = mt.groupby('District')['Transaction_amount'].sum()
    mt1 = mt.sort_values(ascending=False).tail(10).reset_index()  # Reset the index to get 'District' as a column
    fig = px.bar(mt1, x='District', y='Transaction_amount', color='District', color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig)

#**********************************************streamlit part******************************************************************************

#st.set_page_config(layout=='wide')
st.title('PHONEPE DATA VISUALIZATION AND EXPLORATION')
tab1, tab2, tab3 = st.tabs(['Home','Explore Data','Top Charts'])


with tab1:
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("ABOUT:")
        st.write("PhonePe, founded in December 2015, stands as India's premier digital payment app, revolutionizing financial transactions. By linking bank accounts, credit, and debit cards to its mobile wallet, PhonePe enables convenient digital payments, including groceries, bills, and transfers. As a leader in the sector, it has streamlined banking and finance while enhancing security and accessibility.")
        image_path = r"your image location"
        col1.image(PILImage.open(image_path), width=300)
                                      
    with col2:
        st.header("SERVICES PROVIDED:")
        st.write('PhonePe is a prominent digital payment platform in India that offers:')
        st.write('1. UPI Payments: Send money, pay bills, and make purchases using UPI.')
        st.write('2. Recharge and Bills: Recharge phones, pay utility bills, and settle expenses.')
        st.write('3. Money Transfers: Instantly transfer money to contacts and bank accounts.')
        st.write('4. Online/Offline Payments: Pay at merchants using QR codes.')
        st.write('5. Investments: Invest in mutual funds and buy gold.')
        st.write('6. Insurance: Purchase health insurance policies.')         
        st.write('7. Credit Services: Access personal loans and credit cards.')
        st.write('8. Travel Booking: Book flights, buses, and hotels.')
        st.write('9. Gift Cards: Buy and send digital gift cards.')
        st.write('10. E-commerce: Shop various products and services.')
        
    with col3:   
        with st.container():
            video_path = r"C:\Users\USER\Downloads\phonepe.mp4"  # Use raw string or double backslashes
            st.video(video_path)
        
with tab2:
    tr_year = st.selectbox('**Select Year**', ('All','2018','2019','2020','2021','2022'))
    if tr_year == 'All':
        col1, col2 = st.columns(2)
        with col1:
            animate_all_amount()
            Payment_count()
        with col2:
            animate_all()
            Payment_amount()
        state=st.selectbox('**Select State**',('Andaman & Nicobar Islands','Andhra Pradesh', 'Arunachal Pradesh',
       'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
       'Dadra & Nagar Haveli & Daman & Diu', 'Delhi', 'Goa', 'Gujarat',
       'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand',
       'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh',
       'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
       'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim',
       'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
       'Uttarakhand', 'West Bengal'))
        reg_state_all(state)
        
    
    else:
        col1, col2 = st.columns(2)
        with col1:
            Trans_amount(tr_year)
            payment_count_y(tr_year)
        with col2:
            Trans_count(tr_year)
            payment_amount_y(tr_year)
        state=st.selectbox('**Select State**',('Andaman & Nicobar Islands','Andhra Pradesh', 'Arunachal Pradesh',
       'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
       'Dadra & Nagar Haveli & Daman & Diu', 'Delhi', 'Goa', 'Gujarat',
       'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand',
       'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh',
       'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
       'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim',
       'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
       'Uttarakhand', 'West Bengal'))
        reg_state(state,tr_year)
        
        
            
with tab3:
    q=st.selectbox('**Select**', ('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Districts With Lowest Transaction Cmount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Districts With Lowest Transaction Amount'))
    if q=='Top Brands Of Mobiles Used':
        one()
    elif q=='States With Lowest Trasaction Amount':
        two()
    elif q=='Districts With Highest Transaction Amount':
        three()
    elif q=='Districts With Lowest Transaction Count':
        four()
    elif q=='Top 10 States With AppOpens':
        five()
    elif q=='Least 10 States With AppOpens':
        six()
    elif q=='States With Lowest Trasaction Count':
        seven()
    elif q=='States With Highest Trasaction Count':
        eight()
    elif q=='States With Highest Trasaction Amount':
        nine()
    elif q=='Districts With Lowest Transaction Amount':
        ten()
        


