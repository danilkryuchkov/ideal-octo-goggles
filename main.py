from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/provisions_calculator_api/")
def provisions_calculator_api():
    query = request.args.to_dict()
    query = {k: int(v) for k, v in query.items()}
    current_energy = query['current_energy']
    current_hydration = query['current_hydration']
    energy_difference = query['energy_difference']
    hydration_difference = query['hydration_difference']
    




if __name__ == '__main__':
    app.run(debug=True)

