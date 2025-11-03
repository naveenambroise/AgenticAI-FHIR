import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

load_dotenv()
model_name = os.getenv("MODEL", "gpt-3.5-turbo")
llm = init_chat_model(model_name, temperature=0)

# Placeholder FHIR search tool
def search_fhir(resource_query: str) -> str:
    return f"FHIR search placeholder: would search for {resource_query} and return matching FHIR resources (mock)"

tools = [
    {
        "name": "FHIRSearch",
        "func": search_fhir,
        "description": "Search FHIR resources by query and return a short summary",
    }
]

agent = create_agent(llm, tools=tools, name="AgenticFHIR")

if __name__ == "__main__":
    while True:
        q = input("You: ")
        if q.lower() in ["exit", "quit"]:
            break
        print("Bot:", agent.run(q))
