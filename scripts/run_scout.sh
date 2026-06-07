#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${SCOUTPRAIA_PORT:-8516}"
OPEN_BROWSER=true

usage() {
    cat <<'EOF'
Uso:
  scripts/run_scout.sh [--port PORT] [--no-browser]

Opções:
  --port PORT     Porta local do Streamlit. Padrão: 8516
  --no-browser    Não tenta abrir o navegador automaticamente
  -h, --help      Mostra esta ajuda
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --port)
            PORT="${2:-}"
            shift 2
            ;;
        --no-browser)
            OPEN_BROWSER=false
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            printf 'Argumento inválido: %s\n\n' "$1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

if [[ -z "${PORT}" ]] || ! [[ "${PORT}" =~ ^[0-9]+$ ]]; then
    printf 'Porta inválida: %s\n' "${PORT}" >&2
    exit 1
fi

if ! command -v streamlit >/dev/null 2>&1; then
    printf 'Comando não encontrado: streamlit\n' >&2
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    printf 'Comando não encontrado: python3\n' >&2
    exit 1
fi

cd "${ROOT_DIR}"

URL="http://localhost:${PORT}"

cleanup() {
    if [[ -n "${STREAMLIT_PID:-}" ]] && kill -0 "${STREAMLIT_PID}" >/dev/null 2>&1; then
        kill "${STREAMLIT_PID}" >/dev/null 2>&1 || true
        wait "${STREAMLIT_PID}" >/dev/null 2>&1 || true
    fi
}

trap cleanup EXIT INT TERM

printf '== ScoutPraia run ==\n'
printf 'cwd=%s\n' "${ROOT_DIR}"
printf 'url=%s\n' "${URL}"
printf 'open_browser=%s\n\n' "${OPEN_BROWSER}"

streamlit run app.py --server.headless true --server.port "${PORT}" &
STREAMLIT_PID=$!

python3 - "${URL}" <<'PY'
import sys
import time
from urllib.request import urlopen

url = sys.argv[1]
deadline = time.time() + 60
last_error = None

while time.time() < deadline:
    try:
        with urlopen(url, timeout=2) as response:
            if 200 <= response.status < 500:
                print(f"server_ready={url}")
                raise SystemExit(0)
    except Exception as exc:
        last_error = exc
        time.sleep(0.5)

print(f"server_timeout={url}")
if last_error is not None:
    print(f"last_error={last_error}", file=sys.stderr)
raise SystemExit(1)
PY

if [[ "${OPEN_BROWSER}" == true ]]; then
    python3 -m webbrowser -t "${URL}" || printf 'Falha ao abrir navegador automaticamente.\n' >&2
fi

wait "${STREAMLIT_PID}"
