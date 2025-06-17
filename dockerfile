# Dockerfile
FROM ubuntu:22.04

# Instalar Python, R, Julia, utilidades
RUN apt-get update && \
    apt-get install -y python3 python3-pip r-base julia curl git && \
    pip3 install --no-cache-dir papermill jupytext pyyaml

# Instalar kernels de Jupyter
RUN pip3 install ipykernel && \
    Rscript -e "install.packages('IRkernel', repos='https://cloud.r-project.org/'); IRkernel::installspec()" && \
    julia -e 'import Pkg; Pkg.add("IJulia")'

# Copiar la librería
WORKDIR /app
COPY . /app
RUN pip3 install --no-cache-dir .

ENTRYPOINT ["etl-runner"]
