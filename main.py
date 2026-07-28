import logging
import streamlit as st
from chatbot import Chatbot

logging.basicConfig(
    filename="logs.log",
    format="%(asctime)s-%(level)s-%(name)s:%(msg)s",
    level=logging.DEBUG,
)
logger = logging.getLoggier("general-purpose-chatbot")

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
    temp = st.sidebar.slider("Temperature", 0.0, 2, bot.temperature, 0.1)
    max_output_tokens = st.sidebar.slider(
        "Max Output Tokens", 64, 2048, bot.max_output_tokens, 64
    )
    token_budget = st.sidebar.slider("Token Budget", 256, 4096, bot.token_budget, 256)

    bot.temperature(temp)
    bot.max_output_tokens(max_output_tokens)
    bot.token_budget(token_budget)

    st.sidebar.header("⚙️ Settings")
    model_choice = st.sidebar.selectbox(
        "Choose Model",
        ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-3.5-flash"],
        index=["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-3.5-flash"].index(
            bot.model
        ),
    )

    if model_choice != bot.model:
        logger.debug(f"Switching model to {model_choice}")
        bot.switch_model(model_choice)

    st.sidebar.metric("Requests Used Today", bot.request_count)
    st.sidebar.metric("Total Tokens Consumed", bot.get_token_summary())

    if bot.token_log:
        st.sidebar.subheader("Usage Breakdown")
        for i, log in enumerate(bot.token_log, 1):
            st.sidebar.write(
                f"Turn {i}: Prompt={log['prompt']}, Output={log['output']}, Total={log['total']}"
            )

    # Chat UI
    st.title("💬 Gemini Chatbot (OOP + Quota Tracker)")
    if prompt := st.chat_input("Ask me anything..."):
        st.chat_message("user").write(prompt)
        reply = bot.send_message(prompt)
        st.chat_message("assistant").write(reply)

        usage = bot.token_log[-1]
        st.caption(
            f"🔢 Tokens → Prompt: {usage['prompt']}, Output: {usage['output']}, Total: {usage['total']}"
        )


if __name__ == "__main__":
    main()
