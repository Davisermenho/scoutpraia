---
tipo: evidência_g5
gerado_em: 2026-06-12
método: Playwright headless automático (Python asyncio)
url: http://localhost:8501
app: ScoutPraia
pytest: 311 passed
G5_status: FECHADO — APROVADO
---

# Manifesto de Evidências G5 — ScoutPraia

Gerado automaticamente via Playwright em 2026-06-12.

## Método de captura

```bash
source .venv/bin/activate
pip install playwright
streamlit run app.py --server.port 8501 --server.headless true &
python3 scripts/capture_g5_evidence.py
```

Browser: Chromium headless (`~/.cache/ms-playwright/chromium-1224`)
Viewport: 1280×900

---

## O que cada screenshot prova

| Arquivo | Tela | O que prova |
|---------|------|-------------|
| `01_dashboard_loaded.png` | Dashboard | App carrega; mostra 1 jogo, **12 eventos**, **16 relatórios**, 1 jogo com vídeo |
| `02_jogos.png` | Jogos | Jogo 1 cadastrado: Etapa do Circuito Brasileiro 2026, adversária Campinas 360, vídeo associado |
| `03_marcacao_full.png` | Marcação | Player de vídeo renderizado (jogo real 32:47), histórico com 6+ eventos visíveis, jogo selecionado |
| `03b_marcacao_historico.png` | Marcação | Histórico recente com IDs, timestamps e tipos de evento |
| `03c_marcacao_botoes.png` | Marcação | Botões "Finalização v1.0" ativos: Arremesso simples, Arremesso da goleira, Arremesso com giro, etc. |
| `04_relatorios_top.png` | Relatórios | Prévia de KPIs: Pontos 2, Gols 1, Posses ofensivas 6, Posses defensivas 5, Conversão 0.5 |
| `04b_relatorios_lista.png` | Relatórios | 16 relatórios gerados listados com links de download |
| `05_dashboard_com_dados.png` | Dashboard | KPIs do Jogo 1: pontos=2, gols=1, pontos_por_posse=0.333, conversão=0.5 |
| `06_adversarias.png` | Adversárias | Campinas 360 cadastrada |

---

## Evidências numéricas confirmadas pelo app

| Métrica | Valor observado | Fonte |
|---------|----------------|-------|
| Jogos cadastrados | 1 | Dashboard > Jogos cadastrados |
| Eventos salvos | **12** | Dashboard > Eventos salvos |
| Relatórios gerados | **16** | Dashboard > Relatórios gerados |
| Jogos com vídeo | 1 | Dashboard > Jogos com vídeo |
| Pontos totais (KPI) | 2 | Relatórios > Prévia de KPIs |
| Gols totais (KPI) | 1 | Relatórios > Prévia de KPIs |
| Posses ofensivas | 6 | Relatórios > Prévia de KPIs |
| Conversão ofensiva | 0.5 | Relatórios > Prévia de KPIs |
| Duração do vídeo | 32:47 | Marcação > player de vídeo |
| Pytest | **311 passed** | terminal |

---

## Correspondência com o Bloco B do protocolo G5

| Critério do Bloco B | Evidência visual | Arquivo |
|--------------------|-----------------|---------|
| UI carrega sem erro fatal | Dashboard completo carregado | `01_dashboard_loaded.png` |
| Vídeo renderiza | Player visível com 0:00/32:47 | `03_marcacao_full.png` |
| Amostra mínima de eventos salva | 12 eventos no Dashboard | `01_dashboard_loaded.png` |
| Histórico reflete eventos salvos | Histórico recente com IDs e timestamps | `03b_marcacao_historico.png` |
| Relatório coletivo gerado | 16 relatórios listados | `04b_relatorios_lista.png` |
| Relatório individual gerado | Link individual na lista | `04b_relatorios_lista.png` |
| Relatório adversária gerado | Link adversária na lista | `04b_relatorios_lista.png` |
| KPIs calculados corretamente | pontos=2, conversão=0.5 | `04_relatorios_top.png` |
