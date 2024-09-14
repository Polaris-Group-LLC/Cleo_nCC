from agency_swarm.tools import BaseTool
from pydantic import Field
import subprocess

class DebuggerTool(BaseTool):
    """
    A tool that allows the DevelopmentAgent to debug code by setting breakpoints, stepping through code, and inspecting variables.
    It integrates with IDEs like IntelliJ IDEA or Eclipse to provide a comprehensive debugging experience.
    """

    file_path: str = Field(
        ..., description="The path to the code file that needs to be debugged."
    )
    line_number: int = Field(
        ..., description="The line number where the breakpoint should be set."
    )
    ide: str = Field(
        ..., description="The IDE to use for debugging. Options are 'intellij' or 'eclipse'."
    )

    def run(self):
        """
        Sets a breakpoint at the specified line in the given file and starts the debugger in the chosen IDE.
        """
        if self.ide.lower() == 'intellij':
            ide_command = [
                'idea', 'debug', '--file', self.file_path, '--line', str(self.line_number)
            ]
        elif self.ide.lower() == 'eclipse':
            ide_command = [
                'eclipse', '-debug', self.file_path, '-line', str(self.line_number)
            ]
        else:
            return f"Unsupported IDE: {self.ide}. Please choose 'intellij' or 'eclipse'."

        try:
            subprocess.run(ide_command, check=True)
            return f"Started debugging {self.file_path} at line {self.line_number} in {self.ide}."
        except subprocess.CalledProcessError as e:
            return f"Failed to start debugging {self.file_path} in {self.ide}. Error: {str(e)}"

# Example usage:
# tool = DebuggerTool(file_path='/path/to/code.py', line_number=42, ide='intellij')
# result = tool.run()
# print(result)