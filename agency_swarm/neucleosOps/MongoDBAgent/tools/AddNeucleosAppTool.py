from agency_swarm.tools import BaseTool
from pydantic import Field
from pymongo import MongoClient
import os
from datetime import datetime

class AddNeucleosAppTool(BaseTool):
    """
    A tool for adding a new Neucleos app to the MongoDB database.
    """

    app_name: str = Field(..., description="The name of the new Neucleos app")
    app_description: str = Field(..., description="A brief description of the new Neucleos app")
    multiple_instance: bool = Field(..., description="Whether multiple instances of this app are allowed")

    def run(self):
        """
        Adds a new Neucleos app to the MongoDB database.
        """
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