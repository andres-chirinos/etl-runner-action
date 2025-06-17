FROM python:3.8

RUN apt-get update && \
    apt-get install -y r-base julia && \
    pip install --no-cache-dir papermill jupytext pyyaml ipykernel && \
    python -m ipykernel install --user && \
    R -e "install.packages('IRkernel', repos='https://cloud.r-project.org/'); IRkernel::installspec()" && \
    julia -e 'using Pkg; Pkg.add("IJulia"); using IJulia;'

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .

ENTRYPOINT ["etl-runner"]