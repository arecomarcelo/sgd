"""
Painéis de visualização para os dashboards do SGD
Réplicas EXATAS dos layouts do SGR conforme imagens de referência
"""

from datetime import datetime
from decimal import Decimal

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from dashboard.models import VendaConfiguracao, VendaProdutos, Vendas

# Import para requirements.txt
try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    # Se não tiver instalado, criar fallback
    pass


def get_filtros_periodo():
    """
    Retorna filtros fixos do SGD:
    - Data Inicial: 01 do mês atual
    - Data Final: Dia atual
    """
    hoje = datetime.now()
    data_inicial = f"01/{hoje.month:02d}/{hoje.year}"
    data_final = hoje.strftime("%d/%m/%Y")
    return data_inicial, data_final


def parse_valor(valor_str):
    """Converte string de valor monetário para Decimal"""
    try:
        valor_limpo = valor_str.strip().replace(",", ".")
        return Decimal(valor_limpo)
    except:
        return Decimal("0")


def parse_quantidade(quantidade_str):
    """Converte string de quantidade para Decimal"""
    try:
        valor_limpo = quantidade_str.strip().replace(",", ".")
        return Decimal(valor_limpo)
    except:
        return Decimal("0")


def format_currency(value):
    """Formata valor como moeda brasileira"""
    return (
        f"R$ {float(value):,.2f}".replace(".", "#").replace(",", ".").replace("#", ",")
    )


@st.cache_data(ttl=300)  # Cache de 5 minutos
def get_vendas_periodo():
    """
    Busca vendas do período com filtros fixos aplicados
    Retorna queryset filtrado
    """
    data_inicial, data_final = get_filtros_periodo()

    di_parts = data_inicial.split("/")
    df_parts = data_final.split("/")

    di_str = f"{di_parts[2]}-{di_parts[1]}-{di_parts[0]}"  # YYYY-MM-DD
    df_str = f"{df_parts[2]}-{df_parts[1]}-{df_parts[0]}"  # YYYY-MM-DD

    vendas = Vendas.objects.all()

    vendas_filtradas = []
    for venda in vendas:
        try:
            data_venda = venda.data.strip()

            if "/" in data_venda:
                parts = data_venda.split("/")
                if len(parts) == 3:
                    venda_str = f"{parts[2]}-{parts[1]}-{parts[0]}"
                else:
                    continue
            elif "-" in data_venda:
                venda_str = data_venda
            else:
                continue

            if di_str <= venda_str <= df_str:
                vendas_filtradas.append(venda)
        except:
            continue

    return vendas_filtradas


