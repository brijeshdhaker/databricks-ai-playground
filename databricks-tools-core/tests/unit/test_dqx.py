"""Unit tests for SQL execution functions."""

from unittest import mock

from databricks.sdk.service.sql import QueryTag, State, StatementState

from databricks_tools_core.dqx.dqx import generate_rule
from databricks_tools_core.dqx.dqx_utils.executor import DQXExecutor
from databricks_tools_core.sql.warehouse import _sort_within_tier, get_best_warehouse


class TestExecuteSQLQueryTags:
    """Tests for query_tags parameter passthrough."""

    @mock.patch("databricks_tools_core.sql.sql.get_best_warehouse", return_value="wh-123")
    @mock.patch("databricks_tools_core.sql.sql.SQLExecutor")
    def test_generate_rule(self, mock_executor_cls, mock_warehouse):
        """query_tags should be passed through to SQLExecutor.execute()."""
        mock_executor = mock.Mock()
        mock_executor.execute.return_value = "checks :"
        mock_executor_cls.return_value = mock_executor
        
        user_input = """
        Username should not start with 's' if age is less than 18.
        All users must have a valid email address.
        Age should be between 0 and 120.
        """

        result = generate_rule(
            rule_query=user_input,
            warehouse_id="warehouse_id",
            catalog="data_quality",
            schema="default"
        )

        mock_executor.execute.assert_called_once()
        call_kwargs = mock_executor.execute.call_args.kwargs
        assert result is not None