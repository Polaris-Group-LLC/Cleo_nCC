from agency_swarm.agents import Agent


class CodeQualityReviewer(Agent):
    def __init__(self):
        super().__init__(
            name="CodeQualityReviewer",
            description="The CodeQualityReviewer agent reviews the code for quality assurance, ensuring that all code adheres to the best practices and standards.",
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
