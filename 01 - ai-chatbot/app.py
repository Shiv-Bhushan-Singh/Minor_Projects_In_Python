import streamlit as st

from services.context_manager import build_context

from services.database_service import (
    add_message,
    create_conversation,
    delete_conversation,
    get_conversations,
    get_messages,
    initialize_database
)

from services.ollama_service import (
    check_ollama_health,
    generate_response,
    get_available_models
)

from utils.config import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    OLLAMA_MODEL
)


SYSTEM_PROMPT = """
You are a helpful, knowledgeable AI assistant.

Follow these principles:

1. Give accurate and useful answers.
2. Do not invent facts when you are uncertain.
3. Explain technical concepts clearly.
4. Start from fundamentals when the user is learning.
5. Use examples when they improve understanding.
6. Structure longer answers using headings and bullet points.
7. Be concise when a short answer is sufficient.
8. Maintain context from the conversation.
"""


st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)


# DATABASE INITIALIZATION
initialize_database()



# SESSION STATE
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


if "conversation_id" not in st.session_state:

    st.session_state.conversation_id = None


if "temperature" not in st.session_state:

    st.session_state.temperature = (
        DEFAULT_TEMPERATURE
    )


if "max_tokens" not in st.session_state:

    st.session_state.max_tokens = (
        DEFAULT_MAX_TOKENS
    )


if "selected_model" not in st.session_state:

    st.session_state.selected_model = (
        OLLAMA_MODEL
    )



# SIDEBAR
with st.sidebar:

    st.header("⚙️ Settings")


    # Ollama Status
    ollama_running = check_ollama_health()


    if ollama_running:

        st.success(
            "Ollama is running"
        )

    else:

        st.error(
            "Ollama is not running"
        )


    st.divider()

    # Model Selection
    models = get_available_models()


    if models:

        default_index = 0

        if (
            st.session_state.selected_model
            in models
        ):

            default_index = models.index(
                st.session_state.selected_model
            )


        st.session_state.selected_model = (
            st.selectbox(
                "Model",
                models,
                index=default_index
            )
        )

    else:

        st.warning(
            "No Ollama models found."
        )


    # Temperature
    st.session_state.temperature = (
        st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.5,
            value=st.session_state.temperature,
            step=0.1,
            help=(
                "Lower values make responses "
                "more deterministic. Higher values "
                "make responses more creative."
            )
        )
    )


    # Maximum Output Tokens
    st.session_state.max_tokens = (
        st.slider(
            "Maximum response tokens",
            min_value=128,
            max_value=4096,
            value=st.session_state.max_tokens,
            step=128
        )
    )


    st.divider()


    # New Conversation
    if st.button(
        "➕ New Conversation",
        use_container_width=True
    ):

        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        st.session_state.conversation_id = None

        st.rerun()


    # Conversation History

    st.subheader("💬 Conversations")


    conversations = get_conversations()


    for conversation in conversations:

        conversation_id = conversation["id"]

        title = conversation["title"]


        col1, col2 = st.columns(
            [4, 1]
        )


        with col1:

            if st.button(
                title,
                key=f"conversation_{conversation_id}",
                use_container_width=True
            ):

                stored_messages = get_messages(
                    conversation_id
                )


                st.session_state.messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    }
                ]


                for message in stored_messages:

                    st.session_state.messages.append(
                        {
                            "role": message["role"],
                            "content": message["content"]
                        }
                    )


                st.session_state.conversation_id = (
                    conversation_id
                )


                st.rerun()


        with col2:

            if st.button(
                "🗑️",
                key=f"delete_{conversation_id}"
            ):

                delete_conversation(
                    conversation_id
                )


                if (
                    st.session_state.conversation_id
                    == conversation_id
                ):

                    st.session_state.messages = [
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        }
                    ]

                    st.session_state.conversation_id = (
                        None
                    )


                st.rerun()


st.title("🤖 AI Chatbot")

# st.caption(
#     f"Powered by Ollama • "
#     f"{st.session_state.selected_model}"
# )


# DISPLAY CHAT HISTORY

for message in st.session_state.messages:

    if message["role"] == "system":

        continue


    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )



prompt = st.chat_input(
    "Ask me anything..."
)



# PROCESS USER MESSAGE
if prompt:

    prompt = prompt.strip()


    if not prompt:

        st.warning(
            "Please enter a message."
        )

        st.stop()


    # Create conversation if necessary

    if st.session_state.conversation_id is None:

        title = prompt[:50]

        if len(prompt) > 50:

            title += "..."


        st.session_state.conversation_id = (
            create_conversation(title)
        )


    conversation_id = (
        st.session_state.conversation_id
    )


    # Add user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    add_message(
        conversation_id,
        "user",
        prompt
    )


    # Display user message
    with st.chat_message("user"):

        st.markdown(prompt)


    # Build context
    context = build_context(
        st.session_state.messages
    )


    # Generate response
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""


        try:

            for chunk in generate_response(
                messages=context,
                model=st.session_state.selected_model,
                temperature=(
                    st.session_state.temperature
                ),
                max_tokens=(
                    st.session_state.max_tokens
                )
            ):

                full_response += chunk


                response_placeholder.markdown(
                    full_response
                    + "▌"
                )


            response_placeholder.markdown(
                full_response
            )


        except RuntimeError as error:

            st.error(
                str(error)
            )

            full_response = ""


    # Save assistant response
    if full_response:

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )


        add_message(
            conversation_id,
            "assistant",
            full_response
        )