from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
import numpy as np
import pandas as pd
pd.set_option('display.max_colwidth', 100)
from sklearn.model_selection import train_test_split

class MVP_classification(object):
    def __init__(self, my_data):
        self.clf = tree.DecisionTreeClassifier()
        self.X = []
        self.Y = []
        self.data = my_data
        self.le = preprocessing.LabelEncoder()

    def train(self):
        self.clf.fit(self.X_train, self.Y_train)


    def feature_to_vector(self):
        pos = self.le.fit_transform(self.data['Pos'])
        i = 0
        for index, row in self.data.iterrows():
            feature = [pos[i], row['PTS_x'], row['TRB_x'], row['AST_x'], row['WS_x'], row['PER'], row['TOV']]
            i += 1
            self.X.append(feature)
            if row['Rank'] > 3:
                self.Y.append(0)
            else:
                self.Y.append(1)
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size = 0.2, random_state=1)

    def test(self):
        result = self.clf.predict(self.X_test)
        self.evaluation(result, self.Y_test)

    def evaluation(self, result, golden):
        accuracy = accuracy_score(golden, result)
        print "The accuracy is %.2f" % accuracy

    def baseline(self):
        golden = []
        baseline_result = []
        baseline_mvp = self.data.groupby('Year')['PTS_x'].nlargest(3)
        baseline_mvp = baseline_mvp.to_frame()
        baseline_mvp = baseline_mvp.groupby('Year')['PTS_x'].min()
        baseline_mvp = baseline_mvp.to_frame().reset_index(drop = False)
        #print baseline_mvp.query("Year == 2001")['PTS_x']
        for index, row in self.data.iterrows():
            if row['Rank'] <= 3:
                golden.append(1)
            else:
                golden.append(0)
            y = row["Year"]
            #print baseline_mvp.query("Year==@y").iloc[0]["PTS_x"]
            if row['PTS_x'] >= baseline_mvp.query("Year == @y").iloc[0]['PTS_x']:
                baseline_result.append(1)
            else:
                baseline_result.append(0)
        #print baseline_result
        self.evaluation(baseline_result, golden)

def data_joining():
    player_data = pd.read_csv('./../nba_data/Seasons_Stats.csv', sep=",", header=0)
    mvp_year = pd.read_csv('../nba_data/nba_mvp_candidate_by_year.csv', sep=",", header=0)
    df_player_data = pd.DataFrame(player_data)
    df_player_data.set_index(['Year', 'Player'])
    df_mvp_data = pd.DataFrame(mvp_year)
    df_mvp_data.set_index(['Year', 'Player'])
    # print df_mvp_data.head(5)
    df_join_data = pd.merge(df_mvp_data, df_player_data, how='left', on=['Year', 'Player'])
    mvp_data = df_join_data.query('Year > 2000 and Rank < 10')
    mvp_data.to_csv('mvp_data_for_decision_tree.csv', sep=',')

if __name__ == "__main__":
    mvp_data = pd.read_csv('./mvp_data_for_decision_tree.csv', sep=',')
    mvp_data = mvp_data.dropna(how='any')
    solution = MVP_classification(mvp_data)
    solution.feature_to_vector()
    solution.train()
    print "Decision Tree Result:"
    solution.test()
    print "Baseline Result:"
    solution.baseline()