from scoutpraia.services.attack_no_shot_contract import (
    ATTACK_NO_SHOT_EVENTS,
    ATTACK_NO_SHOT_RESULT,
    AttackNoShotInput,
    IntraObserverMarking,
    evaluate_intra_observer_consistency,
    validate_attack_no_shot_entry,
)


def test_attack_no_shot_has_seven_events_with_auto_result():
    assert len(ATTACK_NO_SHOT_EVENTS) == 7
    for event in ATTACK_NO_SHOT_EVENTS.values():
        assert event.result_possession_auto == ATTACK_NO_SHOT_RESULT
        assert event.validation_source
        assert event.ui_type


def test_technical_error_unforced_passes_with_required_fields_and_subtype():
    result = validate_attack_no_shot_entry(
        AttackNoShotInput(
            event_code="technical_error_unforced",
            athlete_id="athlete-1",
            court_zone="central",
            position_code="central",
            technical_error_subtype="pass_error",
        )
    )
    assert result.ok is True
    assert result.result_possession_auto == "lost_possession_no_shot"
    assert result.points == 0


def test_technical_error_unforced_fails_without_technical_subtype():
    result = validate_attack_no_shot_entry(
        AttackNoShotInput(
            event_code="technical_error_unforced",
            athlete_id="athlete-1",
            court_zone="central",
            position_code="central",
        )
    )
    assert result.ok is False
    assert "technical_error_unforced exige subtipo_erro_tecnico válido." in result.errors


def test_technical_error_forced_derives_defense_forced_error():
    result = validate_attack_no_shot_entry(
        AttackNoShotInput(
            event_code="technical_error_forced",
            athlete_id="athlete-1",
            court_zone="lateral-direita",
            position_code="lateral",
            technical_error_subtype="reception_error",
        )
    )
    assert result.ok is True
    assert result.defense_forced_error is True


def test_passive_play_turnover_requires_passive_subtype():
    result = validate_attack_no_shot_entry(
        AttackNoShotInput(event_code="passive_play_turnover", system_code="AT_4_0")
    )
    assert result.ok is False
    assert "passive_play_turnover exige subtipo_jogo_passivo válido." in result.errors


def test_passive_play_turnover_passes_with_system_and_subtype():
    result = validate_attack_no_shot_entry(
        AttackNoShotInput(
            event_code="passive_play_turnover",
            system_code="AT_4_0",
            passive_play_subtype="passive_fifth_pass_no_shot",
        )
    )
    assert result.ok is True


def test_bad_substitution_requires_substitution_subtype():
    result = validate_attack_no_shot_entry(
        AttackNoShotInput(event_code="bad_substitution_attack", system_code="AT_3_1")
    )
    assert result.ok is False
    assert "bad_substitution_attack exige subtipo_erro_substituicao válido." in result.errors


def test_substitution_violation_other_requires_review_marker():
    result = validate_attack_no_shot_entry(
        AttackNoShotInput(
            event_code="bad_substitution_attack",
            system_code="AT_3_1",
            substitution_error_subtype="substitution_violation_other",
        )
    )
    assert result.ok is False
    assert "bad_substitution_attack exige review_marker = Sim nesta condição." in result.errors


def test_turnover_unclassified_requires_review_marker():
    result = validate_attack_no_shot_entry(
        AttackNoShotInput(event_code="turnover_unclassified")
    )
    assert result.ok is False
    assert "turnover_unclassified exige review_marker = Sim nesta condição." in result.errors


def test_turnover_unclassified_passes_with_review_marker():
    result = validate_attack_no_shot_entry(
        AttackNoShotInput(event_code="turnover_unclassified", review_marker=True)
    )
    assert result.ok is True
    assert result.review_marker is True


def test_event_outside_module_is_blocked():
    result = validate_attack_no_shot_entry(AttackNoShotInput(event_code="shot_attempt"))
    assert result.ok is False
    assert result.errors[0].startswith("Evento fora do módulo Ataque sem Finalização v1.0")


def test_finish_goal_zone_and_points_are_forbidden():
    result = validate_attack_no_shot_entry(
        AttackNoShotInput(
            event_code="offensive_foul",
            athlete_id="athlete-1",
            court_zone="central",
            position_code="central",
            finish_type_code="GIRO",
            goal_zone="alto-direito",
            points=2,
        )
    )
    assert result.ok is False
    assert "tipo_finalizacao_code não é permitido." in result.errors
    assert "zona_gol não é permitida." in result.errors
    assert "pontos_jogada deve ser 0." in result.errors


def test_intra_observer_consistency_passes_at_or_above_85_percent():
    result = evaluate_intra_observer_consistency(
        [
            IntraObserverMarking("L1", "technical_error_unforced", "technical_error_unforced"),
            IntraObserverMarking("L2", "technical_error_forced", "technical_error_forced"),
            IntraObserverMarking("L3", "offensive_foul", "offensive_foul"),
            IntraObserverMarking("L4", "passive_play_turnover", "passive_play_turnover"),
            IntraObserverMarking("L5", "bad_substitution_attack", "bad_substitution_attack"),
            IntraObserverMarking("L6", "turnover_unclassified", "turnover_unclassified"),
            IntraObserverMarking("L7", "goal_area_invasion_attack", "goal_area_invasion_attack"),
        ]
    )
    assert result["approved"] is True
    assert result["requires_dictionary_review"] is False
    assert result["consistency_percent"] == 100.0


def test_intra_observer_consistency_fails_below_85_percent():
    result = evaluate_intra_observer_consistency(
        [
            IntraObserverMarking("L1", "technical_error_unforced", "technical_error_forced"),
            IntraObserverMarking("L2", "technical_error_forced", "technical_error_forced"),
            IntraObserverMarking("L3", "offensive_foul", "offensive_foul"),
            IntraObserverMarking("L4", "passive_play_turnover", "turnover_unclassified"),
        ]
    )
    assert result["approved"] is False
    assert result["requires_dictionary_review"] is True
    assert result["divergent_lance_ids"] == ["L1", "L4"]
