"""
DQX Executor - Internal class for executing SQL queries on Databricks.
"""

import time
import logging
from typing import Any, Dict, List, Optional

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import StatementState
#
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.labs.dqx.config import InputConfig

from ...auth import get_workspace_client

logger = logging.getLogger(__name__)


class DQXExecutionError(Exception):
    """Exception raised when SQL execution fails.

    Provides detailed error messages for LLM consumption.
    """

class DQXExecutor:
    """Generate SQL queries on Databricks SQL Warehouses."""
    """Execute SQL queries on Databricks SQL Warehouses."""

    def __init__(self, warehouse_id: str, client: Optional[WorkspaceClient] = None):
        """
        Initialize the SQL executor.

        Args:
            warehouse_id: SQL warehouse ID to use for queries
            client: Optional WorkspaceClient (creates new one if not provided)

        Raises:
            SQLExecutionError: If no warehouse ID is provided
        """
        if not warehouse_id:
            raise DQXExecutionError(
                "No SQL warehouse ID provided. "
                "Either specify a warehouse_id or let the system select one automatically."
            )
        self.warehouse_id = warehouse_id
        self.client = client or get_workspace_client()

    def generate_rule(
        self,
        rule_query: str,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
        row_limit: Optional[int] = None,
        timeout: int = 180,
        query_tags: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate a DQX query quality rules from a natural language description:.

        Args:
            sql_query: SQL query to execute
            catalog: Optional catalog context for the query
            schema: Optional schema context for the query
            row_limit: Optional maximum number of rows to return
            timeout: Timeout in seconds (default: 180)
            query_tags: Optional query tags for cost attribution and filtering.
                Format: "key:value,key2:value2" (e.g., "team:eng,cost_center:701").
                Appears in system.query.history and Query History UI.

        Returns:
            List of generated dqx rules

        Raises:
            DQXExecutionError: If query execution fails with detailed error message
        """
        logger.debug(f"Executing DQX Rule query: {rule_query[:100]}...")

        # Build execution parameters
        exec_params = {
            "warehouse_id": self.warehouse_id,
            "statement": rule_query,
            "wait_timeout": "0s",  # Immediate return, we poll manually
        }
        if catalog:
            exec_params["catalog"] = catalog
        if schema:
            exec_params["schema"] = schema
        if row_limit is not None:
            exec_params["row_limit"] = row_limit
        if query_tags:
            from databricks.sdk.service.sql import QueryTag

            exec_params["query_tags"] = [
                QueryTag(key=k.strip(), value=v.strip())
                for pair in query_tags.split(",")
                for k, v in [pair.split(":", 1)]
                if ":" in pair
            ]

        # Submit the rule query
        try:
            from databricks.connect import DatabricksSession
            spark = DatabricksSession.builder.getOrCreate()
            ws = self.client
            generator = DQGenerator(workspace_client=ws) #, spark=spark
            checks = generator.generate_dq_rules_ai_assisted(
                user_input=rule_query,
                input_config=InputConfig(location=f"{catalog}.{schema}.customers")
            )
            response = checks
            #response = self.client.statement_execution.execute_statement(**exec_params)
        except Exception as e:
            raise DQXExecutionError(
                f"Failed to submit SQL query to warehouse '{self.warehouse_id}': {str(e)}. "
                f"Check that the warehouse exists and is accessible."
            )

        logger.debug(f"Generated DQX Rule: {response}")

        # Poll for completion
        poll_interval = 2
        elapsed = 0

        while elapsed < timeout:
            # Still running, wait and poll again
            time.sleep(poll_interval)
            elapsed += poll_interval

        # Timeout reached - cancel the statement
        #self._cancel_statement(statement_id)
        raise DQXExecutionError(
            f"SQL query timed out after {timeout} seconds and was canceled. "
            f"Consider increasing the timeout or optimizing the query. "
        )    