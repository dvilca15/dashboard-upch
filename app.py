import re
import pandas as pd
from dash import Dash, dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import os

UPCH = "UNIVERSIDAD PERUANA CAYETANO HEREDIA"

# ================================
#  LEER EXCEL
# ================================
df = pd.read_excel("EXCEL BASE.xlsx", sheet_name="SEGUIMIENTO")

# ================================
#  CONTADORES 1M / 2M (UPCH)
# ================================
df_filtrado_2m = df[df["IES 2M"] == UPCH]
condicion_count_2m = (df_filtrado_2m["CONDICIÓN FINAL 2M"] == "SELECCIONADO").sum()
becario_count_2m = df_filtrado_2m["BECARIO 2M"].isin(["BECARIO", "ACEPTO"]).sum()

df_filtrado_1m = df[df["IES 1M"] == UPCH]
condicion_count_1m = (df_filtrado_1m["CONDICIÓN FINAL 1M"] == "SELECCIONADO").sum()
becario_count_1m = df_filtrado_1m["BECARIO 1M"].isin(["BECARIO", "ACEPTO"]).sum()

# ================================
#  TARJETAS: TOTAL Y CRECIMIENTO
# ================================
total_becarios = becario_count_1m + becario_count_2m
crecimiento_becarios = ((becario_count_2m - becario_count_1m) / becario_count_1m) * 100 if becario_count_1m > 0 else 0

# ================================
#  GRÁFICO COMPARATIVO 1M vs 2M MEJORADO
# ================================
def crear_grafico_comparativo():
    fig = go.Figure()
    
    # Seleccionados
    fig.add_trace(go.Bar(
        name='Seleccionados',
        x=['Primer Momento', 'Segundo Momento'],
        y=[condicion_count_1m, condicion_count_2m],
        marker_color='#00D4FF',
        text=[f'{condicion_count_1m}', f'{condicion_count_2m}'],
        textposition='outside',
        textfont=dict(size=14, color='white', family='Inter'),
        marker_line=dict(color='rgba(255,255,255,0.3)', width=2)
    ))
    
    # Becarios
    fig.add_trace(go.Bar(
        name='Becarios',
        x=['Primer Momento', 'Segundo Momento'],
        y=[becario_count_1m, becario_count_2m],
        marker_color='#FF6B6B',
        text=[f'{becario_count_1m}', f'{becario_count_2m}'],
        textposition='outside',
        textfont=dict(size=14, color='white', family='Inter'),
        marker_line=dict(color='rgba(255,255,255,0.3)', width=2)
    ))
    
    fig.update_layout(
        title={
            'text': '<b>📊 Seleccionados y Becarios UPCH</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#00D4FF', 'family': 'Inter'}
        },
        barmode='group',
        bargap=0.4,
        bargroupgap=0.15,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color="white"),
        height=350,
        margin=dict(t=80, b=60, l=40, r=40),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=12, color='white', family='Inter')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(size=11, color='white')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color='white', family='Inter')
        )
    )
    
    return fig

# ================================
#  BECARIOS POR CARRERA (1M+2M) – SOLO UPCH
# ================================
def limpiar_carrera(x):
    if pd.isna(x):
        return None
    s = str(x).upper().strip()
    s = (s.replace("Á","A").replace("É","E").replace("Í","I")
           .replace("Ó","O").replace("Ú","U").replace("Ü","U")
           .replace("Ñ","N"))
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^A-Z0-9\s]", "", s)
    return s

df_1m_carr = df[
    (df["IES 1M"] == UPCH) &
    (df["BECARIO 1M"].isin(["BECARIO", "ACEPTO"]))
][["CARRERA ELEGIDA 1M"]].rename(columns={"CARRERA ELEGIDA 1M":"CARRERA"})

df_2m_carr = df[
    (df["IES 2M"] == UPCH) &
    (df["BECARIO 2M"].isin(["BECARIO", "ACEPTO"]))
][["CARRERA ELEGIDA 2M"]].rename(columns={"CARRERA ELEGIDA 2M":"CARRERA"})

df_carreras = pd.concat([df_1m_carr, df_2m_carr], ignore_index=True)
df_carreras["CARRERA"] = df_carreras["CARRERA"].apply(limpiar_carrera)
df_carreras = df_carreras.dropna(subset=["CARRERA"])

