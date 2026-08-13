from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def weather(city:str) -> str:
  """Get weather of a city"""
  return f"Weather in {city} is sunny"


if __name__ == "__main__":
  import sys
  transport = "sse" if "--sse" in sys.argv else "stdio"
  mcp.run(transport=transport)