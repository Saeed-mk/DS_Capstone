# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
        ],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),
    
    html.Br(),
    
    html.Div(id='success-pie-chart'),  # Placeholder for pie chart
    
    html.Br(),
    
    html.P("Payload range (Kg):"),
    
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={min_payload: str(min_payload), max_payload: str(max_payload)},
        value=[min_payload, max_payload]
    ),
    
    html.Div(id='success-payload-scatter-chart'),  # Placeholder for scatter chart
])

# Callback for updating the pie chart
@app.callback(
    Output('success-pie-chart', 'children'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', title='Total Successful Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title=f'Successful Launches for {entered_site}')
    
    return dcc.Graph(figure=fig)

# Callback for updating the scatter chart
@app.callback(
    Output('success-payload-scatter-chart', 'children'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def update_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                        title='Payload vs. Launch Success for All Sites')
    else:
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(site_filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                        title=f'Payload vs. Launch Success for {entered_site}')
    
    return dcc.Graph(figure=fig)

# Run the app
if __name__ == '__main__':
    app.run_server()
