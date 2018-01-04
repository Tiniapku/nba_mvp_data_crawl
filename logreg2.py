import pandas as pd
from sklearn.linear_model import LogisticRegression
import sys
import argparse
# from sklearn.cross_validation import train_test_split
parser = argparse.ArgumentParser()
parser.add_argument('--year', help="The mvp season you want to predict, from 2000 to 2018" )
parser.add_argument('--model', help="The model you want to use, model1 for top-down model and model2 for bottom-up model")
args = parser.parse_args()

mvps = {2018: "?",2017: "Russell Westbrook", 2016: "Stephen Curry", 2015: "Stephen Curry", 2014:"Kevin Durant", 2013:"LeBron James",
2012: "LeBron James", 2011: "Derrick Rose", 2010: "LeBron James", 2009:"LeBron James", 2008:"Kobe Bryant",
2007:"Dirk Nowitzki", 2006: "Steve Nash", 2005:"Steve Nash", 2004:"Kevin Garnett", 2003:"Tim Duncan",
2002:"Tim Duncan", 2001:"Allen Iverson", 2000:"Shaquille O'Neal"}

data = pd.read_csv('mvp_team.csv', sep=',', header=0)
#data_5 = data[data['Rank_player'] <= 5]
all = 0
acc = 0

YEAR_TEST = int(args.year)
data_train = data[data['Year'] < YEAR_TEST]
data_label = data_train['Top1']
# model 1: predict correctly from 2009 - 2017, Chris Paul in 2008
# X = ['PTS/G', 'TRB/G', 'AST/G', 'STL/G', 'BLK/G', 'W/L%', 'WS/48',
#       'PER', "TOV%", 'OWS', 'DWS', 'VORP','BPM']
# model 2: predict correctly from 2000 - 2004 + 2007 - 2016, cannot do it right for Nash
# X =['Rank_team', 'WS', 'Top2WS']
if args.model == "model1":
    X = ['PTS/G', 'TRB/G', 'AST/G', 'STL/G', 'BLK/G', 'W/L%', 'WS/48',
         'PER', "TOV%", 'OWS', 'DWS', 'BPM']
elif args.model == "model2":
    X = ['Rank_team', 'WS', 'Top2WS']
else:
    raise Exception("Wrong model")
# train_x, test_x, train_y, test_y = train_test_split(data_train[X], data_label, train_size = 0.8)

logreg = LogisticRegression()
logreg.fit(data_train[X], data_label)

# train_accuracy = logreg.score(train_x, train_y)
# print "Logistic train accuracy:", train_accuracy
# #
# test_accuracy = logreg.score(test_x, test_y)
# print "Logistic test accuracy:", test_accuracy

# for i in range(len(X)):
#     print X[i], logreg.coef_[0][i]
# print "-------------------------------------"
#
# print "Name, Real_Rank, Pred_prob"
test = data[data['Year'] == YEAR_TEST]
pred = logreg.predict_proba(test[X])
_, rank1 = pred.max(axis=0)
i = 0
# print "-------------------------------------"
for non_MVP, MVP in pred:
    # if rank1 == MVP:
    #     if test.iloc[i]['Player'] == mvps[test_year]:
    #         acc += 1
    #         print str(test_year) + " & " + test.iloc[i]['Player'] + " & " + mvps[test_year] + "\\" + "\\" + " \\hline"
    #     else:
    #         print "\\textbf{" + str(test_year) + "} & \\textbf{" + test.iloc[i]['Player'] + "} & \\textbf{" + mvps[test_year] + "}" + "\\" + "\\" + " \\hline"
    print (test.iloc[i]['Player'], test.iloc[i]['Rank_player'], MVP, "**" if rank1 == MVP else "")
    i += 1
all += 1

