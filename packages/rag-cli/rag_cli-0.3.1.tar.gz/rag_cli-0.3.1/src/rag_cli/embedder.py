import json
import logging
import sys
from typing import Optional, TextIO

from ollama import Client


def run_embedder(ollama_url: str, text: Optional[str] = None, file: Optional[TextIO] = None):
    """Runs the embedder."""

    if text is None and file is None:
        raise ValueError("Either text or file must be provided.")

    logging.basicConfig(level=logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(handler)

    logger.info("Connecting to Ollama")
    client = Client(host=ollama_url)
    logger.info("Connected to Ollama")

    logger.info("Embedding text")

    if text is None and file is not None:
        text_to_use = file.read().strip()
    elif text is not None and file is None:
        text_to_use = text
    else:
        raise RuntimeError("This should not happen!")

    embeddings = client.embeddings(
        model="nomic-embed-text:v1.5",
        prompt=text_to_use,
    )
    embeddings["text"] = text_to_use  # type: ignore

    logger.info("Text embedded")

    sys.stdout.write(json.dumps(embeddings))
