# Check Installation
command -v databricks

# Add Path
PATH=/home/brijeshdhaker/.vscode/extensions/databricks.databricks-2.11.0-linux-x64/bin/databricks

# Check Version
databricks -v
Databricks CLI v1.2.0

# Method 1: Interactive CLI Configuration (Recommended)
databricks configure --profile DEFAULT

# Check the active authentication configuration
databricks auth env --profile DEFAULT

# Alternatively, test access by listing workspace roots
databricks fs ls

# Login
databricks auth login --profile databricks-cli

databricks auth describe --profile databricks-cli

databricks auth token --profile databricks-cli

databricks current-user me --profile databricks-oauth

#
databricks workspace list /Workspace/Users/brijeshdhaker@gmail.com/apps/mcp-builder-app --profile databricks-pat

# Download the app files to your computer:
databricks workspace export-dir /Workspace/Users/brijeshdhaker@gmail.com/apps/mcp-builder-app .

# Sync your changes:
databricks sync --watch . /Workspace/Users/brijeshdhaker@gmail.com/apps/mcp-builder-app

# Deploy to Databricks Apps:
databricks apps deploy mcp-builder-app --source-code-path /Workspace/Users/brijeshdhaker@gmail.com/apps/mcp-builder-app

# Show Details
databricks apps list --profile databricks-pat --output json
databricks apps get mcp-builder-app --profile databricks-pat --output json