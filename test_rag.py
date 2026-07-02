from src.services.analysis_service import CybersecurityCopilotService

service = CybersecurityCopilotService()

result = service.analyze(
    user_text="What is phishing?"
)

print(result)