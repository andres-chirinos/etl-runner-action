import subprocess, nbformat, os, sys


def detect_kernel_from_notebook(nb_path):
    nb = nbformat.read(open(nb_path), as_version=4)
    kernelspec = nb.metadata.get("kernelspec", {})
    return kernelspec.get("name")


def run_notebook(path, params, out_dir, kernel=None):
    if kernel is None:
        kernel = detect_kernel_from_notebook(path)
        if not kernel:
            kernel = "python3"
            # raise ValueError("No kernel name found in notebook and no override provided.")
    args = ["papermill", path, os.path.join(out_dir, "out.ipynb"), "-k", kernel]
    for k, v in params.items():
        args += ["-p", k, str(v)]
    subprocess.check_call(args)


def run_script(path, params, out_dir):
    ext = path.split(".")[-1]
    cmd = []
    if ext == "py":
        cmd = ["python", path] + [f"--{k}={v}" for k, v in params.items()]
    elif ext == "R":
        cmd = ["Rscript", path] + [f"--args {k}={v}" for k, v in params.items()]
    elif ext == "jl":
        cmd = ["julia", path] + [f"--{k}={v}" for k, v in params.items()]
    elif ext == "sh":
        cmd = ["bash", path]
    else:
        raise RuntimeError("Formato no soportado")
    subprocess.check_call(cmd)


def install_dependencies(dep_file):
    import shutil

    if dep_file.endswith(".txt"):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", dep_file])
    elif dep_file.endswith(".yml") or dep_file.endswith(".yaml"):
        if not shutil.which("conda"):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "conda"])
        subprocess.check_call(["conda", "env", "update", "-f", dep_file])
    elif dep_file.endswith(".R"):
        if not shutil.which("Rscript"):
            subprocess.check_call(["apt-get", "update"])
            subprocess.check_call(["apt-get", "install", "-y", "r-base"])
        # Instala IRkernel si no existe
        if not os.path.exists("/usr/local/share/jupyter/kernels/ir"):
            subprocess.check_call(
                [
                    "R",
                    "-e",
                    "install.packages('IRkernel', repos='https://cloud.r-project.org/'); IRkernel::installspec()",
                ]
            )
        subprocess.check_call(["Rscript", dep_file])
    elif dep_file.endswith(".jl"):
        if not shutil.which("julia"):
            subprocess.check_call(["apt-get", "update"])
            subprocess.check_call(["apt-get", "install", "-y", "julia"])
        # Instala IJulia si no existe
        subprocess.check_call(
            ["julia", "-e", 'using Pkg; Pkg.add("IJulia"); using IJulia;']
        )
        subprocess.check_call(["julia", dep_file])
    # Puedes agregar más formatos según lo necesites
