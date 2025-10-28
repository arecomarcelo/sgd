"""
Página de Gerenciamento de Dashboards
Permite atualizar configurações de dashboards existentes
"""

import pandas as pd
import streamlit as st

import django_setup  # Configura Django ORM

# Importa os modelos Django
from dashboard.models import Dashboard, Dashboard_Config, VendaConfiguracao

st.set_page_config(page_title="Gerenciar Dashboards", page_icon="⚙️", layout="wide")

# Header com título e botão de voltar
col_title, col_button = st.columns([5, 1])
with col_title:
    st.title("⚙️ Gerenciar Dashboards")
with col_button:
    st.write("")  # Espaçamento vertical
    if st.button("🎬 Voltar ao Slideshow", key="btn_voltar"):
        st.switch_page("pages/01_🎬_Slideshow.py")

st.markdown("---")

# Painel de Meta de Vendas
st.subheader("🎯 Meta de Vendas")

# Buscar valor atual da meta
try:
    config_meta = VendaConfiguracao.objects.get(Descricao="Meta")
    valor_meta_atual = config_meta.Valor
except VendaConfiguracao.DoesNotExist:
    valor_meta_atual = "0"
    st.warning("⚠️ Configuração de Meta não encontrada no banco de dados")

# Layout em colunas para o campo de meta
col_meta1, col_meta2 = st.columns([3, 1])

with col_meta1:
    nova_meta = st.text_input(
        "Valor da Meta",
        value=valor_meta_atual,
        placeholder="Digite o valor da meta",
        help="💡 Digite o valor da meta de vendas",
        key="input_meta",
    )

with col_meta2:
    st.write("")  # Espaçamento vertical para alinhar o botão
    st.write("")  # Mais espaçamento
    if st.button(
        "💾 Salvar Meta",
        key="btn_salvar_meta",
        help="Clique para salvar o valor da meta",
    ):
        if nova_meta and nova_meta.strip():
            try:
                config_meta = VendaConfiguracao.objects.get(Descricao="Meta")
                config_meta.Valor = nova_meta.strip()
                config_meta.save()
                st.success(f"✅ Meta atualizada com sucesso para: {nova_meta}")
                st.rerun()
            except VendaConfiguracao.DoesNotExist:
                st.error(
                    "❌ Erro: Configuração de Meta não encontrada no banco de dados"
                )
            except Exception as e:
                st.error(f"❌ Erro ao salvar meta: {str(e)}")
        else:
            st.warning("⚠️ Por favor, digite um valor válido para a meta")

st.markdown("---")

# Painel de Ordem Atual
st.subheader("📊 Ordem Atual")

# Buscar dashboards com configuração ordenados
dashboards_ordenados = Dashboard_Config.objects.select_related('Dashboard').order_by(
    'Ordem'
)

if dashboards_ordenados.exists():
    # Criar tabela de ordem atual
    ordem_data = []
    for config in dashboards_ordenados:
        status_icon = "✅" if config.Dashboard.Ativo else "❌"
        ordem_data.append(
            {
                "Ordem": config.Ordem,
                "Dashboard": f"{status_icon} {config.Dashboard.Nome}",
                "Duração": f"{config.Duracao}s",
            }
        )

    # Exibir em formato de tabela
    df_ordem = pd.DataFrame(ordem_data)

    # Exibir tabela estilizada
    st.dataframe(
        df_ordem,
        hide_index=True,
        width="stretch",
        column_config={
            "Ordem": st.column_config.NumberColumn(
                "Ordem", help="Ordem de exibição no slideshow", width="small"
            ),
            "Dashboard": st.column_config.TextColumn(
                "Dashboard",
                help="Nome do dashboard (✅ Ativo / ❌ Inativo)",
                width="large",
            ),
            "Duração": st.column_config.TextColumn(
                "Duração", help="Tempo de exibição em segundos", width="small"
            ),
        },
    )
else:
    st.info("📭 Nenhum dashboard cadastrado com configuração de exibição")

