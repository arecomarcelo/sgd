from django.shortcuts import render
from django.http import JsonResponse
from .models import Dashboard, Dashboard_Config


def slideshow_view(request):
    """
    View principal para exibição dos dashboards em formato de slideshow.
    Renderiza o template com a interface de visualização.
    """
    return render(request, 'dashboard/slideshow.html')


def get_dashboards_config(request):
    """
    API endpoint que retorna a configuração dos dashboards ativos.
    Retorna apenas dashboards ativos (Dashboard.Ativo = True),
    ordenados por Dashboard_Config.Ordem.

    Retorna JSON com:
    - ordem: ordem de exibição
    - nome: nome do dashboard
    - descricao: descrição do dashboard
    - duracao: duração em segundos
    """
    # Busca todas as configurações de dashboards ativos, ordenados por Ordem
    configs = Dashboard_Config.objects.filter(
        Dashboard__Ativo=True
    ).select_related('Dashboard').order_by('Ordem')

    # Monta a lista de dashboards para o frontend
    dashboards_list = []
    for config in configs:
        dashboards_list.append({
            'id': config.id,
            'ordem': config.Ordem,
            'nome': config.Dashboard.Nome,
            'descricao': config.Dashboard.Descricao,
            'duracao': config.Duracao,
        })

    return JsonResponse({
        'success': True,
        'dashboards': dashboards_list,
        'total': len(dashboards_list)
    })
