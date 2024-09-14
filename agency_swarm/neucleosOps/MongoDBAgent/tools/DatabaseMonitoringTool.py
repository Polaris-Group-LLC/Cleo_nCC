from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

class DatabaseMonitoringTool(BaseTool):
    """
    A tool that allows the MongoDBAgent to monitor the performance and health of MongoDB databases.
    It provides real-time metrics and alerts for issues like slow queries, high memory usage, and replication lag.
    Integrates with monitoring platforms like MongoDB Atlas or Prometheus to provide comprehensive monitoring capabilities.
    """

    platform: str = Field(
        ..., description="The monitoring platform to use. Options are 'mongodb_atlas' or 'prometheus'."
    )
    database_name: str = Field(
        ..., description="The name of the MongoDB database to monitor."
    )
    access_token: str = Field(
        ..., description="The access token for authenticating with the chosen platform."
    )
    cluster_id: str = Field(
        default=None, description="The MongoDB Atlas cluster ID, if using MongoDB Atlas."
    )
    prometheus_url: str = Field(
        default=None, description="The Prometheus server URL, if using Prometheus."
    )

    def run(self):
        """
        Monitors the performance and health of the MongoDB database using the chosen platform.
        """
        if self.platform.lower() == 'mongodb_atlas':
            return self._monitor_with_mongodb_atlas()
        elif self.platform.lower() == 'prometheus':
            return self._monitor_with_prometheus()
        else:
            return f"Unsupported platform: {self.platform}. Please choose 'mongodb_atlas' or 'prometheus'."

    def _monitor_with_mongodb_atlas(self):
        """
        Monitors the MongoDB database using MongoDB Atlas.
        """
        if not self.cluster_id:
            return "Cluster ID is required for MongoDB Atlas monitoring."

        api_url = f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{self.cluster_id}/processes/{self.database_name}/measurements"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        params = {
            "granularity": "PT1M",
            "period": "PT1H",
            "m": ["QUERY_EXECUTOR", "MEMORY", "OPCOUNTER", "REPLICATION"]
        }

        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            metrics = response.json()
            return f"MongoDB Atlas metrics for {self.database_name}:\n{metrics}"
        else:
            return f"Failed to retrieve MongoDB Atlas metrics. Error: {response.json()}"

    def _monitor_with_prometheus(self):
        """
        Monitors the MongoDB database using Prometheus.
        """
        if not self.prometheus_url:
            return "Prometheus server URL is required for Prometheus monitoring."

        queries = {
            "slow_queries": 'sum(rate(mongodb_mongod_op_latencies_latency_total{type="read"}[1m])) by (instance)',
            "high_memory_usage": 'sum(rate(mongodb_mongod_mem_resident_bytes[1m])) by (instance)',
            "replication_lag": 'max(mongodb_mongod_replset_member_replication_lag_seconds) by (instance)'
        }

        metrics = {}
        for metric_name, query in queries.items():
            response = requests.get(f"{self.prometheus_url}/api/v1/query", params={"query": query})
            if response.status_code == 200:
                result = response.json().get('data', {}).get('result', [])
                metrics[metric_name] = result
            else:
                metrics[metric_name] = f"Failed to retrieve {metric_name}. Error: {response.json()}"

        return f"Prometheus metrics for {self.database_name}:\n{metrics}"

# Example usage:
# tool = DatabaseMonitoringTool(
#     platform='mongodb_atlas',
#     database_name='myDatabase',
#     access_token=os.getenv('MONGODB_ATLAS_ACCESS_TOKEN'),
#     cluster_id='myClusterId'
# )
# result = tool.run()
# print(result)