# Run as
# streamlit run <filename.py>
import pandas as pd
import datetime as dt
import re
import streamlit as st
import plotly.express as px  # interactive charts
# Set wide layput as default
st.set_page_config(layout="wide")


df = pd.read_csv("Accidental_Drug_Related_Deaths_2012-2018.csv")
df = df[~ df['ResidenceCityGeo'].isna()]
df['latitude'] = df['ResidenceCityGeo'].apply(lambda x: re.findall(r'(\d+\.\d+|-\d+\.\d+)\,', str(x))[0]).astype(float)
df['longitude'] = df['ResidenceCityGeo'].apply(lambda x: re.findall(r'(\d+\.\d+|-\d+\.\d+)\)', str(x))[0]).astype(float)
df['radius'] = 40
opioid_cols = ['Heroin', 'Cocaine', 'Fentanyl', 'FentanylAnalogue', 'Oxycodone', 'Oxymorphone', 'Ethanol',
               'Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad', 'Morphine_NotHeroin', 'Hydromorphone',
               'Other', 'OpiateNOS', 'AnyOpioid']
longitudecenter = df["longitude"].mean()
latitudecenter = df["latitude"].mean()

# st.title("Opioid  Dashboard")
stateval = st.selectbox("Select State", df['InjuryState'].dropna().unique())
df_state = df[df["InjuryState"] == stateval]
df_state['Date'] = pd.to_datetime(df_state['Date'])
df_state['date'] = df_state['Date'].dt.strftime('%m-%Y')
df_state['Age'].fillna(0, inplace=True)

df2 = df_state[opioid_cols]
df2.fillna(0, inplace=True)
df2.replace('Y', 1, inplace=True)
df2 = df2.select_dtypes(['number'])
print(df2)

df3 = pd.DataFrame(df2.sum(axis=0))
df3.rename(columns={0: 'Count'}, inplace=True)
df3.index.name = 'Drug Name'


# create two columns for charts
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### Drug Overdose Incidence map in " + stateval)
    fig6 = px.scatter_mapbox(df_state, lat="latitude", lon="longitude", hover_name="InjuryCity",
                             hover_data=["Age", "Sex"], animation_frame="date", zoom=6)
    fig6.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig6.update_traces(marker={'size': 15})
    fig6.update_layout(mapbox_style="open-street-map")
    st.write(fig6)

    st.markdown("### Incidence timeline in " + stateval)
    fig4 = px.bar(df, x='Date')

    st.write(fig4)

with fig_col2:
    st.markdown("### Drugs used in " + stateval)
    fig1 = px.bar(data_frame=df3, y='Count')
    st.write(fig1)

    st.markdown("### Gender of subjects")
    fig2 = px.histogram(data_frame=df_state, x='Sex')
    st.write(fig2)
