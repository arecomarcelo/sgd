# 📋 Histórico de Alterações - SGD

---

## 📅 08/05/2026

### 🕐 15:50 — Correção de Responsividade: Footer sobrepondo Painel na TV

**🔍 O que foi pedido:**
O footer do slideshow estava sobrepondo o painel quando executado em TV. No desktop funcionava corretamente.

**🛠️ Detalhamento da Solução:**

**Causa raiz identificada:**
- Os painéis são renderizados via `components.html()` dentro de **iframes com altura fixa** (ex: 850px, 750px).
- O footer usa `position: fixed; bottom: 0` na página principal (fora do iframe).
- Em TVs com zoom de browser maior ou viewport reduzida, o footer (em `viewport - 100px`) ficava **dentro da área visível do iframe**, causando sobreposição visual.
- Os `padding-bottom: 200px/180px` nos painéis eram um "hack" aplicado no lugar errado (dentro do iframe, sem efeito sobre o footer externo).

**Correções aplicadas:**

1. **CSS `max-height` como proteção imediata** — adicionado em `01_🎬_Slideshow.py`:
   ```css
   iframe { max-height: calc(100vh - 110px) !important; }
   ```
   Garante que nenhum iframe ultrapasse a área disponível acima do footer.

2. **JavaScript dinâmico** — componente `components.html(height=0)` adicionado em `01_🎬_Slideshow.py`:
   - Mede a altura real do viewport (`window.parent.innerHeight`)
   - Mede a altura real do footer (`.footer-panel.getBoundingClientRect().height`)
   - Redimensiona todos os iframes de painel (height > 300px) para exatamente `viewport - footer - 12px`
   - Responde a eventos de resize (rotação de tela, zoom, etc.)
   - Usa flag `window.parent._sgdResizeAttached` para evitar múltiplos listeners em rerenders

3. **Remoção dos paddings excessivos** em `dashboard/panels.py`:
   - `render_meta_mes`: `padding-bottom: 200px` → `30px`
   - `render_metricas_vendas`: `padding-bottom: 180px` → `40px` (incluindo media queries)
   - `render_texto`: `padding-bottom: 200px/180px` → `50px/40px/30px`
   - `render_ranking_produtos`: `padding-bottom: 180px` → `30px` (incluindo media queries)

**📁 Arquivos Alterados:**

| Arquivo | Alteração |
|---------|-----------|
| `pages/01_🎬_Slideshow.py` | CSS `max-height` + componente JS de redimensionamento dinâmico |
| `dashboard/panels.py` | Redução de `padding-bottom` excessivo em todos os painéis |
