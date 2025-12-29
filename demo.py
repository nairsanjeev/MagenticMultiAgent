import asyncio
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

# Load environment variables from .env file
load_dotenv()

agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are good at telling jokes.",
    name="Joker"
)

async def main():
    result = await agent.run("Tell me a joke")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())