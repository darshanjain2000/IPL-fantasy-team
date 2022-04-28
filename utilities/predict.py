from joblib import load
import numpy as np
import os
from zipfile import ZipFile

tree = load(os.path.join(os.getcwd(), 'utilities', 'tree_model12.pkl'))
forest = load(os.path.join(os.getcwd(), 'utilities', 'forest_model.pkl'))
neural_nets = load(os.path.join(os.getcwd(), 'utilities', 'neural_nets_model.pkl'))

MODEL_INFO = {
  'Random Forest Regressor' : {'accuracy' : 93.08, 
                               'error' : 7.82},
  'Decision Tree Regressor' : {'accuracy' : 86.13, 
                               'error' : 11.01},
  'Neural Networks Regression' : {'accuracy' : 84.68, 
                               'error' : 11.63}
}

def predict_score(venue,team1, team2, toss_winner,toss_decision, model):
  prediction_array = []
  
  # Batting Team
  if team1 == 'Chennai Super Kings':
    prediction_array.append(0)
  elif team1 == 'Deccan Chargers':
    prediction_array.append(1)
  elif team1 == 'Delhi Capitals':
    prediction_array.append(2)
  elif team1 == 'Delhi Daredevils':
    prediction_array.append(3)
  elif team1 == 'Gujarat Lions':
    prediction_array.append(4)
  elif team1 == 'Kings XI Punjab':
    prediction_array.append(5)
  elif team1 == 'Kochi Tuskers Kerala':
    prediction_array.append(6)
  elif team1 == 'Kolkata Knight Riders':
    prediction_array.append(7)
  elif team1 == 'Mumbai Indians':
    prediction_array.append(8)
  elif team1 == 'Pune Warriors':
    prediction_array.append(9)
  elif team1 == 'Rajasthan Royals':
    prediction_array.append(10)
  elif team1 == 'Rising Pune Supergiant':
    prediction_array.append(11)
  elif team1 == 'Rising Pune Supergiants':
    prediction_array.append(12)
  elif team1 == 'Royal Challengers Bangalore':
    prediction_array.append(13)
  elif team1 == 'Sunrisers Hyderabad':
    prediction_array.append(14)

  # print(prediction_array)
  
  # Bowling Team
  if team2 == 'Chennai Super Kings':
     prediction_array.append(0)
  elif team2 == 'Deccan Chargers':
     prediction_array.append(1)
  elif team2 == 'Delhi Capitals':
     prediction_array.append(2)
  elif team2 == 'Delhi Daredevils':
     prediction_array.append(3)
  elif team2 == 'Gujarat Lions':
     prediction_array.append(4)
  elif team2 == 'Kings XI Punjab':
     prediction_array.append(5)
  elif team2 == 'Kochi Tuskers Kerala':
     prediction_array.append(6)
  elif team2 == 'Kolkata Knight Riders':
     prediction_array.append(7)
  elif team2 == 'Mumbai Indians':
     prediction_array.append(8)
  elif team2 == 'Pune Warriors':
     prediction_array.append(9)
  elif team2 == 'Rajasthan Royals':
     prediction_array.append(10)
  elif team2 == 'Rising Pune Supergiant':
     prediction_array.append(11)
  elif team2 == 'Rising Pune Supergiants':
     prediction_array.append(12)
  elif team2 == 'Royal Challengers Bangalore':
     prediction_array.append(13)
  elif team2 == 'Sunrisers Hyderabad':
     prediction_array.append(14)

  # venue      
  if venue == 'Barabati Stadium':
     prediction_array.append(0)
  elif venue == 'Brabourne Stadium' or 'Mumbai': ##############################
     prediction_array.append(1)
  elif venue == 'Buffalo Park':
     prediction_array.append(2)
  elif venue == 'De Beers Diamond Oval':
     prediction_array.append(3)
  elif venue == 'Dr DY Patil Sports Academy':
     prediction_array.append(4)
  elif venue == 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium':
     prediction_array.append(5)
  elif venue == 'Dubai International Cricket Stadium':
     prediction_array.append(6)
  elif venue == 'Eden Gardens':
     prediction_array.append(7)
  elif venue == 'Feroz Shah Kotla':
     prediction_array.append(8)
  elif venue == 'Green Park':
     prediction_array.append(9)
  elif venue == 'Himachal Pradesh Cricket Association Stadium':
     prediction_array.append(10)
  elif venue == 'Holkar Cricket Stadium':
     prediction_array.append(11)
  elif venue == 'JSCA International Stadium Complex':
     prediction_array.append(12)
  elif venue == 'Kingsmead':
     prediction_array.append(13)
  elif venue == 'M Chinnaswamy Stadium':
     prediction_array.append(14)
  elif venue == 'M.Chinnaswamy Stadium':
     prediction_array.append(15)
  elif venue == 'MA Chidambaram Stadium, Chepauk':
     prediction_array.append(16)
  elif venue == 'Maharashtra Cricket Association Stadium':
     prediction_array.append(17)
  elif venue == 'Nehru Stadium':
     prediction_array.append(18)
  elif venue == 'New Wanderers Stadium':
     prediction_array.append(19)
  elif venue == 'Newlands':
     prediction_array.append(20)
  elif venue == 'OUTsurance Oval':
     prediction_array.append(21)
  elif venue == 'Punjab Cricket Association IS Bindra Stadium, Mohali':
     prediction_array.append(22)
  elif venue == 'Punjab Cricket Association Stadium, Mohali':
     prediction_array.append(23)
  elif venue == 'Rajiv Gandhi International Stadium, Uppal':
     prediction_array.append(24)
  elif venue == 'Sardar Patel Stadium, Motera':
     prediction_array.append(25)
  elif venue == 'Saurashtra Cricket Association Stadium':
     prediction_array.append(26)
  elif venue == 'Sawai Mansingh Stadium':
     prediction_array.append(27)
  elif venue == 'Shaheed Veer Narayan Singh International Stadium':
     prediction_array.append(28)
  elif venue == 'Sharjah Cricket Stadium':
     prediction_array.append(29)
  elif venue == 'Sheikh Zayed Stadium':
     prediction_array.append(30)
  elif venue == "St George's Park":
     prediction_array.append(31)
  elif venue == 'Subrata Roy Sahara Stadium':
     prediction_array.append(32)
  elif venue == 'SuperSport Park':
     prediction_array.append(33)
  elif venue == 'Vidarbha Cricket Association Stadium, Jamtha':
     prediction_array.append(34)
  elif venue == 'Wankhede Stadium':
     prediction_array.append(35)
  
  # toss winner
  if toss_winner == 'Chennai Super Kings':
    prediction_array.append(0)
  elif toss_winner == 'Deccan Chargers':
    prediction_array.append(1)
  elif toss_winner == 'Delhi Capitals':
    prediction_array.append(2)
  elif toss_winner == 'Delhi Daredevils':
    prediction_array.append(3)
  elif toss_winner == 'Gujarat Lions':
    prediction_array.append(4)
  elif toss_winner == 'Kings XI Punjab':
    prediction_array.append(5)
  elif toss_winner == 'Kochi Tuskers Kerala':
    prediction_array.append(6)
  elif toss_winner == 'Kolkata Knight Riders':
    prediction_array.append(7)
  elif toss_winner == 'Mumbai Indians':
    prediction_array.append(8)
  elif toss_winner == 'Pune Warriors':
    prediction_array.append(9)
  elif toss_winner == 'Rajasthan Royals':
    prediction_array.append(10)
  elif toss_winner == 'Rising Pune Supergiant':
    prediction_array.append(11)
  elif toss_winner == 'Rising Pune Supergiants':
    prediction_array.append(12)
  elif toss_winner == 'Royal Challengers Bangalore':
    prediction_array.append(13)
  elif toss_winner == 'Sunrisers Hyderabad':
    prediction_array.append(14)

  # toss decison
  if toss_decision == 'bat':
     prediction_array.append(0)
  if toss_decision == 'field':
     prediction_array.append(1)

  # prediction_array = prediction_array + [runs, wickets, overs, runs_last_5, wickets_last_5]
  prediction_array = prediction_array
  prediction_array = np.array([prediction_array])
  # print(prediction_array)
  
  pred = model.predict(prediction_array)
  # return int(round(pred[0]))
  # print(prediction_array)
  return pred
