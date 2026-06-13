from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FieldRelationship:
    relationship_id: str
    sheet_name: str
    field_code: str
    field_type: str
    references_sheet: str
    reference_kind: str
    references_key: str
    relationship_type: str
    ui_component: str
    sqlite_model: str
    sqlite_column_type: str
    allowed_values_source: str
    free_text_allowed: bool
    required_when: str
    blocking_rule: str
    validation_source: str
    agent_action: str
    module_id: str
    notes: str


SHEET_MAP_NAMES = {
    "EVENTOS",
    "MODULE_INDEX",
    "SHEET_MAP",
    "SOURCE_REGISTER",
    "FIELD_DICTIONARY_GLOBAL",
    "RESULT_DOMAIN_GLOBAL",
    "CROSS_MODULE_BOUNDARIES",
    "ZONAS_GOL",
    "ZONAS_QUADRA",
    "SCORER_ROLES",
    "POSIÇÕES",
    "SISTEMAS",
    "CAMPOS_AUXILIARES_GOLEIRA",
    "CAMPOS_AUXILIARES_FINALIZACAO",
    "CAMPOS_AUXILIARES_TRANSICAO",
    "RESULTADOS_GOLEIRA",
}

RUNTIME_TABLES = {"ATHLETES", "EVENT_LOG"}
FUTURE_CONTRACTS = {"VIDEO_ASSET"}
ALLOWED_REFERENCE_KINDS = {
    "sheet",
    "runtime_table",
    "inline_enum",
    "future_contract",
    "computed",
}
CLOSED_UI_COMPONENTS = {
    "selectbox",
    "selectbox_filtered",
    "radio_or_selectbox",
    "multi_select",
    "computed",
    "computed_or_input",
}