def render_meta_mes(theme='dark'):
    """
    Renderiza painel Meta Mês - RÉPLICA EXATA da imagem de referência
    """
    # Buscar meta do mês na configuração
    try:
        meta_config = VendaConfiguracao.objects.filter(Descricao='Meta').first()
        meta_mes = parse_valor(meta_config.Valor) if meta_config else Decimal("0")
    except:
        meta_mes = Decimal("0")

    # Buscar vendas do período
    vendas = get_vendas_periodo()
    total_vendido = sum(parse_valor(v.valortotal) for v in vendas)

    # Calcular percentual
    percentual = float(
        (total_vendido / meta_mes * 100) if meta_mes > 0 else Decimal("0")
    )

    # Cores do tema Dracula at Night
    if theme == 'dark':
        bg_color = "#1a1d2e"  # Background escuro do Dracula
        text_color_primary = "#8be9fd"  # Ciano
        text_color_secondary = "#6272a4"  # Comentário
        card_bg = "#f8f8f2"  # Branco/bege claro
        progress_bar_bg = "#f8f8f2"  # Barra branca
        cor_realizado = "#8be9fd"  # Ciano para progresso
        cor_faltando = "#44475a"  # Cinza do Dracula
    else:
        bg_color = "#f0f0f0"
        text_color_primary = "#1a73e8"
        text_color_secondary = "#5f6368"
        card_bg = "#ffffff"
        progress_bar_bg = "#ffffff"
        cor_realizado = "#4285f4"
        cor_faltando = "#e8eaed"

    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    background: {bg_color};
                    overflow-y: auto;
                }}
                .meta-container {{
                    background: {bg_color};
                    min-height: 100vh;
                    width: 100vw;
                    padding: 30px 20px 200px 20px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: flex-start;
                }}
                .meta-title {{
                    color: {text_color_primary};
                    font-size: 2.5rem;
                    font-weight: 700;
                    margin-bottom: 20px;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    letter-spacing: -0.5px;
                }}
                .meta-title-icon {{
                    font-size: 2.8rem;
                }}
                .progress-bar-container {{
                    width: 90%;
                    max-width: 750px;
                    margin-bottom: 20px;
                }}
                .progress-bar {{
                    background: {progress_bar_bg};
                    border-radius: 25px;
                    height: 30px;
                    width: 100%;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
                }}
                .donut-container {{
                    position: relative;
                    width: 280px;
                    height: 280px;
                    margin: 20px 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .donut-chart {{
                    width: 280px;
                    height: 280px;
                }}
                .donut-center {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    text-align: center;
                }}
                .donut-percent {{
                    color: {text_color_primary};
                    font-size: 4rem;
                    font-weight: 700;
                    line-height: 1;
                    margin-bottom: 5px;
                }}
                .donut-label {{
                    color: {text_color_secondary};
                    font-size: 1.2rem;
                    font-weight: 500;
                }}
                .info-cards {{
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                    width: 90%;
                    max-width: 750px;
                    margin-top: 15px;
                    margin-bottom: 30px;
                }}
                .info-card {{
                    background: {card_bg};
                    border-radius: 16px;
                    padding: 20px 40px;
                    text-align: center;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                }}
                .info-label {{
                    color: #666;
                    font-size: 1rem;
                    font-weight: 600;
                    margin-bottom: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 8px;
                }}
                .info-value {{
                    color: {text_color_primary};
                    font-size: 2rem;
                    font-weight: 700;
                    letter-spacing: -0.5px;
                }}

                @media (max-width: 768px) {{
                    .meta-title {{
                        font-size: 2rem;
                    }}
                    .donut-container {{
                        width: 280px;
                        height: 280px;
                    }}
                    .donut-chart {{
                        width: 280px;
                        height: 280px;
                    }}
                    .donut-percent {{
                        font-size: 3.5rem;
                    }}
                    .info-value {{
                        font-size: 1.8rem;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="meta-container">
                <div class="meta-title">
                    <span class="meta-title-icon">🎯</span>
                    <span>Meta de Vendas do Mês</span>
                </div>

                <div class="progress-bar-container">
                    <div class="progress-bar"></div>
                </div>

                <div class="donut-container">
                    <svg class="donut-chart" viewBox="0 0 100 100">
                        <!-- Círculo de fundo (cinza) -->
                        <circle cx="50" cy="50" r="35"
                                fill="none"
                                stroke="{cor_faltando}"
                                stroke-width="12"/>
                        <!-- Círculo de progresso (azul/ciano) -->
                        <circle cx="50" cy="50" r="35"
                                fill="none"
                                stroke="{cor_realizado}"
                                stroke-width="12"
                                stroke-dasharray="{percentual * 2.199} 219.9"
                                stroke-linecap="round"
                                transform="rotate(-90 50 50)"
                                style="transition: stroke-dasharray 0.5s ease;"/>
                        <!-- Círculo interno (background) -->
                        <circle cx="50" cy="50" r="28" fill="{bg_color}"/>
                    </svg>
                    <div class="donut-center">
                        <div class="donut-percent">{percentual:.0f}%</div>
                        <div class="donut-label">da Meta</div>
                    </div>
                </div>

                <div class="info-cards">
                    <div class="info-card">
                        <div class="info-label">💰 Realizado no Mês</div>
                        <div class="info-value">{format_currency(total_vendido)}</div>
                    </div>

                    <div class="info-card">
                        <div class="info-label">🎯 Meta do Mês</div>
                        <div class="info-value">{format_currency(meta_mes)}</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
    """

    # Usar height adequado para evitar sobreposição com rodapé
    components.html(html_content, height=850, scrolling=False)


def render_metricas_vendas(theme='dark'):
    """
    Renderiza painel Métricas de Vendas - RÉPLICA EXATA da imagem de referência
    """
    # Buscar vendas do período
    vendas = get_vendas_periodo()

    # Calcular métricas
    qtd_vendas = len(vendas)
    total_vendido = sum(parse_valor(v.valortotal) for v in vendas)
    total_custo = sum(parse_valor(v.valorcusto) for v in vendas)

    # Calcular entradas e parcelado (40% entradas, 60% parcelado - aproximação)
    total_entradas = total_vendido * Decimal("0.40")
    total_parcelado = total_vendido * Decimal("0.60")

    ticket_medio = (total_vendido / qtd_vendas) if qtd_vendas > 0 else Decimal("0")
    margem_lucro = total_vendido - total_custo
    percentual_margem = (
        ((margem_lucro / total_vendido) * 100) if total_vendido > 0 else Decimal("0")
    )

    # Cores do tema Dracula at Night
    if theme == 'dark':
        bg_color = "#1a1d2e"  # Background escuro
        text_color_primary = "#8be9fd"  # Ciano
        card_bg = "#f8f8f2"  # Branco/bege claro
        btn_bg = "#44475a"  # Cinza do Dracula
        btn_text = "#f8f8f2"  # Texto claro
    else:
        bg_color = "#f0f0f0"
        text_color_primary = "#1a73e8"
        card_bg = "#ffffff"
        btn_bg = "#ffffff"
        btn_text = "#1a73e8"

    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    background: {bg_color};
                    overflow-y: auto;
                }}
                .metricas-container {{
                    background: {bg_color};
                    min-height: 100vh;
                    width: 100vw;
                    padding: 40px 60px 180px 60px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                }}
                .metricas-title {{
                    color: {text_color_primary};
                    font-size: 2.5rem;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 12px;
                    margin-bottom: 50px;
                    text-align: center;
                }}
                .metricas-grid {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 30px;
                    width: 100%;
                    max-width: 1600px;
                }}
                .metric-card {{
                    background: {card_bg};
                    border-radius: 20px;
                    padding: 40px 30px;
                    text-align: center;
                    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    min-height: 160px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                }}
                .metric-card:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
                }}
                .metric-label {{
                    color: #f59e0b;
                    font-size: 1.15rem;
                    font-weight: 600;
                    margin-bottom: 15px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                }}
                .metric-value {{
                    color: {text_color_primary};
                    font-size: 2.2rem;
                    font-weight: 700;
                    letter-spacing: -0.5px;
                }}

                @media (max-width: 1400px) {{
                    .metricas-container {{
                        padding: 40px 40px 180px 40px;
                    }}
                    .metricas-grid {{
                        gap: 25px;
                    }}
                }}

                @media (max-width: 1200px) {{
                    .metricas-grid {{
                        grid-template-columns: repeat(2, 1fr);
                    }}
                }}

                @media (max-width: 768px) {{
                    .metricas-container {{
                        padding: 30px 20px 180px 20px;
                    }}
                    .metricas-title {{
                        font-size: 2rem;
                    }}
                    .metricas-grid {{
                        grid-template-columns: 1fr;
                        gap: 20px;
                    }}
                    .metric-card {{
                        padding: 30px 20px;
                    }}
                    .metric-value {{
                        font-size: 1.8rem;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="metricas-container">
                <div class="metricas-title">
                    <span>💎</span>
                    <span>Métricas de Vendas</span>
                </div>

                <div class="metricas-grid">
                    <div class="metric-card">
                        <div class="metric-label">💰 Total Entradas</div>
                        <div class="metric-value">{format_currency(total_entradas)}</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-label">⏳ Total Parcelado</div>
                        <div class="metric-value">{format_currency(total_parcelado)}</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-label">💎 Valor Total</div>
                        <div class="metric-value">{format_currency(total_vendido)}</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-label">📊 Total de Vendas</div>
                        <div class="metric-value">{qtd_vendas}</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-label">🎯 Ticket Médio</div>
                        <div class="metric-value">{format_currency(ticket_medio)}</div>
                    </div>

                    <div class="metric-card">
                        <div class="metric-label">📈 Margem Média</div>
                        <div class="metric-value">{float(percentual_margem):.1f}%</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
    """

    components.html(html_content, height=750, scrolling=False)


def render_ranking_vendedores(theme='dark'):
    """
    Renderiza painel Ranking Vendedores - ADAPT ADO DO SGR
    Lógica completa de cálculos e exibição de fotos do SGR
    """
    import base64
    import os
    from datetime import datetime
    from pathlib import Path

    from dateutil.relativedelta import relativedelta

    # Lista completa de vendedores (mesma ordem do SGR)
    # Nome → ID da foto (1-10.png)
    vendedores_tabela = [
        {"nome": "Noé Dutra", "foto": "1"},
        {"nome": "Nilton Jonas Gonçalves de Moraes", "foto": "2"},
        {"nome": "César Henrique Rodrigues", "foto": "3"},
        {"nome": "Rocha Jr.", "foto": "4"},
        {"nome": "Diney Scalabrini", "foto": "5"},
        {"nome": "João Paulo", "foto": "6"},
        {"nome": "Lauro Jarbas de Oliveira", "foto": "7"},
        {"nome": "Giovana Lelis", "foto": "8"},
        {"nome": "Carlos Gabriel Carvalho Macedo", "foto": "9"},
        {"nome": "Cássio Gadagnoto", "foto": "10"},
    ]

    # Função para calcular vendas do mês atual para gauges
    def calcular_vendas_mes_atual_para_gauge(vendedores_nomes):
        """
        Realizado: 01 do mês atual até hoje
        Meta: 01 do mesmo mês do ano anterior até o mesmo dia
        """
        try:
            hoje = datetime.now()
            data_inicio_atual = datetime(hoje.year, hoje.month, 1).date()
            data_fim_atual = hoje.date()

            # Mesmo período do ano anterior
            data_inicio_anterior = data_inicio_atual - relativedelta(years=1)
            data_fim_anterior = data_fim_atual - relativedelta(years=1)

            # Buscar vendas do período atual (realizado)
            vendas_atual = Vendas.objects.filter(
                data__gte=data_inicio_atual.strftime("%d/%m/%Y"),
                data__lte=data_fim_atual.strftime("%d/%m/%Y"),
            )

            # Buscar vendas do período anterior (meta)
            vendas_anterior = Vendas.objects.filter(
                data__gte=data_inicio_anterior.strftime("%d/%m/%Y"),
                data__lte=data_fim_anterior.strftime("%d/%m/%Y"),
            )

            # Processar realizado
            vendas_realizadas = {}
            for venda in vendas_atual:
                nome = venda.vendedornome
                if nome in vendedores_nomes:
                    if nome not in vendas_realizadas:
                        vendas_realizadas[nome] = Decimal("0")
                    vendas_realizadas[nome] += parse_valor(venda.valortotal)

            # Processar meta
            vendas_meta = {}
            for venda in vendas_anterior:
                nome = venda.vendedornome
                if nome in vendedores_nomes:
                    if nome not in vendas_meta:
                        vendas_meta[nome] = Decimal("0")
                    vendas_meta[nome] += parse_valor(venda.valortotal)

            return vendas_realizadas, vendas_meta

        except Exception as e:
            return {}, {}

    # Buscar vendas do período (seguem os filtros aplicados)
    vendas = get_vendas_periodo()

    # Agrupar por vendedor
    vendedores_stats = {}
    for venda in vendas:
        vendedor = venda.vendedornome
        if not vendedor or vendedor.strip() == "":
            continue

        valor = parse_valor(venda.valortotal)

        if vendedor not in vendedores_stats:
            vendedores_stats[vendedor] = {"total": Decimal("0"), "qtd": 0}

        vendedores_stats[vendedor]["total"] += valor
        vendedores_stats[vendedor]["qtd"] += 1

    # Calcular total geral para percentuais (do filtro aplicado)
    total_geral = sum(stats["total"] for stats in vendedores_stats.values())

    # Calcular vendas do mês atual para gauges (sempre mês atual, independente dos filtros)
    vendedores_nomes = [v["nome"] for v in vendedores_tabela]
    vendas_realizadas_gauge, vendas_meta_gauge = calcular_vendas_mes_atual_para_gauge(
        vendedores_nomes
    )

    # Preparar dados completos dos vendedores
    vendedores_completos = []
    for vendedor in vendedores_tabela:
        nome = vendedor["nome"]
        # Gauge: sempre mês atual
        meta_vendedor = float(vendas_meta_gauge.get(nome, 0))
        realizado_vendedor = float(vendas_realizadas_gauge.get(nome, 0))

        if nome in vendedores_stats:
            # Vendedor com vendas no filtro aplicado
            vendedores_completos.append(
                {
                    "nome": nome,
                    "foto": vendedor["foto"],
                    "total_valor": float(vendedores_stats[nome]["total"]),
                    "percentual": float(
                        (vendedores_stats[nome]["total"] / total_geral * 100)
                        if total_geral > 0
                        else 0
                    ),
                    "meta": meta_vendedor,
                    "realizado": realizado_vendedor,
                }
            )
        else:
            # Vendedor sem vendas no filtro
            vendedores_completos.append(
                {
                    "nome": nome,
                    "foto": vendedor["foto"],
                    "total_valor": 0.0,
                    "percentual": 0.0,
                    "meta": meta_vendedor,
                    "realizado": realizado_vendedor,
                }
            )

    # Ordenar por valor total (maior para menor)
    vendedores_ordenados = sorted(
        vendedores_completos, key=lambda x: x["total_valor"], reverse=True
    )

    # Função para carregar foto em base64
    def get_vendedor_foto(foto_id):
        """Carrega foto do vendedor em base64"""
        fotos_dir = Path("/media/areco/Backup/Oficial/Projetos/sgd/imagens/fotos")

        # Tentar .jpg primeiro, depois .png
        for ext in ['.jpg', '.png']:
            foto_path = fotos_dir / f"{foto_id}{ext}"
            if foto_path.exists():
                try:
                    with open(foto_path, "rb") as f:
                        img_data = base64.b64encode(f.read()).decode('utf-8')
                        return f"data:image/png;base64,{img_data}"
                except:
                    continue
        return None

    # Cores do tema
    if theme == 'dark':
        bg_color = "#1a1d2e"
        text_color_primary = "#8be9fd"
        card_bg = "#f8f8f2"
    else:
        bg_color = "#f0f0f0"
        text_color_primary = "#1a73e8"
        card_bg = "#ffffff"

    # Gerar HTML dos cards
    cards_html = ""
    for vendedor in vendedores_ordenados:
        # Calcular percentual da meta (gauge)
        percentual_meta = (
            (vendedor["realizado"] / vendedor["meta"] * 100)
            if vendedor["meta"] > 0
            else 0
        )

        # Percentual do total de vendas (do filtro aplicado)
        percentual_vendas = vendedor["percentual"]

        # Carregar foto
        foto_base64 = get_vendedor_foto(vendedor["foto"])

        # Avatar HTML
        if foto_base64:
            avatar_html = f'<img src="{foto_base64}" class="vendedor-avatar-img" />'
        else:
            iniciais = "".join(
                [nome[0] for nome in vendedor["nome"].split()[:2]]
            ).upper()
            avatar_html = f'<div class="vendedor-avatar-iniciais">{iniciais}</div>'

        cards_html += f"""
        <div class="vendedor-card">
            <div class="vendedor-avatar">
                {avatar_html}
            </div>
            <div class="vendedor-nome">{vendedor["nome"]}</div>
            <div class="vendedor-valor">{format_currency(vendedor["total_valor"])}</div>
            <div class="vendedor-stats">
                <div class="stat-container">
                    <svg class="stat-circle" viewBox="0 0 36 36">
                        <circle cx="18" cy="18" r="16" fill="none" stroke="#e5e7eb" stroke-width="3"/>
                        <circle cx="18" cy="18" r="16" fill="none" stroke="#60A5FA" stroke-width="3"
                                stroke-dasharray="{percentual_vendas * 1.005} 100.5"
                                stroke-linecap="round"
                                transform="rotate(-90 18 18)"/>
                    </svg>
                    <div class="stat-value">{percentual_vendas:.1f}%</div>
                </div>
                <div class="stat-container">
                    <svg class="stat-circle" viewBox="0 0 36 36">
                        <circle cx="18" cy="18" r="16" fill="none" stroke="#e5e7eb" stroke-width="3"/>
                        <circle cx="18" cy="18" r="16" fill="none" stroke="#1e40af" stroke-width="3"
                                stroke-dasharray="{percentual_meta * 1.005} 100.5"
                                stroke-linecap="round"
                                transform="rotate(-90 18 18)"/>
                    </svg>
                    <div class="stat-value">{percentual_meta:.0f}%</div>
                </div>
            </div>
        </div>
        """

    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    background: {bg_color};
                    overflow-y: auto;
                }}
                .ranking-vendedores-container {{
                    background: {bg_color};
                    min-height: 100vh;
                    width: 100vw;
                    padding: 30px 40px 180px 40px;
                }}
                .ranking-title {{
                    color: {text_color_primary};
                    font-size: 2rem;
                    font-weight: 700;
                    margin-bottom: 35px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 12px;
                    text-align: center;
                }}
                .ranking-grid {{
                    display: grid;
                    grid-template-columns: repeat(5, 1fr);
                    gap: 20px 18px;
                    max-width: 1650px;
                    margin: 0 auto;
                }}
                .vendedor-card {{
                    background: {card_bg};
                    border-radius: 16px;
                    padding: 20px 15px;
                    text-align: center;
                    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    min-width: 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
                .vendedor-card:hover {{
                    transform: translateY(-4px);
                    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
                }}
                .vendedor-avatar {{
                    width: 85px;
                    height: 85px;
                    border-radius: 50%;
                    margin: 0 auto 12px;
                    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
                    overflow: hidden;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-shrink: 0;
                }}
                .vendedor-avatar-img {{
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    border-radius: 50%;
                }}
                .vendedor-avatar-iniciais {{
                    width: 85px;
                    height: 85px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.7rem;
                    font-weight: 700;
                }}
                .vendedor-nome {{
                    color: {text_color_primary};
                    font-weight: 600;
                    font-size: 0.95rem;
                    margin-bottom: 8px;
                    min-height: 38px;
                    max-height: 38px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    line-height: 1.2;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    padding: 0 5px;
                    word-break: break-word;
                }}
                .vendedor-valor {{
                    color: {text_color_primary};
                    font-size: 1.3rem;
                    font-weight: 700;
                    margin-bottom: 12px;
                    letter-spacing: -0.5px;
                }}
                .vendedor-stats {{
                    display: flex;
                    justify-content: center;
                    gap: 12px;
                    margin-top: 8px;
                }}
                .stat-container {{
                    position: relative;
                    width: 55px;
                    height: 55px;
                    flex-shrink: 0;
                }}
                .stat-circle {{
                    width: 100%;
                    height: 100%;
                }}
                .stat-value {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    font-size: 0.8rem;
                    font-weight: 700;
                    color: {text_color_primary};
                }}

                @media (max-width: 1600px) {{
                    .ranking-grid {{
                        grid-template-columns: repeat(4, 1fr);
                    }}
                }}

                @media (max-width: 1200px) {{
                    .ranking-grid {{
                        grid-template-columns: repeat(3, 1fr);
                    }}
                }}

                @media (max-width: 900px) {{
                    .ranking-grid {{
                        grid-template-columns: repeat(2, 1fr);
                    }}
                }}

                @media (max-width: 600px) {{
                    .ranking-vendedores-container {{
                        padding: 30px 20px 180px 20px;
                    }}
                    .ranking-title {{
                        font-size: 1.8rem;
                    }}
                    .ranking-grid {{
                        grid-template-columns: 1fr;
                        gap: 20px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="ranking-vendedores-container">
                <div class="ranking-title">
                    <span>🏆</span>
                    <span>Ranking de Vendedores</span>
                </div>

                <div class="ranking-grid">
                    {cards_html}
                </div>
            </div>
        </body>
        </html>
    """

    # Sempre 10 vendedores em grid 5x2 = altura fixa
    components.html(html_content, height=700, scrolling=False)


def render_ranking_produtos(theme='dark'):
    """
    Renderiza painel Ranking Produtos - ADAPTADO DO SGR
    Lógica completa de cálculos e layout do SGR
    """
    # Buscar vendas do período (seguem os filtros aplicados)
    vendas = get_vendas_periodo()
    vendas_ids = [v.id_gestao for v in vendas]

    if not vendas_ids:
        # Renderizar mensagem vazia em HTML
        st.markdown(
            """
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                height: 400px;
                color: #8be9fd;
                font-size: 1.5rem;
            ">
                📦 Nenhum produto encontrado para o período selecionado
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Buscar produtos vendidos
    produtos_vendidos = VendaProdutos.objects.filter(venda_id__in=vendas_ids)

    if not produtos_vendidos.exists():
        st.markdown(
            """
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                height: 400px;
                color: #8be9fd;
                font-size: 1.5rem;
            ">
                📦 Nenhum produto encontrado para o período selecionado
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Agrupar por produto (mesmo do SGR)
    produtos_stats = {}
    for item in produtos_vendidos:
        nome = item.nome.strip() if item.nome else "Produto sem nome"
        qtd = parse_quantidade(item.quantidade)

        if nome not in produtos_stats:
            produtos_stats[nome] = {"quantidade": Decimal("0"), "num_vendas": 0}

        produtos_stats[nome]["quantidade"] += qtd
        produtos_stats[nome]["num_vendas"] += 1

    # Ordenar por quantidade total e pegar TOP 10 (mesmo do SGR)
    ranking = sorted(
        produtos_stats.items(), key=lambda x: x[1]["quantidade"], reverse=True
    )[:10]

    if not ranking:
        st.markdown(
            """
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                height: 400px;
                color: #8be9fd;
                font-size: 1.5rem;
            ">
                📦 Nenhum produto encontrado
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Cores do tema
    if theme == 'dark':
        bg_color = "#1a1d2e"
        text_color_primary = "#8be9fd"
    else:
        bg_color = "#f0f0f0"
        text_color_primary = "#1a73e8"

    # Função para determinar gradiente do card (mesmo do SGR)
    def get_gradient(rank):
        if rank == 1:
            return "linear-gradient(135deg, #FFD700 0%, #FFA500 100%)"  # Ouro
        elif rank == 2:
            return "linear-gradient(135deg, #C0C0C0 0%, #808080 100%)"  # Prata
        elif rank == 3:
            return "linear-gradient(135deg, #CD7F32 0%, #8B4513 100%)"  # Bronze
        else:
            return "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"  # Roxo padrão

    # Gerar HTML dos cards
    cards_html = ""
    for idx, (produto, stats) in enumerate(ranking):
        rank = idx + 1
        gradient = get_gradient(rank)

        cards_html += f"""
        <div class="produto-card" style="background: {gradient};">
            <div class="produto-rank">#{rank}</div>
            <div class="produto-nome" title="{produto}">
                {produto.upper()}
            </div>
            <div class="produto-metric">
                <span class="produto-metric-label">📦 Qtd. Total</span>
                <span class="produto-metric-value">{int(stats["quantidade"])}</span>
            </div>
            <div class="produto-metric">
                <span class="produto-metric-label">🛒 Nº Vendas</span>
                <span class="produto-metric-value">{stats["num_vendas"]}</span>
            </div>
        </div>
        """

    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    background: {bg_color};
                    overflow-y: auto;
                }}
                .ranking-produtos-container {{
                    background: {bg_color};
                    min-height: 100vh;
                    width: 100vw;
                    padding: 30px 40px 180px 40px;
                }}
                .ranking-title {{
                    color: {text_color_primary};
                    font-size: 2rem;
                    font-weight: 700;
                    margin-bottom: 35px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 12px;
                    text-align: center;
                }}
                .ranking-grid {{
                    display: grid;
                    grid-template-columns: repeat(5, 1fr);
                    gap: 20px 18px;
                    max-width: 1650px;
                    margin: 0 auto;
                }}
                .produto-card {{
                    border-radius: 16px;
                    padding: 20px 15px;
                    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                    color: white;
                    display: flex;
                    flex-direction: column;
                    min-width: 0;
                }}
                .produto-card:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 10px 22px rgba(0, 0, 0, 0.25);
                }}
                .produto-rank {{
                    font-size: 2.3rem;
                    font-weight: 700;
                    opacity: 0.4;
                    line-height: 1;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                }}
                .produto-nome {{
                    font-size: 1rem;
                    font-weight: 700;
                    margin-bottom: 15px;
                    min-height: 48px;
                    max-height: 48px;
                    display: -webkit-box;
                    -webkit-line-clamp: 2;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.4);
                    line-height: 1.3;
                    word-break: break-word;
                }}
                .produto-metric {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin: 6px 0;
                    padding: 10px 12px;
                    background: rgba(0, 0, 0, 0.25);
                    border-radius: 8px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }}
                .produto-metric-label {{
                    font-size: 0.9rem;
                    font-weight: 600;
                    opacity: 1;
                    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
                }}
                .produto-metric-value {{
                    font-size: 1.3rem;
                    font-weight: 900;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
                }}

                @media (max-width: 1600px) {{
                    .ranking-grid {{
                        grid-template-columns: repeat(4, 1fr);
                    }}
                }}

                @media (max-width: 1200px) {{
                    .ranking-grid {{
                        grid-template-columns: repeat(3, 1fr);
                    }}
                }}

                @media (max-width: 900px) {{
                    .ranking-grid {{
                        grid-template-columns: repeat(2, 1fr);
                    }}
                }}

                @media (max-width: 600px) {{
                    .ranking-produtos-container {{
                        padding: 30px 20px 180px 20px;
                    }}
                    .ranking-title {{
                        font-size: 1.8rem;
                    }}
                    .ranking-grid {{
                        grid-template-columns: 1fr;
                        gap: 20px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="ranking-produtos-container">
                <div class="ranking-title">
                    <span>🏆</span>
                    <span>Ranking de Produtos</span>
                </div>

                <div class="ranking-grid">
                    {cards_html}
                </div>
            </div>
        </body>
        </html>
    """

    components.html(html_content, height=700, scrolling=False)
