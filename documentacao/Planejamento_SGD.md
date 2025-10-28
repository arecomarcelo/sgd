# 🎯 Planejamento - Sistema SGD (Sistema de Gestão de Dashboard)

## 📌 Objetivo do Projeto

Criar um sistema Django que controle a exibição de Dashboards em formato de slides com transição automática, importando painéis do sistema SGR (Sistema de Gestão de Relatórios) localizado em `/media/areco/Backup/Oficial/Projetos/sgr`.

---

## 🔄 Sistema SGR (Origem dos Dashboards)

**SGR - Sistema de Gestão de Relatórios**

- **Tipo**: Aplicação Streamlit (Python)
- **Localização**: `/media/areco/Backup/Oficial/Projetos/sgr`
- **Execução**: `streamlit run app.py`
- **Painéis de Vendas**: `/media/areco/Backup/Oficial/Projetos/sgr/apps/vendas/views.py`

### Dashboards a Serem Importados:

Os seguintes painéis do relatório de vendas do SGR serão integrados ao SGD:

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

| #   | Tarefa                               | Status        | Observações                  |
| --- | ------------------------------------ | ------------- | ------------------------------ |
| 1.1 | Criar aplicação Django 'dashboard' | ✅ Concluído | App criado com sucesso         |
| 1.2 | Implementar modelo Dashboard         | ✅ Concluído | Nome, Descrição, Ativo       |
| 1.3 | Implementar modelo Dashboard_Config  | ✅ Concluído | Dashboard FK, Ordem, Duração |
| 1.4 | Registrar app em INSTALLED_APPS      | ✅ Concluído | settings.py atualizado         |
| 1.5 | Criar migrações (makemigrations)   | ✅ Concluído | 0001_initial.py criado         |
| 1.6 | Aplicar migrações (migrate)        | ✅ Concluído | Tabelas criadas no PostgreSQL  |
| 1.7 | Registrar modelos no Django Admin    | ✅ Concluído | admin.py com customizações   |
| 1.8 | Testar criação de dados via Admin  | ✅ Concluído | Pronto para uso                |

---

### 🖥️ Fase 2 - Interface de Visualização (Streamlit)

**Status**: ✅ Concluída em 27/10/2025

**Decisão de Arquitetura**: Interface implementada com **Streamlit** (ao invés de Django Templates) para facilitar integração futura com SGR (também Streamlit).

| #    | Tarefa                                         | Status        | Observações                                     |
| ---- | ---------------------------------------------- | ------------- | ------------------------------------------------- |
| 2.1  | Criar aplicação Streamlit base               | ✅ Concluído | app.py com auto-redirect para slideshow           |
| 2.2  | Implementar página de slideshow               | ✅ Concluído | pages/01_🎬_Slideshow.py                          |
| 2.3  | Implementar lógica de ordenação             | ✅ Concluído | Ordenação por Dashboard_Config.Ordem            |
| 2.4  | Implementar rotação automática              | ✅ Concluído | streamlit-autorefresh com duração configurável |
| 2.5  | Implementar CSS tela cheia                     | ✅ Concluído | Background preto, sem scrollbars, 100vh/100vw     |
| 2.6  | Implementar transições entre slides          | ✅ Concluído | fadeIn animation + scale effect CSS               |
| 2.7  | Criar página de gerenciamento                 | ✅ Concluído | pages/02_⚙️_Gerenciar.py                        |
| 2.8  | Implementar controles de ordem/duração       | ✅ Concluído | number_input com ajuste automático de ordem      |
| 2.9  | Implementar ativar/desativar dashboards        | ✅ Concluído | Botão toggle com atualização no DB             |
| 2.10 | Implementar exibição de imagens temporárias | ✅ Concluído | Normalização de nomes + fallback                |
| 2.11 | Adicionar modelo VendaAtualizacao              | ✅ Concluído | managed=False (tabela existente)                  |
| 2.12 | Criar painel de rodapé com info atualização | ✅ Concluído | Cards com Período e Data/Hora                    |
| 2.13 | Ajustar centralização de imagens             | ✅ Concluído | Flexbox center + object-fit contain               |
| 2.14 | Testar exibição completa                     | ✅ Concluído | 4 dashboards rodando corretamente                 |

