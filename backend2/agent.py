from agents import (Agent, Runner, OpenAIResponsesModel, AsyncOpenAI, set_tracing_disabled, function_tool,
enable_verbose_stdout_logging)
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)

# ✅ OpenRouter client
provider = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ✅ CORRECT model wrapper
model = OpenAIResponsesModel(
    model="google/gemini-2.0-flash-exp:free",
    openai_client=provider
)
agent = Agent(
    name="Assistant",
    instructions="""
    You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
    First call `retrieve`.
    Use ONLY retrieved content.
    If not found, say "I don't know".
    """,
    model=model,
)

result = Runner.run_sync(
    agent,
    input="what is physical ai? explain shortly"
)

print(result.final_output)