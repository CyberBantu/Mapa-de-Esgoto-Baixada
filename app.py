import streamlit as st
import pandas as pd
import plotly.express as px
import geobr

# Carrega os dados
mapa = geobr.read_census_tract(code_tract=33)
dados_ibge = pd.read_excel('Baixada_esgoto.xlsx')
mapa['code_tract'] = pd.to_numeric(mapa['code_tract'], errors='coerce')
dados_ibge['Cod_setor'] = pd.to_numeric(dados_ibge['Cod_setor'], errors='coerce')
resultado = pd.merge(mapa, dados_ibge, left_on='code_tract', right_on='Cod_setor', how='inner')
resultado.crs = "EPSG:4326"  # Define o CRS como WGS

# Exibe o gráfico no Streamlit
st.set_page_config(layout="wide")
st.header('Mapa de Esgoto a Céu Aberto na Baixada Fluminense')
st.caption('Fonte - Censo de 2010')
st.markdown(
    """
    <style>
    .reportview-container {
        max-width: 90%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
fig = px.choropleth_mapbox(resultado,
                            geojson=resultado.geometry,
                            locations=resultado.index,
                            color='Porc_geral',
                            color_continuous_scale="YlOrRd",
                            range_color=(0, resultado['Porc_geral'].max()),
                            mapbox_style="carto-positron",
                            center={"lat": resultado.centroid.y.mean(), "lon": resultado.centroid.x.mean()},
                            zoom=10,
                            opacity=0.35,
                            labels={'Porc_geral': 'Esgoto a Céu Aberto (%)',
                                    'name_muni': 'Município',
                                    'zone': 'Zona',
                                    'name_district': 'Distrito',
                                    'Nome_do_bairro': 'Bairro'},
                            hover_data={'name_muni': True,
                                        'zone': True,
                                        'name_district': True,
                                        'Nome_do_bairro': True,
                                        'Porc_geral': True},
                                          width=1200,  # Ajuste a largura
                                            height=800)
st.plotly_chart(fig, use_container_width=True)
