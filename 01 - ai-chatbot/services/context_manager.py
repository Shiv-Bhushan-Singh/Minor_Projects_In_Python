from typing import Dict, List

from utils.config import MAX_RECENT_MESSAGES


def build_context(
    messages: List[Dict[str, str]]
) -> List[Dict[str, str]]:

    if not messages:
        return []


    system_message = None

    conversation_messages = []


    for message in messages:

        if message["role"] == "system":

            system_message = message

        else:

            conversation_messages.append(
                message
            )


    recent_messages = conversation_messages[
        -MAX_RECENT_MESSAGES:
    ]


    context = []


    if system_message:

        context.append(
            system_message
        )


    context.extend(
        recent_messages
    )


    return context