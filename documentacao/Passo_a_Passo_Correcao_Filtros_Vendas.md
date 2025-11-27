# 📋 Passo a Passo: Correção de Filtros de Vendas

## 🎯 Objetivo
Corrigir cálculos de vendas para excluir:
1. Vendas com situações específicas (canceladas, excluídas)
2. Vendas de vendedores não cadastrados

---

## 🔍 Problema Identificado

### Sintoma
O dashboard exibe valores maiores que o real devido a inclusão de:
- Vendas canceladas/excluídas
- Vendas de vendedores não cadastrados na tabela `Vendedores`

### Query SQL Correta
```sql
SELECT SUM(v."ValorTotal"::NUMERIC) AS total_vendas
FROM "Vendas" v
WHERE TRIM(v."VendedorNome") IN (SELECT "Nome" FROM "Vendedores")
  AND v."SituacaoNome" NOT IN ('Cancelada (sem financeiro)', 'Não considerar - Excluidos')
  AND v."Data"::DATE >= DATE_TRUNC('month', CURRENT_DATE)::DATE
  AND v."Data"::DATE <= CURRENT_DATE
```

---

## 📝 Passo a Passo da Implementação

### **PASSO 1: Identificar o arquivo de busca de vendas**

**Localização típica:**
- Arquivo que contém funções de busca/cálculo de vendas
- Pode ser: `panels.py`, `views.py`, `utils.py`, ou similar

**Como identificar:**
```bash
# Procurar por funções que buscam vendas
grep -r "Vendas.objects" .
grep -r "get_vendas" .
```

---

### **PASSO 2: Adicionar import do modelo Vendedores**

**Localização:** Início do arquivo (seção de imports)

**ANTES:**
```python
from dashboard.models import VendaConfiguracao, VendaProdutos, Vendas
```

**DEPOIS:**
```python
from dashboard.models import VendaConfiguracao, VendaProdutos, Vendas, Vendedores
```

**⚠️ Importante:**
- Verifique se o modelo `Vendedores` existe no seu projeto
- O nome pode variar: `Vendedor`, `Vendedores`, `Seller`, etc.

---

### **PASSO 3: Atualizar função principal de busca de vendas**

**Identificar a função:** Geralmente algo como `get_vendas_periodo()`, `buscar_vendas()`, etc.

#### **3.1 - Definir lista de situações excluídas**

**Adicionar no início da função:**
```python
# Situações a serem excluídas
situacoes_excluidas = ["Cancelada (sem financeiro)", "Não considerar - Excluidos"]
```

**⚠️ Importante:**
- Ajuste os nomes das situações conforme seu banco de dados
- Verifique os valores exatos no campo `SituacaoNome`

#### **3.2 - Buscar vendedores válidos**

**Adicionar após definir situações excluídas:**
```python
# Buscar lista de vendedores válidos
vendedores_validos = set(Vendedores.objects.values_list('nome', flat=True))
```

**⚠️ Importante:**
- Ajuste o nome do campo: pode ser `nome`, `Nome`, `name`, etc.
- O `set()` melhora performance nas comparações

#### **3.3 - Aplicar filtros no loop de vendas**

**ANTES:**
```python
vendas_filtradas = []
for venda in vendas:
    try:
        data_venda = venda.data.strip()
        # ... processamento de data ...
        if di_str <= venda_str <= df_str:
            vendas_filtradas.append(venda)
    except:
        continue
```

**DEPOIS:**
```python
vendas_filtradas = []
for venda in vendas:
    try:
        # Filtrar por situação
        if venda.situacaonome in situacoes_excluidas:
            continue

        # Filtrar apenas vendedores válidos (trim do nome)
        vendedor_nome = venda.vendedornome.strip() if venda.vendedornome else ""
        if vendedor_nome not in vendedores_validos:
            continue

        data_venda = venda.data.strip()
        # ... processamento de data ...
        if di_str <= venda_str <= df_str:
            vendas_filtradas.append(venda)
    except:
        continue
```

