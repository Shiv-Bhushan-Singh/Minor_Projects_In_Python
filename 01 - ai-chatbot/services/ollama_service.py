import json
from typing import Dict, Generator, List

import requests

from utils.config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL
)

from utils.logger import logger


OLLAMA_CHAT_URL = (
    f"{OLLAMA_BASE_URL}/api/chat"
)


def check_ollama_health() -> bool:

    try:

        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=5
        )

        response.raise_for_status()

        return True

    except requests.RequestException as error:

        logger.error(
            "Ollama health check failed: %s",
            error
        )

        return False


def get_available_models() -> List[str]:

    try:

        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        models = data.get(
            "models",
            []
        )

        return [
            model.get("name")
            for model in models
            if model.get("name")
        ]

    except requests.RequestException as error:

        logger.error(
            "Unable to retrieve Ollama models: %s",
            error
        )

        return []


def generate_response(
    messages: List[Dict[str, str]],
    model: str = OLLAMA_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 1024
) -> Generator[str, None, None]:

    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        }
    }


    try:

        with requests.post(
            OLLAMA_CHAT_URL,
            json=payload,
            stream=True,
            timeout=(10, 300)
        ) as response:

            response.raise_for_status()


            for line in response.iter_lines():

                if not line:
                    continue


                try:

                    data = json.loads(line)

                except json.JSONDecodeError:

                    logger.warning(
                        "Invalid JSON received from Ollama."
                    )

                    continue


                message = data.get(
                    "message",
                    {}
                )


                content = message.get(
                    "content",
                    ""
                )


                if content:

                    yield content


                if data.get("done"):

                    break


    except requests.exceptions.ConnectionError as error:

        logger.error(
            "Ollama connection failed: %s",
            error
        )

        raise RuntimeError(
            "Cannot connect to Ollama. "
            "Make sure Ollama is running."
        ) from error


    except requests.exceptions.Timeout as error:

        logger.error(
            "Ollama request timed out."
        )

        raise RuntimeError(
            "Ollama took too long to respond."
        ) from error


    except requests.exceptions.HTTPError as error:

        logger.error(
            "Ollama returned HTTP error: %s",
            error
        )

        raise RuntimeError(
            f"Ollama returned an HTTP error: "
            f"{response.status_code}"
        ) from error


    except requests.exceptions.RequestException as error:

        logger.error(
            "Ollama request failed: %s",
            error
        )

        raise RuntimeError(
            "An error occurred while communicating "
            "with Ollama."
        ) from error