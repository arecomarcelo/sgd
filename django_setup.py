"""
Configuração do Django ORM para uso standalone com Streamlit
"""

import os
from pathlib import Path

import django

# Define o módulo de settings do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Configurar Django
django.setup()
