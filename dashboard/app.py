import os
from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json
import trimesh
from urllib.parse import unquote

app = Flask(__name__)

# Load the jet data
jet_data = pd.read_csv('jet_data.csv')

@app.route('/')
def index():
    return render_template('index.html', jet_models=jet_data['Jet Model'].tolist())

@app.route('/get_jet_data')
def get_jet_data():
    return jsonify(jet_data.to_dict('records'))

@app.route('/altitude_speed_chart')
def altitude_speed_chart():
    fig = go.Figure(data=go.Scatter(
        x=jet_data['Max Speed (km/h)'],
        y=jet_data['Altitude Limit (ft)'],
        mode='markers',
        text=jet_data['Jet Model'],
        marker=dict(size=10, color=jet_data['Max Speed (km/h)'], colorscale='Viridis', showscale=True)
    ))
    fig.update_layout(title='Altitude vs Speed', xaxis_title='Max Speed (km/h)', yaxis_title='Altitude Limit (ft)')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/flight_range_chart')
def flight_range_chart():
    fig = go.Figure(data=[
        go.Bar(name='Flight Time', x=jet_data['Jet Model'], y=jet_data['Flight Time (hours)']),
        go.Bar(name='Range', x=jet_data['Jet Model'], y=jet_data['Range (km)'])
    ])
    fig.update_layout(title='Flight Time and Range', barmode='group')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/usage_pie_chart')
def usage_pie_chart():
    fig = go.Figure(data=[go.Pie(labels=jet_data['Jet Usage'], values=jet_data['Jet Usage'].value_counts())])
    fig.update_layout(title='Jet Usage Distribution')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/radar_chart')
def radar_chart():
    categories = ['Max Speed', 'Altitude Limit', 'Range', 'Fuel Capacity', 'Flight Time', 'Fuel Efficiency']
    fig = go.Figure()

    for _, jet in jet_data.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[jet['Max Speed (km/h)'], jet['Altitude Limit (ft)'], jet['Range (km)'],
               jet['Fuel Capacity (liters)'], jet['Flight Time (hours)'], jet['Fuel Efficiency (km/liter)']],
            theta=categories,
            fill='toself',
            name=jet['Jet Model']
        ))

    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, title='Jet Performance Comparison')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/get_3d_model/<jet_model>')
def get_3d_model(jet_model):
    jet_model = unquote(jet_model)
    # Construct the file path
    model_path = os.path.join('models', f'{jet_model}.glb')
    print(f"Looking for model at: {model_path}")

    # Check if the file exists
    if not os.path.exists(model_path):
        return jsonify({'error': 'Model not found'}), 404
    
    # Load the GLB file
    try:
        mesh = trimesh.load(model_path)
        
        # Extract vertices and faces
        vertices = mesh.vertices.tolist()
        faces = mesh.faces.tolist()
        
        return jsonify({
            'vertices': vertices,
            'faces': faces
        })
    except Exception as e:
        print(f"Error loading model: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