FIELD_RELATIONSHIPS = (
    FieldRelationship("REL-GK-001", "CAMPOS_AUXILIARES_GOLEIRA", "goalkeeper_id", "entity_ref", "ATHLETES", "runtime_table", "athlete_id", "many_to_one", "selectbox", "Athlete", "INTEGER FK", "ATHLETES.athlete_id", False, "Obrigatório em goalkeeper_save, goalkeeper_goal_allowed e goalkeeper_specialist_exchange", "block_if event_code in [goalkeeper_save, goalkeeper_goal_allowed, goalkeeper_specialist_exchange] and empty", "CAMPOS_AUXILIARES_GOLEIRA + ATHLETES", "gerar selectbox de atleta; criar FK; domínio fechado", "goalkeeper_v1", "Identifica atleta em função de goleira no evento."),
    FieldRelationship("REL-GK-002", "CAMPOS_AUXILIARES_GOLEIRA", "linked_finalization_id", "event_ref", "EVENT_LOG", "runtime_table", "event_id", "many_to_one_filtered", "selectbox_filtered", "EventLog", "INTEGER FK", "EVENT_LOG.event_id where module_id=finalization_v1", False, "Obrigatório em goalkeeper_save e goalkeeper_goal_allowed", "block_if event_code in [goalkeeper_save, goalkeeper_goal_allowed] and empty; block_if event_code=goalkeeper_specialist_exchange and not empty", "CAMPOS_AUXILIARES_GOLEIRA + EVENT_LOG", "gerar selectbox filtrado por finalização; criar FK; bloquear troca goleira-especialista com finalização vinculada", "goalkeeper_v1", "Vincula defesa/gol sofrido à finalização que gerou a ação."),
    FieldRelationship("REL-GK-003", "CAMPOS_AUXILIARES_GOLEIRA", "linked_finalization_event_code", "enum_ref", "EVENTOS", "sheet", "event_code", "many_to_one_filtered", "selectbox", "EventDefinition", "TEXT FK", "EVENTOS.event_code filtered by finalization_v1", False, "Obrigatório em goalkeeper_save e goalkeeper_goal_allowed", "block_if value not in [simple_shot, spin_shot, inflight_shot, goalkeeper_shot, six_metre_throw]; block_if value=shootout_attempt", "CAMPOS_AUXILIARES_GOLEIRA + EVENTOS", "gerar selectbox de eventos de finalização permitidos; bloquear shootout_attempt", "goalkeeper_v1", "Inclui six_metre_throw para medir eficiência da goleira contra 6m."),
    FieldRelationship("REL-GK-004", "CAMPOS_AUXILIARES_GOLEIRA", "result_goalkeeper", "enum_ref", "RESULTADOS_GOLEIRA", "sheet", "result_code", "many_to_one", "selectbox", "GoalkeeperResult", "TEXT FK/ENUM", "RESULTADOS_GOLEIRA.result_code", False, "Obrigatório em goalkeeper_save e goalkeeper_goal_allowed", "block_if empty; block_if value not in RESULTADOS_GOLEIRA; block_if event_code=goalkeeper_save and value=goal_allowed; block_if event_code=goalkeeper_goal_allowed and value != goal_allowed", "CAMPOS_AUXILIARES_GOLEIRA + RESULTADOS_GOLEIRA", "gerar selectbox; criar enum/FK; bloquear resultado incompatível com evento", "goalkeeper_v1", "Classifica defesa ou gol sofrido sem calcular pontos."),
    FieldRelationship("REL-GK-005", "CAMPOS_AUXILIARES_GOLEIRA", "save_type", "enum_inline", "INLINE", "inline_enum", "value", "closed_enum", "selectbox", "GoalkeeperSaveType", "TEXT ENUM", "reaction_save; positioning_save; foot_save; hand_save; body_save; spread_save; other_review", False, "Obrigatório em goalkeeper_save", "block_if empty; block_if other_review and review_marker != Sim", "CAMPOS_AUXILIARES_GOLEIRA", "gerar enum/selectbox; não criar eventos separados por parte do corpo", "goalkeeper_v1", "Tipo observável da defesa."),
    FieldRelationship("REL-GK-016", "CAMPOS_AUXILIARES_GOLEIRA", "specialist_id", "entity_ref", "ATHLETES", "runtime_table", "athlete_id", "many_to_one", "selectbox", "Athlete", "INTEGER FK", "ATHLETES.athlete_id", False, "Obrigatório em goalkeeper_specialist_exchange", "block_if event_code=goalkeeper_specialist_exchange and empty", "CAMPOS_AUXILIARES_GOLEIRA + ATHLETES", "gerar selectbox de atleta; criar FK", "goalkeeper_v1", "Especialista vinculada à troca com goleira."),
    FieldRelationship("REL-FIN-001", "CAMPOS_AUXILIARES_FINALIZACAO", "goal_zone", "enum_ref", "ZONAS_GOL", "sheet", "zone_id", "many_to_one", "selectbox", "ZonasGol", "TEXT FK/ENUM", "ZONAS_GOL.zone_id", False, "Quando trajetória ao gol for visível ou inferível com segurança", "block_if value not in ZONAS_GOL; block_if trajectory_visible=Não and goal_zone not empty", "CAMPOS_AUXILIARES_FINALIZACAO + ZONAS_GOL", "gerar selectbox de ZONAS_GOL; domínio fechado", "finalization_v1", "Zona do gol é domínio fechado."),
    FieldRelationship("REL-FIN-002", "CAMPOS_AUXILIARES_FINALIZACAO", "court_location", "enum_ref", "ZONAS_QUADRA", "sheet", "zone_id", "many_to_one", "selectbox", "ZonasQuadra", "TEXT FK/ENUM", "ZONAS_QUADRA.zone_id", False, "Quando localização da finalização for registrada", "block_if value not in ZONAS_QUADRA", "CAMPOS_AUXILIARES_FINALIZACAO + ZONAS_QUADRA", "gerar selectbox de ZONAS_QUADRA; domínio fechado", "finalization_v1", "Zona da quadra é domínio espacial fechado."),
    FieldRelationship("REL-FIN-003", "CAMPOS_AUXILIARES_FINALIZACAO", "scorer_role", "enum_ref", "SCORER_ROLES", "sheet", "role_code", "many_to_one", "selectbox", "ScorerRole", "TEXT FK/ENUM", "SCORER_ROLES.role_code", False, "Quando houver finalização", "block_if value not in SCORER_ROLES", "CAMPOS_AUXILIARES_FINALIZACAO + SCORER_ROLES", "gerar selectbox de papel da finalizadora; bloquear especialista como posição fixa", "finalization_v1", "Especialista é papel dinâmico, não posição."),
    FieldRelationship("REL-TR-001", "CAMPOS_AUXILIARES_TRANSICAO", "trigger_event_id", "event_ref", "EVENT_LOG", "runtime_table", "event_id", "many_to_one_filtered", "selectbox_filtered", "EventLog", "INTEGER FK", "EVENT_LOG.event_id", False, "Obrigatório quando gatilho vier de evento registrado", "block_if trigger_event_required and empty", "CAMPOS_AUXILIARES_TRANSICAO + EVENT_LOG", "gerar selectbox filtrado por eventos permitidos de gatilho", "transition_v1", "Vincula transição ao evento que iniciou a cadeia."),
    FieldRelationship("REL-TR-002", "CAMPOS_AUXILIARES_TRANSICAO", "terminal_event_id", "event_ref", "EVENT_LOG", "runtime_table", "event_id", "many_to_one_filtered", "selectbox_filtered", "EventLog", "INTEGER FK", "EVENT_LOG.event_id", False, "Obrigatório quando houver evento terminal", "block_if result_transition requires terminal_event and empty", "CAMPOS_AUXILIARES_TRANSICAO + EVENT_LOG", "gerar selectbox filtrado por finalization_v1 ou attack_no_shot_v1 conforme resultado", "transition_v1", "Vincula transição ao evento terminal."),
    FieldRelationship("REL-TR-003", "CAMPOS_AUXILIARES_TRANSICAO", "transition_start_zone", "enum_ref", "ZONAS_QUADRA", "sheet", "zone_id", "many_to_one", "selectbox", "ZonasQuadra", "TEXT FK/ENUM", "ZONAS_QUADRA.zone_id", False, "Obrigatório em transition_sequence", "block_if value not in ZONAS_QUADRA", "CAMPOS_AUXILIARES_TRANSICAO + ZONAS_QUADRA", "gerar selectbox de zona inicial", "transition_v1", "Zona onde inicia a cadeia de transição."),
    FieldRelationship("REL-GLOBAL-001", "EVENTOS", "module_id", "enum_ref", "MODULE_INDEX", "sheet", "module_id", "many_to_one", "selectbox", "ModuleIndex", "TEXT FK", "MODULE_INDEX.module_id", False, "Obrigatório em evento técnico", "block_if module_id not in MODULE_INDEX", "EVENTOS + MODULE_INDEX", "gerar FK; filtrar EVENTOS por module_id antes de gerar UI", "global", "Relacionamento central entre evento e módulo."),
    FieldRelationship("REL-GLOBAL-004", "SOURCE_REGISTER", "related_sheets", "enum_ref", "SHEET_MAP", "sheet", "sheet_name", "many_to_many_semicolon_list", "multi_select", "SheetMap", "TEXT LIST FK", "SHEET_MAP.sheet_name", False, "Quando fonte se relacionar a abas", "block_if any related_sheet not in SHEET_MAP", "SOURCE_REGISTER + SHEET_MAP", "validar abas relacionadas contra SHEET_MAP", "global", "Evita referências a abas inexistentes."),
    FieldRelationship("REL-CV-001", "EVENT_LOG", "timestamp_ms", "video_time", "VIDEO_ASSET", "future_contract", "timestamp_ms", "many_to_one_time", "computed_or_input", "VideoTimestamp", "INTEGER", "video timeline", False, "Obrigatório em todo evento registrado no vídeo", "block_if empty; block_if timestamp_ms < 0", "future_EVENT_LOG_contract", "criar coluna INTEGER timestamp_ms; usar para ordenação temporal e ground truth futuro", "global", "Preparação para vídeo/action spotting."),
    FieldRelationship("REL-CV-002", "EVENT_LOG", "frame_index", "video_frame", "VIDEO_ASSET", "future_contract", "frame_index", "many_to_one_time", "computed", "VideoFrame", "INTEGER", "computed_from timestamp_ms and fps", False, "Obrigatório quando vídeo/fps disponíveis", "block_if fps available and frame_index empty", "future_EVENT_LOG_contract", "criar coluna INTEGER frame_index calculada por fps; não armazenar apenas texto", "global", "Compatível com action spotting/visão computacional."),
    FieldRelationship("REL-CV-003", "EVENT_LOG", "action_visibility", "enum_inline", "INLINE", "inline_enum", "value", "closed_enum", "selectbox", "ActionVisibility", "TEXT ENUM", "visible; partially_visible; occluded; inferred_review", False, "Obrigatório quando evento vier de vídeo", "block_if inferred_review and review_marker != Sim", "future_EVENT_LOG_contract", "gerar enum de visibilidade; mapear trajectory_visible quando aplicável", "global", "Base para qualidade de ground truth e futura visão computacional."),
)


