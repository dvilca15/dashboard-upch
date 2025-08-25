# styles.py
"""
Módulo para estilos CSS del dashboard
"""

CUSTOM_CSS = """
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
    height: 430px;
    display: flex;
    flex-direction: column;
}

.table-container {
    background: rgba(255, 255, 255, 0.01);
    border-radius: 15px;
    padding: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 2rem;
    height: 430px;
    display: flex;
    flex-direction: column;
}

.table-title {
    color: #00D4FF;
    font-size: 1.5rem;
    font-weight: 600;
    text-align: center;
    margin-bottom: 1.5rem;
    flex-shrink: 0;
}

.table-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}
"""