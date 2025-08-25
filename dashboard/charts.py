# charts.py
"""
Módulo para generación de gráficos del dashboard UPCH
"""
import plotly.graph_objects as go


def crear_grafico_comparativo(contadores):
    """Crea el gráfico comparativo 1M vs 2M"""
    fig = go.Figure()
    
    # Seleccionados
    fig.add_trace(go.Bar(
        name='Seleccionados',
        x=['Primer Momento', 'Segundo Momento'],
        y=[contadores['condicion_count_1m'], contadores['condicion_count_2m']],
        marker_color='#00D4FF',
        text=[f'{contadores["condicion_count_1m"]}', f'{contadores["condicion_count_2m"]}'],
        textposition='outside',
        textfont=dict(size=14, color='white', family='Inter'),
        marker_line=dict(color='rgba(255,255,255,0.3)', width=2)
    ))
    
    # Becarios
    fig.add_trace(go.Bar(
        name='Becarios',
        x=['Primer Momento', 'Segundo Momento'],
        y=[contadores['becario_count_1m'], contadores['becario_count_2m']],
        marker_color='#FF6B6B',
        text=[f'{contadores["becario_count_1m"]}', f'{contadores["becario_count_2m"]}'],
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


def crear_grafico_carreras(df_carreras_count):
    """Crea el gráfico de becarios por carrera"""
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


def crear_grafico_universidades(df_universidades):
    """Crea el gráfico de becarios por universidad"""
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
        height=350,
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