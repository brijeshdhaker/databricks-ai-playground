"""
Integration tests for SQL execution functions.

Tests:
- execute_sql
- execute_sql_multi
"""

import pytest
from databricks_tools_core.dqx.dqx import generate_rule, DQXExecutionError


@pytest.mark.integration
class TestGenerateRule:
    """Tests for generate_rule function."""

    def test_generate_rule(self, warehouse_id):
        """Should generate a simple DQX Rule."""

        user_input = """
        Username should not start with 's' if age is less than 18.
        All users must have a valid email address.
        Age should be between 0 and 120.
        """
        result = generate_rule(
            rule_query=user_input,
            warehouse_id=warehouse_id,
            catalog="data_quality",
            schema="default"
        )

        assert isinstance(result, str)
        assert len(result) == 1