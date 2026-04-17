"""
Configuração do Django ORM para uso standalone com Streamlit
"""

import os

import django

# Injeta st.secrets["database"] em os.environ para que settings.py
# encontre as credenciais tanto no Streamlit Cloud quanto localmente via .env
try:
    import streamlit as st
    db_secrets = st.secrets.get("database", {})
    for key in ("DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"):
        if key in db_secrets and key not in os.environ:
            os.environ[key] = str(db_secrets[key])
except Exception:
    pass  # Fora do contexto Streamlit ou secrets não configurados — usa .env

# Define o módulo de settings do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Configurar Django
django.setup()
