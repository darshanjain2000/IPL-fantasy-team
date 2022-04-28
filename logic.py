import findspark
findspark.init()
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, ArrayType, DateType
from pyspark.sql.functions import col,array_contains,udf,desc
import pandas as pd
import numpy as np
import datetime

# from matplotlib import pyplot as plt
import numpy as np


spark = SparkSession.builder.appName('IPL Pre-Match Analysis').getOrCreate()

ipl_teams = ["Chennai Super Kings","Delhi Capitals","Kolkata Knight Riders","Mumbai Indians","Kings XI Punjab","Rajasthan Royals","Royal Challengers Bangalore","Sunrisers Hyderabad"]

cities = ['Bangalore', 'Kochi', 'Chennai', 'Centurion', 'Ranchi', 'Mumbai', 'Ahmedabad', 'Durban', 'Kolkata', 'Cape Town', 'Dharamsala', 'Sharjah', 'Johannesburg', 'Kimberley', 'Pune', 'Delhi', 'Raipur', 'Chandigarh', 'Nagpur', 'Abu Dhabi', 'Bloemfontein', 'Kanpur', 'Hyderabad', 'Rajkot', 'Port Elizabeth', 'Dubai', 'Indore', 'Cuttack', 'East London', 'Jaipur', 'Visakhapatnam']

teams_squad = {
    
    "Chennai Super Kings" : ["MS Dhoni","BH Varma","Imran Tahir","HA Reddy","RD Gaikwad","MM Ali","HA Nishaanth","RA Jadeja","DL Chahar","N Jagadeesan","SK Raina","KM Asif","SN Thakur","RS Kishore","F du Plessis","DJ Bravo","CA Pujara","Karn Sharma","L Ngidi","AT Rayudu","JP Behrendorff","MJ Santner","K Gowtham","SM Curran","RV Uthappa"],
    "Delhi Capitals" : ["RR Pant","K Rabada","MP Stoinis","SW Billings","AM Rahane","CR Woakes","R Ashwin","SPD Smith","M Siddharth","S Mulani","Vishnu Vinod","A Joshi","Lalit Yadav","Avesh Khan","AR Patel","SS Iyer","A Mishra","I Sharma","Ripal Patel","S Dhawan","SO Hetmyer","P Dubey","PP Shaw","A Nortje","UT Yadav","L Meriwala","TK Curran"],
    "Kolkata Knight Riders": ["EJG Morgan","Shivam Mavi","S Sandeep Warrier", "Kuldeep Yadav","Shakib Al Hasan","SP Narine","Vaibhav Arora","LH Ferguson","BCJ Cutting","Tim Seifert","KK Nair","SP Jackson","V Iyer","KD Karthik","Harbhajan Singh","PJ Cummins","AD Russell","M Prasidh Krishna","Shubman Gill","N Rana","P Negi","KL Nagarkoti","Varun Chakaravarthy","Gurkeerat Singh" ,"RA Tripathi"],
    "Mumbai Indians":["RG Sharma","AP Tare","AS Roy","Anmolpreet Singh","CA Lynn","DS Kulkarni","KH Pandya","HH Pandya","Ishan Kishan","JJ Bumrah","KA Pollard","J Yadav","Mohsin Khan","Yudhvir Charak","Q de Kock","RD Chahar","SS Tiwary","SA Yadav","TA Boult","AF Milne","NM Coulter-Nile","PP Chawla","JDS Neesham","Marco Jansen","Arjun Tendulkar"],
    "Kings XI Punjab":["KL Rahul","Harpreet Brar","Ishan Porel","Utkarsh Singh","MC Henriques","Jhye Richardson","Mandeep Singh","CJ Jordan","DJ Hooda","R Bishnoi","Arshdeep Singh","Riley Meredith","SN Khan","MA Agarwal","Mohammed Shami","Darshan Nalkande","Shahrukh Khan","N Pooran","Fabian Allen","CH Gayle","M Ashwin","Jalaj Saxena","Dawid Malan","Saurabh Kumar","P Simran Singh"],
    "Rajasthan Royals": ["SV Samson","Kuldip Yadav","BA Stokes","CH Morris","AJ Tye","Kartik Tyagi","S Gopal","R Tewatia","JD Unadkat","M Markande","Gerald Coetzee","MK Lomror","R Parag","YBK Jaiswal","Anuj Rawat","A Singh","JC Archer","Chetan Sakariya","S Dube","KC Cariappa","Mustafizur Rahman","DA Miller","LS Livingstone","JC Buttler","M Vohra"],
    "Royal Challengers Bangalore" : ["V Kohli","Mohammed Siraj","SC Kuggeleijn","AB de Villiers","DR Sams","Shahbaz Ahmed","Finn Allen","KS Bharat","YS Chahal","NA Saini","K Jamieson","DT Christian","D Padikkal","GJ Maxwell","S Prabhudessai","Sachin Baby","P Deshpande","Washington Sundar","H Patel","A Zampa","KW Richardson","R Patidar","M Azharuddeen"],
    "Sunrisers Hyderabad": ["KS Williamson","Rashid Khan","WP Saha","KK Ahmed","Abdul Samad","Sandeep Sharma","Mujeeb Ur Rahman","SP Goswami","KM Jadhav","DA Warner","Mohammad Nabi","Abhishek Sharma","Basil Thampi","JJ Roy","JO Holder","B Kumar","J Suchith","Virat Singh","T Natarajan","S Nadeem","JM Bairstow","MK Pandey","V Shankar","S Kaul","PK Garg"],   
}

