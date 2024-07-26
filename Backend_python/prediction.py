import csv

from pathlib import Path
import os


import matplotlib
matplotlib.use('agg')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn import metrics
from sklearn.feature_selection import chi2
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report


from sklearn.ensemble import RandomForestClassifier

from sklearn.ensemble import GradientBoostingClassifier

from sklearn.svm import SVC


from dateutil import parser
from datetime import datetime


def date_to_numeric(date_str):

    try:
        # Parse the date string
        parsed_date = parser.parse(date_str)
        
        # Reference date (Unix epoch)
        epoch = datetime(1970, 1, 1)
        
        # Calculate the number of days since the epoch
        numeric_value = (parsed_date - epoch).days

        return numeric_value
    
    except:
        return 00
    

def player_name(player):

    # Changing the name of the players to their first name
    if ("magnus" in player.lower()) or ("carlsen" in player.lower()):
        return "Magnus"
    
    elif ("hikaru" in player.lower()) or ("nakamura" in player.lower()):
        return "Hikaru"
    
    elif ("ding" in player.lower()) or ("liren" in player.lower()):
        return "Ding"
    
    elif ("alireza" in player.lower()) or ("firouzja" in player.lower()):
        return "Alireza"
    
    elif ("anish" in player.lower()) or ("giri" in player.lower()):
        return "Anish"
    
    elif ("ian" in player.lower()) or ("nepomniachtchi" in player.lower()):
        return "Ian"
    
    elif ("fabiano" in player.lower()) or ("caruana" in player.lower()):
        return "Fabiano"
    
    elif ("nodirbek" in player.lower()) or ("abdusattorov" in player.lower()):
        return "Nodirbek"
    
    else:
        print ("Wrong Player name ---> " + player)
        return player

    
    
def predict(player_1, player_2,model_type):

    result = {}

    pythonfilepath = os.path.dirname(__file__)

    file_name = player_1 + "_vs_" + player_2 + ".csv"
    path = pythonfilepath + "/Games_dataset/" + player_1 + "_vs_others/"

    filename = path + file_name

    df = pd.read_csv(filename)

    # Remove draws 
    df = df[df['Who_won'] != "Draw"]

    # Changing the name of the players to a comman name ::
    df['Player_Black'] = df.apply(lambda row: player_name(row['Player_Black']), axis=1)
    df['Player_White'] = df.apply(lambda row: player_name(row['Player_White']), axis=1)

    # Mapping B to Player_Black and W to Player_White 
    df['Who_won'] = df.apply(lambda row: row['Player_Black'] if (row['Who_won'] == 'B') else row['Player_White'], axis=1)
    df['Who_won'] = df.apply(lambda row: player_1 if (player_1 in row['Who_won']) else player_2, axis=1)

    # Replace if player_1 win to 1 otherwise 0
    df['Who_won'].replace([player_1, player_2], [1,0], inplace=True)

    # Replace time control as numeric encoding 
    # Time control encoding :: 
    # Blitz -----> 0
    # Rapid -----> 1
    # Classical -----> 2
    # Bullet -----> 3
    # Unknown -----> 4
    df['Time_Control'].replace(["Blitz", "Rapid",  "Classical",  "Bullet", "Unknown"], [0, 1, 2, 3, 4], inplace=True)

    # Add a color row for the primary player i.e., player_1 where 0 signifies black and 1 signifies white
    df["Color"] = None
    df['Color'] = df.apply(lambda row: 0 if (player_1 in row['Player_Black']) else 1, axis=1)

    # Replace date with numeric encoding where it's the number of days since the epoch
    df['Date'] = df.apply(lambda row: date_to_numeric(row['Date']), axis=1)

    # Drop the useless data columns
    df = df.drop(columns=['Game_Number', 'Player_White' , 'Player_Black'])

    # Numeric encode the Game(openings) 
    # Maybe a later feature to add for now drop the game
    df = df.drop(columns=['Game'])

    # Fix the indexing for the columns
    df = df.reindex(columns=['Time_Control', 'Date', 'Color', 'Who_won'])

    X = df.iloc[:,0:3] # All features
    Y = df.iloc[:,-1] # Target output -> Who won 

    # Select the top 3 features 

    best_features = SelectKBest(score_func=chi2, k=3)
    fit = best_features.fit(X,Y)


    # Data frames for the features and the score of each feature
    df_scores= pd.DataFrame(fit.scores_)
    df_columns= pd.DataFrame(X.columns)

    # Combine all the features and their scores in a data frame
    features_scores= pd.concat([df_columns, df_scores], axis=1)
    features_scores.columns= ['Features', 'Score']
    features_scores.sort_values(by = 'Score')


    # Display the features_scores [RN not useful because we only have 3 features]
    # print(features_scores)

    # Build the Model
    X = df[['Time_Control', 'Date', 'Color']]
    Y = df[['Who_won']]

    # Split the dataset into train and test
    X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=0.2,random_state=100)

    if model_type == "RandomForest":
        # Random Forest [Has better acc than logistic regression in most cases]
        rf = RandomForestClassifier(random_state=42)
        rf.fit(X_train, y_train.values.ravel())
        y_pred = rf.predict(X_test)

    elif model_type == "LogisticRegression":
        # Create a logistic regression body
        logreg= LogisticRegression()
        logreg.fit(X_train,y_train.values.ravel())

        # Predict the likelihood of a win for player_1 using the logistic regression body we created
        y_pred = logreg.predict(X_test)

    elif model_type == "GradientBoosting":
        gb = GradientBoostingClassifier(random_state=42)
        gb.fit(X_train, y_train.values.ravel())
        y_pred = gb.predict(X_test)
    
    elif model_type == "SupportVectorMachine":
        svc = SVC(probability=True)
        svc.fit(X_train, y_train.values.ravel())
        y_pred = svc.predict(X_test)
    
    else:
        print ("Invalid Model type")
        return 
    

    print (X_test) #test dataset
    print (y_pred) #predicted values
    print() # Add a line break

    # Evaluate the Model’s Performance
    print('Accuracy: ',metrics.accuracy_score(y_test, y_pred))
    print('Recall: ',metrics.recall_score(y_test, y_pred, zero_division=1))
    print("Precision:",metrics.precision_score(y_test, y_pred, zero_division=1))
    print("CL Report:",metrics.classification_report(y_test, y_pred, zero_division=1))

    result['Accuracy'] = metrics.accuracy_score(y_test, y_pred)
    result['Recall'] = metrics.recall_score(y_test, y_pred)
    result['Precision'] = metrics.precision_score(y_test, y_pred)
    result['CL Report'] = metrics.classification_report(y_test, y_pred)
    result['predictions'] = y_pred



    # ROC Curve

    if model_type == "RandomForest":
        y_pred_proba = rf.predict_proba(X_test) [::,1]

    elif model_type == "LogisticRegression":
        y_pred_proba = logreg.predict_proba(X_test) [::,1]

    elif model_type == "GradientBoosting":
        y_pred_proba = gb.predict_proba(X_test) [::,1]
    
    elif model_type == "SupportVectorMachine":
        y_pred_proba = svc.predict_proba(X_test) [::,1]
    
    else:
        print ("Invalid Model type")
        return 
    

    false_positive_rate, true_positive_rate, _ = metrics.roc_curve(y_test, y_pred_proba)
    auc = metrics.roc_auc_score(y_test, y_pred_proba)

    plt.figure()
    plt.plot(false_positive_rate, true_positive_rate, label="AUC=" + str(auc))
    plt.title('ROC Curve for ' + player_1 + "_vs_" + player_2 )
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.legend(loc=4)

    # Save the plot as a file
    root = os.path.dirname(pythonfilepath)
    plt.savefig(root + '/frontend_ts/src/roc_curve.png')
    plt.close()

    return result


