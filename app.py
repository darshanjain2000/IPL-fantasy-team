from logic import final_data,htmlOutput
from flask import Flask, json, request,redirect,render_template

api=Flask(__name__,template_folder='template')


@api.route('/')
def default():
    return render_template('index.html')

@api.route('/tool',methods=['POST','GET'])
def webTool():
    value=request.form    
    t1 = value['team1']
    t2 = value['team2']
    city =value['venue']
    t1=int(t1)
    t2=int(t2)
    city=int(city)
    if(t1==t2):
        return ("Both teams cannot be same. Please do it again.")
    
    total_matches,h2h_wins,key_players,toss_match_win_count,tmw_decision,match_win_decision,mean = htmlOutput(t1,t2,city)
    
    return render_template('webTool.html',
                           total_matches=total_matches,
                           
#                            h2h_wins=h2h_wins,
                           tables1=[h2h_wins.to_html(classes='data')], titles1=h2h_wins.columns.values,
                           
#                            key_players=key_players,
                           tables2=[key_players.to_html(classes='data')], titles2=key_players.columns.values,
                           
                           toss_match_win_count=toss_match_win_count,
                           
#                            tmw_decision=tmw_decision,
                           tables3=[tmw_decision.to_html(classes='data')], titles3=tmw_decision.columns.values,
                           
#                            match_win_decision=match_win_decision,
                           tables4=[match_win_decision.to_html(classes='data')], titles4=match_win_decision.columns.values,
                           
                           runrate=mean)

@api.route('/api')
def apiOption():
    return render_template('apiOption.html')

@api.route('/predict', methods=['GET'])
def server_api():

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

    result=final_data(t1,t2,city)
    # result=t1
    print(result)
    return json.dumps(result)

if __name__ == '__main__':
    api.run()
