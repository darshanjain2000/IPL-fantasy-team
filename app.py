# from logic import final_data,htmlOutput
from flask import Flask, json, request,redirect,render_template

api=Flask(__name__,template_folder='template')

ipl_teams = ["Chennai Super Kings","Delhi Capitals","Kolkata Knight Riders","Mumbai Indians","Kings XI Punjab","Rajasthan Royals","Royal Challengers Bangalore","Sunrisers Hyderabad"]
cities = ['Bangalore', 'Kochi', 'Chennai', 'Centurion', 'Ranchi', 'Mumbai', 'Ahmedabad', 'Durban', 'Kolkata', 'Cape Town', 'Dharamsala', 'Sharjah', 'Johannesburg', 'Kimberley', 'Pune', 'Delhi', 'Raipur', 'Chandigarh', 'Nagpur', 'Abu Dhabi', 'Bloemfontein', 'Kanpur', 'Hyderabad', 'Rajkot', 'Port Elizabeth', 'Dubai', 'Indore', 'Cuttack', 'East London', 'Jaipur', 'Visakhapatnam']

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
    
    # assign value to variable from function calls parent function
    total_matches, h2h_wins, key_players, toss_match_win_count, tmw_decision,\
    match_win_decision, mean, t1_topbat, t1_topbowl, t2_topbat, t2_topbowl,\
    team_pc,team_pc2,rr_team,rr_team2\
    = htmlOutput(t1,t2,city)
    
    return render_template('webTool.html',team1=ipl_teams[t1-1],team2=ipl_teams[t2-1],venue=cities[city-1],
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
                           
                           runrate=mean,
                           
                           tables5=[t1_topbat.to_html(classes='data')], titles5=t1_topbat.columns.values,
                           tables6=[t1_topbowl.to_html(classes='data')], titles6=t1_topbowl.columns.values,
                           tables7=[t2_topbat.to_html(classes='data')], titles7=t2_topbat.columns.values,
                           tables8=[t2_topbowl.to_html(classes='data')], titles8=t2_topbowl.columns.values,
                           
                           team_pc=team_pc,
                           team_pc2=team_pc2,
                           
                           rr_team=rr_team,
                           rr_team2=rr_team2)

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
