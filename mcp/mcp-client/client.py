from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import asyncio
import os
import sys

load_dotenv()

# Resolve absolute path to server scripts
math_server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../mcp-tools/mathserver.py"))
weather_server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../mcp-tools/weather.py"))

async def main():
  client = MultiServerMCPClient(
    {
      "math": {
        "command": sys.executable,
        "args": [math_server_path],
        "transport": "stdio"
      },
      "weather": {
        "command": sys.executable,
        "args": [weather_server_path],
        "transport": "stdio"
      }
    }
  )

  os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

  tools = await client.get_tools()
  model = ChatGroq(model="llama-3.3-70b-versatile")

  agent = create_react_agent(model, tools)

  weather_response = await agent.ainvoke({
    "messages": [{"role": "user", "content": "what is the weather in New Delhi?"}]
  })

  print("Weather Response:\n", weather_response["messages"][-1].content)

  math_response = await agent.ainvoke({
    "messages": [{"role": "user", "content": "what is 2 + 2?"}]
  })

  print("Math Response:\n", math_response["messages"][-1].content)

if __name__ == "__main__":
  asyncio.run(main())