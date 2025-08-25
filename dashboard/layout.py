# layout.py
"""
Módulo para el layout principal del dashboard
"""
from dash import html, dcc
import dash_bootstrap_components as dbc


def crear_layout(contadores, grafico_comparativo, grafico_carreras, tabla_modalidad, grafico_universidades):
    """Crea el layout principal del dashboard"""
    return html.Div([
        dbc.Container([
            # Header principal
            html.H1("🎓 Dashboard UPCH 2025", className="main-title"),
            html.P("Universidad Peruana Cayetano Heredia", className="subtitle"),
            
            # Tarjetas de métricas
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div(f"{contadores['total_becarios']}", className="metric-number"),
                        html.Div("Total Becarios", className="metric-label")
                    ], className="metric-card")
                ], md=6),
                
                dbc.Col([
                    html.Div([
                        html.Div(f"{contadores['crecimiento_becarios']:.1f}%", className="metric-number"),
                        html.Div("Crecimiento de Becarios", className="metric-label")
                    ], className="metric-card metric-card-growth")
                ], md=6)
            ], className="mb-4"),
            
            # Primera fila de gráficos
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Graph(figure=grafico_comparativo, config={'displayModeBar': False})
                    ], className="chart-container")
                ], md=6),
                
                dbc.Col([
                    html.Div([
                        dcc.Graph(figure=grafico_carreras, config={'displayModeBar': False})
                    ], className="chart-container")
                ], md=6)
            ]),
            
            # Segunda fila: Tabla y gráfico universidades
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
                        dcc.Graph(figure=grafico_universidades, config={'displayModeBar': False})
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