league_schema = StructType() \
      .add("id",IntegerType(),True) \
      .add("city",StringType(),True) \
      .add("date",StringType(),True) \
      .add("player_of_match",StringType(),True) \
      .add("venue",StringType(),True) \
      .add("neutral_venue",IntegerType(),True) \
      .add("team1",StringType(),True) \
      .add("team2",StringType(),True) \
      .add("toss_winner",StringType(),True) \
      .add("toss_decision",StringType(),True) \
      .add("winner",StringType(),True) \
      .add("result",StringType(),True) \
      .add("result_margin",IntegerType(),True) \
      .add("method",StringType(),True) \
      .add("umpire1",StringType(),True) \
      .add("umpire2",StringType(),True)
      
league_data = spark.read.format("csv") \
      .option("header", True) \
      .schema(league_schema) \
      .load("IPL Matches 2008-2020.csv")

match_schema = StructType() \
      .add("id",IntegerType(),True) \
      .add("inning",IntegerType(),True) \
      .add("over",IntegerType(),True) \
      .add("ball",IntegerType(),True) \
      .add("batsman",StringType(),True) \
      .add("non_striker",StringType(),True) \
      .add("bowler",StringType(),True) \
      .add("batsman_runs",IntegerType(),True) \
      .add("extra_runs",IntegerType(),True) \
      .add("total_runs",IntegerType(),True) \
      .add("non_boundary",IntegerType(),True) \
      .add("is_wicket",IntegerType(),True) \
      .add("dismissal_kind",StringType(),True) \
      .add("player_dismissed",StringType(),True) \
      .add("fielder",StringType(),True) \
      .add("extras_type",StringType(),True) \
      .add("batting_team",StringType(),True) \
      .add("bowling_team",StringType(),True)
      
match_data = spark.read.format("csv") \
      .option("header", True) \
      .schema(match_schema) \
      .load("IPL Ball-by-Ball 2008-2020.csv")

def head_to_head(t1,t2):
    
    teams = [t1,t2]
    h2h = league_data.filter(league_data.team1.isin(teams)).filter(league_data.team2.isin(teams))
    total_matches = h2h.count()
    h2h_wins = h2h.groupBy("winner").count()
    
    return h2h,total_matches,h2h_wins

def Key_Players(t1,t2,h2h):
    
    team1_squad = teams_squad[t1]
    team2_squad = teams_squad[t2]

    match_squad = team1_squad + team2_squad

    pom = h2h.filter(h2h.player_of_match.isin(match_squad))

    key_players = pom.groupby("player_of_match").agg(F.count('player_of_match').alias('points')).sort(desc("points"))
    
    return key_players

def Venue_Stats(city):
    
    venue = league_data.filter(league_data.city == city)
    ven_count = venue.count()
    
    return venue, ven_count

def Toss_Winner_Stats(venue):
    
    toss_match_win_count = venue.filter(venue.toss_winner == venue.winner).count()
    tmw_decision = venue.filter(venue.toss_winner == venue.winner).groupBy("toss_decision").count()
    
    return toss_match_win_count, tmw_decision

def MatchWinnerDecision(winner,toss_winner,toss_decision):
    
    if(winner == toss_winner):
        return toss_decision
    else:
        if(toss_decision == "bat"):
            return "field"
        else:
            return "bat"
        
def Match_Win_Toss(venue):
    
    udf_MWD = udf(MatchWinnerDecision, StringType())
    venue_with_toss = venue.withColumn("winner_toss", udf_MWD("winner","toss_winner","toss_decision"))
    match_win_decision = venue_with_toss.groupBy("winner_toss").count()
    
    return match_win_decision

def TeamsAtVenue(venue,t):
    
    team_venue = venue.filter((venue.team1 == t) | (venue.team2 == t))
    team_total = team_venue.count()
    team_venue_win = team_venue.filter(col("winner") == t).count()
    team_pc = int((team_venue_win/team_total) * 100)
    
    return team_venue, team_total, team_venue_win, team_pc

