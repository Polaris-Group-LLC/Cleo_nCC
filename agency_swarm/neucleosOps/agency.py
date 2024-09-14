from agency_swarm import Agency
from MongoDBAgent import MongoDBAgent
from CodeQualityReviewer import CodeQualityReviewer
from DocumentationAgent import DocumentationAgent
from DevelopmentAgent import DevelopmentAgent
from CleoCX import CleoCX
from Devid import Devid
from BrowsingAgent import BrowsingAgent

cleo_cx = CleoCX()
dev = DevelopmentAgent()
doc = DocumentationAgent()
code_review = CodeQualityReviewer()
browse = BrowsingAgent()
devid = Devid()
# mongo = MongoDBAgent()


agency = Agency([cleo_cx, dev, devid,  # Add devid here
                 [cleo_cx, dev],
                 [cleo_cx, doc],
                 [cleo_cx, code_review],
                 [cleo_cx, browse],
                 # [cleo_cx, mongo],
                 [dev, doc],
                 [dev, code_review],
                 [dev, browse],
                 # [dev, mongo],
                 [devid, doc],
                [devid, code_review],
                 [devid, browse]],  # Close the square bracket here
                shared_instructions='./agency_manifesto.md',
                max_prompt_tokens=25000,
                temperature=0.3)  # Close the parenthesis here

if __name__ == '__main__':
    agency.demo_gradio(share=True)