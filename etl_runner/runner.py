from etl_runner.actions import UploadToDrive, PublishToKaggle
from etl_runner.utils import (
    update_readme_from_config,
    open_or_update_issue,
    load_config,
    get_source_cfg,
)
from etl_runner.kernel import run_notebook, run_script, install_dependencies
import sys, json, yaml, subprocess, os


def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--config", default="etl_config.yaml")
    p.add_argument("--source", required=True)
    p.add_argument("--out-dir", default="output")
    p.add_argument(
        "--kernel", default=None, help="Kernel name override for notebook execution"
    )
    args = p.parse_args()

    cfg = load_config(args.config)
    src = get_source_cfg(cfg, args.source)
    os.makedirs(args.out_dir, exist_ok=True)

    # Instala dependencias si están definidas
    dep_file = src.get("dependencies")
    if dep_file:
        install_dependencies(dep_file)

    path = os.path.join(src["path"], src["main"])
    params = src.get("params", {})
    kernel = args.kernel or src.get("kernel")
    if path.endswith(".ipynb"):
        run_notebook(path, params, args.out_dir, kernel=kernel)
    else:
        run_script(path, params, args.out_dir)


if __name__ == "__main__":
    main()
