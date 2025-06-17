FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl && \
    pip install --no-cache-dir papermill jupytext pyyaml ipykernel && \
    python -m ipykernel install --user && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .

ENTRYPOINT ["etl-runner"]