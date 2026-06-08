#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${SCOUTPRAIA_PORT:-8516}"
OPEN_BROWSER=true
BROWSER_OPEN_CMD="${SCOUTPRAIA_BROWSER_OPEN_CMD:-}"

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

port_in_use() {
    python3 - "${1}" <<'PY'
import socket
import sys

port = int(sys.argv[1])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.settimeout(0.2)
    occupied = sock.connect_ex(("127.0.0.1", port)) == 0
raise SystemExit(0 if occupied else 1)
PY
}

open_browser_url() {
    local url="${1}"

    if [[ -n "${BROWSER_OPEN_CMD}" ]]; then
        "${BROWSER_OPEN_CMD}" "${url}"
        return $?
    fi

    case "$(uname -s)" in
        Darwin)
            if command -v open >/dev/null 2>&1; then
                open "${url}"
                return $?
            fi
            ;;
        Linux)
            if command -v xdg-open >/dev/null 2>&1; then
                xdg-open "${url}"
                return $?
            fi
            if command -v gio >/dev/null 2>&1; then
                gio open "${url}"
                return $?
            fi
            if command -v sensible-browser >/dev/null 2>&1; then
                sensible-browser "${url}"
                return $?
            fi
            ;;
    esac

    return 1
}

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

if port_in_use "${PORT}"; then
    printf 'Porta já está em uso: %s\n' "${PORT}" >&2
    exit 1
fi

streamlit run app.py --server.headless true --server.port "${PORT}" &
STREAMLIT_PID=$!

python3 - "${URL}" "${STREAMLIT_PID}" <<'PY'
import os
import sys
import time
from urllib.request import urlopen

url = sys.argv[1]
pid = int(sys.argv[2])
deadline = time.time() + 60
last_error = None

def process_alive(process_id: int) -> bool:
    try:
        os.kill(process_id, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True

while time.time() < deadline:
    if not process_alive(pid):
        print("streamlit_process_exited_before_ready", file=sys.stderr)
        raise SystemExit(1)
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
    if ! open_browser_url "${URL}"; then
        printf 'Falha ao abrir navegador automaticamente. Abra manualmente: %s\n' "${URL}" >&2
    fi
fi

wait "${STREAMLIT_PID}"
