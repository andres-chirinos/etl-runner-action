import sys, json, yaml, subprocess, os

def load_config(config_path):
    return yaml.safe_load(open(config_path))

def get_source_cfg(cfg, source_id):
    for s in cfg["sources"]:
        if s["id"] == source_id:
            return s
    raise ValueError(f"Fuente no encontrada: {source_id}")

def detect_kernel_from_notebook(nb_path):
    import nbformat
    nb = nbformat.read(open(nb_path), as_version=4)
    kernelspec = nb.metadata.get("kernelspec", {})
    return kernelspec.get("name")

def run_notebook(path, params, out_dir, kernel=None):
    if kernel is None:
        kernel = detect_kernel_from_notebook(path)
        if not kernel:
            kernel = "python3"
            #raise ValueError("No kernel name found in notebook and no override provided.")
    args = ["papermill", path, os.path.join(out_dir, "out.ipynb"), "-k", kernel]
    for k, v in params.items():
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

def install_dependencies(dep_file):
    if dep_file.endswith(".txt"):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", dep_file])
    elif dep_file.endswith(".yml") or dep_file.endswith(".yaml"):
        subprocess.check_call(["conda", "env", "update", "-f", dep_file])
    elif dep_file.endswith(".R"):
        subprocess.check_call(["Rscript", dep_file])
    # Puedes agregar más formatos según lo necesites

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="etl_config.yaml")
    p.add_argument("--source", required=True)
    p.add_argument("--out-dir", default="output")
    p.add_argument("--kernel", default=None, help="Kernel name override for notebook execution")
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
