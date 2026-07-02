from src.services.analysis_service import CybersecurityCopilotService

service = CybersecurityCopilotService()

result = service.analyze(
    user_text="""
PowerShell brute force attack with failed login attempts followed by success
"""
)

print("\n========== FINAL RESULT ==========\n")

print(result["final_answer"])