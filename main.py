import requests

from flask import Flask, render_template
import plotly.graph_objs as go

app = Flask(__name__)


@app.route('/')
def index():
    # API endpoint and API key
    url = "https://api.covidactnow.org/v2/states.json"
    api_key = "5691f53393414fef847d4fa1e784495e"

    # Make the API request
    response = requests.get(url, params={"apiKey": api_key})

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()

        # Extract relevant data for charts
        states = [state_data["state"] for state_data in data]
        cases = [state_data["actuals"]["cases"] for state_data in data]
        deaths = [state_data["actuals"]["deaths"] for state_data in data]
        vaccinations_initiated = [
            state_data["metrics"]["vaccinationsInitiatedRatio"] for state_data in data]

        # Create Plotly bar chart for cases
        cases_chart = go.Bar(x=states, y=cases, name='Total Cases')
        cases_layout = go.Layout(
            title='Total COVID-19 Cases', barmode='group', width=1000, height=600)
        cases_fig = go.Figure(data=[cases_chart], layout=cases_layout)
        cases_html = cases_fig.to_html(full_html=False)

        # Create Plotly bar chart for deaths
        deaths_chart = go.Bar(x=states, y=deaths, name='Total Deaths')
        deaths_layout = go.Layout(
            title='Total COVID-19 Deaths', barmode='group', width=800, height=500)
        deaths_fig = go.Figure(data=[deaths_chart], layout=deaths_layout)
        deaths_html = deaths_fig.to_html(full_html=False)

        # Create Plotly bar chart for vaccinations initiated
        vaccinations_chart = go.Bar(
            x=states, y=vaccinations_initiated, name='Vaccinations Initiated Ratio')
        vaccinations_layout = go.Layout(
            title='Vaccinations Initiated Ratio', barmode='group', width=1200, height=700)
        vaccinations_fig = go.Figure(
            data=[vaccinations_chart], layout=vaccinations_layout)
        vaccinations_html = vaccinations_fig.to_html(full_html=False)

        return render_template('index.html', cases_html=cases_html, deaths_html=deaths_html, vaccinations_html=vaccinations_html)
    else:
        return "Error fetching data from API"


if __name__ == '__main__':
    app.run(debug=True)
