#!/usr/bin/env bash
set -euo pipefail

printf '== ScoutPraia current-state verification ==\n'
printf 'date_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf 'cwd=%s\n' "$(pwd)"
printf 'git_branch=%s\n' "$(git branch --show-current 2>/dev/null || echo none)"
printf 'git_head=%s\n' "$(git rev-parse --short HEAD 2>/dev/null || echo none)"
printf '\n== Required MVP doc checks ==\n'
player_id_count=$(sed -n '/### `match_roster`/,/### `sets`/p' MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md | grep -c -- '- `player_id`')
kpi_title_count=$(grep -c '^## 13\.1 KPIs coletivos$' MVP_TECNICO_ANALISE_VIDEOS_HANDEBOL_PRAIA.md)
printf 'match_roster_player_id_count=%s\n' "$player_id_count"
printf 'kpi_13_1_title_count=%s\n' "$kpi_title_count"
test "$player_id_count" -eq 1
test "$kpi_title_count" -eq 1

printf '\n== Python import ==\n'
python3 -c "import scoutpraia; print(scoutpraia.__doc__)"

printf '\n== Database init and taxonomy seed ==\n'
python3 -m scoutpraia.core.database
python3 - <<'PY'
from sqlmodel import Session, select
from scoutpraia.core.database import engine
from scoutpraia.models.taxonomy import EventDefinition, TaxonomyVersion
from scoutpraia.services.taxonomy_service import EVENT_DEFINITIONS, TAXONOMY_NAME

with Session(engine) as session:
    taxonomy = session.exec(select(TaxonomyVersion).where(TaxonomyVersion.name == TAXONOMY_NAME)).first()
    if taxonomy is None:
        raise SystemExit('taxonomy_missing')
    definitions = session.exec(select(EventDefinition).where(EventDefinition.taxonomy_version_id == taxonomy.id)).all()
    print(f'taxonomy={taxonomy.name}')
    print(f'taxonomy_status={taxonomy.status}')
    print(f'event_definitions={len(definitions)}')
    print(f'expected_event_definitions={len(EVENT_DEFINITIONS)}')
    if len(definitions) != len(EVENT_DEFINITIONS):
        raise SystemExit('definition_count_mismatch')
PY

printf '\n== Tests ==\n'
python3 -m pytest

printf '\n== Git whitespace check ==\n'
git diff --check

printf '\n== Working tree summary ==\n'
git status --short