**⚠️ Importante:**
- Ajuste nomes dos campos: `situacaonome`, `vendedornome` podem variar
- O `.strip()` remove espaços em branco (equivalente ao TRIM do SQL)

---

### **PASSO 4: Atualizar queries diretas (se houver)**

**Identificar queries diretas:**
```python
# Exemplo de query direta
vendas = Vendas.objects.filter(
    data__gte=data_inicial,
    data__lte=data_final
)
```

**ANTES:**
```python
vendas_atual = Vendas.objects.filter(
    data__gte=data_inicio_atual.strftime("%d/%m/%Y"),
    data__lte=data_fim_atual.strftime("%d/%m/%Y"),
)
```

**DEPOIS:**
```python
# Situações a serem excluídas
situacoes_excluidas = ["Cancelada (sem financeiro)", "Não considerar - Excluidos"]

# Buscar lista de vendedores válidos
vendedores_validos = set(Vendedores.objects.values_list('nome', flat=True))

vendas_atual = Vendas.objects.filter(
    data__gte=data_inicio_atual.strftime("%d/%m/%Y"),
    data__lte=data_fim_atual.strftime("%d/%m/%Y"),
).exclude(situacaonome__in=situacoes_excluidas)
```

**E no processamento:**
```python
for venda in vendas_atual:
    nome = venda.vendedornome.strip() if venda.vendedornome else ""
    # Filtrar apenas vendedores válidos
    if nome in vendedores_validos:
        # ... processar venda ...
```

---

### **PASSO 5: Atualizar documentação da função**

**ANTES:**
```python
def get_vendas_periodo():
    """
    Busca vendas do período com filtros fixos aplicados
    Retorna queryset filtrado
    """
```

**DEPOIS:**
```python
def get_vendas_periodo():
    """
    Busca vendas do período com filtros fixos aplicados
    Retorna queryset filtrado
    Exclui vendas com situação "Cancelada (sem financeiro)" e "Não considerar - Excluidos"
    Filtra apenas vendedores que existem na tabela Vendedores
    """
```

---

## ✅ Checklist de Validação

### Antes de testar:
- [ ] Import do modelo `Vendedores` adicionado
- [ ] Lista `situacoes_excluidas` definida com valores corretos
- [ ] Busca de `vendedores_validos` implementada
- [ ] Filtro de situação aplicado em todos os loops
- [ ] Filtro de vendedor válido aplicado em todos os loops
- [ ] `.strip()` aplicado ao nome do vendedor
- [ ] Documentação das funções atualizada

### Para testar:
1. [ ] Limpar cache (se usar cache)
2. [ ] Recarregar a aplicação
3. [ ] Verificar o valor exibido no dashboard
4. [ ] Comparar com a query SQL direta no banco

### Query de teste SQL:
```sql
-- Execute no banco para comparar resultado
SELECT SUM(v."ValorTotal"::NUMERIC) AS total_vendas
FROM "Vendas" v
WHERE TRIM(v."VendedorNome") IN (SELECT "Nome" FROM "Vendedores")
  AND v."SituacaoNome" NOT IN ('Cancelada (sem financeiro)', 'Não considerar - Excluidos')
  AND v."Data"::DATE >= DATE_TRUNC('month', CURRENT_DATE)::DATE
  AND v."Data"::DATE <= CURRENT_DATE;
```

---

## 🔧 Adaptações por Tecnologia

### Django (ORM)
```python
# Buscar vendedores válidos
vendedores_validos = set(Vendedores.objects.values_list('nome', flat=True))

# Excluir situações
.exclude(situacaonome__in=situacoes_excluidas)

# Filtrar por vendedor (no loop)
if vendedor_nome in vendedores_validos:
```

