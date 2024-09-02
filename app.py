from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
import subprocess
import json  # Import JSON module

app = Flask(__name__)

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('coffee.db')
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grind_size TEXT,
            portion INTEGER,
            water_temp INTEGER,
            brew_time INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Ensure init_db is called before every request
@app.before_request
def before_request():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_settings():
    data = request.json
    conn = sqlite3.connect('coffee.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO settings (grind_size, portion, water_temp, brew_time) VALUES (?, ?, ?, ?)', 
                   (data['grind_size'], data['portion'], data['water_temp'], data['brew_time']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Settings saved!"})

# Endpoint to get entries from the database
@app.route('/api/entries', methods=['GET'])
def get_entries():
    conn = sqlite3.connect('coffee.db')
    cursor = conn.cursor()
    cursor.execute('SELECT grind_size, portion, water_temp, brew_time FROM settings')
    rows = cursor.fetchall()
    conn.close()
    
    entries = [{'grind_size': row[0], 'portion': row[1], 'water_temp': row[2], 'brew_time': row[3]} for row in rows]
    return jsonify(entries)

@app.route('/analyze', methods=['GET'])
def analyze_data():
    # Fetch data from SQLite database
    conn = sqlite3.connect('coffee.db')
    df = pd.read_sql_query("SELECT * FROM settings", conn)
    conn.close()
    
    # Save the DataFrame to a CSV file that will be passed to the R script
    df.to_csv('input_data.csv', index=False)
    
    # Run the R script and capture the output
    result = subprocess.run(
        ['Rscript', 'analyze_coffee.R'],
        input=open('input_data.csv').read(),
        text=True,
        capture_output=True
    )
    
    # Parse the JSON result from R and ensure it is a valid JSON object
    try:
        analysis_results = json.loads(result.stdout)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse analysis results."}), 500

    return jsonify(analysis_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
