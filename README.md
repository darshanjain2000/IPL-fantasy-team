# IPL fantasy team assistant Web Tool and API

Now make calculated risk over your fantasy sport team.

Get best options of players for your IPL fantasy team using data of every ball ever played in IPL (2008-2020)

This python code uses pySpark, numpy and pandas majorly to find out various best players in different situation such as venue, opposite team, toss, pitch stats, etc.

In tool, plotted some graph for quick glance.

# Analysis Attributes
1.Total Matches team1 vs team2\n
2.Head to head wins
3.Key players in team1 vs team2
4.Toss winner choice at venue
5.Match winner toss decision team1 vs team2
6.Match winner toss decision at venue
7.Run rate at venue
8.Team1 top run-scorer at venue
9.Team1 top wicket-taker at venue
10.Team2 top run-scorer at venue
11.Team2 top wicket-taker at venue
12.Team1 win percentage at venue
13.Team2 win percentage at venue


# API
use localhost as endpoint

for using api there is 3 field team1 team2 and city range from 1-8, 1-8, 1-31 respectively

value associated with no. -

ipl_teams = ["Chennai Super Kings","Delhi Capitals","Kolkata Knight Riders","Mumbai Indians","Kings XI Punjab","Rajasthan Royals","Royal Challengers Bangalore","Sunrisers Hyderabad"]

cities = ['Bangalore', 'Kochi', 'Chennai', 'Centurion', 'Ranchi', 'Mumbai', 'Ahmedabad', 'Durban', 'Kolkata', 'Cape Town', 'Dharamsala', 'Sharjah', 'Johannesburg', 'Kimberley', 'Pune', 'Delhi', 'Raipur', 'Chandigarh', 'Nagpur', 'Abu Dhabi', 'Bloemfontein', 'Kanpur', 'Hyderabad', 'Rajkot', 'Port Elizabeth', 'Dubai', 'Indore', 'Cuttack', 'East London', 'Jaipur', 'Visakhapatnam']

sample call

localhost:5000/predict?team1=4&team2=3&city=5
