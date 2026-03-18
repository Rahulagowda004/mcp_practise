import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": ["server.py"],  # path to your server file
            }
        }
    )

    # Load tools from MCP server
    tools = await client.get_tools()

    # Create agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="Always use tools for calculations. Do not solve on your own."
    )

    # Run query
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is (4 + 6) * 5?"}]}
    )

    print(response)

if __name__ == "__main__":
    asyncio.run(main())