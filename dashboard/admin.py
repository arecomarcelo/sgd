from django.contrib import admin

from .models import Dashboard, Dashboard_Config


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    """
    Administração do modelo Dashboard.
    """

    list_display = ('Nome', 'Descricao', 'Ativo')
    list_filter = ('Ativo',)
    search_fields = ('Nome', 'Descricao')
    list_editable = ('Ativo',)
    ordering = ('Nome',)


@admin.register(Dashboard_Config)
class DashboardConfigAdmin(admin.ModelAdmin):
    """
    Administração do modelo Dashboard_Config.
    Configuração da ordem e duração de exibição dos dashboards.
    """

    list_display = ('Ordem', 'Dashboard', 'Duracao', 'dashboard_ativo')
    list_filter = ('Dashboard__Ativo',)
    search_fields = ('Dashboard__Nome',)
    ordering = ('Ordem',)

    def dashboard_ativo(self, obj):
        """Exibe se o dashboard associado está ativo."""
        return obj.Dashboard.Ativo

    dashboard_ativo.boolean = True
    dashboard_ativo.short_description = 'Dashboard Ativo'
