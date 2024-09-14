from agency_swarm.agents import Agent
from .tools.AddNeucleosAppTool import AddNeucleosAppTool

class MongoDBAgent(Agent):
    def __init__(self):
        super().__init__(
            name="MongoDBAgent",
            description="The MongoDBAgent manages and optimizes the MongoDB databases used within the neucleos platform.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[AddNeucleosAppTool],  # Add the new tool here
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )
        
    def response_validator(self, message):
        return message
