from src.services.analysis_service import CybersecurityCopilotService

service = CybersecurityCopilotService()
result = service.analyze("Investigate IP 8.8.8.8 and URL http://example.com", "")
print("Final Answer:")
print(result["final_answer"])
print("Evidence:")
print(result.get("evidence"))