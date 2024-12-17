import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# ตั้งค่าฟอนต์สำหรับภาษาไทย
plt.rcParams['font.family'] = 'tahoma'

# การเชื่อมต่อ MySQL
username = 'root'
password = 'rootpassword'
host = 'localhost'
database = 'mydb'
connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}/{database}"
engine = create_engine(connection_string)


# Connect to the MySQL database and fetch data

def fetch_data():
    query = '''
    SELECT
        MONTH(Service_Date) AS month, 
        COUNT(CASE WHEN TitleName IN ('นาย ','หญิง','นายแพทย์','แพทย์หญิง','นางสาว','ว่าที่ร้อยตรีหญิง') THEN 1 END) AS layperson,  
        COUNT(CASE WHEN TitleName IN ('พระภิกษุ ','พระมหา','พระปลัด','พระครูสมุห์','พระอธิการ','พระครูใบฎีกา','พระครูสังฆรักษ์','พระครูวนัยธร','สามเณร') THEN 1 END) AS Monk 
    FROM clinicvisit
    WHERE Service_Date BETWEEN '2020-01-01' AND '2024-12-31'
    GROUP BY month
    ORDER BY month
    '''
    df = pd.read_sql(query, engine)
    return df


df = fetch_data()

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Monthly Clinic Visit Dashboard", style={'text-align': 'center', 'color': '#0078D7'}),

    # Graphs and metrics
    html.Div([
        dcc.Graph(id='monthly-bar'),
    ], style={'display': 'flex', 'justify-content': 'space-around'}),
])


# Callback to update the graph
@app.callback(
    Output('monthly-bar', 'figure'),
    Input('monthly-bar', 'id')
)
def update_dashboard(_):
    # Refresh data from the database
    df = fetch_data()

    # Bar chart for layperson and monks
    bar_fig = px.bar(
        df,
        x='month',
        y=['layperson', 'Monk'],
        title='Monthly Clinic Visits by Layperson and Monks',
        labels={'value': 'Number of Visits', 'month': 'Month'},
        barmode='group',
        color_discrete_sequence=['#636EFA', '#EF553B']
    )

    return bar_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
