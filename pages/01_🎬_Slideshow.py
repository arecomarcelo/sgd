"""
Página de Slideshow
Exibe os dashboards em rotação automática com transição suave
"""
import streamlit as st
import django_setup  # Configura Django ORM
from streamlit_autorefresh import st_autorefresh

# Importa os modelos Django
from dashboard.models import Dashboard, Dashboard_Config

st.set_page_config(
    page_title="Slideshow",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo CSS customizado
st.markdown("""
<style>
    /* Esconde header, footer e sidebar do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* Remove padding e margens do container principal */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Remove scrollbars */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        overflow: hidden !important;
        height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Estilo do card do dashboard - ocupa toda a tela */
    .dashboard-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px;
        text-align: center;
        color: white;
        height: 100vh;
        width: 100vw;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        animation: fadeIn 0.8s ease-in-out;
        position: fixed;
        top: 0;
        left: 0;
        box-sizing: border-box;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    .dashboard-title {
        font-size: 4rem;
        font-weight: bold;
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }

    .dashboard-description {
        font-size: 2rem;
        margin-bottom: 40px;
        line-height: 1.6;
    }

    .dashboard-info {
        background: rgba(255, 255, 255, 0.2);
        padding: 20px 40px;
        border-radius: 50px;
        font-size: 1.5rem;
        margin-top: 20px;
    }

    /* Botão de engrenagem fixo - Container Streamlit */
    div[data-testid="stVerticalBlock"] > div:has(button[kind="secondary"]) {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 99999 !important;
        width: 60px !important;
        height: 60px !important;
    }

    /* Estilo do botão de engrenagem */
    button[kind="secondary"] {
        width: 60px !important;
        height: 60px !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 50% !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
        padding: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 1) !important;
        transform: scale(1.1) rotate(90deg) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
    }

    button[kind="secondary"] p {
        font-size: 30px !important;
        margin: 0 !important;
        line-height: 1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Buscar dashboards ativos ordenados
dashboards_config = Dashboard_Config.objects.filter(
    Dashboard__Ativo=True
).select_related('Dashboard').order_by('Ordem')

if not dashboards_config.exists():
    st.error("❌ Nenhum dashboard ativo encontrado!")
    st.info("👉 Clique no botão de engrenagem para gerenciar dashboards")
    st.stop()

# Inicializar estado da sessão
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# Obter dashboard atual
total_dashboards = dashboards_config.count()
current_config = list(dashboards_config)[st.session_state.current_index]
current_dashboard = current_config.Dashboard
duracao = current_config.Duracao

# Auto-refresh baseado na duração
count = st_autorefresh(interval=duracao * 1000, key="slideshow_refresh")

# Avançar para próximo slide
if count > 0:
    st.session_state.current_index = (st.session_state.current_index + 1) % total_dashboards

# Exibir dashboard
st.markdown(f"""
<div class="dashboard-card">
    <div class="dashboard-title">{current_dashboard.Nome}</div>
    <div class="dashboard-description">{current_dashboard.Descricao}</div>
    <div class="dashboard-info">
        📊 Slide {st.session_state.current_index + 1} de {total_dashboards} |
        ⏱️ {duracao}s |
        🔄 Ordem: {current_config.Ordem}
    </div>
</div>
""", unsafe_allow_html=True)

# Botão de engrenagem para navegação
if st.button("⚙️", key="settings_btn", type="secondary", help="Gerenciar Dashboards"):
    st.switch_page("pages/02_⚙️_Gerenciar.py")