def test_relationship_ids_are_unique_and_nonempty() -> None:
    ids = [row.relationship_id for row in FIELD_RELATIONSHIPS]
    assert all(ids)
    assert len(ids) == len(set(ids))


def test_reference_kind_is_explicit_and_valid() -> None:
    for row in FIELD_RELATIONSHIPS:
        assert row.reference_kind in ALLOWED_REFERENCE_KINDS
        assert row.references_sheet
        assert row.references_key


def test_sheet_references_point_to_existing_sheet_map_entries() -> None:
    for row in FIELD_RELATIONSHIPS:
        if row.reference_kind == "sheet":
            assert row.references_sheet in SHEET_MAP_NAMES


def test_runtime_tables_and_future_contracts_do_not_pretend_to_be_sheets() -> None:
    for row in FIELD_RELATIONSHIPS:
        if row.references_sheet in RUNTIME_TABLES:
            assert row.reference_kind == "runtime_table"
        if row.references_sheet in FUTURE_CONTRACTS:
            assert row.reference_kind == "future_contract"


def test_inline_enums_use_closed_values_not_sheet_references() -> None:
    for row in FIELD_RELATIONSHIPS:
        if row.reference_kind == "inline_enum":
            assert row.references_sheet == "INLINE"
            assert row.references_key == "value"
            assert ";" in row.allowed_values_source
            assert row.ui_component in CLOSED_UI_COMPONENTS


