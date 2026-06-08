# Method 1: Interactive CLI Configuration (Recommended)
databricks configure --profile DEFAULT

# Check the active authentication configuration
databricks auth env --profile DEFAULT

# Alternatively, test access by listing workspace roots
databricks fs ls