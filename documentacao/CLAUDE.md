# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projeto SGD (Sistema de Gestão de Dashboard)

Este é um projeto Django 5.2.2 que controla a exibição de Dashboards em formato de slides com transição automática.

### Integração com SGS (Sistema de Gestão de Relatórios)

O SGD importa e exibe painéis do **SGS - Sistema de Gestão de Relatórios**, uma aplicação Streamlit localizada em:
- **Localização**: `/media/areco/Backup/Oficial/Projetos/sgr`
- **Tipo**: Aplicação Streamlit (Python)
- **Comando de execução**: `streamlit run app.py`
- **Painéis**: Meta Mês, Métricas de Venda, Ranking Vendedores, Ranking Produtos

## Diretrizes de Codificação

### Princípios Fundamentais

1. **Revisão de Alterações**: Sempre revise suas alterações de modo a não alterar ou prejudicar a execução já implementada
2. **Idioma**: Sempre responder em Português do Brasil
3. **Listagem de Arquivos**: Sempre listar os nomes dos arquivos alterados
4. **Finalização**: Sempre finalize suas respostas com uma linha em branco `*** FINALIZADO ***`
5. **Histórico de Interações**: Ao finalizar uma interação, armazene no arquivo `Historico.md` (crie se não existir) na pasta `documentacao/`:
   - Dia (somente na primeira interação do dia) e a cada nova interação a Hora da Tarefa
   - O que foi pedido
   - Detalhamento da Solução ou Implementação
   - Lista de Arquivos Alterados ou Criados
   - Utilize emojis para tornar clara a compreensão
   - Utilize UTF-8 e o Fuso Horário Local
6. **MODELOS**: Os modelos já existem no banco de dados e **NÃO devem gerar migrações**
7. **NOVOS MODELOS**: Quando um modelo não existir, será informado como "Novo Modelo" na descrição e pedido para que seja implementado

### Organização de Arquivos

- Todos os documentos criados devem ser armazenados na pasta `documentacao/`
- Toda pasta ou arquivo criado deve estar dentro do domínio da aplicação (`/media/areco/Backup/Oficial/Projetos/sgd/`)
- Jamais criar arquivos fora do domínio do projeto

## Estrutura do Projeto

- **app/**: Diretório principal do projeto Django
  - `settings.py`: Configurações do projeto (PostgreSQL)
  - `urls.py`: Configuração de rotas principais
  - `wsgi.py` e `asgi.py`: Servidores de aplicação
- **dashboard/**: App Django para gerenciamento de dashboards
  - `models.py`: Modelos Dashboard e Dashboard_Config
  - `views.py`: Views do slideshow e API
  - `admin.py`: Configuração do Django Admin
  - `urls.py`: Rotas do app
  - `templates/`: Templates HTML do slideshow
- **documentacao/**: Documentação do projeto
  - `CLAUDE.md`: Este arquivo
  - `Historico.md`: Histórico de interações
  - `Planejamento_SGD.md`: Roadmap do projeto
- **venv/**: Ambiente virtual Python
- **requirements.txt**: Dependências do projeto (Django, psycopg2-binary, etc.)

## Comandos de Desenvolvimento

### Ambiente Virtual
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Desativar ambiente virtual
deactivate
```

### Execução da Aplicação
```bash
# Executar servidor de desenvolvimento
python manage.py runserver

# Executar em porta específica (8001 conforme padrão do projeto)
python manage.py runserver 8001
```

### Migrações de Banco de Dados
```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Ver status das migrações
python manage.py showmigrations
```

### Gerenciamento de Aplicações
```bash
# Criar nova aplicação Django
python manage.py startapp <nome_da_app>

# Criar superusuário
python manage.py createsuperuser
```

### Testes
```bash
# Executar todos os testes
python manage.py test

# Executar testes de uma app específica
python manage.py test <nome_da_app>

# Executar teste específico
python manage.py test <nome_da_app>.tests.<NomeDoTeste>
```

### Shell Django
```bash
# Abrir shell interativo do Django
python manage.py shell
```

## Configurações Importantes

- **Banco de Dados**: PostgreSQL
  - Database: `sga`
  - Host: `195.200.1.244`
  - Port: `5432`
  - User: `postgres`
- **Timezone**: America/Sao_Paulo
- **Linguagem**: pt-br
- **Debug Mode**: Atualmente ativado (desenvolvimento)
- **Porta Padrão**: 8001 (deixar 8000 livre conforme padrão do projeto)

## Estrutura do Banco de Dados

### Modelos Implementados:

**Dashboard:**
- Nome (CharField, 50 caracteres)
- Descricao (CharField, 255 caracteres)
- Ativo (BooleanField, default=True)

**Dashboard_Config:**
- Dashboard (ForeignKey)
- Ordem (IntegerField) - ordem de exibição
- Duracao (IntegerField) - duração em segundos

### Observações:
- Sempre verificar se um modelo já existe antes de criar migrações
- Modelos existentes não devem gerar novas migrações (ver Diretrizes de Codificação)

## Dependências

As dependências do projeto devem ser mantidas no arquivo `requirements.txt`. Quando adicionar novas bibliotecas:

```bash
# Instalar dependências
pip install -r requirements.txt

# Adicionar nova dependência
pip install <pacote>
pip freeze > requirements.txt
```
