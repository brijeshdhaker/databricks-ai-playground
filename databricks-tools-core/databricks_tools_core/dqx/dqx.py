"""
DQX Execution

High-level functions for generating DQX Rules on Databricks.
"""

import logging
from typing import Any, Dict, List, Optional
from .dqx_utils.executor import DQXExecutor, DQXExecutionError
from .warehouse import get_best_warehouse

logger = logging.getLogger(__name__)




def generate_rule(
    rule_query: str,
    warehouse_id: Optional[str] = None,
    catalog: Optional[str] = None,
    schema: Optional[str] = None,
    timeout: int = 180,
    query_tags: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Generate a DQX Rules on a Databricks Unity Catalog Warehouse.

    If no warehouse_id is provided, automatically selects the best available
    warehouse using get_best_warehouse().

    Args:
        sql_query: SQL query to execute
        warehouse_id: Optional warehouse ID. If not provided, auto-selects one.
        catalog: Optional catalog context. If not provided, use fully qualified names.
        schema: Optional schema context. If not provided, use fully qualified names.
        timeout: Timeout in seconds (default: 180)
        query_tags: Optional query tags for cost attribution and filtering.
            Format: "key:value,key2:value2" (e.g., "team:eng,cost_center:701").
            Appears in system.query.history and Query History UI.

    Returns:
        List of dictionaries, each representing a row with column names as keys.
        Example: [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

    Raises:
        SQLExecutionError: If query execution fails, with detailed error message:
            - No warehouse available
            - Warehouse not accessible
            - Query syntax error
            - Query timeout
            - Permission denied
    """
    # Auto-select warehouse if not provided
    if not warehouse_id:
        logger.debug("No warehouse_id provided, selecting best available warehouse")
        warehouse_id = get_best_warehouse()
        if not warehouse_id:
            raise DQXExecutionError(
                "No SQL warehouse available in the workspace. "
                "Please create a SQL warehouse or start an existing one, "
                "or provide a specific warehouse_id."
            )
        logger.debug(f"Auto-selected warehouse: {warehouse_id}")

    # Execute the query
    executor = DQXExecutor(warehouse_id=warehouse_id)
    return executor.generate_rule(
        rule_query=rule_query,
        catalog=catalog,
        schema=schema,
        timeout=timeout,
        query_tags=query_tags,
    )