def test_false_free_text_forces_closed_ui_component() -> None:
    for row in FIELD_RELATIONSHIPS:
        if not row.free_text_allowed:
            assert row.ui_component in CLOSED_UI_COMPONENTS
            assert "text_input" not in row.agent_action


def test_event_refs_are_not_modeled_as_free_text() -> None:
    event_refs = [row for row in FIELD_RELATIONSHIPS if row.field_type == "event_ref"]
    assert event_refs
    for row in event_refs:
        assert row.reference_kind == "runtime_table"
        assert row.references_sheet == "EVENT_LOG"
        assert row.ui_component == "selectbox_filtered"
        assert row.sqlite_column_type == "INTEGER FK"


def test_video_future_readiness_stays_blocked_as_future_contract() -> None:
    video_rows = [row for row in FIELD_RELATIONSHIPS if row.relationship_id.startswith("REL-CV-")]
    assert {row.field_code for row in video_rows} == {
        "timestamp_ms",
        "frame_index",
        "action_visibility",
    }
    assert {row.sheet_name for row in video_rows} == {"EVENT_LOG"}
    assert {row.reference_kind for row in video_rows} == {"future_contract", "inline_enum"}
    assert all(row.module_id == "global" for row in video_rows)


def test_required_structural_actions_are_not_declared_as_operational_imports() -> None:
    for row in FIELD_RELATIONSHIPS:
        assert "importar_v1" not in row.agent_action
        assert row.module_id in {
            "goalkeeper_v1",
            "finalization_v1",
            "transition_v1",
            "global",
        }
        