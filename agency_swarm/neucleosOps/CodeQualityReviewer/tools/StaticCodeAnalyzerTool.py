from agency_swarm.tools import BaseTool
from pydantic import Field
import subprocess
import requests
import os

class StaticCodeAnalyzerTool(BaseTool):
    """
    A tool that allows the CodeQualityReviewer to perform static code analysis on the codebase.
    It supports multiple programming languages and provides detailed reports on code quality issues.
    Integrates with static analysis tools like SonarQube or ESLint to provide comprehensive analysis results.
    """

    tool: str = Field(
        ..., description="The static analysis tool to use. Options are 'sonarqube' or 'eslint'."
    )
    repo_url: str = Field(
        ..., description="The repository URL for the codebase to be analyzed."
    )
    branch: str = Field(
        default="main", description="The branch to analyze. Default is 'main'."
    )
    access_token: str = Field(
        ..., description="The access token for authenticating with the chosen tool, if applicable."
    )
    sonar_project_key: str = Field(
        default=None, description="The SonarQube project key, if using SonarQube."
    )
    eslint_config_path: str = Field(
        default=None, description="The path to the ESLint configuration file, if using ESLint."
    )

    def run(self):
        """
        Performs static code analysis using the chosen tool and provides detailed reports on code quality issues.
        """
        if self.tool.lower() == 'sonarqube':
            return self._analyze_with_sonarqube()
        elif self.tool.lower() == 'eslint':
            return self._analyze_with_eslint()
        else:
            return f"Unsupported tool: {self.tool}. Please choose 'sonarqube' or 'eslint'."

    def _analyze_with_sonarqube(self):
        """
        Performs static code analysis using SonarQube.
        """
        try:
            subprocess.run(["git", "clone", self.repo_url], check=True)
            repo_name = self.repo_url.split('/')[-1].replace('.git', '')
            os.chdir(repo_name)
            subprocess.run(["git", "checkout", self.branch], check=True)

            sonar_scanner_command = [
                "sonar-scanner",
                f"-Dsonar.projectKey={self.sonar_project_key}",
                f"-Dsonar.sources=.",
                f"-Dsonar.host.url=https://sonarqube.example.com",
                f"-Dsonar.login={self.access_token}"
            ]

            subprocess.run(sonar_scanner_command, check=True)
            return f"Successfully performed static code analysis with SonarQube on {self.repo_url}"
        except subprocess.CalledProcessError as e:
            return f"Failed to perform static code analysis with SonarQube. Error: {str(e)}"

    def _analyze_with_eslint(self):
        """
        Performs static code analysis using ESLint.
        """
        try:
            subprocess.run(["git", "clone", self.repo_url], check=True)
            repo_name = self.repo_url.split('/')[-1].replace('.git', '')
            os.chdir(repo_name)
            subprocess.run(["git", "checkout", self.branch], check=True)

            eslint_command = ["eslint", ".", "--config", self.eslint_config_path or ".eslintrc.js"]

            result = subprocess.run(eslint_command, capture_output=True, text=True)
            if result.returncode == 0:
                return f"ESLint analysis completed successfully:\n{result.stdout}"
            else:
                return f"ESLint analysis found issues:\n{result.stdout}\n{result.stderr}"
        except subprocess.CalledProcessError as e:
            return f"Failed to perform static code analysis with ESLint. Error: {str(e)}"

# Example usage:
# tool = StaticCodeAnalyzerTool(
#     tool='sonarqube',
#     repo_url='https://github.com/yourusername/yourrepo.git',
#     branch='main',
#     access_token=os.getenv('SONARQUBE_ACCESS_TOKEN'),
#     sonar_project_key='your_project_key'
# )
# result = tool.run()
# print(result)