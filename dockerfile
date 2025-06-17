FROM python:3.8

#USER root
#RUN apt-get update && apt-get install -y \
#        python3-dev \
        #build-essential \
        #r-base \
        #curl \
        #git \ #&& rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir papermill jupytext pyyaml ipykernel 
# && \
        # Rscript -e "install.packages('IRkernel', repos='https://cloud.r-project.org/'); IRkernel::installspec()"

WORKDIR /app
COPY . /app
RUN pip3 install --no-cache-dir .

ENTRYPOINT ["etl-runner"]