from agency_swarm.tools import BaseTool
from pydantic import Field
import subprocess
import requests
import os

class DocPublisherTool(BaseTool):
    """
    A tool that enables the DocumentationAgent to publish documentation to various platforms.
    It supports platforms like ReadTheDocs, GitHub Pages, and Confluence.
    The tool automates the process of converting documentation files into the required format for each platform and handles the publishing process.
    """

    platform: str = Field(
        ..., description="The platform to publish to. Options are 'readthedocs', 'github_pages', or 'confluence'."
    )
    repo_url: str = Field(
        ..., description="The repository URL for the documentation source code."
    )
    branch: str = Field(
        default="main", description="The branch to use for publishing. Default is 'main'."
    )
    access_token: str = Field(
        ..., description="The access token for authenticating with the chosen platform."
    )
    confluence_space: str = Field(
        default=None, description="The Confluence space key, if publishing to Confluence."
    )
    confluence_title: str = Field(
        default=None, description="The Confluence page title, if publishing to Confluence."
    )

    def run(self):
        """
        Publishes the documentation to the chosen platform.
        """
        if self.platform.lower() == 'readthedocs':
            return self._publish_to_readthedocs()
        elif self.platform.lower() == 'github_pages':
            return self._publish_to_github_pages()
        elif self.platform.lower() == 'confluence':
            return self._publish_to_confluence()
        else:
            return f"Unsupported platform: {self.platform}. Please choose 'readthedocs', 'github_pages', or 'confluence'."

    def _publish_to_readthedocs(self):
        """
        Publishes documentation to ReadTheDocs.
        """
        # Assuming the repository is already configured with ReadTheDocs
        api_url = f"https://readthedocs.org/api/v3/projects/"
        headers = {
            "Authorization": f"token {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "name": self.repo_url.split('/')[-1],
            "repository": {
                "url": self.repo_url,
                "type": "git"
            }
        }

        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 201:
            return f"Successfully triggered build on ReadTheDocs for {self.repo_url}"
        else:
            return f"Failed to trigger build on ReadTheDocs. Error: {response.json()}"

    def _publish_to_github_pages(self):
        """
        Publishes documentation to GitHub Pages.
        """
        try:
            subprocess.run(["git", "clone", self.repo_url], check=True)
            repo_name = self.repo_url.split('/')[-1].replace('.git', '')
            os.chdir(repo_name)
            subprocess.run(["git", "checkout", self.branch], check=True)
            subprocess.run(["mkdocs", "gh-deploy"], check=True)
            return f"Successfully published to GitHub Pages from {self.repo_url}"
        except subprocess.CalledProcessError as e:
            return f"Failed to publish to GitHub Pages. Error: {str(e)}"

    def _publish_to_confluence(self):
        """
        Publishes documentation to Confluence.
        """
        if not self.confluence_space or not self.confluence_title:
            return "Confluence space key and page title are required for publishing to Confluence."

        api_url = f"https://your-confluence-instance.atlassian.net/wiki/rest/api/content"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "type": "page",
            "title": self.confluence_title,
            "space": {
                "key": self.confluence_space
            },
            "body": {
                "storage": {
                    "value": self._convert_docs_to_confluence_format(),
                    "representation": "storage"
                }
            }
        }

        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return f"Successfully published to Confluence in space {self.confluence_space} with title {self.confluence_title}"
        else:
            return f"Failed to publish to Confluence. Error: {response.json()}"

    def _convert_docs_to_confluence_format(self):
        """
        Converts documentation files to Confluence format.
        """
        # Placeholder for actual conversion logic
        # This should convert markdown or other formats to Confluence's storage format
        return "<h1>Converted Documentation</h1><p>This is a placeholder for the converted documentation content.</p>"

# Example usage:
# tool = DocPublisherTool(
#     platform='github_pages',
#     repo_url='https://github.com/yourusername/yourrepo.git',
#     branch='main',
#     access_token=os.getenv('GITHUB_ACCESS_TOKEN')
# )
# result = tool.run()
# print(result)