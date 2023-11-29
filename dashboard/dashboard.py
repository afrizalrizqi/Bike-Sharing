import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import numpy as np

df = pd.read_csv("https://raw.githubusercontent.com/afrizalrizqi/Bike-Sharing/main/data/hour.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

st.set_page_config(page_title="Analisis Data : Bike Sharing",
                   page_icon="bar_chart",
                   layout="wide"
                   )

#Membuat helper function

def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='dteday').agg({
        "casual" : "sum",
        "registered" : "sum",
        "cnt" : "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "dteday" : "weathersit",
        "cnt" : "total_rides",
        "casual" : "casual_rides",
        "registered" : "registered_rides"
    }, inplace=True)
    
    return monthly_users_df

def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    seasonly_users_df = pd.melt(seasonly_users_df,
                                      id_vars=['season'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    seasonly_users_df = seasonly_users_df.sort_values('season')
    
    return seasonly_users_df

def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    weekday_users_df = pd.melt(weekday_users_df,
                                      id_vars=['weekday'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'],
                                             categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    weekday_users_df = weekday_users_df.sort_values('weekday')
    
    return weekday_users_df

def create_hourly_users_df(df):
    hourly_users_df = df.groupby("hr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return hourly_users_df

#Make filter components (komponen filter)

min_date = df["dteday"].min()
max_date = df["dteday"].max()

# SIDEBAR

with st.sidebar:
    st.sidebar.header("Filter")
    
    #mengambil start date dan end date
    start_date, end_date = st.date_input(
        label = "Data Filter", min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )
    
st.sidebar.header("Visit My Profile")
    
st.sidebar.markdown("Afrizal Rizqi Syahputra")
    
col1, col2 = st.sidebar.columns(2)
    
#hubungkan filter dengan main_df
main_df = df[
    (df["dteday"] >= str(start_date)) &
    (df["dteday"] <= str(end_date))
]
    
# assign main_df ke helper functions yang telah dibuat sebelumnya

monthly_users_df = create_monthly_users_df(main_df)
weekday_users_df = create_weekday_users_df(main_df)
seasonly_users_df = create_seasonly_users_df(main_df)
hourly_users_df = create_hourly_users_df(main_df)

# MAINPAGE
st.title(":bar_chart: Analisis Data Bike Sharing")
st.markdown("##")

col1, col2 = st.columns(2)

with col1:
    registered_users = main_df['registered'].sum()
    st.metric("Registered Users", value = registered_users)
    
with col2:
    casual_users = main_df['casual'].sum()
    st.metric("Casual Users", value = casual_users)

st.markdown('---')

# CHART
# fig = px.bar(monthly_users_df,
#               x='weathersit',
#               y=['casual_rides', 'registered_rides'],
#               title="Pada musim apa banyak pengguna"
#               )
# st.plotly_chart(fig, use_container_width=True)


question1 = main_df.groupby(by="weathersit").dteday.nunique().sort_values(ascending=False)
print(question1)
# biw=plt.bar(['1','2','3'], question1)

x = np.linspace(main_df)
y = np.sin(x)

fig, ax=plt.subplots()
ax.plot(x,y)

# st.plotly_chart(biw, use_container_width=True)