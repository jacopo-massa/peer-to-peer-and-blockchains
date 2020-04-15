"""
Module to plot the data collected from the logger (main.py)
"""

import os
import webbrowser
from ast import literal_eval
from collections import Counter
from threading import Timer

import dash
import dash_core_components as dcc
import dash_html_components as dhc
import dash_table as dt
import pandas
import plotly.express as px
import plotly.graph_objects as go

from utils import DASH_PORT, DASH_ADDRESS, CSV_PATH, IMG_PATH

try:
    data = pandas.read_csv(CSV_PATH)
except FileNotFoundError:
    raise SystemExit("Can't find log file!")

# create the dataframe from the rows of the csv file (set path in utils.py)
df = pandas.DataFrame(data)

# convert the protocols from string representation to the 'literal' one (so python list)
df.protocols = df.protocols.apply(literal_eval)

# remove seconds from timestamp
df.timestamp = df.timestamp.apply(lambda t: t[:t.rfind(":")])

# group data by timestamp, performing some aggregation functions
df_timestamp_groups = df.groupby(['timestamp'], as_index=False)
df_timestamp = df_timestamp_groups.agg({'peer': 'count', 'latency': 'mean'})

# remove duplicate peers, to make stats on unique peers
df_no_dup = df.drop_duplicates(subset='peer', keep="first")
df_regions = df_no_dup.groupby(['country'], as_index=False).count()

""" COUNTRY WORLD - World map with peer-sized bubbles """
country_world = px.scatter_geo(df_regions,
                               locationmode='country names', locations="country", size_max=30,
                               hover_name="country", hover_data=['peer'], size="peer", color="country",
                               width=1200, height=600, title="Unique peers: location")

""" COUNTRY PIE - Pie chart with peer percentages by country """
country_pie = px.pie(df_regions, values="peer", names='country',
                     title="Unique peers: distribution per country")
# region_pie.update_layout(autosize=False, width=450, height=450)

""" HOUR-DAILY - Bar chart showing the variation of latency and number of peers , for each collected timestamp """
timestamp_bars = go.Figure(data=[
    go.Bar(name='Peers', x=df_timestamp.timestamp, y=df_timestamp.peer),
    go.Bar(name='Latency (ms)', x=df_timestamp.timestamp, y=df_timestamp.latency)
])
timestamp_bars.update_layout(barmode='group', bargroupgap=0.1,
                             title='Hour-daily behaviour', xaxis=dict(title_text="Time"))

""" AVG-HOUR - Bar chart showing the average variation of latency and number of peers , grouped by hour """
df_timestamp['dtime'] = pandas.to_datetime(df_timestamp['timestamp'])
df_timestamp['hour'] = df_timestamp['dtime'].dt.hour
df_avg_hour_groups = df_timestamp.groupby(['hour'], as_index=False)
df_avg_hour = df_avg_hour_groups.agg({'peer': 'mean', 'latency': 'mean'})

avg_hour_bars = go.Figure(data=[
    go.Bar(name='Peers', x=df_avg_hour.hour, y=df_avg_hour.peer),
    go.Bar(name='Latency (ms)', x=df_avg_hour.hour, y=df_avg_hour.latency)
])
avg_hour_bars.update_layout(barmode='group', bargroupgap=0.1,
                            title='Average-hour behaviour', xaxis=dict(title_text="Hour"))

""" PROTOCOL LINE - Line chart showing the variation of protocols used by peers """
protocol_names = list(set(x for sublist in df.protocols.to_list() for x in sublist))
df_protocols = pandas.DataFrame(columns=['timestamp', 'protocol', 'size'])
for name, group in df_timestamp_groups:
    protocol_group = Counter(x for sublist in group.protocols.to_list() for x in sublist)
    for prot in protocol_names:
        df_protocols = df_protocols.append({'timestamp': name, 'protocol': prot, 'size': 0}, ignore_index=True)
    for prot, sz in protocol_group.items():
        df_protocols.loc[(df_protocols['timestamp'] == name) & (df_protocols['protocol'] == prot), ['size']] = sz