carreras_filtrar = [
    "PSICOLOGIA",
    "ENFERMERIA",
    "ESTOMATOLOGIA",
    "INGENIERIA INFORMATICA",
    "INGENIERIA INDUSTRIAL",
    "FARMACIA Y BIOQUIMICA",
    "INGENIERIA AMBIENTAL",
    "BIOLOGIA",
    "MEDICINA VETERINARIA Y ZOOTECNIA",
    "TECNOLOGIA MEDICA EN LA ESPECIALIDAD DE LABORATORIO CLINICO Y ANATOMIA PATOLOGICA",
]
df_carreras = df_carreras[df_carreras["CARRERA"].isin(carreras_filtrar)]

df_carreras_count = (
    df_carreras.groupby("CARRERA")
    .size()
    .reset_index(name="TOTAL")
)

# 🔹 Acortar nombre largo SOLO para el gráfico
df_carreras_count["CARRERA"] = df_carreras_count["CARRERA"].replace(
    {"TECNOLOGIA MEDICA EN LA ESPECIALIDAD DE LABORATORIO CLINICO Y ANATOMIA PATOLOGICA":
     "LABORATORIO CLINICO Y ANATOMIA PATOLOGICA"}
)

df_carreras_count = df_carreras_count.sort_values("TOTAL", ascending=True)

def crear_grafico_carreras():
    fig = go.Figure()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
              '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9']
    
    fig.add_trace(go.Bar(
        y=df_carreras_count["CARRERA"],
        x=df_carreras_count["TOTAL"],
        orientation='h',
        marker_color=colors[:len(df_carreras_count)],
        text=df_carreras_count["TOTAL"],
        textposition='outside',
        textfont=dict(size=12, color='white', family='Inter'),
        marker_line=dict(color='rgba(255,255,255,0.2)', width=1)
    ))
    
    fig.update_layout(
        title={
            'text': '<b>📚 Becarios por Carrera</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#00D4FF', 'family': 'Inter'}
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=11, color="white"),
        height=350,
        margin=dict(t=80, b=40, l=40, r=40),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(size=11, color='white')
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=10, color='white')
        )
    )
    
    return fig

# ================================
#  TABLA: BECARIOS POR MODALIDAD (1M+2M)
# ================================
df_modalidad = pd.concat([
    df[(df["IES 1M"] == UPCH) & (df["BECARIO 1M"].isin(["BECARIO", "ACEPTO"]))][["MODALIDAD"]],
    df[(df["IES 2M"] == UPCH) & (df["BECARIO 2M"].isin(["BECARIO", "ACEPTO"]))][["MODALIDAD"]]
])

df_modalidad_count = (
    df_modalidad.groupby("MODALIDAD")
    .size()
    .reset_index(name="TOTAL")
)
df_modalidad_count["PORCENTAJE"] = (df_modalidad_count["TOTAL"] / df_modalidad_count["TOTAL"].sum()) * 100
df_modalidad_count["PORCENTAJE"] = df_modalidad_count["PORCENTAJE"].round(2).astype(str) + "%"

# 🔹 ORDENAR DE MAYOR A MENOR
df_modalidad_count = df_modalidad_count.sort_values("TOTAL", ascending=False)

tabla_modalidad = dash_table.DataTable(
    columns=[
        {"name": "MODALIDAD", "id": "MODALIDAD"},
        {"name": "TOTAL", "id": "TOTAL"},
        {"name": "PORCENTAJE", "id": "PORCENTAJE"},
    ],
    data=df_modalidad_count.to_dict("records"),
    style_table={
        "overflowX": "auto",
        "backgroundColor": "rgba(0,0,0,0)",
        "border": "none",
        "height": "300px"  # 🔹 ALTURA FIJA PARA LA TABLA
    },
    style_header={
        "backgroundColor": "rgba(0, 212, 255, 0.2)",
        "color": "#00D4FF",
        "fontWeight": "bold",
        "textAlign": "center",
        "fontFamily": "Inter, sans-serif",
        "fontSize": "14px",
        "border": "1px solid rgba(0, 212, 255, 0.3)"
    },
    style_cell={
        "textAlign": "center",
        "backgroundColor": "rgba(255, 255, 255, 0.01)",
        "color": "white",
        "fontFamily": "Inter, sans-serif",
        "fontSize": "12px",
        "border": "1px solid rgba(255,255,255,0.1)",
        "padding": "12px"
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgba(255, 255, 255, 0.02)'
        }
    ]
)

