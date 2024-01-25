from flask import Flask, request, jsonify
import pandas as pd
from utils import *

app = Flask(__name__)

@app.route("/")
def home():
    return "use /provisions_calculator_api/?current_energy=55&current_hydration=55&goal_energy=98&goal_hydration=98"

@app.route("/provisions_calculator_api/")
def provisions_calculator_api():
    query = request.args.to_dict()
    query = {k: int(v) for k, v in query.items()}
    current_energy = query['current_energy']
    current_hydration = query['current_hydration']
    goal_energy = query['goal_energy']
    goal_hydration = query['goal_hydration']

    df = pd.read_csv('current_items.csv')
    response = best_to_consume_df(current_energy, current_hydration, goal_energy, goal_hydration, df)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

