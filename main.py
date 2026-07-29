import logging
import sys
import streamlit as st

logging.basicConfig(
    handlers=[
        logging.FileHandler("logs.log"),  # Outputs to a file
        logging.StreamHandler(sys.stdout),  # Outputs to terminal console
    ],
    format="%(asctime)s-%(levelname)s-%(name)s:%(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

from chatbot import Chatbot
from config import AVAILABLE_MODELS


# -------------------------------
# Streamlit UI
# -------------------------------
def main():
    st.set_page_config(page_title="Gemini Chatbot", page_icon="💬")

    # Initialize bot
    if "bot" not in st.session_state:
        st.session_state.bot = Chatbot()

    bot = st.session_state.bot
    logger.debug(f"Starting chatbot model - {bot.model}")

    # Sidebar controls
    st.sidebar.header("⚙️ Settings")
    temp = st.sidebar.slider("Temperature", 0.0, 2.0, bot.temperature, 0.1)
    max_output_tokens = st.sidebar.slider(
        "Max Output Tokens", 64, 2048, bot.max_output_tokens, 64
    )
    token_budget = st.sidebar.slider("Token Budget", 256, 4096, bot.token_budget, 256)

    bot.temperature = temp
    bot.max_output_tokens = max_output_tokens
    bot.token_budget = token_budget

    st.sidebar.header("⚙️ Settings")

    model_choice = st.sidebar.selectbox(
        "Choose Model",
        AVAILABLE_MODELS,
        index=AVAILABLE_MODELS.index(bot.model),
    )

    if model_choice != bot.model:
        logger.debug(f"Switching model to {model_choice}")
        bot.switch_model(model_choice)

    # --- Sidebar Metrics ---
    st.sidebar.metric("Requests Used Today", bot.request_count)
    st.sidebar.metric("Current Model Tokens", bot.get_token_summary())

    # Model-wise breakdown
    st.sidebar.subheader("Per‑Model Token Usage")
    token_stats = bot.get_all_token_summaries()

    for model, total in token_stats.items():
        st.sidebar.write(f"{model}: {total} tokens")

    # Grand total across all models
    grand_total = sum(token_stats.values())
    st.sidebar.metric("Total Tokens (All Models)", grand_total)

    # Bar chart visualization
    if token_stats:
        st.sidebar.subheader("📊 Token Usage Chart")
        st.sidebar.bar_chart(token_stats)

    # --- Chat UI ---
    st.title("💬 Gemini Chatbot (OOP + Quota Tracker)")
    if prompt := st.chat_input("Ask me anything..."):
        st.chat_message("user").write(prompt)
        reply = bot.send_message(prompt)
        st.chat_message("assistant").write(reply)

        usage = bot.token_usage[bot.model][-1]
        st.caption(
            f"🔢 Tokens → Prompt: {usage.get('prompt', 0)}, Output: {usage.get('output', 0)}, Total: {usage.get('total', 0)}"
        )


if __name__ == "__main__":
    main()