def predict_singlePlayer(player_1,model_type):

    result = {}

    pythonfilepath = os.path.dirname(__file__)

    file_name = player_1 + "_vs_all"  + ".csv"
    path = pythonfilepath + "/Games_dataset/" + player_1 + "_vs_others/"

    filename = path + file_name

    df = pd.read_csv(filename)

    # Remove draws 
    df = df[df['Who_won'] != "Draw"]

    # Changing the name of the players to a comman name ::
    df['Player_Black'] = df.apply(lambda row: player_name(row['Player_Black']), axis=1)
    df['Player_White'] = df.apply(lambda row: player_name(row['Player_White']), axis=1)


    # Mapping B to Player_Black and W to Player_White 
    df['Who_won'] = df.apply(lambda row: row['Player_Black'] if (row['Who_won'] == 'B') else row['Player_White'], axis=1)
    df['Who_won'] = df.apply(lambda row: player_1 if (player_1 in row['Who_won']) else "Opponent", axis=1)

    # Replace if player_1 win to 1 otherwise 0
    df['Who_won'].replace([player_1, "Opponent"], [1,0], inplace=True)

    # Replace time control as numeric encoding 
    # Time control encoding :: 
    # Blitz -----> 0
    # Rapid -----> 1
    # Classical -----> 2
    # Bullet -----> 3
    # Unknown -----> 4
    df['Time_Control'].replace(["Blitz", "Rapid",  "Classical",  "Bullet", "Unknown"], [0, 1, 2, 3, 4], inplace=True)

    # Add a color row for the primary player i.e., player_1 where 0 signifies black and 1 signifies white
    df["Color"] = None
    df['Color'] = df.apply(lambda row: 0 if (player_1 in row['Player_Black']) else 1, axis=1)

    # Replace date with numeric encoding where it's the number of days since the epoch
    df['Date'] = df.apply(lambda row: date_to_numeric(row['Date']), axis=1)

    # Drop the useless data columns
    df = df.drop(columns=['Game_Number', 'Player_White' , 'Player_Black'])

    # Numeric encode the Game(openings) 
    # Maybe a later feature to add for now drop the game
    df = df.drop(columns=['Game'])

    # Fix the indexing for the columns
    df = df.reindex(columns=['Time_Control', 'Date', 'Color', 'Who_won'])

    X = df.iloc[:,0:3] # All features
    Y = df.iloc[:,-1] # Target output -> Who won 

    # Select the top 3 features 

    best_features = SelectKBest(score_func=chi2, k=3)
    fit = best_features.fit(X,Y)


    # Data frames for the features and the score of each feature
    df_scores= pd.DataFrame(fit.scores_)
    df_columns= pd.DataFrame(X.columns)

    # Combine all the features and their scores in a data frame
    features_scores= pd.concat([df_columns, df_scores], axis=1)
    features_scores.columns= ['Features', 'Score']
    features_scores.sort_values(by = 'Score')


    # Display the features_scores [RN not useful because we only have 3 features]
    # print(features_scores)

    # Build the Model
    X = df[['Time_Control', 'Date', 'Color']]
    Y = df[['Who_won']]

    # Split the dataset into train and test
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train,X_test,y_train,y_test=train_test_split(X_scaled,Y,test_size=0.2,random_state=100)

    if model_type == "RandomForest":
        # Random Forest [Has better acc than logistic regression in most cases]
        rf = RandomForestClassifier(random_state=42)
        rf.fit(X_train, y_train.values.ravel())
        y_pred = rf.predict(X_test)

    elif model_type == "LogisticRegression":
        # Create a logistic regression body
        logreg= LogisticRegression()
        logreg.fit(X_train,y_train.values.ravel())

        # Predict the likelihood of a win for player_1 using the logistic regression body we created
        y_pred = logreg.predict(X_test)

    elif model_type == "GradientBoosting":
        gb = GradientBoostingClassifier(random_state=42)
        gb.fit(X_train, y_train.values.ravel())
        y_pred = gb.predict(X_test)
    
    elif model_type == "SupportVectorMachine":
        svc = SVC(probability=True)
        svc.fit(X_train, y_train.values.ravel())
        y_pred = svc.predict(X_test)
    
    else:
        print ("Invalid Model type")
        return 
    
    print (X_test) #test dataset
    print (y_pred) #predicted values
    print() # Add a line break

    # Evaluate the Model’s Performance
    print('Accuracy: ',metrics.accuracy_score(y_test, y_pred))
    print('Recall: ',metrics.recall_score(y_test, y_pred, zero_division=1))
    print("Precision:",metrics.precision_score(y_test, y_pred, zero_division=1))
    print("CL Report:",metrics.classification_report(y_test, y_pred, zero_division=1))

    result['Accuracy'] = metrics.accuracy_score(y_test, y_pred)
    result['Recall'] = metrics.recall_score(y_test, y_pred)
    result['Precision'] = metrics.precision_score(y_test, y_pred)
    result['CL Report'] = metrics.classification_report(y_test, y_pred)
    result['predictions'] = y_pred


    # ROC Curve

    if model_type == "RandomForest":
        y_pred_proba = rf.predict_proba(X_test) [::,1]

    elif model_type == "LogisticRegression":
        y_pred_proba = logreg.predict_proba(X_test) [::,1]

    elif model_type == "GradientBoosting":
        y_pred_proba = gb.predict_proba(X_test) [::,1]
    
    elif model_type == "SupportVectorMachine":
        y_pred_proba = svc.predict_proba(X_test) [::,1]
    
    else:
        print ("Invalid Model type")
        return 
    
    false_positive_rate, true_positive_rate, _ = metrics.roc_curve(y_test, y_pred_proba)
    auc = metrics.roc_auc_score(y_test, y_pred_proba)

    plt.figure()
    plt.plot(false_positive_rate, true_positive_rate, label="AUC=" + str(auc))
    plt.title('ROC Curve for ' + player_1 + "_vs_all" )
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.legend(loc=4)

    # Save the plot as a file
    root = os.path.dirname(pythonfilepath)
    plt.savefig(root + '/frontend_ts/src/roc_curve.png')
    plt.close()


    return result



# player_1 = "Magnus"
# player_2 = "Hikaru"
# player_3 = "Anish"
# player_4 = "Alireza"
# player_5 = "Ian"
# player_6 = "Fabi"
# player_7 = "Ding"
# player_8 = "Nodirbek"


# model_type1 = "LogisticRegression" 
# model_type2 = "RandomForest" 
# model_type3 = "GradientBoosting" 
# model_type4 = "SupportVectorMachine"



# predict(player_1,player_2,model_type2)

# predict_singlePlayer(player_6,model_type2)


# For Magnus 
# LR ---> 69%
# RF ---> 71%
# GB ---> 70%
# SVM ---> 69%

# For Hikaru 
# LR ---> 55%
# RF ---> 67%
# GB ---> 57%
# SVM ---> 53%

# For Ian 
# LR ---> 50%
# RF ---> 72%
# GB ---> 62%
# SVM ---> 50%

# For Fabi 
# LR ---> 92%
# RF ---> 89%
# GB ---> 90%
# SVM ---> 95%

# On avg it looks like the RandomForest model has the highest accuracy

# Highest acc in all the cases --> predict_singlePlayer(player_6)