protocol_scatter = px.line(df_protocols, x='timestamp', y='size', color='protocol',
                           line_group='protocol', line_dash='protocol',
                           labels={'timestamp': 'Time', 'size': 'Peers'},
                           hover_name='protocol', title='Protocol usage variation')

""" GENERAL STATS - Table with statistics on the whole swarm, and on the unique peers"""
tot_peers = df['peer'].count()
unq_peers = df_no_dup['peer'].count()

tot_latency = round(df['latency'].mean(), 4)
unq_latency = round(df_no_dup['latency'].mean(), 4)

df_tot_conn = df.groupby(['direction'], as_index=False)['peer'].count()
tot_ingoing = df_tot_conn['peer'][0]
tot_outgoing = df_tot_conn['peer'][1]

df_unq_conn = df_no_dup.groupby(['direction'], as_index=False)['peer'].count()
unq_ingoing = df_unq_conn['peer'][0]
unq_outgoing = df_unq_conn['peer'][1]

fields = ['Peers (unique): ', 'Ingoing connections (unique)']
stats_table = dt.DataTable(id='general_stats',
                           style_header={'fontWeight': 'bold'},
                           style_cell={'textAlign': 'center'},
                           style_data_conditional=[{
                               'if': {'column_id': 'data'},
                               'fontWeight': 'bold'}],
                           columns=[{'name': 'Data', 'id': 'data'},
                                    {'name': 'Tot. peers', 'id': 'total'},
                                    {'name': 'Unique peers', 'id': 'unique'}],
                           data=[{'data': 'Number of peers', 'total': tot_peers, 'unique': unq_peers},
                                 {'data': 'Ingoing Connections', 'total': tot_ingoing, 'unique': unq_ingoing},
                                 {'data': 'Outgoing Connections', 'total': tot_outgoing, 'unique': unq_outgoing},
                                 {'data': 'AVG Latency (ms)', 'total': tot_latency, 'unique': unq_latency}])

""" TITLE & PERIOD OF ANALYSIS - Html components """
title_page = dhc.H1("Monitoring the Interplanetary File System (IPFS)")
period = dhc.P(dcc.Markdown("Data collected from **{}** to **{}**"
                            .format(df_timestamp['timestamp'].min(), df_timestamp['timestamp'].max())))

# Setup the Flask app to show an html page containing all the plots.
app = dash.Dash()
app.title = "IPFS Analysis"
app.layout = dhc.Div([
    title_page, period,
    dhc.Div(stats_table, style={'display': 'inline-block', 'width': '50%'}),
    dhc.Div(dcc.Graph(id="country_world", figure=country_world)),
    dhc.Div(dcc.Graph(id="country_pie", figure=country_pie)),
    dhc.Div(dcc.Graph(id="timestamp_bars", figure=timestamp_bars)),
    dhc.Div(dcc.Graph(id="avg_hour_bars", figure=avg_hour_bars)),
    dhc.Div(dcc.Graph(id="protocol_scatter", figure=protocol_scatter))
])

if __name__ == '__main__':
    # create directory to save plots
    if not os.path.exists(IMG_PATH):
        os.mkdir(IMG_PATH)

    # generate single plots as html pages
    country_world.write_html(os.path.join(IMG_PATH, "country_world.html"))
    country_pie.write_html(os.path.join(IMG_PATH, "country_pie.html"))
    timestamp_bars.write_html(os.path.join(IMG_PATH, "hour_daily_behaviour.html"))
    avg_hour_bars.write_html(os.path.join(IMG_PATH, "avg_hour_behaviour.html"))
    protocol_scatter.write_html(os.path.join(IMG_PATH, "protocols.html"))

    # wait on second, then open the web page on which the Flask app is running.
    Timer(1, webbrowser.open_new_tab, args=[DASH_ADDRESS]).start()
    app.run_server(port=DASH_PORT)
