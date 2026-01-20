"""
Core helpers for interacting with the Ollama server.
"""

import http.client
import json
import shutil
import subprocess
import warnings

HTTP_ERROR_STATUS = 400


def is_ollama_running(
    host: str = "127.0.0.1",
    port: int = 11434,
    timeout: float = 0.2,
) -> bool:
    """
    Return True when an Ollama server responds on the given host/port.

    We use a lightweight HTTP request to the tags endpoint to avoid
    false positives when another service is bound to the same port.

    Args:
        host: Hostname or IP address to probe.
        port: Port to probe.
        timeout: Socket timeout in seconds.

    Returns:
        True when the Ollama tags endpoint responds; otherwise False.
    """

    conn: http.client.HTTPConnection | None = None
    try:
        conn = http.client.HTTPConnection(host, port, timeout=timeout)
        conn.request("GET", "/api/tags")
        response = conn.getresponse()
        if response.status >= HTTP_ERROR_STATUS:
            return False
        payload = response.read()
        data = json.loads(payload)
        return isinstance(data, dict) and "models" in data
    except (OSError, http.client.HTTPException, json.JSONDecodeError):
        return False
    finally:
        if conn is not None:
            conn.close()


def run_ollama_server(
    host: str = "127.0.0.1",
    port: int = 11434,
    timeout: float = 0.2,
) -> bool:
    """
    Start the Ollama server when it is not already running.

    Args:
        host: Hostname or IP address to probe.
        port: Port to probe.
        timeout: Socket timeout in seconds.

    Returns:
        True when the server is already running or successfully started;
        False when Ollama is not installed or fails to start.
    """

    if is_ollama_running(host=host, port=port, timeout=timeout):
        return True

    if shutil.which("ollama") is None:
        warnings.warn(
            "Ollama does not appear to be installed or available on PATH. "
            "Install it from https://ollama.com/download and ensure the "
            "`ollama` command is accessible in this environment.",
            UserWarning,
            stacklevel=2,
        )
        return False

    subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
    )
    return is_ollama_running(host=host, port=port, timeout=timeout)


def is_model_installed(
    model: str,
    host: str = "127.0.0.1",
    port: int = 11434,
    timeout: float = 0.2,
) -> bool:
    """
    Return True when the named model is present in Ollama.

    Args:
        model: Model name to look up (for example, "llama3" or "llama3:latest").
        host: Hostname or IP address to probe.
        port: Port to probe.
        timeout: Socket timeout in seconds.

    Returns:
        True when the model appears in the Ollama tags list; otherwise False.
    """

    conn: http.client.HTTPConnection | None = None
    try:
        conn = http.client.HTTPConnection(host, port, timeout=timeout)
        conn.request("GET", "/api/tags")
        response = conn.getresponse()
        if response.status >= HTTP_ERROR_STATUS:
            return False
        payload = response.read()
        data = json.loads(payload)
        models = data.get("models", [])
        return any(
            isinstance(entry, dict) and entry.get("name") == model for entry in models
        )
    except (OSError, http.client.HTTPException, json.JSONDecodeError):
        return False
    finally:
        if conn is not None:
            conn.close()


def install_model(
    model: str,
    host: str = "127.0.0.1",
    port: int = 11434,
    timeout: float = 0.2,
) -> bool:
    """
    Install a model if it is not already present in Ollama.

    Args:
        model: Model name to install (for example, "llama3" or "llama3:latest").
        host: Hostname or IP address to probe.
        port: Port to probe.
        timeout: Socket timeout in seconds.

    Returns:
        True when the model is already installed or installs successfully;
        otherwise False.
    """

    if is_model_installed(model, host=host, port=port, timeout=timeout):
        return True

    if not run_ollama_server(host=host, port=port, timeout=timeout):
        return False

    try:
        subprocess.run(
            ["ollama", "pull", model],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return False

    return is_model_installed(model, host=host, port=port, timeout=timeout)


def ensure_model_and_server_ready(
    model: str,
    host: str = "127.0.0.1",
    port: int = 11434,
    timeout: float = 0.2,
) -> bool:
    """
    Ensure the server is running and the requested model is available.

    Args:
        model: Model name to ensure is present (for example, "llama3:latest").
        host: Hostname or IP address to probe.
        port: Port to probe.
        timeout: Socket timeout in seconds.

    Returns:
        True when the server is running and the model is available; otherwise False.
    """

    if not run_ollama_server(host=host, port=port, timeout=timeout):
        return False

    if is_model_installed(model, host=host, port=port, timeout=timeout):
        return True

    return install_model(model, host=host, port=port, timeout=timeout)
