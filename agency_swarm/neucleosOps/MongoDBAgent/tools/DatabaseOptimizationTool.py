from agency_swarm.tools import BaseTool
from pydantic import Field
import pymongo
import os

class DatabaseOptimizationTool(BaseTool):
    """
    A tool that enables the MongoDBAgent to optimize MongoDB databases by analyzing query performance and suggesting indexes.
    It provides actionable insights to improve database efficiency by integrating with MongoDB's query profiler and index suggestions.
    """

    mongo_uri: str = Field(
        ..., description="The MongoDB connection URI."
    )
    database_name: str = Field(
        ..., description="The name of the MongoDB database to optimize."
    )
    collection_name: str = Field(
        ..., description="The name of the MongoDB collection to analyze."
    )

    def run(self):
        """
        Optimizes the MongoDB database by analyzing query performance and suggesting indexes.
        """
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.database_name]
        collection = db[self.collection_name]

        # Enable the query profiler
        db.command({"profile": 2})

        # Analyze query performance
        slow_queries = self._get_slow_queries(db)

        # Suggest indexes based on slow queries
        index_suggestions = self._suggest_indexes(slow_queries)

        # Disable the query profiler
        db.command({"profile": 0})

        return {
            "slow_queries": slow_queries,
            "index_suggestions": index_suggestions
        }

    def _get_slow_queries(self, db):
        """
        Retrieves slow queries from the MongoDB profiler.
        """
        profiler_data = db.system.profile.find({"millis": {"$gt": 100}}).sort("millis", pymongo.DESCENDING)
        slow_queries = []
        for entry in profiler_data:
            slow_queries.append({
                "query": entry.get("query"),
                "millis": entry.get("millis"),
                "ns": entry.get("ns"),
                "op": entry.get("op"),
                "command": entry.get("command")
            })
        return slow_queries

    def _suggest_indexes(self, slow_queries):
        """
        Suggests indexes based on slow queries.
        """
        index_suggestions = []
        for query in slow_queries:
            if "query" in query:
                for field in query["query"]:
                    index_suggestions.append({
                        "collection": query["ns"],
                        "index": {field: 1}
                    })
            elif "command" in query and "filter" in query["command"]:
                for field in query["command"]["filter"]:
                    index_suggestions.append({
                        "collection": query["ns"],
                        "index": {field: 1}
                    })
        return index_suggestions

# Example usage:
# tool = DatabaseOptimizationTool(
#     mongo_uri=os.getenv('MONGO_URI'),
#     database_name='myDatabase',
#     collection_name='myCollection'
# )
# result = tool.run()
# print(result)