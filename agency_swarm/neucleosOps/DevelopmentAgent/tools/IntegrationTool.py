from agency_swarm.tools import BaseTool
from pydantic import Field
import requests

class IntegrationTool(BaseTool):
    """
    A tool that facilitates the integration of the DevelopmentAgent with other agents like DocumentationAgent,
    CodeQualityReviewer, and MongoDBAgent. It supports API calls and data exchange between agents using
    secure and efficient communication protocols like REST or GraphQL.
    """

    target_agent: str = Field(
        ..., description="The target agent to integrate with. Options are 'DocumentationAgent', 'CodeQualityReviewer', or 'MongoDBAgent'."
    )
    api_endpoint: str = Field(
        ..., description="The API endpoint of the target agent."
    )
    request_type: str = Field(
        ..., description="The type of API request. Options are 'GET', 'POST', 'PUT', 'DELETE'."
    )
    payload: dict = Field(
        default=None, description="The payload to send with the API request, if applicable."
    )
    headers: dict = Field(
        default=None, description="The headers to include with the API request, if applicable."
    )

    def run(self):
        """
        Facilitates the integration by making the appropriate API call to the target agent and handling the response.
        """
        try:
            if self.request_type.upper() == 'GET':
                response = requests.get(self.api_endpoint, headers=self.headers, params=self.payload)
            elif self.request_type.upper() == 'POST':
                response = requests.post(self.api_endpoint, headers=self.headers, json=self.payload)
            elif self.request_type.upper() == 'PUT':
                response = requests.put(self.api_endpoint, headers=self.headers, json=self.payload)
            elif self.request_type.upper() == 'DELETE':
                response = requests.delete(self.api_endpoint, headers=self.headers, json=self.payload)
            else:
                return f"Unsupported request type: {self.request_type}. Please choose 'GET', 'POST', 'PUT', or 'DELETE'."

            response.raise_for_status()  # Raise an error for bad status codes
            return f"Response from {self.target_agent}:\n{response.json()}"
        except requests.exceptions.RequestException as e:
            return f"Failed to communicate with {self.target_agent}. Error: {str(e)}"

# Example usage:
# tool = IntegrationTool(
#     target_agent='DocumentationAgent',
#     api_endpoint='https://api.documentationagent.com/docs',
#     request_type='GET',
#     headers={'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
# )
# result = tool.run()
# print(result)