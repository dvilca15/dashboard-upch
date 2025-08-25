# components.py
"""
Módulo para componentes de la interfaz de usuario
"""
from dash import dash_table


def crear_tabla_modalidad(df_modalidad_count):
    """Crea la tabla de modalidades"""
    return dash_table.DataTable(
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
            "height": "300px"
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