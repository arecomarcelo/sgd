from django.db import models


class Dashboard(models.Model):
    """
    Modelo para armazenar os Dashboards disponíveis no sistema.
    Os dashboards serão importados do SGS (Sistema de Gestão de Relatórios).
    """
    class Meta:
        db_table = "Dashboard"
        ordering = ["Nome"]
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboards"

    Nome = models.CharField(max_length=50, verbose_name="Nome")
    Descricao = models.CharField(max_length=255, verbose_name="Descrição")
    Ativo = models.BooleanField(null=True, blank=True, default=True, verbose_name="Ativo")

    def __str__(self):
        return self.Nome


class Dashboard_Config(models.Model):
    """
    Modelo para configurar a ordem e duração de exibição dos Dashboards.
    Define a sequência de exibição em formato de slides com transição automática.
    """
    class Meta:
        db_table = "Dashboard_Config"
        ordering = ["Ordem"]
        verbose_name = "Dashboard Configuração"
        verbose_name_plural = "Dashboard Configurações"

    Dashboard = models.ForeignKey(
        Dashboard,
        on_delete=models.CASCADE,
        verbose_name="Dashboard"
    )
    Ordem = models.IntegerField(verbose_name="Ordem de Exibição")
    Duracao = models.IntegerField(verbose_name="Duração (segundos)")

    def __str__(self):
        return f"{self.Ordem} - {self.Dashboard.Nome} ({self.Duracao}s)"
