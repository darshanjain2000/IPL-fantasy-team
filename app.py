# from typing_extensions import final
from flask import Flask, json, request
from logic import final_data

api = Flask(__name__)

@api.route('/predict', methods=['GET'])

def get_prediction():

    # endpoint/predict?team1=1&team2=2&city=3
    t1 = request.args.get('team1', None)
    t2 = request.args.get('team2', None)
    city = request.args.get('city', None)
    t1=int(t1)
    t2=int(t2)
    city=int(city)

    if(t1<1 or t1>8 or t2<1 or t2>8 or 31< city <1):
        return ("Invalid Choice. Please enter again.")
    elif(t1==t2):
        return ("Both teams cannot be same. Please select again.")

    # result=final_data(t1,t2,city)
    result=t1
    return json.dumps(result)

if __name__ == '__main__':
    api.run()