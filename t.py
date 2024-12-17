import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Sample data for dashboard
data = {
    'Ward': ['ICU', 'General', 'Maternity', 'Pediatrics'],
    'Patients': [15, 45, 30, 25],
    'Doctors': [5, 10, 7, 6],
    'Beds_Available': [5, 15, 10, 12]
}

df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Hospital Dashboard", style={'text-align': 'center', 'color': '#0078D7'}),

    # Dropdown for selecting wards
    dcc.Dropdown(
        id='ward-selector',
        options=[{'label': ward, 'value': ward} for ward in df['Ward']],
        value='ICU',
        style={'width': '50%', 'margin': '0 auto'}
    ),

    html.Br(),

    # Graphs and metrics
    html.Div([
        dcc.Graph(id='patient-bar'),
        dcc.Graph(id='bed-pie'),
    ], style={'display': 'flex', 'justify-content': 'space-around'}),

    html.Div(id='ward-summary', style={'text-align': 'center', 'font-size': '18px'})
])

# Callbacks for interactivity
@app.callback(
    [Output('patient-bar', 'figure'),
     Output('bed-pie', 'figure'),
     Output('ward-summary', 'children')],
    Input('ward-selector', 'value')
)
def update_dashboard(selected_ward):
    # Filter data for the selected ward
    ward_data = df[df['Ward'] == selected_ward].iloc[0]

    # Bar chart for number of patients and doctors
    bar_fig = px.bar(
        x=['Patients', 'Doctors'],
        y=[ward_data['Patients'], ward_data['Doctors']],
        title=f'Patients and Doctors in {selected_ward}',
        labels={'x': 'Category', 'y': 'Count'},
        color_discrete_sequence=['#636EFA']
    )

    # Pie chart for beds available
    pie_fig = px.pie(
        names=['Beds Used', 'Beds Available'],
        values=[ward_data['Patients'], ward_data['Beds_Available']],
        title=f'Bed Availability in {selected_ward}',
        color_discrete_sequence=['#EF553B', '#00CC96']
    )

    # Summary text
    summary = (f"In {selected_ward}, there are {ward_data['Patients']} patients, "
               f"{ward_data['Doctors']} doctors, and {ward_data['Beds_Available']} beds available.")

    return bar_fig, pie_fig, summary

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
