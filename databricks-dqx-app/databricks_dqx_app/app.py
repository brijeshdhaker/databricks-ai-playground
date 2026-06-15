# app.py
# python databricks_dqx_app/app.py
# databricks apps run-local --prepare-environment --debug
# databricks sync --watch . /Workspace/Users/someone@example.com/databricks_apps/dash-hello-world_2025_12_05-21_35/dash-hello-world-app
# databricks apps deploy dash-hello-world --source-code-path /Workspace/Users/someone@example.com/databricks_apps/dash-hello-world_2025_12_05-21_35/dash-hello-world-app
# 
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
from databricks.connect.session import DatabricksSession
from pyspark.sql.functions import col

spark = DatabricksSession.builder.serverless().getOrCreate()

# Data transformations with Spark in Python
df = spark.read.table("samples.nyctaxi.trips") \
    .select('trip_distance', 'fare_amount') \
    .filter(col('trip_distance') < 10) \
    .limit(1000)
    

chart_data = df.toPandas()

# Initialize the Dash app with Bootstrap styling
dash_app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
dash_app.layout = dbc.Container([
    dbc.Row([dbc.Col(html.H1('Trip cost by distance'), width=12)]),
    dcc.Graph(
        id='fare-scatter',
        figure=px.scatter(chart_data, x='trip_distance', y='fare_amount',
            labels={'trip_distance': 'Trip distance (miles)', 'fare_amount': 'Fare amount (USD)'},
            template='simple_white'),
        style={'height': '500px', 'width': '1000px'}
    )
], fluid=True)

if __name__ == '__main__':
    print("Hello from databricks-dqx-app !!")
    dash_app.run(debug=True)