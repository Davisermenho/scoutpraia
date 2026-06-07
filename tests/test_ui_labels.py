from scoutpraia.pages import reports as reports_page
from scoutpraia.ui_labels import (
    column_label,
    direction_label,
    display_value_label,
    event_type_label,
    kpi_label,
    report_type_label,
    team_side_label,
    zone_label,
)


def test_core_ui_labels_translate_known_internal_values() -> None:
    assert event_type_label("shot_attempt") == "Tentativa de finalização"
    assert event_type_label("goal_scored") == "Gol marcado"
    assert team_side_label("team") == "Equipe"
    assert team_side_label("opponent") == "Adversária"
    assert zone_label("left_wing") == "Ponta esquerda"
    assert direction_label("left") == "Esquerda"
    assert report_type_label("opponent") == "adversária"


def test_display_value_label_translates_known_values_and_preserves_unknowns() -> None:
    assert display_value_label("team") == "Equipe"
    assert display_value_label("right") == "Direita"
    assert display_value_label("center") == "Centro"
    assert display_value_label("custom_value") == "custom_value"


def test_kpi_preview_rows_use_portuguese_metric_labels() -> None:
    rows = reports_page._kpi_preview_rows(
        {
            "points_total": 5,
            "offensive_conversion_rate": 0.75,
            "preferred_attack_side": "left",
            "critical_warnings": ["alerta"],
        }
    )

    assert rows == [
        {column_label("metric"): kpi_label("points_total"), column_label("value"): "5"},
        {
            column_label("metric"): kpi_label("offensive_conversion_rate"),
            column_label("value"): "0.75",
        },
        {
            column_label("metric"): kpi_label("preferred_attack_side"),
            column_label("value"): "Esquerda",
        },
    ]
