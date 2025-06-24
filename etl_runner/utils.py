import os
import yaml


def update_readme_from_config(config_path, readme_path="README.md"):
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    # Ejemplo: actualiza la sección de fuentes en el README
    with open(readme_path, "r") as f:
        content = f.read()
    sources = "\n".join(f"- {src['id']}" for src in cfg.get("sources", []))
    new_content = (
        content.split("## Configuración:")[0]
        + f"## Configuración:\n\n### Fuentes:\n{sources}\n"
    )
    with open(readme_path, "w") as f:
        f.write(new_content)
    print("README actualizado con las fuentes del config.")


def open_or_update_issue(issue_path, message):
    # Simula la gestión de issues como un archivo plano
    if os.path.exists(issue_path):
        print(f"Issue ya existe: {issue_path}. Actualizando mensaje.")
    else:
        print(f"Creando nueva issue: {issue_path}")
    with open(issue_path, "w") as f:
        f.write(message)


def load_config(config_path):
    return yaml.safe_load(open(config_path))


def get_source_cfg(cfg, source_id):
    for s in cfg["sources"]:
        if s["id"] == source_id:
            return s
    raise ValueError(f"Fuente no encontrada: {source_id}")
