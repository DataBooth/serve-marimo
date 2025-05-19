from fastapi import FastAPI
from pathlib import Path
import marimo

# Absolute path to the notebooks directory, relative to this file
notebooks_dir = Path(__file__).parent / "notebooks"

builder = marimo.create_asgi_app().with_dynamic_directory(
    path="/notebooks", directory=str(notebooks_dir)
)
marimo_app = builder.build()

app = FastAPI()


@app.get("/")
def root():
    notebooks = [f.name for f in notebooks_dir.glob("*.py")]
    return {
        "message": "Go to /notebooks/{notebook_name} to view a notebook.",
        "notebooks": notebooks,
    }


app.mount("/", marimo_app)
