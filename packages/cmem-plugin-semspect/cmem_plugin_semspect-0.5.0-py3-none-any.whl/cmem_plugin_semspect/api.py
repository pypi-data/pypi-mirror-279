"""SemSpect API."""

from datetime import datetime

from pydantic import BaseModel, Field
from requests import request


class Index(BaseModel):
    """SemSpect Database Index"""

    status: str
    timestamp: datetime
    description: str
    directory: str = Field(alias="indexDirectory")


class Operation(BaseModel):
    """SemSpect Database Operation"""

    id: str = Field(alias="operationId")
    status: str
    timestamp: datetime
    description: str


class Database(BaseModel):
    """SemSpect Database"""

    id: str
    data_version: str = Field(alias="dataVersion")
    index: Index
    operations: list[Operation]


class Client:
    """SemSpect API client"""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_databases(self) -> dict[str, Database]:
        """Get all databases."""
        response = request("GET", f"{self.base_url}/api/database", timeout=5)
        response.raise_for_status()
        content: dict = response.json()
        result: dict[str, Database] = {}
        for _ in content["databases"]:
            database = Database(**_)
            key = database.id
            result[key] = database
        return result

    def get_database(self, database_id: str) -> Database:
        """Get a specific database."""
        return self.get_databases()[database_id]

    def get_operation(self, operation_id: str) -> Operation:
        """Get a specific operation."""
        databases = self.get_databases()
        for database in databases.values():
            for operation in database.operations:
                if operation.id == operation_id:
                    return operation
        raise KeyError(f"Operation with id {operation_id} not found.")

    def update_database(self, database: Database, url: str, description: str) -> Operation:
        """Request to update a database.

        returns an operation

        Example: curl -X PUT 'http://docker.localhost:8080/semspect/api/database/cmem/content'
            -H 'Content-Type: application/json'
            --data-binary '{
                "dataSources": ["https://download.eccenca.com/ontologies/prod.fibo-quickstart-2022Q3.ttl"],
                "description" : "test dataset"
                }'
        """
        headers = {"Content-Type": "application/json"}
        data = '{"dataSources": ["' + url + '"], "description" : "' + description + '"}'
        response = request(
            "PUT",
            f"{self.base_url}/api/database/{database.id}/content",
            headers=headers,
            data=data,
            timeout=5,
        )
        response.raise_for_status()
        return Operation(**response.json())
