# -*- coding: utf-8 -*-
"""
Created on Thu May 16 11:47:00 2024

@author: SimoneBruno
"""

#libs go here
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_table

import plotly.graph_objects as go

#%%
#import files here
df = pd.read_excel(r"C:\Users\SimoneBruno\OneDrive - ICMA\Simone\55) QT plotly\master sheet .xlsx")

df['Date'] = pd.to_datetime(df['Date']).dt.strftime("%Y-%m-%d")



df.iloc[:, 1:] *= 1000000

#%%
# #start the app here

# # Get the list of columns excluding 'Date'
# columns = df.columns[1:]

# # Initialize the Dash app
# app = Dash(__name__)

# # Define the layout of the app
# app.layout = html.Div([
#     html.H1("Interactive PSPP, CSPP and PEPP Chart"),
#     html.P("Use the below dropdown to select the facility to plot"),
#     dcc.Dropdown(
#         id='column-selector',
#         options=[{'label': col, 'value': col} for col in columns],
#         value=columns.tolist(),
#         multi=True
#     ),
#     html.P("Select dates below or zoom on the chart"),
#     dcc.DatePickerRange(
#         id='date-picker',
#         min_date_allowed=df['Date'].min(),
#         max_date_allowed=df['Date'].max(),
#         start_date=df['Date'].min(),
#         end_date=df['Date'].max(),
#     ),
#     dcc.Graph(id='bar-chart'),
#     html.H2("Selected Dates Table"),
#     html.H3("Change dates and dropdown above to update table"),
#     dash_table.DataTable(id='data-table', 
#                          columns=[{"name": i, "id": i} for i in df.columns],
#                          data=df.to_dict('records'))
# ])

# # Define the callback to update the chart and table based on selected columns and date range
# @app.callback(
#     [Output('bar-chart', 'figure'),
#      Output('data-table', 'columns'),
#      Output('data-table', 'data')],
#     [Input('column-selector', 'value'),
#      Input('date-picker', 'start_date'),
#      Input('date-picker', 'end_date')]
# )
# def update_chart_and_table(selected_columns, start_date, end_date):
#     if not selected_columns:
#         selected_columns = columns  # Fallback to all columns if none selected

#     # Filter data based on the selected date range
#     filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

#     # Update the stacked bar chart
#     fig = px.bar(filtered_df, x='Date', y=selected_columns, title="Holdings Over Time")
    
#     # Update the data table
#     table_columns = [{"name": "Date", "id": "Date"}] + [{"name": col, "id": col} for col in selected_columns]
#     table_data = filtered_df[["Date"] + selected_columns].to_dict('records')
    
#     return fig, table_columns, table_data

# # Run the app on port 8051
# if __name__ == '__main__':
#     app.run_server(debug=True, port=8051)
    
#%%
    
# Get the list of columns excluding 'Date'
columns = df.columns[1:]

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Interactive PSPP, CSPP and PEPP Chart"),
    html.P("Use the below dropdown to select the facility to plot"),
    dcc.Dropdown(
        id='column-selector',
        options=[{'label': col, 'value': col} for col in columns],
        value=columns.tolist(),
        multi=True
    ),
    html.P("Select dates below or zoom on the chart"),
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=df['Date'].min(),
        max_date_allowed=df['Date'].max(),
        start_date=df['Date'].min(),
        end_date=df['Date'].max(),
    ),
    html.P("Tick the box below to show the sum of the selected facilities above"),
    dcc.Checklist(
        id='line-checkbox',
        options=[{'label': 'Show Sum Line', 'value': 'sum-line'}],
        value=[]
    ),
    dcc.Graph(id='bar-chart'),
    html.H2("Selected Dates Table"),
    html.H3("Change dates and dropdown above to update table"),
    dash_table.DataTable(id='data-table', 
                         columns=[{"name": i, "id": i} for i in df.columns],
                         data=df.to_dict('records'))
])

# Define the callback to update the chart and table based on selected columns and date range
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('data-table', 'columns'),
     Output('data-table', 'data')],
    [Input('column-selector', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('line-checkbox', 'value')]
)
def update_chart_and_table(selected_columns, start_date, end_date, show_sum_line):
    if not selected_columns:
        selected_columns = columns  # Fallback to all columns if none selected

    print("Selected columns:", selected_columns)
    print("Start date:", start_date)
    print("End date:", end_date)
    print("Show Sum Line:", show_sum_line)

    # Filter data based on the selected date range
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    

    # Update the stacked bar chart
    fig = px.bar(filtered_df, x='Date', y=selected_columns, title="Holdings Over Time")
    fig.update_yaxes(title_text="Holdings in €")
    
    # If 'Show Sum Line' checkbox is checked, add a line chart showing the sum of the selected columns
    if 'sum-line' in show_sum_line:
        sum_series = filtered_df[selected_columns].sum(axis=1)
        fig.add_trace(go.Scatter(x=filtered_df['Date'], y=sum_series, mode='lines', name='Sum'))

    print("Figure:", fig)

    # Update the data table
    table_columns = [{"name": "Date", "id": "Date"}] + [{"name": col, "id": col} for col in selected_columns]
    table_data = filtered_df[["Date"] + selected_columns].to_dict('records')
    
    return fig, table_columns, table_data

# Run the app on port 8051
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