st.markdown("---")


# Função para ajustar ordens automaticamente
def ajustar_ordens(dashboard_id, nova_ordem, ordem_antiga):
    """
    Ajusta as ordens dos demais dashboards para evitar duplicatas
    """
    configs = Dashboard_Config.objects.exclude(Dashboard__id=dashboard_id).order_by(
        'Ordem'
    )

    if nova_ordem > ordem_antiga:
        # Movendo para baixo (aumentando ordem)
        # Todos os dashboards entre ordem_antiga+1 e nova_ordem devem subir (ordem-1)
        for config in configs:
            if ordem_antiga < config.Ordem <= nova_ordem:
                config.Ordem -= 1
                config.save()
    elif nova_ordem < ordem_antiga:
        # Movendo para cima (diminuindo ordem)
        # Todos os dashboards entre nova_ordem e ordem_antiga-1 devem descer (ordem+1)
        for config in configs:
            if nova_ordem <= config.Ordem < ordem_antiga:
                config.Ordem += 1
                config.save()


# Listar Dashboards
st.header("📋 Dashboards Cadastrados")

dashboards = Dashboard.objects.all().order_by('Nome')

if dashboards.exists():
    for dash in dashboards:
        with st.expander(f"{'✅' if dash.Ativo else '❌'} {dash.Nome}", expanded=False):

            # Buscar configuração
            try:
                config = Dashboard_Config.objects.get(Dashboard=dash)

                # Layout em colunas
                col1, col2, col3 = st.columns([3, 2, 1])

                with col1:
                    st.write(f"**Descrição:** {dash.Descricao}")
                    st.write(
                        f"**Status:** {'Ativo ✅' if dash.Ativo else 'Inativo ❌'}"
                    )

                with col2:
                    st.write("**Configurações de Exibição:**")

                    # Controle updown para Ordem
                    nova_ordem = st.number_input(
                        "Ordem de Exibição",
                        min_value=1,
                        value=config.Ordem,
                        step=1,
                        key=f"ordem_{dash.id}",
                    )

                    # Controle updown para Duração
                    nova_duracao = st.number_input(
                        "Duração (segundos)",
                        min_value=1,
                        value=config.Duracao,
                        step=1,
                        key=f"duracao_{dash.id}",
                    )

                with col3:
                    st.write("**Ações:**")

                    # Botão para ativar/desativar
                    if st.button(
                        f"{'🔴 Desativar' if dash.Ativo else '🟢 Ativar'}",
                        key=f"toggle_{dash.id}",
                    ):
                        dash.Ativo = not dash.Ativo
                        dash.save()
                        st.success(
                            f"Dashboard {'ativado' if dash.Ativo else 'desativado'} com sucesso!"
                        )
                        st.rerun()

                    # Botão para salvar alterações
                    if st.button("💾 Salvar", key=f"save_{dash.id}"):
                        ordem_alterada = nova_ordem != config.Ordem

                        # Ajustar ordens dos demais se necessário
                        if ordem_alterada:
                            ajustar_ordens(dash.id, nova_ordem, config.Ordem)

                        # Atualizar config
                        config.Ordem = nova_ordem
                        config.Duracao = nova_duracao
                        config.save()

                        st.success(
                            f"✅ Dashboard '{dash.Nome}' atualizado com sucesso!"
                        )
                        st.rerun()

            except Dashboard_Config.DoesNotExist:
                st.warning("⚠️ Sem configuração de exibição")
                st.info(
                    "💡 Este dashboard precisa de uma configuração para ser exibido no slideshow"
                )
else:
    st.info("📭 Nenhum dashboard cadastrado ainda.")
    st.warning(
        "⚠️ A funcionalidade de cadastro foi desabilitada. Entre em contato com o administrador."
    )

st.markdown("---")
st.caption(
    "💡 **Dica**: Ajuste a ordem e duração dos dashboards conforme necessário. Clique em 'Salvar' para aplicar as alterações."
)