**Funcionalidades Implementadas:**

- ✅ Auto-start do slideshow ao abrir aplicação
- ✅ Tela cheia sem distrações (header, footer, sidebar ocultos)
- ✅ Botão de engrenagem fixo (topo direito) para gerenciamento
- ✅ Painel de rodapé fixo com período e data de atualização
- ✅ Sistema de normalização de nomes para imagens
- ✅ Página de gerenciamento com ordem atual e controles
- ✅ 4 dashboards configurados e funcionando

---

### 🔗 Fase 3 - Integração com SGR (Streamlit)

**Status**: 🚀 Pronta para Iniciar

**Contexto**: Substituir imagens temporárias por dashboards dinâmicos do SGR, utilizando componentes Streamlit nativos ou integração via iframe.

| #   | Tarefa                                   | Status      | Observações                              |
| --- | ---------------------------------------- | ----------- | ------------------------------------------ |
| 3.1 | Analisar estrutura do SGR Streamlit      | ⏳ Pendente | Aplicação Streamlit em sgr/              |
| 3.2 | Definir estratégia de integração      | ⏳ Pendente | iframe, componente, ou importação direta |
| 3.3 | Implementar painel "Meta Mês"           | ⏳ Pendente | Substituir imagem por dashboard real       |
| 3.4 | Implementar painel "Métricas de Vendas" | ⏳ Pendente | Substituir imagem por dashboard real       |
| 3.5 | Implementar painel "Ranking Vendedores"  | ⏳ Pendente | Substituir imagem por dashboard real       |
| 3.6 | Implementar painel "Ranking Produtos"    | ⏳ Pendente | Substituir imagem por dashboard real       |
| 3.7 | Remover pasta /imagens/ temporária      | ⏳ Pendente | Limpar imagens de teste                    |
| 3.8 | Testar integração completa             | ⏳ Pendente | Validação end-to-end                     |

---

### 🎨 Fase 4 - Refinamentos e Melhorias (Opcional)

**Status**: ⏳ Aguardando Fase 3

| #   | Tarefa                             | Status      | Observações                   |
| --- | ---------------------------------- | ----------- | ------------------------------- |
| 4.1 | Adicionar modo tela cheia          | ⏳ Pendente | F11 automático                 |
| 4.2 | Implementar indicador de progresso | ⏳ Pendente | Barra ou contador               |
| 4.3 | Adicionar controles manuais        | ⏳ Pendente | Play, Pause, Próximo, Anterior |
| 4.4 | Implementar logs de exibição     | ⏳ Pendente | Auditoria                       |
| 4.5 | Adicionar temas visuais            | ⏳ Pendente | Dark/Light mode                 |
| 4.6 | Otimizar performance               | ⏳ Pendente | Cache, preload                  |

---

## 📊 Progresso Geral

- **Fase 1**: ✅✅✅✅✅✅✅✅ 100% (8/8) ✅ **CONCLUÍDA**
- **Fase 2**: ✅✅✅✅✅✅✅✅✅✅✅✅✅✅ 100% (14/14) ✅ **CONCLUÍDA**
- **Fase 3**: ⬜⬜⬜⬜⬜⬜⬜⬜ 0% (0/8) 🚀 **PRONTA PARA INICIAR**
- **Fase 4**: ⬜⬜⬜⬜⬜⬜ 0% (0/6)

**Progresso Total**: 22/36 tarefas (61%)

---

## 📝 Observações

- Este documento será atualizado conforme o progresso do projeto
- Cada fase deve ser concluída antes de iniciar a próxima
- Tarefas podem ser adicionadas ou removidas conforme necessidade
- Status possíveis: ⏳ Pendente | 🔄 Em Progresso | ✅ Concluído | ❌ Cancelado

---

**Última Atualização**: 27/10/2025 às 16:55
