from agency_swarm.tools import BaseTool
from pydantic import Field
import subprocess

class CodeTestingTool(BaseTool):
    """
    A tool that enables the DevelopmentAgent to run unit tests and integration tests on the codebase.
    It supports popular testing frameworks like JUnit, PyTest, and Mocha.
    """

    test_framework: str = Field(
        ..., description="The testing framework to use. Options are 'junit', 'pytest', or 'mocha'."
    )
    test_directory: str = Field(
        ..., description="The directory containing the tests to be run."
    )

    def run(self):
        """
        Runs the specified tests using the chosen testing framework and provides detailed test reports.
        """
        if self.test_framework.lower() == 'junit':
            test_command = ['mvn', 'test', '-f', self.test_directory]
        elif self.test_framework.lower() == 'pytest':
            test_command = ['pytest', self.test_directory, '--maxfail=1', '--disable-warnings', '-q', '--tb=short']
        elif self.test_framework.lower() == 'mocha':
            test_command = ['mocha', self.test_directory]
        else:
            return f"Unsupported testing framework: {self.test_framework}. Please choose 'junit', 'pytest', or 'mocha'."

        try:
            result = subprocess.run(test_command, capture_output=True, text=True, check=True)
            return f"Test Results:\n{result.stdout}\n\nErrors:\n{result.stderr}"
        except subprocess.CalledProcessError as e:
            return f"Failed to run tests. Error: {str(e)}\n\nOutput:\n{e.output}\n\nErrors:\n{e.stderr}"

# Example usage:
# tool = CodeTestingTool(test_framework='pytest', test_directory='/path/to/tests')
# result = tool.run()
# print(result)