def Teams_Venue_id(team_venue):
    
    team_ven_id = team_venue.select("id").collect()
    for i in range(0,len(team_ven_id)):
        team_ven_id[i] = team_ven_id[i].id
        
    return team_ven_id

def team_MatchStats(matches,team):
    
    venue_matches = match_data.filter(match_data.id.isin(matches))
    team_matches = venue_matches.filter(venue_matches.batting_team == team)
    inn_match = team_matches.groupBy("id").agg(F.sum('total_runs').alias('sum_runs'), F.count('id').alias('sum_balls'))
    
    inn_runs = inn_match.select("sum_runs").collect()
    for i in range(0,len(inn_runs)):
        inn_runs[i] = inn_runs[i].sum_runs
        
    inn_balls = inn_match.select("sum_balls").collect()
    for i in range(0,len(inn_balls)):
        inn_balls[i] = inn_balls[i].sum_balls
        
    return inn_runs,inn_balls

def calcRR_Team(runs,balls):
    
    if(balls < 120):
        overs = int(balls/6)
        return round(runs/overs,2)
    else:
        return round(runs/20,2)
    
def RR_Teams(team_ven_id,t):
    
    team_runs, team_balls = team_MatchStats(team_ven_id,t)
    
    team_rr = [0 for x in range(0,len(team_ven_id))]
    for i in range(0,len(team_ven_id)):    
        team_rr[i] = calcRR_Team(team_runs[i],team_balls[i])
        
    return team_rr

def venue_id(venue):
    
    venueMatchesID = venue.select("id").collect()

    for i in range(0,len(venueMatchesID)):
        venueMatchesID[i] = venueMatchesID[i].id

    return venueMatchesID

def venue_MatchStats(matches):
    
    venue_matches = match_data.filter(match_data.id.isin(matches))
    inn_match = venue_matches.groupBy("id").agg(F.sum('total_runs').alias('sum_runs'), F.count('id').alias('sum_balls'))
    
    inn_runs = inn_match.select("sum_runs").collect()
    for i in range(0,len(inn_runs)):
        inn_runs[i] = inn_runs[i].sum_runs
        
    inn_balls = inn_match.select("sum_balls").collect()
    for i in range(0,len(inn_balls)):
        inn_balls[i] = inn_balls[i].sum_balls
        
    return inn_runs,inn_balls
    
    
def calcRR_Venue(runs,balls):
    
    if(balls < 240):
        overs = int(balls/6)
        return round(runs/overs,2)
    else:
        return round(runs/40,2)
    

def RR_Venue(venueMatches,venue_runs,venue_balls):

    run_rate = [0 for x in range(0,len(venueMatches))]

    for i in range(0,len(venueMatches)):

        run_rate[i] = calcRR_Venue(venue_runs[i],venue_balls[i])

    return run_rate

def top_players_venue(matches,team):
    
    venue_matches = match_data.filter(match_data.id.isin(matches))
    bat_team = venue_matches.filter(venue_matches.batting_team == team)
    bat_squad = bat_team.filter(bat_team.batsman.isin(teams_squad[team]))
    top_bat = bat_squad.groupBy("batsman").agg(F.sum('batsman_runs').alias('runs_scored')).sort(desc("runs_scored"))
    
    bowl_team = venue_matches.filter(venue_matches.bowling_team == team)
    bowl_squad = bowl_team.filter(bowl_team.bowler.isin(teams_squad[team]))
    wickets = bowl_squad.filter(bowl_squad.is_wicket == 1)
    bowler_wickets = wickets.filter(wickets.dismissal_kind != "run out")
    top_bowl = bowler_wickets.groupby("bowler").agg(F.count('is_wicket').alias("wickets")).sort(desc("wickets"))
    
    return top_bat, top_bowl
