import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------------------------------
# PREPARING THE DATA FOR ANALYSIS

df0 = pd.read_csv('/YourFilePathHere/ViewingActivity.csv')
df = df0

# Dropping the columns that are not needed
df = df.drop(['Profile Name', 'Attributes', 'Supplemental Video Type', 'Bookmark', 'Latest Bookmark',
              'Country', 'Device Type'], axis=1)

# Change the 'Start Time' to a 'datetime' data type
df['Start Time'] = pd.to_datetime(df['Start Time'])

# Split the Start Time column into four new columns (day, month, year, time)
df['Day'] = df['Start Time'].dt.day
df['Month'] = df['Start Time'].dt.month
df['Year'] = df['Start Time'].dt.year
df['Time'] = df['Start Time'].dt.time

# Find out which weekday it is and add a new column for that
# Drop the Start Time column
df['Weekday'] = df['Start Time'].dt.day_name()
df = df.drop(['Start Time'], axis=1)

# Change 'Duration' to a timedelta format
df['Duration'] = pd.to_timedelta(df['Duration'])

# Take only the rows in which the Duration is greater than 00:15:00
# as we don't want to include any Trailers or Shows that weren't finished
df = df[df['Duration']> '0 days 00:15:00']

# Split the Title column to create columns for the Number of Season and the Episode Name
df[['Film Title', '# of Season', 'Episode Name']] = df['Title'].str.split(':', 2, expand=True)
df = df.drop(['Title'], axis=1)


# -----------------------------------------------------------------------------------------------------
# ANALYSIS

# How many unique films and or series have been watched
films_unique = df['Film Title'].unique()
len_films_unique = len(films_unique)

# How much time (in hours, whole number) was spend watching Netflix
df['Duration in Hours'] = df['Duration'].dt.total_seconds()
df['Duration in Hours'] = df['Duration in Hours']/3600
duration_hours = int(df['Duration in Hours'].sum())

# A pie chart that shows the overall percentage distribution of days of the week that Netflix was watched.
# This includes all years (in this case: 2015-2022)
pie_chart = px.pie(df['Weekday'], names='Weekday', hole=.4,
                   title='A Week of Watching Netflix',
                   color_discrete_sequence=px.colors.qualitative.Pastel,
                   )
pie_chart.update_traces(textposition='inside', textinfo='percent+label', textfont_size=10)
pie_chart.update_layout(title_x=0.5)

# A table that shows the top 10 post watched films/series throughout all years (2015-2022)
# based on the overall time watched (overall "duration")
top10 = df.groupby(['Film Title'])['Duration'].sum().nlargest(10)
top10_as_string = top10.astype(str)

table = go.Figure(data=[go.Table(
    header=dict(values=('Title', 'Total Time Watched'),
                fill_color='#dfd7ca',
                line_color='#dfd7ca',
                align='left'),
    cells=dict(values=[top10.index, top10_as_string],
               fill_color='white',
               line_color='#dfd7ca',
               align='left'),
)])
table.update_layout(title_text="Top 10 Series", title_x=0.5)

# A line chart that showcases my Netflix behaviour through the years.
year_clustered = df.groupby('Year').sum().reset_index()
line_chart = px.line(year_clustered, x='Year', y='Duration in Hours',
                     title='Watching Netflix Through The Years')
line_chart.update_layout(title_x=0.5, plot_bgcolor='#FBF9F9')
line_chart.update_traces(line_color="#66c5cc", line_width=3)


# -----------------------------------------------------------------------------------------------------
# APP LAYOUT

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

app.layout = dbc.Container(html.Div([

    dbc.Row(
        dbc.Col(html.Div([
            html.H1('My Netflix Dashboard', style={'text-align': 'center', 'marginTop': 55}),
            html.H4('Looking at the Years 02/2015 - 01/2022',
                    style={'text-align': 'center', 'marginTop': 10, 'paddingBottom': 50})
        ]))
    ),

    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                        html.H3(len_films_unique, className="display-3"),
                        html.H4("unique films or series watched."),
                    ],
                    className="h-10 p-5 border rounded-3",
                ),
                md=6, ),

            dbc.Col(
                html.Div(
                    [
                        html.H3(duration_hours, className="display-3"),
                        html.H4("hours watched in total."),
                    ],
                    className="h-10 p-5 border rounded-3",
                ),
                md=6,
            ),

        ]
    ),

    dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=table)),
            dbc.Col(dcc.Graph(figure=pie_chart)),
        ]
    ),

    dbc.Row(
        dbc.Col(dcc.Graph(figure=line_chart))
    ),

    dbc.Row(
        dbc.Col(html.Div([
            dcc.Graph(id="netflix_per_month")])
        )
    ),

    dbc.Row(
        dbc.Col(html.Div([
            html.Br(),
            html.P('Choose a year:', style={'text-align': 'center'}),
            dcc.Dropdown(
                id='dropdown_year',
                options=[
                    {'label': "2015", 'value': 2015},
                    {'label': "2016", 'value': 2016},
                    {'label': "2017", 'value': 2017},
                    {'label': "2018", 'value': 2018},
                    {'label': "2019", 'value': 2019},
                    {'label': "2020", 'value': 2020},
                    {'label': "2021", 'value': 2021},
                    {'label': "2022", 'value': 2022},
                    ],
                value=2018,
                style={'width': '40%', 'display': 'block', 'margin-left': 'auto',
                       'margin-right': 'auto', 'text-align': 'center'}
            ),
        ])
        )
    ),

    dbc.Row(
        dbc.Col([
            html.Br(),
            html.P('© Kathrin Hälbich, 2022',
                   style={'text-align': 'center', 'marginTop': 80,
                          'paddingBottom': 50, 'color': '#D6DBDF'})
        ])
    )

]))


# -----------------------------------------------------------------------------------------------------
# CONNECT THE GRAPHS WITH DASH COMPONENTS

@app.callback(
    Output(component_id="netflix_per_month", component_property="figure"),
    [Input(component_id="dropdown_year", component_property="value")]
)
def update_graph(year):
    month_cluster = df.loc[df['Year'] == year].groupby('Month').sum().reset_index()
    fig = px.bar(month_cluster, x="Month", y="Duration in Hours",
                 title='Monthly Time Spend Watching Netflix', height=500)
    fig.update_xaxes(tickvals=[1,2,3,4,5,6,7,8,9,10,11,12], range=[0,13],
                     ticktext=["January", "February", "March", "April", "May", "June",
                               "July", "August", "September", "October", "November", "December"])
    fig.update_layout(title_x=0.5, xaxis_tickangle=-45, plot_bgcolor="white", margin_pad=10)
    fig.update_traces(marker_color=px.colors.qualitative.Pastel)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
