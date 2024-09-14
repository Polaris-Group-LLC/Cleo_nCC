from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

class DocEditorTool(BaseTool):
    """
    A tool that allows the DocumentationAgent to edit and format documentation files.
    It supports markdown and rich text editing, with features like version control and collaborative editing.
    Integrates with platforms like GitHub or Google Docs to provide a seamless editing experience.
    """

    platform: str = Field(
        ..., description="The platform to use for editing. Options are 'github' or 'google_docs'."
    )
    file_path: str = Field(
        ..., description="The path to the documentation file to be edited."
    )
    content: str = Field(
        ..., description="The new content to be added or updated in the documentation file."
    )
    commit_message: str = Field(
        default=None, description="The commit message for version control, if applicable."
    )
    access_token: str = Field(
        ..., description="The access token for authenticating with the chosen platform."
    )

    def run(self):
        """
        Edits and formats the documentation file on the chosen platform, supporting version control and collaborative editing.
        """
        if self.platform.lower() == 'github':
            return self._edit_github_file()
        elif self.platform.lower() == 'google_docs':
            return self._edit_google_docs_file()
        else:
            return f"Unsupported platform: {self.platform}. Please choose 'github' or 'google_docs'."

    def _edit_github_file(self):
        """
        Edits a file on GitHub, supporting version control.
        """
        repo_owner = "your_repo_owner"
        repo_name = "your_repo_name"
        branch = "main"
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{self.file_path}"

        headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Get the current file content and SHA
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            return f"Failed to fetch file from GitHub. Error: {response.json()}"

        file_info = response.json()
        sha = file_info['sha']

        # Update the file content
        data = {
            "message": self.commit_message or "Update documentation",
            "content": self._encode_content(self.content),
            "sha": sha,
            "branch": branch
        }

        response = requests.put(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return f"Successfully updated the file on GitHub: {self.file_path}"
        else:
            return f"Failed to update file on GitHub. Error: {response.json()}"

    def _edit_google_docs_file(self):
        """
        Edits a Google Docs file, supporting collaborative editing.
        """
        doc_id = self.file_path  # In the case of Google Docs, file_path will be the document ID
        api_url = f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        requests_body = {
            "requests": [
                {
                    "insertText": {
                        "location": {
                            "index": 1
                        },
                        "text": self.content
                    }
                }
            ]
        }

        response = requests.post(api_url, headers=headers, json=requests_body)
        if response.status_code == 200:
            return f"Successfully updated the Google Docs file: {doc_id}"
        else:
            return f"Failed to update Google Docs file. Error: {response.json()}"

    def _encode_content(self, content):
        """
        Encodes the content to base64 as required by the GitHub API.
        """
        import base64
        return base64.b64encode(content.encode()).decode()

# Example usage:
# tool = DocEditorTool(
#     platform='github',
#     file_path='docs/README.md',
#     content='# Updated Documentation\n\nThis is the updated content.',
#     commit_message='Update README.md',
#     access_token=os.getenv('GITHUB_ACCESS_TOKEN')
# )
# result = tool.run()
# print(result)