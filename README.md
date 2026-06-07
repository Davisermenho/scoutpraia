# ScoutPraia

MVP local em Python para marcar vídeos de handebol de praia, gerar clipes, KPIs e relatórios.

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m scoutpraia.core.database
streamlit run app.py
```

## Execução rápida

Para subir a aplicação local e abrir a URL padrão automaticamente:

```bash
scripts/run_scout.sh
```

Opções úteis:

```bash
scripts/run_scout.sh --port 8517
scripts/run_scout.sh --no-browser
```

Lançador gráfico de 1 clique:

- arquivo pronto: `ScoutPraia.desktop`
- executa `scripts/run_scout.sh` a partir de `/home/davis/SCOUT`
- mantém um terminal visível para facilitar diagnóstico e encerramento da sessão

## Escopo do MVP

- Monólito local em Python.
- Interface local com Streamlit.
- Persistência em SQLite.
- Processamento de vídeo via FFmpeg/ffprobe.
- Relatórios HTML com Jinja.
- Exportação PDF ainda não implementada neste MVP.

## Não faz parte do MVP

- React.
- FastAPI.
- API pública.
- PostgreSQL.
- Autenticação.
- Multiusuário.
- Deploy.
