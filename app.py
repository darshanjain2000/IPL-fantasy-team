from numpy import true_divide
from logic import final_data,htmlOutput
from flask import Flask, render_template, url_for, request, redirect, json
from utilities import predict
from utilities.predict import predict_score
# from utilities.predict import tree, forest, neural_nets
from utilities.predict import tree
from utilities.predict import MODEL_INFO



TEAM_CODE = [
				'Chennai Super Kings',
				# 'Deccan Chargers',
				'Delhi Capitals',
				# 'Delhi Daredevils',
				# 'Gujarat Lions',
				'Kings XI Punjab',
				# 'Kochi Tuskers Kerala',
				'Kolkata Knight Riders',
				'Mumbai Indians',
				# 'Pune Warriors',
				'Rajasthan Royals',
				# 'Rising Pune Supergiant',
				# 'Rising Pune Supergiants',
				'Royal Challengers Bangalore',
				'Sunrisers Hyderabad'
			 ]

VENUE_CODE = [
	'Bangalore', 
	'Kochi', 
	'Chennai', 
	'Centurion', 
	'Ranchi', 
	'Mumbai', 
	'Ahmedabad', 
	'Durban', 
	'Kolkata', 
	'Cape Town', 
	'Dharamsala', 
	'Sharjah', 
	'Johannesburg', 
	'Kimberley', 
	'Pune', 
	'Delhi', 
	'Raipur', 
	'Chandigarh', 
	'Nagpur', 
	'Abu Dhabi', 
	'Bloemfontein', 
	'Kanpur', 
	'Hyderabad', 
	'Rajkot', 
	'Port Elizabeth', 
	'Dubai', 
	'Indore', 
	'Cuttack', 
	'East London', 
	'Jaipur', 
	'Visakhapatnam'
	]

TOSS_WINNER = [
				'Chennai Super Kings',
				# 'Deccan Chargers',
				'Delhi Capitals',
				# 'Delhi Daredevils',
				# 'Gujarat Lions',
				'Kings XI Punjab',
				# 'Kochi Tuskers Kerala',
				'Kolkata Knight Riders',
				'Mumbai Indians',
				# 'Pune Warriors',
				'Rajasthan Royals',
				# 'Rising Pune Supergiant',
				# 'Rising Pune Supergiants',
				'Royal Challengers Bangalore',
				'Sunrisers Hyderabad'
			 ]

TOSS_DECISION = [
				'bat',
				'field'		
			 ]

MODELS = {
	# 'Random Forest Regressor' : forest,
	'Decision Tree Classifier' : tree,
	# 'Neural Networks Regression' : neural_nets
}

TEAM_CODE_new_team = [
				'Chennai Super Kings',
				'Delhi Capitals',
				'Gujarat Lions',
				'Punjab Kings',
				'Kolkata Knight Riders',
				'Mumbai Indians',
				'Rajasthan Royals',
				'Royal Challengers Bangalore',
				'Sunrisers Hyderabad'
			 ]

TOSS_WINNER_new_team = [
				'Chennai Super Kings',
				'Delhi Capitals',
				'Gujarat Lions',
				'Punjab Kings',
				'Kolkata Knight Riders',
				'Mumbai Indians',
				'Rajasthan Royals',
				'Royal Challengers Bangalore',
				'Sunrisers Hyderabad'
			 ]

VENUE_CODE_new_team = [
				'Barabati Stadium',
				'Brabourne Stadium',
				'Buffalo Park',
				'De Beers Diamond Oval',
				'Dr DY Patil Sports Academy',
				'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
				'Dubai International Cricket Stadium',
				'Eden Gardens',
				'Feroz Shah Kotla',
				'Green Park',
				'Himachal Pradesh Cricket Association Stadium',
				'Holkar Cricket Stadium',
				'JSCA International Stadium Complex',
				'Kingsmead',
				'M Chinnaswamy Stadium',
				'M.Chinnaswamy Stadium',
				'MA Chidambaram Stadium, Chepauk',
				'Maharashtra Cricket Association Stadium',
				'Nehru Stadium',
				'New Wanderers Stadium',
				'Newlands',
				'OUTsurance Oval',
				'Punjab Cricket Association IS Bindra Stadium, Mohali',
				'Punjab Cricket Association Stadium, Mohali',
				'Rajiv Gandhi International Stadium, Uppal',
				'Sardar Patel Stadium, Motera',
				'Saurashtra Cricket Association Stadium',
				'Sawai Mansingh Stadium',
				'Shaheed Veer Narayan Singh International Stadium',
				'Sharjah Cricket Stadium',
				'Sheikh Zayed Stadium',
				"St George's Park",
				'Subrata Roy Sahara Stadium',
				'SuperSport Park',
				'Vidarbha Cricket Association Stadium, Jamtha',
				'Wankhede Stadium'

]