# ================================
#  NUEVO GRÁFICO: BECARIOS POR UNIVERSIDAD (1M vs 2M)
# ================================
universidades_filtro = [
    "UNIVERSIDAD PERUANA DE CIENCIAS APLICADAS S.A.C.",
    "UNIVERSIDAD CIENTIFICA DEL SUR S.A.C.",
    "UNIVERSIDAD PERUANA CAYETANO HEREDIA",
    "PONTIFICIA UNIVERSIDAD CATOLICA DEL PERU",
    "UNIVERSIDAD CONTINENTAL",
    "UNIVERSIDAD DE PIURA",
    "UNIVERSIDAD DE SAN MARTIN DE PORRES",
    "UNIVERSIDAD PRIVADA SAN IGNACIO DE LOYOLA",
    "UNIVERSIDAD PERUANA UNION",
    "UNIVERSIDAD DEL PACIFICO"
]

df_uni_1m = df[(df["BECARIO 1M"].isin(["BECARIO", "ACEPTO"])) & (df["IES 1M"].isin(universidades_filtro))][["IES 1M"]].rename(columns={"IES 1M": "UNIVERSIDAD"})
df_uni_2m = df[(df["BECARIO 2M"].isin(["BECARIO", "ACEPTO"])) & (df["IES 2M"].isin(universidades_filtro))][["IES 2M"]].rename(columns={"IES 2M": "UNIVERSIDAD"})

conteo_1m = df_uni_1m.value_counts().reset_index(name="PRIMER MOMENTO")
conteo_2m = df_uni_2m.value_counts().reset_index(name="SEGUNDO MOMENTO")

df_universidades = pd.merge(conteo_1m, conteo_2m, on="UNIVERSIDAD", how="outer").fillna(0).astype({"PRIMER MOMENTO": int, "SEGUNDO MOMENTO": int})
df_universidades = df_universidades.set_index("UNIVERSIDAD").loc[universidades_filtro].reset_index()

# 🔹 ORDENAR POR TOTAL DE BECARIOS (SUMA DE AMBOS MOMENTOS) DE MAYOR A MENOR
df_universidades["TOTAL_BECARIOS"] = df_universidades["PRIMER MOMENTO"] + df_universidades["SEGUNDO MOMENTO"]
df_universidades = df_universidades.sort_values("TOTAL_BECARIOS", ascending=True)  # ascending=True para que en el gráfico horizontal aparezca de mayor a menor


def crear_grafico_universidades():
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Primer Momento',
        y=df_universidades["UNIVERSIDAD"],
        x=df_universidades["PRIMER MOMENTO"],
        orientation='h',
        marker_color='#4ECDC4',
        text=df_universidades["PRIMER MOMENTO"],
        textposition='outside',
        textfont=dict(size=11, color='white', family='Inter'),
        marker_line=dict(color='rgba(255,255,255,0.3)', width=2)
    ))
    
    fig.add_trace(go.Bar(
        name='Segundo Momento',
        y=df_universidades["UNIVERSIDAD"],
        x=df_universidades["SEGUNDO MOMENTO"],
        orientation='h',
        marker_color='#FF6B6B',
        text=df_universidades["SEGUNDO MOMENTO"],
        textposition='outside',
        textfont=dict(size=11, color='white', family='Inter'),
        marker_line=dict(color='rgba(255,255,255,0.3)', width=2)
    ))
    
    fig.update_layout(
        title={
            'text': '<b>🏛️ Becarios por Universidad</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#00D4FF', 'family': 'Inter'}
        },
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=10, color="white"),
        height=350,  # 🔹 MISMA ALTURA QUE LOS OTROS GRÁFICOS
        margin=dict(t=80, b=40, l=40, r=40),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(size=10, color='white')
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=9, color='white')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color='white', family='Inter')
        )
    )
    
    return fig

# CSS personalizado modificado para contenedores de igual altura
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

