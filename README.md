# ScoutPraia

MVP local em Python para marcar vídeos de handebol de praia, gerar clipes, KPIs e relatórios.

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 -m scoutpraia.core.database
streamlit run app.py
```

Se `python3 -m venv .venv` falhar por ausência de `ensurepip` / `python3-venv`, use o fallback local já versionado:

```bash
scripts/setup_venv.sh
source .venv/bin/activate
cp .env.example .env
python3 -m scoutpraia.core.database
streamlit run app.py
```

Observações do fallback:

- `scripts/setup_venv.sh` depende de `virtualenv` disponível no ambiente.
- se `.venv` já existir, o script bloqueia a recriação silenciosa;
- para remover e recriar `.venv`, use `scripts/setup_venv.sh --force`.

## Execução rápida

Para subir a aplicação local e abrir a URL padrão automaticamente:

```bash
scripts/run_scout.sh
```

Comportamento do launcher:

- se `./.venv` existir, o script ativa essa virtualenv automaticamente antes de procurar `streamlit`;
- isso evita usar um `streamlit` global diferente do ambiente do projeto;
- se não houver `.venv`, o script continua tentando usar os comandos disponíveis no ambiente atual.

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
