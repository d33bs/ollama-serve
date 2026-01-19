"""
Command-line interface for ollama-serve.
"""

import fire

from .main import show_message


def trigger() -> None:
    """
    Entry point for the `ollama-serve` console script.
    """

    fire.Fire({"show_message": show_message})
