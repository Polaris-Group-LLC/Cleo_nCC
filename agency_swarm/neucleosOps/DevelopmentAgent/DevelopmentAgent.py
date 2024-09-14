from agency_swarm.agents import Agent


class DevelopmentAgent(Agent):
    def __init__(self):
        super().__init__(
            name="DevelopmentAgent",
            description="The DevelopmentAgent focuses on the continuous development and improvement of the neucleos platform, ensuring that all technical aspects are up-to-date and functioning optimally.",
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
