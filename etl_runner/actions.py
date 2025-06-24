import os


class OutputAction:
    def run(self, files, config):
        raise NotImplementedError("Implementa este método en subclases.")


class UploadToDrive(OutputAction):
    def run(self, files, config):
        print(f"Subiendo {files} a Google Drive (simulado)")


class PublishToKaggle(OutputAction):
    def run(self, files, config):
        print(f"Publicando {files} en Kaggle (simulado)")