body {
    font-family: 'Inter', sans-serif !important;
    background: linear-gradient(135deg, #0F0F0F 0%, #1a1a2e 50%, #16213e 100%) !important;
    min-height: 100vh;
}

.main-container {
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
    padding: 2rem;
    margin: 2rem auto;
}

.metric-card {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(255, 107, 107, 0.15) 100%);
    border: 2px solid rgba(0, 212, 255, 0.4);
    border-radius: 15px;
    padding: 1.8rem;
    text-align: center;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    margin-bottom: 1rem;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
}

.metric-card-growth {
    border: 2px solid rgba(76, 205, 196, 0.4);
    background: linear-gradient(135deg, rgba(76, 205, 196, 0.15) 0%, rgba(255, 107, 107, 0.15) 100%);
}

.metric-number {
    font-size: 3.5rem;
    font-weight: 800;
    color: white;
    text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    margin-bottom: 0.5rem;
}

.metric-label {
    color: #E0E0E0;
    font-size: 1.2rem;
    margin-top: 0.5rem;
    font-weight: 600;
}

.main-title {
    background: linear-gradient(45deg, #00D4FF, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-align: center;
}

.subtitle {
    color: #B0B0B0;
    font-size: 1.2rem;
    font-weight: 300;
    text-align: center;
    margin-bottom: 3rem;
}

.chart-container {
    background: rgba(255, 255, 255, 0.01);
    border-radius: 15px;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 2rem;
    height: 430px; /* 🔹 ALTURA FIJA PARA TODOS LOS CONTENEDORES */
    display: flex;
    flex-direction: column;
}

.table-container {
    background: rgba(255, 255, 255, 0.01);
    border-radius: 15px;
    padding: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 2rem;
    height: 430px; /* 🔹 MISMA ALTURA QUE LOS GRÁFICOS */
    display: flex;
    flex-direction: column;
}

.table-title {
    color: #00D4FF;
    font-size: 1.5rem;
    font-weight: 600;
    text-align: center;
    margin-bottom: 1.5rem;
    flex-shrink: 0; /* 🔹 NO SE ENCOGE */
}

.table-content {
    flex: 1; /* 🔹 TOMA TODO EL ESPACIO DISPONIBLE */
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}
"""

# ================================
#  DASH APP
# ================================
app = Dash(__name__, external_stylesheets=[
    dbc.themes.CYBORG,
    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
])

# Inyectar CSS personalizado
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
''' + custom_css + '''
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    dbc.Container([
        # Header principal
        html.H1("🎓 Dashboard UPCH 2025", className="main-title"),
        html.P("Universidad Peruana Cayetano Heredia", className="subtitle"),
        
        # Tarjetas de métricas
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div(f"{total_becarios}", className="metric-number"),
                    html.Div("Total Becarios", className="metric-label")
                ], className="metric-card")
            ], md=6),
            
            dbc.Col([
                html.Div([
                    html.Div(f"{crecimiento_becarios:.1f}%", className="metric-number"),
                    html.Div("Crecimiento de Becarios", className="metric-label")
                ], className="metric-card metric-card-growth")
            ], md=6)
        ], className="mb-4"),
        
        # Primera fila de gráficos
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(figure=crear_grafico_comparativo(), config={'displayModeBar': False})
                ], className="chart-container")
            ], md=6),
            
            dbc.Col([
                html.Div([
                    dcc.Graph(figure=crear_grafico_carreras(), config={'displayModeBar': False})
                ], className="chart-container")
            ], md=6)
        ]),
        
        # Segunda fila: Tabla y gráfico universidades - MODIFICADO
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📋 Becarios por Modalidad", className="table-title"),
                    html.Div([
                        tabla_modalidad
                    ], className="table-content")
                ], className="table-container")
            ], md=6),
            
            dbc.Col([
                html.Div([
                    dcc.Graph(figure=crear_grafico_universidades(), config={'displayModeBar': False})
                ], className="chart-container")
            ], md=6)
        ]),
        
        # Footer
        html.Hr(style={'margin': '2rem 0', 'border': '1px solid rgba(255,255,255,0.1)'}),
        html.Div([
            html.P("📊 Dashboard automatizado • Análisis integral • UPCH 2025", 
                   style={'textAlign': 'center', 'color': '#666', 'fontSize': '0.9rem'})
        ])
        
    ], fluid=True, className="main-container")
])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Render asigna el puerto
    app.run(host="0.0.0.0", port=port, debug=False)