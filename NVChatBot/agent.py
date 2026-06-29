from google.adk import Agent

with open("E:\\ORGANIZATION DEVELOPMENT\\NEX VITALS\\NexVitalsSupport\\NexVitalsSupportMicroServices\\NVChatBot\\instruction.txt", "r", encoding="utf-8") as f:
    instruction_text = f.read()

root_agent = Agent(
    name= "NVAI",
    description="NexVitals Support AI Agent",
    instruction=instruction_text,
    model="gemini-3-flash-preview",
    tools=[]
)