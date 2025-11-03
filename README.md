# AgenticAI-FHIR

Sample Agentic AI project demonstrating a simple LangChain agent that exposes a placeholder FHIR lookup tool.

Run (PowerShell):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
.\venv\Scripts\Activate.ps1
python examples\run_demo.py
```

This project contains a placeholder `search_fhir` tool that returns mock FHIR resource summaries. Replace with a real FHIR client for production.
