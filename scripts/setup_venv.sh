#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${SCOUTPRAIA_VENV_DIR:-${ROOT_DIR}/.venv}"
REQUIREMENTS="${SCOUTPRAIA_REQUIREMENTS:-${ROOT_DIR}/requirements.txt}"
FORCE_RECREATE=false

usage() {
    cat <<EOF
Uso:
  scripts/setup_venv.sh [--force]

Opções:
  --force     Remove a .venv existente antes de recriar
  -h, --help  Mostra esta ajuda

Variáveis opcionais:
  SCOUTPRAIA_VENV_DIR         Caminho alternativo para a virtualenv
  SCOUTPRAIA_REQUIREMENTS     Caminho alternativo para o requirements.txt
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --force)
            FORCE_RECREATE=true
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

if [[ ! -f "${REQUIREMENTS}" ]]; then
    printf 'ERRO: requirements.txt não encontrado em %s\n' "${REQUIREMENTS}" >&2
    exit 1
fi

VIRTUALENV_BIN=""
for candidate in \
    "${HOME}/.local/bin/virtualenv" \
    "$(command -v virtualenv 2>/dev/null || true)"
do
    if [[ -x "${candidate}" ]]; then
        VIRTUALENV_BIN="${candidate}"
        break
    fi
done

if [[ -z "${VIRTUALENV_BIN}" ]]; then
    printf 'ERRO: virtualenv não encontrado.\n' >&2
    printf 'Instale com: pip3 install --user virtualenv\n' >&2
    exit 1
fi

if [[ -d "${VENV_DIR}" ]]; then
    if [[ "${FORCE_RECREATE}" != true ]]; then
        printf 'ERRO: a virtualenv já existe em %s\n' "${VENV_DIR}" >&2
        printf 'Use --force para remover e recriar.\n' >&2
        exit 1
    fi

    printf 'Removendo virtualenv existente em %s...\n' "${VENV_DIR}"
    rm -rf "${VENV_DIR}"
fi

printf 'Criando virtualenv em %s com %s...\n' "${VENV_DIR}" "${VIRTUALENV_BIN}"
"${VIRTUALENV_BIN}" "${VENV_DIR}"

printf 'Instalando dependências...\n'
"${VENV_DIR}/bin/pip" install -r "${REQUIREMENTS}"

printf '\nVirtualenv pronta. Para ativar manualmente:\n'
printf '  source %s/bin/activate\n' "${VENV_DIR}"
