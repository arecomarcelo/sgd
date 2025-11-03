#!/usr/bin/env python3
"""
Script para corrigir chaves CSS em f-strings do Streamlit.
Escapa { e } para {{ e }}, mas preserva variáveis Python como {bg_color}.
"""

import re

# Variáveis Python que NÃO devem ser escapadas
PYTHON_VARS = [
    'bg_color',
    'text_color',
    'card_bg',
    'border_color',
    'footer_bg',
    'st.session_state.current_index',
    'total_dashboards',
    'progresso_percentual',
    'periodo',
    'data_atualizacao',
]


def fix_css_line(line):
    """
    Escapa chaves CSS em uma linha, mas preserva variáveis Python.
    """
    # Se a linha já tem chaves duplas, retornar como está
    if '{{' in line or '}}' in line:
        return line

    # Verificar se a linha contém alguma variável Python
    has_python_var = any(f'{{{var}}}' in line for var in PYTHON_VARS)

    if has_python_var:
        # Linha tem variável Python - substituir APENAS as chaves CSS
        # Estratégia: proteger temporariamente as variáveis Python
        protected_line = line
        placeholders = {}

        for i, var in enumerate(PYTHON_VARS):
            pattern = f'{{{var}}}'
            if pattern in protected_line:
                placeholder = f'___PYVAR{i}___'
                placeholders[placeholder] = pattern
                protected_line = protected_line.replace(pattern, placeholder)

        # Agora escapar todas as chaves restantes
        protected_line = protected_line.replace('{', '{{').replace('}', '}}')

        # Restaurar as variáveis Python
        for placeholder, original in placeholders.items():
            protected_line = protected_line.replace(placeholder, original)

        return protected_line
    else:
        # Linha sem variáveis Python - escapar todas as chaves
        return line.replace('{', '{{').replace('}', '}}')


# Ler o arquivo
with open('pages/01_🎬_Slideshow.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Processar linha por linha
fixed_lines = []
in_css = False
css_start_line = None

for i, line in enumerate(lines):
    # Detectar início do bloco CSS
    if '<style>' in line:
        in_css = True
        css_start_line = i
        fixed_lines.append(line)
    # Detectar fim do bloco CSS
    elif '</style>' in line:
        in_css = False
        fixed_lines.append(line)
    # Se estiver dentro do CSS, corrigir as chaves
    elif in_css:
        fixed_lines.append(fix_css_line(line))
    # Fora do CSS, manter como está
    else:
        fixed_lines.append(line)

# Salvar arquivo corrigido
with open('pages/01_🎬_Slideshow.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print(f"✅ Arquivo corrigido!")
print(f"   Bloco CSS processado a partir da linha {css_start_line}")
print(f"   Total de linhas: {len(fixed_lines)}")
