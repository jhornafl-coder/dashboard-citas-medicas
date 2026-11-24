import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Citas Médicas", layout="wide")

@st.cache_data
def cargar_datos():
    df = pd.read_csv('citas_medicas.csv')
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month
    return df

df = cargar_datos()

st.title('🏥 Dashboard de Gestión de Citas Médicas')
st.markdown('**Hospital de Lima Norte** — Análisis de 5,000 citas')

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de citas", len(df))
col2.metric("Atendidas", f"{(df['estado']=='Atendida').mean()*100:.1f}%")
col3.metric("Canceladas", f"{(df['estado']=='Cancelada').mean()*100:.1f}%")
col4.metric("No asistió", f"{(df['estado']=='No asistió').mean()*100:.1f}%")

st.subheader('📊 Citas por Especialidad')
esp = df['especialidad'].value_counts().reset_index()
esp.columns = ['especialidad', 'cantidad']
fig1 = px.bar(esp, x='especialidad', y='cantidad',
              labels={'especialidad': 'Especialidad', 'cantidad': 'Cantidad'},
              color='cantidad', color_continuous_scale='Blues')
st.plotly_chart(fig1, use_container_width=True)

st.subheader('🥧 Estado de las Citas')
fig2 = px.pie(df, names='estado', hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

st.subheader('📈 Citas por Mes')
citas_mes = df.groupby('mes').size().reset_index(name='cantidad')
fig3 = px.line(citas_mes, x='mes', y='cantidad', markers=True,
               labels={'mes': 'Mes', 'cantidad': 'Cantidad de citas'})
st.plotly_chart(fig3, use_container_width=True)

st.subheader('👥 Distribución de Edades')
fig4 = px.histogram(df, x='edad', nbins=30, labels={'edad': 'Edad'})
st.plotly_chart(fig4, use_container_width=True)