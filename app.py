from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# I'm assuming that these are the 3 api's that we are going to call and I'm going to implement them
api_urls = [
    'http://127.0.0.1:5000/api1',
    'http://127.0.0.1:5000/api2',
    'http://127.0.0.1:5000/api3'
]

# For now these APIs are all returning static data
# for these 3 api's I'm accepting the member_id since it's part of the api requirement
# but since I'm responding with a static data I'm not really using the member_id
@app.route('/api1')
def api1():
    member_id = request.args.get('member_id')
    if not member_id:
        return jsonify({'error': 'Missing member_id'})
    return jsonify({'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000})

@app.route('/api2')
def api2():
    member_id = request.args.get('member_id')
    if not member_id:
        return jsonify({'error': 'Missing member_id'})
    return jsonify({'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000})

@app.route('/api3')
def api3():
    member_id = request.args.get('member_id')
    if not member_id:
        return jsonify({'error': 'Missing member_id'})
    return jsonify({'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000})


def average_strategy(responses):
    coalesced_data = {}
    for key in responses[0]:
        values = [r[key] for r in responses]
        coalesced_data[key] = sum(values) // len(values)
    return coalesced_data

def minimum_deductible_strategy(responses):
    deductible_values = [r['deductible'] for r in responses]
    min_deductible = min(deductible_values)
    min_deductible_responses = [r for r in responses if r['deductible'] == min_deductible]
    return min_deductible_responses[0]


# managing different strategies for coalescing here
# to add a new strategy we just add a new entry in this map like "minimum_deductible" and 
# add the implementatio
coalescing_strategies = {
    'average': average_strategy,
    'minimum_deductible': minimum_deductible_strategy
}


@app.route('/api/coalesce')
def coalesce():
    member_id = request.args.get('member_id')
    
    if not member_id:
        return jsonify({'error': 'Missing member_id'})
    responses = []

    # calling the 3 apis
    for url in api_urls:
        response = requests.get(url, params={'member_id': member_id})
        if response.status_code == 200:
            responses.append(response.json())

    # Coalesce the responses using the chosen strategy
    # the default would be average method
    strategy = request.args.get('strategy', 'average')
    if strategy in coalescing_strategies:
        coalesced_data = coalescing_strategies[strategy](responses)
    else:
        return jsonify({'error': 'Invalid coalescing strategy'})

    return jsonify(coalesced_data)



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
