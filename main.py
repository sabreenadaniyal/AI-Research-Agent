### Without Streamlit ###

# import os
# import asyncio
# from dotenv import load_dotenv
# from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Runner

# # Load environment variables
# load_dotenv()
# gemini_api_key = os.getenv("GEMINI_API_KEY")

# # Validate API Key
# if not gemini_api_key:
#     raise ValueError("🔐 GEMINI_API_KEY is not set. Please define it in your .env file.")

# # External Gemini-compatible client setup
# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# # Model and config setup
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True
# )

# # Research Agent Definition
# research_agent = Agent(
#     name='Research Agent',
#     instructions=(
#         "You are a Research Agent. Your task is to gather factual, relevant, "
#         "and concise information from trusted sources. Respond with accurate summaries, "
#         "definitions, and explanations suitable for non-expert users."
#     )
# )

# # CLI Input & Execution
# def main():
#     print("🧠 Welcome to AI Research Agent")
#     print("-" * 60)

#     user_input = input("👉 What do you want to research?\n> ")

#     if not user_input.strip():
#         print("⚠️ No input provided. Exiting.")
#         return

#     print("\n🔬 Researching... please wait\n")

#     response = asyncio.run(Runner.run(
#         research_agent,
#         input=user_input,
#         run_config=config
#     ))

#     print("✅ Research complete!")
#     print("\n📄 Result:\n")
#     print(response.final_output)




##### With Streamlit #####

import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Runner

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("🔐 Please set GEMINI_API_KEY in your .env file.")
    st.stop()

# Setup OpenAI-compatible client
client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model and config
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)
config = RunConfig(
    model=model,
    model_provider=client
)

# Page settings
st.set_page_config(page_title="🔍 AI Research Agent", page_icon="🧠")

# Sidebar
st.sidebar.title("🛠️ Agent Settings")
mode = st.sidebar.radio("🧠 Select Response Style", ["📝 Simple", "🧒 Explain Like I'm 5", "💻 Technical"])

instructions = {
    "📝 Simple": "Give a short, clear summary for any question.",
    "🧒 Explain Like I'm 5": "Explain the answer in very simple terms, like to a 5-year-old.",
    "💻 Technical": "Give a detailed and technical explanation with examples if needed."
}

# Agent setup
agent = Agent(
    name="Research Agent",
    instructions=instructions[mode]
)

# Header
st.title("🔍 Ask the AI Research Agent")
st.markdown("Type any question below and get instant answers powered by **Gemini AI**!")

# User input
question = st.text_input("💬 What do you want to learn about?", placeholder="e.g., Write anything here..?")

# Submit
if st.button("🚀 Get Answer") and question:
    with st.spinner("🤖 Thinking..."):
        response = asyncio.run(Runner.run(agent, input=question, run_config=config))
    st.success("✅ Done!")
    st.markdown("### 📄 Result:")
    st.write(response.final_output)

# Footer
st.markdown("---")
st.markdown("🌟 Built with ❤️ Sabreena Daniyal ")
