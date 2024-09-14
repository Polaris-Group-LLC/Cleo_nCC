from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

class CodeReviewPlatformTool(BaseTool):
    """
    A tool that enables the CodeQualityReviewer to conduct code reviews on a collaborative platform.
    It supports platforms like GitHub or GitLab, allowing for inline comments and review requests.
    The tool automates the process of fetching pull requests or merge requests and facilitates the review process.
    """

    platform: str = Field(
        ..., description="The platform to use for code reviews. Options are 'github' or 'gitlab'."
    )
    repo_url: str = Field(
        ..., description="The repository URL for the codebase to be reviewed."
    )
    access_token: str = Field(
        ..., description="The access token for authenticating with the chosen platform."
    )
    pull_request_id: int = Field(
        ..., description="The ID of the pull request or merge request to review."
    )
    comment: str = Field(
        ..., description="The comment to add to the pull request or merge request."
    )
    file_path: str = Field(
        ..., description="The path to the file to comment on."
    )
    line_number: int = Field(
        ..., description="The line number to comment on."
    )

    def run(self):
        """
        Conducts a code review on the chosen platform, allowing for inline comments and review requests.
        """
        if self.platform.lower() == 'github':
            return self._review_on_github()
        elif self.platform.lower() == 'gitlab':
            return self._review_on_gitlab()
        else:
            return f"Unsupported platform: {self.platform}. Please choose 'github' or 'gitlab'."

    def _review_on_github(self):
        """
        Conducts a code review on GitHub.
        """
        repo_owner, repo_name = self._parse_github_repo_url()
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{self.pull_request_id}/comments"

        headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        data = {
            "body": self.comment,
            "path": self.file_path,
            "position": self.line_number
        }

        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 201:
            return f"Successfully added comment to GitHub pull request {self.pull_request_id}"
        else:
            return f"Failed to add comment to GitHub pull request. Error: {response.json()}"

    def _review_on_gitlab(self):
        """
        Conducts a code review on GitLab.
        """
        project_id = self._get_gitlab_project_id()
        api_url = f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests/{self.pull_request_id}/discussions"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        data = {
            "body": self.comment,
            "position": {
                "position_type": "text",
                "new_path": self.file_path,
                "new_line": self.line_number
            }
        }

        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 201:
            return f"Successfully added comment to GitLab merge request {self.pull_request_id}"
        else:
            return f"Failed to add comment to GitLab merge request. Error: {response.json()}"

    def _parse_github_repo_url(self):
        """
        Parses the GitHub repository URL to extract the owner and repository name.
        """
        parts = self.repo_url.rstrip('/').split('/')
        repo_owner = parts[-2]
        repo_name = parts[-1].replace('.git', '')
        return repo_owner, repo_name

    def _get_gitlab_project_id(self):
        """
        Retrieves the GitLab project ID using the repository URL.
        """
        api_url = f"https://gitlab.com/api/v4/projects"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        params = {
            "search": self.repo_url.split('/')[-1].replace('.git', '')
        }

        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            projects = response.json()
            if projects:
                return projects[0]['id']
            else:
                raise ValueError("GitLab project not found.")
        else:
            raise ValueError(f"Failed to retrieve GitLab project ID. Error: {response.json()}")

# Example usage:
# tool = CodeReviewPlatformTool(
#     platform='github',
#     repo_url='https://github.com/yourusername/yourrepo.git',
#     access_token=os.getenv('GITHUB_ACCESS_TOKEN'),
#     pull_request_id=1,
#     comment='This is a review comment.',
#     file_path='path/to/file.py',
#     line_number=10
# )
# result = tool.run()
# print(result)