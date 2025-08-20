# app.py
from flask import Flask, render_template, request, jsonify
# from indeed import scrape_site1
from naukri import scrape_naukri
from timesjobs import scrape_tj
from glassdoor import scrape_foundit
import pandas as pd

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    text1 = data.get('text1', '')

    if text1:
        info_site1 = scrape_naukri(text1)
        info_site2 = scrape_foundit(text1)
        info_site3 = scrape_tj(text1)

        combined_info = info_site1 + info_site2 + info_site3
        export_to_csv(combined_info)
        return jsonify({'success': True, 'message': 'Scraping complete'})
    else:
        return jsonify({'success': False, 'message': 'Speech not recognized'})


@app.route('/results')
def results():
    df = pd.read_csv("data.csv")
    info = df.to_dict(orient='records') if not df.empty else []
    return render_template('results.html', info=info)


def export_to_csv(results):
    df = pd.DataFrame(results)
   # df.to_csv("data.csv", mode="w", index=False)
    try:
        existing_data = pd.read_csv("data.csv", nrows=0)
        if not existing_data.empty:
            df.to_csv("data.csv", mode="w", index=False, header=False)
        else:
            df.to_csv("data.csv", mode="w", index=False, header=True)
    except FileNotFoundError:
        df.to_csv("data.csv", mode="w", index=False, header=True)


@app.route('/visualize')
def visualize():
    df = pd.read_csv("data.csv")
    df['skills'] = df['skills'].str.lower()
    json_data = df.to_json(orient='records')
    # Write JSON data to a file
    with open("static/data.json", "w") as json_file:
        json_file.write(json_data)
    # Render the template with the path to the JSON file
    return render_template('emptyrr.html', json_data_url="/static/data.json")

@app.route('/visualizedrilldown')
def visualizedrilldown():
    df = pd.read_csv("data.csv")
    df['skills'] = df['skills'].str.lower()
    json_data = df.to_json(orient='records')
    # Write JSON data to a file
    with open("static/data.json", "w") as json_file:
        json_file.write(json_data)
    # Render the template with the path to the JSON file
    return render_template('drilldown.html', json_data_url="/static/data.json")


@app.route('/visualizestackedbar')
def visualizestackedbar():
    df = pd.read_csv("data.csv")
    df['skills'] = df['skills'].str.lower()
    json_data = df.to_json(orient='records')
    # Write JSON data to a file
    with open("static/data.json", "w") as json_file:
        json_file.write(json_data)
    # Render the template with the path to the JSON file
    return render_template('stackedbar.html', json_data_url="/static/data.json")


@app.route('/visualizewordbubble')
def visualizewordbubble():
    df = pd.read_csv("data.csv")
    df['skills'] = df['skills'].str.lower()
    json_data = df.to_json(orient='records')
    # Write JSON data to a file
    with open("static/data.json", "w") as json_file:
        json_file.write(json_data)
    # Render the template with the path to the JSON file
    return render_template('wordbubble.html', json_data_url="/static/data.json")


if __name__ == "__main__":
    app.run(debug=True)
