from agency_swarm.agents import Agent


class Cleo(Agent):
    def __init__(self):
        super().__init__(
            name="Cleo",
            description="Cleo is the CEO and the primary agent for user interaction in the Cleo_nCC agency. Cleo handles user inquiries, provides information about the platform, and coordinates with other agents as the agency expands.",
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
