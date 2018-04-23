import dash
import numpy as np
import pandas as pd
import simplejson as js
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv('volcano_db.csv', encoding='latin-1')

with open('token.txt', 'r') as tk:
	token = tk.read()

for index, row in df.iterrows():
    if row['Last Known'] == '?':
        df.drop(index, inplace=True)

status = []
for i in df.Status:
    if i not in status:
        status.append(i)

def clustering(strata):
	categorise = []
	for index, row in df.iterrows():
		if row['Status'] == strata:
			categorise.append(row)
	lats = list(pd.DataFrame(categorise)['Latitude'])
	lons = list(pd.DataFrame(categorise)['Longitude'])
	last_name = list(pd.DataFrame(categorise)['Volcano Name'])
	return lats, lons, last_name

lava = {}
for i in status:
	lava.update({i : [j for j in df]})

app.layout = html.Div([
	html.Div([
		html.H3('Volcanic Mountains')
	], style={'textAlign' : 'center'}),
	dcc.Dropdown(
		id='categories',
		options=[{'label' : s,'value' : s} for s in lava.keys()],
		placeholder='Volcano type -here: ',
		#value=['Anthropology'],
		multi=False,
	),
	dcc.Graph(id='volcano_plot')
])
@app.callback(
	Output('volcano_plot', 'figure'),
	[Input('categories', 'value')]
)

def map_plotter(strata):
	try:
		graphs = [] 
		for st in strata:
			lats, lons, last_name = clustering(strata)
			graphs.append(go.Scattermapbox(
					lat=lats,
					lon=lons,
					mode='marker',
					marker=go.Marker(
						size=6,
						color='rgb(255, 0, 0)',
						opacity=0.7
					),
				text=last_name,
				hoverinfo='text'
				)
			)

		layout = go.Layout(
			height=700,
			#width=500,
			title='Volcanoes',
			autosize=True,
			hovermode='closest',
			showlegend=False,
			mapbox = dict(
				accesstoken=token,
				bearing=0,
				pitch=0,
				zoom=0.6,
				style='light'
			),
		)

		fig = {'data' : graphs, 'layout' : layout}
		return fig

	except Exception as e:
		with open('errors.txt', 'w') as error:
			error.write(str(e))
			#print(str(e))

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
for css in external_css:
	app.css.append_css({'external_url' : css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})

if __name__ == '__main__':
	app.run_server(debug=True)