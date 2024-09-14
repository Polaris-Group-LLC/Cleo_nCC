from agency_swarm.tools import BaseTool
from pydantic import Field
import subprocess

class CodeEditorTool(BaseTool):
    """
    A tool that allows the DevelopmentAgent to edit code files.
    It supports syntax highlighting, code completion, and error detection for multiple programming languages
    by integrating with popular code editors like VSCode or Sublime Text.
    """

    file_path: str = Field(
        ..., description="The path to the code file that needs to be edited."
    )
    editor: str = Field(
        ..., description="The code editor to use for editing the file. Options are 'vscode' or 'sublime'."
    )

    def run(self):
        """
        Opens the specified code file in the chosen editor.
        """
        if self.editor.lower() == 'vscode':
            editor_command = ['code', self.file_path]
        elif self.editor.lower() == 'sublime':
            editor_command = ['subl', self.file_path]
        else:
            return f"Unsupported editor: {self.editor}. Please choose 'vscode' or 'sublime'."

        try:
            subprocess.run(editor_command, check=True)
            return f"Opened {self.file_path} in {self.editor}."
        except subprocess.CalledProcessError as e:
            return f"Failed to open {self.file_path} in {self.editor}. Error: {str(e)}"

# Example usage:
# tool = CodeEditorTool(file_path='/path/to/code.py', editor='vscode')
# result = tool.run()
# print(result)