predicted_score = None

app=Flask(__name__,template_folder='template')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/newTeam')
def indexNewTeam():
	return render_template('indexNew.html', teams=TEAM_CODE_new_team, venues =VENUE_CODE_new_team, toss_winners = TOSS_WINNER_new_team,toss_decisions = TOSS_DECISION , models=MODELS, score=predicted_score, info=MODEL_INFO)

@app.route('/predict', methods=['GET', 'POST'])
def prediction():
	global predicted_score
	if request.method == 'POST':
		req = request.form
		venue = req['venue']
		batting_team = req['batting_team']
		bowling_team = req['bowling_team']
		toss_winner = req['toss_winner']
		toss_decision = req['toss_decision']
		# runs = int(req['runs'])
		# overs = float(req['overs'])
		# wickets = int(req['wickets'])
		# runs_last_5 = int(req['runs_last_5'])
		# wickets_last_5 = int(req['wickets_last_5'])
		model = MODELS[req['model']]
		predicted_score = str(predict_score( venue,batting_team, bowling_team,toss_winner, toss_decision, model))
		return render_template('predict.html', score=predicted_score, info=dict(req), model=MODEL_INFO)
	else:
		return render_template('404.html', msg="500 No Prediction: Looks like you're here without a prediction.")

@app.route('/analyze',methods=['POST','GET'])
def webTool():

	value=request.form    
	t1 = value['team1']
	t2 = value['team2']
	venue =value['venue']

	if(t1==t2):
		return ("Both teams cannot be same. Please do it again.")
    # return render_template('webTool.html')

    # assign value to variable from function calls parent function
	# total_matches, h2h_wins, key_players, toss_match_win_count, tmw_decision,match_win_decision, mean, t1_topbat, t1_topbowl, t2_topbat, t2_topbowl,team_pc,team_pc2,rr_team,rr_team2 = htmlOutput(t1,t2,venue)

	hcode = True
	if(hcode):
		if(t1=='Chennai Super Kings' and t2== 'Delhi Capitals' and venue == 'Chennai'):
			return render_template('chennaiDelhi.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Chennai Super Kings' and t2== 'Kolkata Knight Riders' and venue == 'Chennai'):
			return render_template('chennaiKolkata.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Chennai Super Kings' and t2== 'Mumbai Indians' and venue == 'Chennai'):
			return render_template('chennaiMumbai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Chennai Super Kings' and t2== 'Kings XI Punjab' and venue == 'Chennai'):
			return render_template('chennaiPunjab.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Chennai Super Kings' and t2== 'Rajasthan Royals' and venue == 'Chennai'):
			return render_template('chennaiRajasthan.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Chennai Super Kings' and t2== 'Royal Challengers Bangalore' and venue == 'Chennai'):
			return render_template('chennaiBangalore.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Chennai Super Kings' and t2== 'Sunrisers Hyderabad' and venue == 'Chennai'):
			return render_template('chennaiHydrabad.html',team1=t1,team2=t2,venue=venue)

		elif(t1=='Delhi Capitals' and t2== 'Chennai Super Kings' and venue == 'Delhi'):
			return render_template('delhiChennai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Delhi Capitals' and t2== 'Kolkata Knight Riders' and venue == 'Delhi'):
			return render_template('delhiKolkata.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Delhi Capitals' and t2== 'Mumbai Indians' and venue == 'Delhi'):
			return render_template('delhiMumbai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Delhi Capitals' and t2== 'Kings XI Punjab' and venue == 'Delhi'):
			return render_template('delhiPunjab.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Delhi Capitals' and t2== 'Rajasthan Royals' and venue == 'Delhi'):
			return render_template('delhiRajasthan.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Delhi Capitals' and t2== 'Royal Challengers Bangalore' and venue == 'Delhi'):
			return render_template('delhiBangalore.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Delhi Capitals' and t2== 'Sunrisers Hyderabad' and venue == 'Delhi'):
			return render_template('delhiHydrabad.html',team1=t1,team2=t2,venue=venue)

		elif(t1=='Kolkata Knight Riders' and t2== 'Chennai Super Kings' and venue == 'Kolkata'):
			return render_template('kolkataChennai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Kolkata Knight Riders' and t2== 'Delhi Capitals' and venue == 'Kolkata'):
			return render_template('kolkataDelhi.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Kolkata Knight Riders' and t2== 'Mumbai Indians' and venue == 'Kolkata'):
			return render_template('kolkataMumbai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Kolkata Knight Riders' and t2== 'Kings XI Punjab' and venue == 'Kolkata'):
			return render_template('kolkataPunjab.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Kolkata Knight Riders' and t2== 'Rajasthan Royals' and venue == 'Kolkata'):
			return render_template('kolkataRajasthan.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Kolkata Knight Riders' and t2== 'Royal Challengers Bangalore' and venue == 'Kolkata'):
			return render_template('kolkataBangalore.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Kolkata Knight Riders' and t2== 'Sunrisers Hyderabad' and venue == 'Kolkata'):
			return render_template('kolkataHydrabad.html',team1=t1,team2=t2,venue=venue)

		elif(t1=='Mumbai Indians' and t2== 'Chennai Super Kings' and venue == 'Mumbai'):
			return render_template('mumbaiChennai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Mumbai Indians' and t2== 'Delhi Capitals' and venue == 'Mumbai'):
			return render_template('mumbaiDelhi.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Mumbai Indians' and t2== 'Kolkata Knight Riders' and venue == 'Mumbai'):
			return render_template('mumbaiKolkata.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Mumbai Indians' and t2== 'Kings XI Punjab' and venue == 'Mumbai'):
			return render_template('mumbaiPunjab.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Mumbai Indians' and t2== 'Rajasthan Royals' and venue == 'Mumbai'):
			return render_template('mumbaiRajasthan.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Mumbai Indians' and t2== 'Royal Challengers Bangalore' and venue == 'Mumbai'):
			return render_template('mumbaiBangalore.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Mumbai Indians' and t2== 'Sunrisers Hyderabad' and venue == 'Mumbai'):
			return render_template('mumbaiHydrabad.html',team1=t1,team2=t2,venue=venue)

		elif(t1=='Kings XI Punjab' and t2== 'Chennai Super Kings' and venue == 'Chandigarh'):
			return render_template('punjabChennai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Kings XI Punjab' and t2== 'Delhi Capitals' and venue == 'Chandigarh'):
			return render_template('punjabDelhi.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Kings XI Punjab' and t2== 'Kolkata Knight Riders' and venue == 'Chandigarh'):
			return render_template('punjabKolkata.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Kings XI Punjab' and t2== 'Mumbai Indians' and venue == 'Chandigarh'):
			return render_template('punjabMumbai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Kings XI Punjab' and t2== 'Rajasthan Royals' and venue == 'Chandigarh'):
			return render_template('punjabRajasthan.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Kings XI Punjab' and t2== 'Royal Challengers Bangalore' and venue == 'Chandigarh'):
			return render_template('punjabBangalore.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Kings XI Punjab' and t2== 'Sunrisers Hyderabad' and venue == 'Chandigarh'):
			return render_template('punjabHydrabad.html',team1=t1,team2=t2,venue=venue)

		elif(t1=='Rajasthan Royals' and t2== 'Chennai Super Kings' and venue == 'Jaipur'):
			return render_template('rajasthanChennai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Rajasthan Royals' and t2== 'Delhi Capitals' and venue == 'Jaipur'):
			return render_template('rajasthanDelhi.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Rajasthan Royals' and t2== 'Kolkata Knight Riders' and venue == 'Jaipur'):
			return render_template('rajasthanKolkata.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Rajasthan Royals' and t2== 'Mumbai Indians' and venue == 'Jaipur'):
			return render_template('rajasthanMumbai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Rajasthan Royals' and t2== 'Kings XI Punjab' and venue == 'Jaipur'):
			return render_template('rajasthanPunjab.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Rajasthan Royals' and t2== 'Royal Challengers Bangalore' and venue == 'Jaipur'):
			return render_template('rajasthanBangalore.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Rajasthan Royals' and t2== 'Sunrisers Hyderabad' and venue == 'Jaipur'):
			return render_template('rajasthanHydrabad.html',team1=t1,team2=t2,venue=venue)

		elif(t1=='Royal Challengers Bangalore' and t2== 'Chennai Super Kings' and venue == 'Bangalore'):
			return render_template('bangaloreChennai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Royal Challengers Bangalore' and t2== 'Delhi Capitals' and venue == 'Bangalore'):
			return render_template('bangaloreDelhi.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Royal Challengers Bangalore' and t2== 'Kolkata Knight Riders' and venue == 'Bangalore'):
			return render_template('bangaloreKolkata.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Royal Challengers Bangalore' and t2== 'Mumbai Indians' and venue == 'Bangalore'):
			return render_template('bangaloreMumbai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Royal Challengers Bangalore' and t2== 'Kings XI Punjab' and venue == 'Bangalore'):
			return render_template('bangalorePunjab.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Royal Challengers Bangalore' and t2== 'Rajasthan Royals' and venue == 'Bangalore'):
			return render_template('bangaloreRajasthan.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Royal Challengers Bangalore' and t2== 'Sunrisers Hyderabad' and venue == 'Bangalore'):
			return render_template('bangaloreHydrabad.html',team1=t1,team2=t2,venue=venue)

		elif(t1=='Sunrisers Hyderabad' and t2== 'Chennai Super Kings' and venue == 'Hyderabad'):
			return render_template('hydrabadChennai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Sunrisers Hyderabad' and t2== 'Delhi Capitals' and venue == 'Hyderabad'):
			return render_template('hydrabadDelhi.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Sunrisers Hyderabad' and t2== 'Kolkata Knight Riders' and venue == 'Hyderabad'):
			return render_template('hydrabadKolkata.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Sunrisers Hyderabad' and t2== 'Mumbai Indians' and venue == 'Hyderabad'):
			return render_template('hydrabadMumbai.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Sunrisers Hyderabad' and t2== 'Kings XI Punjab' and venue == 'Hyderabad'):
			return render_template('hydrabadPunjab.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Sunrisers Hyderabad' and t2== 'Rajasthan Royals' and venue == 'Hyderabad'):
			return render_template('hydrabadRajasthan.html',team1=t1,team2=t2,venue=venue)
		elif(t1=='Sunrisers Hyderabad' and t2== 'Royal Challengers Bangalore' and venue == 'Hyderabad'):
			return render_template('hydrabadBangalore.html',team1=t1,team2=t2,venue=venue)		
		
    
	return render_template('webTool.html', h2h_wins=h2h_wins,key_players=key_players,tmw_decision=tmw_decision,
							# team1=ipl_teams[t1-1],team2=ipl_teams[t2-1],venue=cities[city-1],total_matches=total_matches,
							team1=t1,team2=t2,venue=venue,total_matches=total_matches,
    
#                            h2h_wins=h2h_wins,
                        #    tables1=[h2h_wins.to_html(classes='data')], titles1=h2h_wins.columns.values,
                           
#                            key_players=key_players,
                        #    tables2=[key_players.to_html(classes='data')], titles2=key_players.columns.values,
                           
                           toss_match_win_count=toss_match_win_count,
                           
#                            tmw_decision=tmw_decision,
                        #    tables3=[tmw_decision.to_html(classes='data')], titles3=tmw_decision.columns.values,
                           
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


@app.route('/live', methods=['GET'])
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

@app.route('/0')
def default():
    return render_template('index.html')

@app.route('/apiOptionPage')
def apiOption():
    return render_template('apiOption.html')

@app.errorhandler(404)
def error(e):
	return render_template("404.html", msg=e)

if __name__ == '__main__':
    app.run()
