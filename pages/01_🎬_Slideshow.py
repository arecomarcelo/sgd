"""
Página de Slideshow
Exibe os dashboards em rotação automática com transição suave
"""

import os
from pathlib import Path

import streamlit as st
from streamlit_autorefresh import st_autorefresh

import django_setup  # Configura Django ORM

# Importa os modelos Django
from dashboard.models import Dashboard, Dashboard_Config, VendaAtualizacao

st.set_page_config(
    page_title="Slideshow",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilo CSS customizado
st.markdown(
    """
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
        background: #000000;
        padding: 0;
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

    /* Estilo para imagem centralizada em tela cheia */
    .dashboard-image-container {
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        background: #000000;
    }

    /* Ajusta a imagem para tela cheia centralizada */
    .stImage {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100vw !important;
        height: 100vh !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
    }

    .stImage img {
        max-width: 95vw !important;
        max-height: 85vh !important;
        width: auto !important;
        height: auto !important;
        object-fit: contain !important;
        margin: 0 auto !important;
        display: block !important;
    }

    /* Botão de engrenagem fixo - Container Streamlit */
    div[data-testid="stVerticalBlock"] > div:has(button[kind="secondary"]) {
        position: fixed !important;
        top: 20px !important;
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

    /* Painel fixo no rodapé */
    .footer-panel {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: rgba(0, 0, 0, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        padding: 15px 30px !important;
        z-index: 9999 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 40px !important;
        border-top: 2px solid rgba(255, 255, 255, 0.1) !important;
    }

    .footer-card {
        background: rgba(255, 255, 255, 0.1) !important;
        padding: 12px 30px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    .footer-label {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.9rem !important;
        margin-bottom: 5px !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    .footer-value {
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Buscar dashboards ativos ordenados
dashboards_config = (
    Dashboard_Config.objects.filter(Dashboard__Ativo=True)
    .select_related('Dashboard')
    .order_by('Ordem')
)

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
    st.session_state.current_index = (
        st.session_state.current_index + 1
    ) % total_dashboards

# Buscar imagem de teste (temporário)
# Converte nome do dashboard para nome de arquivo
# Exemplo: "Meta Mês" -> "meta_mes.png"
nome_dashboard_normalizado = (
    current_dashboard.Nome.lower()
    .replace(' ', '_')
    .replace('ê', 'e')
    .replace('é', 'e')
    .replace('á', 'a')
    .replace('í', 'i')
    .replace('ó', 'o')
    .replace('ú', 'u')
    .replace('ã', 'a')
    .replace('õ', 'o')
    .replace('ç', 'c')
)
imagem_path = Path(f"imagens/{nome_dashboard_normalizado}.png")

# Exibir dashboard com imagem (se existir)
if imagem_path.exists():
    # Layout com imagem em tela cheia, sem painéis
    st.markdown(
        '<div class="dashboard-image-container">',
        unsafe_allow_html=True,
    )
    st.image(str(imagem_path))
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Layout sem imagem (original)
    st.markdown(
        f"""
    <div class="dashboard-card">
        <div class="dashboard-title">{current_dashboard.Nome}</div>
        <div class="dashboard-description">{current_dashboard.Descricao}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Buscar informações de atualização
try:
    venda_atualizacao = VendaAtualizacao.objects.latest('id')
    periodo = venda_atualizacao.Periodo
    data_atualizacao = f"{venda_atualizacao.Data} {venda_atualizacao.Hora}"
except VendaAtualizacao.DoesNotExist:
    periodo = "N/A"
    data_atualizacao = "N/A"

# Painel fixo no rodapé com informações de atualização
st.markdown(
    f"""
    <div class="footer-panel">
        <div class="footer-card">
            <div class="footer-label">📅 Período</div>
            <div class="footer-value">{periodo}</div>
        </div>
        <div class="footer-card">
            <div class="footer-label">🕐 Data Atualização</div>
            <div class="footer-value">{data_atualizacao}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Botão de engrenagem para navegação
if st.button("⚙️", key="settings_btn", type="secondary", help="Gerenciar Dashboards"):
    st.switch_page("pages/02_⚙️_Gerenciar.py")
