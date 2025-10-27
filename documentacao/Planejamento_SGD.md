# 🎯 Planejamento - Sistema SGD (Sistema de Gestão de Dashboard)

## 📌 Objetivo do Projeto

Criar um sistema Django que controle a exibição de Dashboards em formato de slides com transição automática, importando painéis do sistema SGS (Sistema de Gestão de Relatórios) localizado em `/media/areco/Backup/Oficial/Projetos/sgr`.

---

## 🔄 Sistema SGS (Origem dos Dashboards)

**SGS - Sistema de Gestão de Relatórios**
- **Tipo**: Aplicação Streamlit (Python)
- **Localização**: `/media/areco/Backup/Oficial/Projetos/sgr`
- **Execução**: `streamlit run app.py`
- **Painéis de Vendas**: `/media/areco/Backup/Oficial/Projetos/sgr/apps/vendas/views.py`

### Dashboards a Serem Importados:
Os seguintes painéis do relatório de vendas do SGS serão integrados ao SGD:
- Meta Mês
- Métricas de Venda
- Ranking Vendedores
- Ranking Produtos

---

## 📋 Regras de Negócio

1. ✅ **Ordem de Exibição**: Dashboards exibidos conforme `Dashboard_Config.Ordem`
2. ✅ **Filtro de Ativos**: Apenas dashboards com `Dashboard.Ativo = True` são exibidos
3. ✅ **Duração**: Cada dashboard permanece visível por `Dashboard_Config.Duracao` segundos
4. ✅ **Transição Automática**: Após expirar o tempo, próximo dashboard é carregado
5. ✅ **Loop Contínuo**: Processo se repete continuamente

---

## 🗺️ Roadmap de Implementação

### 📦 Fase 1 - Estrutura Base (Modelos e Admin)
**Status**: ✅ Concluída em 27/10/2025

| # | Tarefa | Status | Observações |
|---|--------|--------|-------------|
| 1.1 | Criar aplicação Django 'dashboard' | ✅ Concluído | App criado com sucesso |
| 1.2 | Implementar modelo Dashboard | ✅ Concluído | Nome, Descrição, Ativo |
| 1.3 | Implementar modelo Dashboard_Config | ✅ Concluído | Dashboard FK, Ordem, Duração |
| 1.4 | Registrar app em INSTALLED_APPS | ✅ Concluído | settings.py atualizado |
| 1.5 | Criar migrações (makemigrations) | ✅ Concluído | 0001_initial.py criado |
| 1.6 | Aplicar migrações (migrate) | ✅ Concluído | Tabelas criadas no PostgreSQL |
| 1.7 | Registrar modelos no Django Admin | ✅ Concluído | admin.py com customizações |
| 1.8 | Testar criação de dados via Admin | ✅ Concluído | Pronto para uso |

---

### 🖥️ Fase 2 - Interface de Visualização
**Status**: ✅ Concluída em 27/10/2025

| # | Tarefa | Status | Observações |
|---|--------|--------|-------------|
| 2.1 | Criar view para listagem de dashboards ativos | ✅ Concluído | Views criadas (slideshow_view, get_dashboards_config) |
| 2.2 | Implementar lógica de ordenação | ✅ Concluído | Ordenação por Dashboard_Config.Ordem |
| 2.3 | Criar template HTML para exibição | ✅ Concluído | Template responsivo com gradient design |
| 2.4 | Implementar JavaScript para rotação automática | ✅ Concluído | Fetch API + timers automáticos |
| 2.5 | Implementar transições entre slides | ✅ Concluído | fadeIn animation + scale effect |
| 2.6 | Implementar loop contínuo | ✅ Concluído | Retorna ao primeiro após último |
| 2.7 | Configurar rotas (urls.py) | ✅ Concluído | URLs configuradas (/ e /api/config/) |
| 2.8 | Testar exibição e transições | ✅ Concluído | Servidor testado na porta 8001 |

---

### 🔗 Fase 3 - Integração com SGS (Streamlit)
**Status**: ⏳ Aguardando Fase 2

| # | Tarefa | Status | Observações |
|---|--------|--------|-------------|
| 3.1 | Analisar estrutura do SGS Streamlit | ⏳ Pendente | Aplicação Streamlit em sgr/ |
| 3.2 | Definir estratégia de integração | ⏳ Pendente | iframe, componente, ou API |
| 3.3 | Implementar painel "Meta Mês" | ⏳ Pendente | - |
| 3.4 | Implementar painel "Métricas de Venda" | ⏳ Pendente | - |
| 3.5 | Implementar painel "Ranking Vendedores" | ⏳ Pendente | - |
| 3.6 | Implementar painel "Ranking Produtos" | ⏳ Pendente | - |
| 3.7 | Testar integração completa | ⏳ Pendente | Validação end-to-end |

---

### 🎨 Fase 4 - Refinamentos e Melhorias (Opcional)
**Status**: ⏳ Aguardando Fase 3

| # | Tarefa | Status | Observações |
|---|--------|--------|-------------|
| 4.1 | Adicionar modo tela cheia | ⏳ Pendente | F11 automático |
| 4.2 | Implementar indicador de progresso | ⏳ Pendente | Barra ou contador |
| 4.3 | Adicionar controles manuais | ⏳ Pendente | Play, Pause, Próximo, Anterior |
| 4.4 | Implementar logs de exibição | ⏳ Pendente | Auditoria |
| 4.5 | Adicionar temas visuais | ⏳ Pendente | Dark/Light mode |
| 4.6 | Otimizar performance | ⏳ Pendente | Cache, preload |

---

## 📊 Progresso Geral

- **Fase 1**: ✅✅✅✅✅✅✅✅ 100% (8/8) ✅ **CONCLUÍDA**
- **Fase 2**: ✅✅✅✅✅✅✅✅ 100% (8/8) ✅ **CONCLUÍDA**
- **Fase 3**: ⬜⬜⬜⬜⬜⬜⬜ 0% (0/7)
- **Fase 4**: ⬜⬜⬜⬜⬜⬜ 0% (0/6)

**Progresso Total**: 16/29 tarefas (55%)

---

## 📝 Observações

- Este documento será atualizado conforme o progresso do projeto
- Cada fase deve ser concluída antes de iniciar a próxima
- Tarefas podem ser adicionadas ou removidas conforme necessidade
- Status possíveis: ⏳ Pendente | 🔄 Em Progresso | ✅ Concluído | ❌ Cancelado

---

**Última Atualização**: 27/10/2025 às 11:57
