from agency_swarm import Agency
from Cleo import Cleo
from Devid import Devid
from BrowsingAgent import BrowsingAgent  # Add this import

cleo = Cleo()
devid = Devid()
browsing_agent = BrowsingAgent()  # Create an instance of BrowsingAgent

agency = Agency([cleo, devid, browsing_agent,  # Add browsing_agent to the top-level agents
                 [cleo, devid],
                 [cleo, browsing_agent]],  # Add communication flow between Cleo and BrowsingAgent
                shared_instructions='./agency_manifesto.md',
                max_prompt_tokens=25000,
                temperature=0.3,
                )

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5151))
    agency.demo_gradio(server_port=port)