### SQLAlchemy
```python
# Buscar vendedores válidos
vendedores_validos = set([v.nome for v in session.query(Vendedores.nome).all()])

# Excluir situações
.filter(~Vendas.situacaonome.in_(situacoes_excluidas))

# Filtrar por vendedor
.filter(Vendas.vendedornome.in_(vendedores_validos))
```

### Raw SQL
```sql
SELECT * FROM Vendas v
WHERE TRIM(v.VendedorNome) IN (SELECT Nome FROM Vendedores)
  AND v.SituacaoNome NOT IN ('Cancelada (sem financeiro)', 'Não considerar - Excluidos')
  AND v.Data >= DATE_TRUNC('month', CURRENT_DATE)
  AND v.Data <= CURRENT_DATE
```

---

## ⚠️ Pontos de Atenção

### 1. Nomes de Campos
Os nomes de campos podem variar entre projetos:
- `VendedorNome` vs `vendedor_nome` vs `vendedorNome`
- `SituacaoNome` vs `situacao_nome` vs `status`
- Verifique no seu modelo qual convenção é usada

### 2. Formato de Data
Verifique como as datas são armazenadas:
- String: `"27/11/2025"` ou `"2025-11-27"`
- Date/DateTime: objeto Python
- Timestamp: número

### 3. Cache
Se usar cache (`@st.cache_data`, `@cache`, etc.):
- Limpe o cache após alterações
- Use TTL (Time To Live) adequado
- Considere invalidar cache após alterações

### 4. Performance
Para grandes volumes de dados:
- Use `.values_list()` ao invés de `.all()`
- Considere usar `set()` para listas de comparação
- Aplique filtros no banco quando possível (`.exclude()`, `.filter()`)

---

## 📊 Exemplo Completo

```python
from django.db.models import Sum
from decimal import Decimal
from datetime import datetime

def get_vendas_periodo():
    """
    Busca vendas do período com filtros fixos aplicados
    Retorna queryset filtrado
    Exclui vendas com situação "Cancelada (sem financeiro)" e "Não considerar - Excluidos"
    Filtra apenas vendedores que existem na tabela Vendedores
    """
    # Período: 01 do mês atual até hoje
    hoje = datetime.now()
    data_inicial = datetime(hoje.year, hoje.month, 1).date()
    data_final = hoje.date()

    # Situações a serem excluídas
    situacoes_excluidas = [
        "Cancelada (sem financeiro)",
        "Não considerar - Excluidos"
    ]

    # Buscar lista de vendedores válidos
    vendedores_validos = set(
        Vendedores.objects.values_list('nome', flat=True)
    )

    # Buscar vendas
    vendas = Vendas.objects.all()

    vendas_filtradas = []
    for venda in vendas:
        try:
            # Filtrar por situação
            if venda.situacaonome in situacoes_excluidas:
                continue

            # Filtrar apenas vendedores válidos
            vendedor_nome = venda.vendedornome.strip() if venda.vendedornome else ""
            if vendedor_nome not in vendedores_validos:
                continue

            # Filtrar por data
            # (adapte conforme formato do seu projeto)
            data_venda = venda.data
            if data_inicial <= data_venda <= data_final:
                vendas_filtradas.append(venda)

        except Exception as e:
            # Log do erro se necessário
            continue

    return vendas_filtradas
```

---

## 📞 Suporte

Se encontrar problemas:

1. **Verifique os nomes dos campos** no seu modelo
2. **Teste a query SQL** diretamente no banco
3. **Compare os resultados** entre SQL e código Python
4. **Verifique os logs** para erros não tratados

---

## 📚 Referências

- Django ORM: https://docs.djangoproject.com/en/stable/topics/db/queries/
- Python sets: https://docs.python.org/3/tutorial/datastructures.html#sets
- SQL TRIM: https://www.postgresql.org/docs/current/functions-string.html

---

**Documento criado em:** 27/11/2024
**Versão:** 1.0
**Projeto base:** SGD - Sistema de Gestão de Dashboards
