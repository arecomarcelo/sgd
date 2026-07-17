**27/10/2025**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***
  

### **15:25 - Commit Inicial**

- Criação da App **SGD** (**Sistema de Gestão de Dashboard**)

### **15:39 - Commit 01**

- Ajuste **requirements.txt**

### **17:05 - Commit 02**

- Implementado:
    - Painel de **Informações de Atualização**
    - **Imagens** dos **Dashboards Reais**

**28/10/2025**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***
  

### **16:43 - Commit 03**

- Implementada atualização da **Meta** no **Módulo ⚙️ Gerenciar Dashboards**

**03/11/2025**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***
  

### **10:21 - Commit 04**

- Implementada **Exibição Real Dasboads**

### **13:09 - Commit 05**

- Correção **Exibição Fotos Vendedores**

### **13:35 - Commit 06**

- Ajuste **Background Cards

**18/11/2025**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***
  

### **10:03 - Commit 07**

- Ajuste Novo Modelo **RPA_Atualizacao**

**27/11/2025**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***
  

### **15:05 - Commit 08**

- Ajustes:
    - Totalização do **Valor Total** considerando:
        - Vendedores (Tabela)
        - Situação, exceto: **Cancelada (sem financeiro)**  e **'Não considerar - Excluidos'**

**19/01/2026**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***
  

### **13:39 - Commit 09**

- Implementado **Painel Mensagem Dinâmica**


### **10:10 - Commit 10**

- **Painel Mensagem Dinâmica**:
    - Ajuste **Tamanho do Fonte**

**26/01/2026**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***
  

### **14:00 - Commit 11**

- Ajuste **Gravação Mensagem Automática** no Modelo **Dashboard_Config**

**12/02/2026**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***
  

### **09:53 - Commit 12**

- Inserção Novos Vendedores: **André** e **João Victor**

**18/02/2026**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***
  

### **14:49 - Commit 13**

- Painel **Configurações**:
    - Atualização de **Nome Curto** e **Percentual Meta**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***
  
**19/02/2026**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***

### **14:59 - Commit 14**

- Ajustes Layout **Painel Ranking Vendedores**

### **15:10 - Commit 15**

- Ajustes Layout **Painel Ranking Vendedores** Fonte e Cores

**17/04/2026**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***

### **15:22 - Commit 16**

- Remoção de **usuario** e **senha** Hardcode

### **15:25 - Commit 17**

- Correção de **usuario** e **senha** Hardcode

**08/05/2026**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***

### **15:50 - Commit 18**

- Ajuste: **Altura dos painéis para evitar sobreposição do footer em TVs**

**11/05/2026**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***

### **09:14 - Commit 19**

- Ajuste **Modelos Alteração Tipo de Campos**

**17/07/2026**

- #### ***Instalar requirements.txt***
  
- #### Verificado: ***Executar formata.py***

### **11:29 - Commit 20**

- Correção dos Erros **Recorrentes ao Ajuste das Tabelas Vendas e VendasProdutos**
    - Causa: colunas **Data**, **PrazoEntrega**, **ID_Gestao** e **Venda_ID** alteradas no banco de `varchar` para `date`/`bigint`, mas os models Django ainda declaravam `CharField` — o parsing manual de string de data (`.strip()`/`.split("/")`) quebrava silenciosamente e descartava todas as vendas do período, zerando o dashboard
    - `dashboard/models.py`: campos `Vendas.data`/`prazoentrega` → `DateField`, `Vendas.id_gestao`/`VendaProdutos.venda_id` → `BigIntegerField`, novas colunas `Origem` (Vendas) e `CodigoExpedicao` (VendaProdutos) adicionadas
    - `dashboard/panels.py`: filtro de período reescrito para comparar objetos `date` nativos, sem parsing manual de string
    - Testado via `streamlit run app.py --server.port 8001` — 4 painéis validados no navegador com dados reais (48 vendas no período)

### **11:32 - Commit 21**

- Formatação **Black/Isort** de `dashboard/models.py` (sem alteração de lógica)