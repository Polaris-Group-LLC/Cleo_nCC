from agency_swarm.agents import Agent


class DocumentationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="DocumentationAgent",
            description="The DocumentationAgent maintains and updates all documentation related to the neucleos platform and its implementation, ensuring that all knowledge and context are integrated into the neucleos docs.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )
        
    def response_validator(self, message):
        return message
