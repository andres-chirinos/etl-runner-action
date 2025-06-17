# ETL Runner

Ejecuta pipelines ETL multiproceso (notebooks/scripts) definidos en un archivo `etl_config.yaml`.

## Características
- Soporte para notebooks (`.ipynb`) y scripts (`.py`, `.R`, `.jl`, `.sh`).
- Ejecución multiproceso de fuentes definidas en YAML.
- Uso como acción de GitHub, CLI o Docker.

## Instalación

### Docker
```bash
docker pull ghcr.io/andres-chirinos/etl-runner:latest
```

### Python (local)
```bash
pip install .
```

## Uso

### CLI
```bash
etl-runner --source <id_fuente> --config <ruta/etl_config.yaml> --out-dir <directorio_salida>
```

### Docker
```bash
docker run --rm -v "$PWD:/app" ghcr.io/andres-chirinos/etl-runner:latest \
  --source <id_fuente> --config <ruta/etl_config.yaml> --out-dir <directorio_salida>
```

### GitHub Action
```yaml
- name: Ejecutar ETL Runner
  uses: andres-chirinos/etl-runner-action@v1
  with:
    source: <id_fuente>
    config-path: etl_config.yaml
    out-dir: output
```

## Configuración: etl_config.yaml
Ejemplo:
```yaml
sources:
  - id: api1
    params:
      url: "https://api1.com/data"
      output_path: "data/api1.csv"
  - id: web2
    params:
      selector: ".value"
      output_path: "data/web2.json"
```

## Ejemplo de workflow (GitHub Actions)
Ver `example/example1.yml`:
```yaml
jobs:
  etl:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        source: [api1, web2, archivo3]
    steps:
      - uses: actions/checkout@v4
      - name: Ejecutar ETL Runner
        uses: andres-chirinos/etl-runner-action@v1
        with:
          source: ${{ matrix.source }}
          config-path: etl_config.yaml
          out-dir: outputs/${{ matrix.source }}
      - name: Subir resultados
        uses: actions/upload-artifact@v4
        with:
          name: resultado-${{ matrix.source }}
          path: outputs/${{ matrix.source }}
```

## Licencia
MIT
