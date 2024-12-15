from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# ข้อมูลตัวอย่าง
df = px.data.gapminder()

# สร้างกราฟ
fig = px.scatter(
    df[df['year'] == 2007],
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60
)

# สร้างแอป Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("ตัวอย่างแดชบอร์ดด้วย Dash"),
    dcc.Graph(
        id='scatter-plot',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
