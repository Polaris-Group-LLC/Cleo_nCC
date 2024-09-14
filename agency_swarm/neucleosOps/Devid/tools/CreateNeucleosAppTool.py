from agency_swarm.tools import BaseTool
from pydantic import Field
from pymongo import MongoClient
from datetime import datetime
import os

class CreateNeucleosAppTool(BaseTool):
    """
    A tool for creating a new Neucleos app, adding it to the MongoDB database,
    creating the necessary files, and updating the TabPanel.tsx file.
    """

    app_name: str = Field(..., description="The name of the new Neucleos app")
    app_description: str = Field(..., description="A brief description of the new Neucleos app")
    multiple_instance: bool = Field(..., description="Whether multiple instances of this app are allowed")

    def run(self):
        # Step 1: Create app folder and files
        folder_result = self._create_app_folder()
        
        # Step 2: Add to MongoDB
        mongo_result = self._add_to_mongodb()
        
        # Step 3: Update TabPanel.tsx
        tab_panel_result = self._update_tab_panel()
        
        return f"{folder_result}\n{mongo_result}\n{tab_panel_result}"

    def _create_app_folder(self):
        base_path = "/Users/god/1d/frontend/neucleosApps"
        app_folder_name = self.app_name.replace(" ", "")
        app_folder_path = os.path.join(base_path, app_folder_name)
        
        # Create the app folder
        os.makedirs(app_folder_path, exist_ok=True)
        
        # Create the main app file
        main_file_path = os.path.join(app_folder_path, f"{app_folder_name}.tsx")
        with open(main_file_path, 'w') as f:
            f.write(f"""
import React from 'react';

export const {app_folder_name} = () => {{
  return (
    <div>
      <h1>{self.app_name}</h1>
      <p>{self.app_description}</p>
    </div>
  );
}};
""")
        
        return f"Created app folder and main file at {app_folder_path}"

    def _add_to_mongodb(self):
        # MongoDB connection details
        mongo_uri = "mongodb+srv://jaybo:neucleos1@cluster0.uxqj69t.mongodb.net/"
        database_name = "Neucleos-apps"
        collection_name = "app-library"

        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]

        # Create new app document
        new_app = {
            "appName": self.app_name,
            "description": self.app_description,
            "componentName": self.app_name.replace(" ", ""),
            "renderLocation": "Main",
            "version": "1.0.0",
            "multipleInstance": str(self.multiple_instance).lower(),
            "category": "core",
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "iconSVG": '<svg xmlns="http://www.w3.org/2000/svg" width="1.09rem" height="1rem" viewBox="0 0 256 237"><path fill="#217CAF" d="M200.325 125.27c-30.749 0-55.675 24.927-55.675 55.677s24.926 55.677 55.675 55.677S256 211.696 256 180.947c0-30.75-24.926-55.677-55.675-55.677m-144.65.005C24.927 125.275 0 150.197 0 180.947s24.927 55.677 55.675 55.677c30.75 0 55.678-24.928 55.678-55.677c0-30.75-24.928-55.672-55.678-55.672m128-69.6c0 30.75-24.927 55.68-55.674 55.68c-30.75 0-55.676-24.93-55.676-55.68C72.325 24.928 97.25 0 128 0c30.747 0 55.673 24.93 55.673 55.674"/></svg>'
        }

        # Insert the new app into the database
        result = collection.insert_one(new_app)

        # Close the MongoDB connection
        client.close()

        if result.inserted_id:
            return f"Successfully added new Neucleos app '{self.app_name}' with ID: {result.inserted_id}"
        else:
            return "Failed to add new Neucleos app"

    def _update_tab_panel(self):
        file_path = "/Users/god/1d/frontend/components/ui/Cockpit/TabPanel.tsx"
        with open(file_path, 'r') as file:
            content = file.read()

        component_name = self.app_name.replace(" ", "")
        tab_name = self.app_name.lower().replace(" ", "_")
        import_path = f"@/neucleosApps/{component_name}/{component_name}"

        # Add new import statement
        import_statement = f"import {{ {component_name} }} from '{import_path}';"
        content = import_statement + '\n' + content

        # Update tabComponents object
        tab_component_entry = f"{tab_name}: {component_name},"
        content = content.replace("const tabComponents: Record<string, React.ComponentType> = {",
                                  f"const tabComponents: Record<string, React.ComponentType> = {{\n  {tab_component_entry}")

        # Add new TabsTrigger
        tabs_trigger = f"<TabsTrigger value=\"{tab_name}\">{self.app_name}</TabsTrigger>"
        content = content.replace("</TabsList>", f"{tabs_trigger}\n        </TabsList>")

        # Add new TabsContent
        tabs_content = f"<TabsContent value=\"{tab_name}\">\n          <{component_name} />\n        </TabsContent>"
        content = content.replace("</Tabs>", f"{tabs_content}\n      </Tabs>")

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(content)

        return f"Successfully updated TabPanel.tsx to include the new app: {self.app_name}"