def htmlOutput(t1,t2,c_inp):

    t1=ipl_teams.index(t1)
    t2=ipl_teams.index(t2)
    c_inp=cities.index(c_inp)

    team1 = ipl_teams[t1-1]
    team2 = ipl_teams[t2-1]
    city = cities[c_inp-1]

    venue, ven_count = Venue_Stats(city)
    venueMatchesID = venue_id(venue)

    #call all function-------------
    
    h2h,total_matches,h2h_wins = head_to_head(team1,team2)
    
    key_players = Key_Players(team1,team2,h2h)
    
    toss_match_win_count, tmw_decision = Toss_Winner_Stats(venue)
    
    match_win_decision = Match_Win_Toss(venue)
    
    #run rate at venue
    runs,balls = venue_MatchStats(venueMatchesID)
    rr_venue = RR_Venue(venueMatchesID,runs,balls)
    mean = round(sum(rr_venue)/len(rr_venue),2)
    
    # top batsman and wicket keeper at venue from both team
    t1_topbat, t1_topbowl = top_players_venue(venueMatchesID,team1)    
    t2_topbat, t2_topbowl = top_players_venue(venueMatchesID,team2)
    
    #team wining probablity at venue (team_pc)
    team_venue, team_total, team_venue_win, team_pc = TeamsAtVenue(venue,team1)
    team_venue2, team_total2, team_venue_win2, team_pc2 = TeamsAtVenue(venue,team2)
    
    #team run rate at venue
    team_ven_id = Teams_Venue_id(team_venue)
    team_ven_id2 = Teams_Venue_id(team_venue2)
    rr_team = RR_Teams(team_ven_id,team1)
    rr_team2 = RR_Teams(team_ven_id2,team2)
    
    # convert spark dataframe to pandas dataframe
    h2h_wins=h2h_wins.toPandas()
    # h2h_wins=[ [h2h_wins['winner'][0], h2h_wins['count'][0]], [h2h_wins['winner'][1], h2h_wins['count'][1]]]
    key_players=key_players.toPandas()
    # key_players = [ [key_players['player_of_match'][0],key_players['points'][0]],[key_players['player_of_match'][1],key_players['points'][1]],[key_players['player_of_match'][2],key_players['points'][2]],[key_players['player_of_match'][3],key_players['points'][3]],[key_players['player_of_match'][4],key_players['points'][4]],[key_players['player_of_match'][5],key_players['points'][5]]  ]
    tmw_decision=tmw_decision.toPandas()
    # tmw_decision = [ ["Fielding",tmw_decision['count'][0]],["Batting",tmw_decision['count'][1]]  ]
    # match_win_decision=match_win_decision.toPandas()
    match_win_decision=h2h_wins
    t1_topbat=t1_topbat.toPandas()
    t1_topbowl=t1_topbowl.toPandas()
    t2_topbat=t2_topbat.toPandas()
    t2_topbowl=t2_topbowl.toPandas()
    
    
    return total_matches,h2h_wins,key_players,toss_match_win_count,\
            tmw_decision,match_win_decision,mean,\
            t1_topbat, t1_topbowl,t2_topbat, t2_topbowl,\
            team_pc,team_pc2,\
            rr_team,rr_team2

    
#     print('\ntotal matches')
#     print(total_matches)
#     print(type(total_matches))
    
#     print('\nh2h_wins') #
#     print(h2h_wins)
#     print(type(h2h_wins))
    
#     h2h_wins=h2h_wins.toPandas()
#     print('\nh2h_wins PANDAS')##
#     print(h2h_wins)
#     print(type(h2h_wins))
    
def final_data(t1,t2,c_inp):

    result={'stats':None,
           'players':None,
           'toss':None,
           'city analysis':None,
           'run rate':None}

        
    team1 = ipl_teams[t1-1]
    team2 = ipl_teams[t2-1]

        
    city = cities[c_inp-1]

    option = ['A','B','C','D','E']

    venue, ven_count = Venue_Stats(city)
    venueMatchesID = venue_id(venue)

    for menu in option:
        if(menu == "a" or menu == "A"):
            
            h2h,total_matches,h2h_wins = head_to_head(team1,team2)
            
#             temp1= team1+" Vs "+team2+" Statistics"
            h2h_wins=h2h_wins.toPandas()
            h2h_wins=h2h_wins.to_json()
            result['stats']={"total matches":total_matches,"head 2 head wins":h2h_wins} #
            
        elif(menu == "b" or menu =="B"):
            
            h2h,total_matches,h2h_wins = head_to_head(team1,team2)
                            
            key_players = Key_Players(team1,team2,h2h)
            
#             temp2 = "Key Players in "+team1+" Vs "+team2
            key_players=key_players.toPandas()
            key_players=key_players.to_json()
            result['players']={"key players":key_players} #
            
        elif(menu == "c" or menu == "C"):
            
            toss_match_win_count, tmw_decision = Toss_Winner_Stats(venue)
            
            
#             temp3 = "Toss Win Analysis at "+city
            tmw_decision=tmw_decision.toPandas()
            tmw_decision=tmw_decision.to_json()
            result['toss']={'total match win count':toss_match_win_count,'total match win decision' :tmw_decision} #
            
        elif(menu == "d" or menu == "D"):
            continue
            
            
            match_win_decision = Match_Win_Toss(venue)
            
#             temp4 = "Match Win Toss Analysis at "+city
            match_win_decision=match_win_decision.toPandas()
            atch_win_decision=match_win_decision.to_json()
            result['city analysis']={'match win decision': match_win_decision} #
    
            
        elif(menu == "e" or menu == "E"):
            
            runs,balls = venue_MatchStats(venueMatchesID)
            
            rr_venue = RR_Venue(venueMatchesID,runs,balls)
            
            mean = round(sum(rr_venue)/len(rr_venue),2)
                
#             temp4 =  "Run-Rate at "+city
            result['run rate']={'avearge run rate in that city': mean}
    return result
