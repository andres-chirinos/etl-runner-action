from setuptools import setup, find_packages

setup(
    name="etl-runner",
    version="0.1.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["etl-runner=runner.runner:main"]},
    install_requires=[
        "pyyaml", "papermill", "jupytext"
    ]
)
