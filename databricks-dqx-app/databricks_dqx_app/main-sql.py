from databricks.sql.client import Connection, List, Row
import os
#
from databricks_dqx_app.helpers import get_connection_personal_access_token, select_nyctaxi_trips

#
connection: Connection = get_connection_personal_access_token(
    server_hostname = os.getenv("DATABRICKS_HOST"),
    http_path = os.getenv("DATABRICKS_HTTP_PATH"),
    access_token = os.getenv("DATABRICKS_TOKEN")
)

#
rows: List[Row] = select_nyctaxi_trips(
    connection = connection,
    num_rows = 2
)

for row in rows:
    print(row)