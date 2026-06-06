from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


def render_report(template_dir: Path, template_name: str, payload: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_name)
    return template.render(**payload)
