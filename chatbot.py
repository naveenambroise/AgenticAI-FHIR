import os
import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

load_dotenv()
model_name = os.getenv("MODEL", "gpt-3.5-turbo")
llm = init_chat_model(model_name, temperature=0)

# Simple FHIR lookup using the public HAPI FHIR demo server
FHIR_BASE = os.getenv("FHIR_BASE", "https://hapi.fhir.org/baseR4")

def search_fhir(resource_query: str) -> str:
    """Search Patients by name on the HAPI FHIR public server and return a short summary.

    This is a lightweight template for a real integration and uses unauthenticated public FHIR demo.
    """
    try:
        params = {"name": resource_query}
        url = f"{FHIR_BASE}/Patient"
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("total", 0) == 0 or not data.get("entry"):
            return f"No Patient resources found for '{resource_query}'."
        # Summarize first 3 matches
        summaries = []
        for entry in data.get("entry", [])[:3]:
            resource = entry.get("resource", {})
            pid = resource.get("id", "<no-id>")
            name = " ".join([n.get("given", [""])[0] for n in resource.get("name", [])]) if resource.get("name") else "<no-name>"
            family = resource.get("name", [])[0].get("family") if resource.get("name") else None
            if family:
                full_name = f"{name} {family}".strip()
            else:
                full_name = name
            gender = resource.get("gender", "unknown")
            birth = resource.get("birthDate", "unknown")
            summaries.append(f"Patient id={pid}, name={full_name}, gender={gender}, birthDate={birth}")
        return "\n".join(summaries)
    except Exception as e:
        return f"FHIR lookup error: {str(e)}"

tools = [
    {
        "name": "FHIRSearch",
        "func": search_fhir,
        "description": "Search FHIR Patient resources by name and return a short summary",
    }
]

agent = create_agent(llm, tools=tools, name="AgenticFHIR")

if __name__ == "__main__":
    while True:
        q = input("You: ")
        if q.lower() in ["exit", "quit"]:
            break
        print("Bot:", agent.run(q))
