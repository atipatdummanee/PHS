from dash import Dash, html, dcc
import plotly.express as px

# ข้อมูลตัวอย่าง
df = px.data.gapminder()

# สร้างกราฟ Scatter Plot
scatter_fig = px.scatter(
    df[df['year'] == 2007],
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=50
)

# สร้างกราฟ Line Plot
line_fig = px.line(
    df[df['continent'] == 'Asia'],
    x="year",
    y="lifeExp",
    color="country",
    title="Life Expectancy Over Time (Asia)"
)

# สร้างกราฟ Bar Chart
bar_fig = px.bar(
    df[df['year'] == 2007],
    x="continent",
    y="pop",
    color="continent",
    title="Population by Continent"
)

# สร้างแอป Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("แดชบอร์ดตัวอย่างด้วย Dash", style={"textAlign": "center"}),

    html.Div([
        dcc.Graph(
            id='scatter-plot',
            figure=scatter_fig
        ),
        dcc.Graph(
            id='line-plot',
            figure=line_fig
        ),
        dcc.Graph(
            id='bar-chart',
            figure=bar_fig
        ),
    ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"})
])

if __name__ == '__main__':
    app.run_server(debug=True)
