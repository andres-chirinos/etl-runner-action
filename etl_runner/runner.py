import sys, json, yaml, subprocess, os

def load_config(config_path):
    return yaml.safe_load(open(config_path))

def get_source_cfg(cfg, source_id):
    for s in cfg["sources"]:
        if s["id"] == source_id:
            return s
    raise ValueError(f"Fuente no encontrada: {source_id}")

def run_notebook(path, params, out_dir):
    args = ["papermill", path, os.path.join(out_dir,"out.ipynb")]
    for k,v in params.items():
        args += ["-p", k, str(v)]
    subprocess.check_call(args)

def run_script(path, params, out_dir):
    ext = path.split('.')[-1]
    cmd = []
    if ext == "py":
        cmd = ["python", path] + [f"--{k}={v}" for k,v in params.items()]
    elif ext == "R":
        cmd = ["Rscript", path] + [f"--args {k}={v}" for k,v in params.items()]
    elif ext == "jl":
        cmd = ["julia", path] + [f"--{k}={v}" for k,v in params.items()]
    elif ext == "sh":
        cmd = ["bash", path]
    else:
        raise RuntimeError("Formato no soportado")
    subprocess.check_call(cmd)

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="etl_config.yaml")
    p.add_argument("--source", required=True)
    p.add_argument("--out-dir", default="output")
    args = p.parse_args()

    cfg = load_config(args.config)
    src = get_source_cfg(cfg, args.source)
    os.makedirs(args.out_dir, exist_ok=True)

    path = os.path.join(src["path"], src["main"])
    params = src.get("params", {})
    if path.endswith(".ipynb"):
        run_notebook(path, params, args.out_dir)
    else:
        run_script(path, params, args.out_dir)

if __name__ == "__main__":
    main()
