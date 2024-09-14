from agency_swarm.agents import Agent


class CleoCX(Agent):
    def __init__(self):
        super().__init__(
            name="CleoCX",
            description="CleoCX oversees the entire neucleosOps agency, ensuring alignment with the mission and goals. She facilitates communication between agents and users.",
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
