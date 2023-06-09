# -*- coding: utf-8 -*-
"""Team2_FlightDelay_Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X56_mAK8zZbZKNc3H9y4wfJJv6GEL51Y

### Data Preprocessing
"""

# import libraries
import pandas as pd
import seaborn as sns
import numpy as np
from scipy.stats import norm
from scipy.stats import cauchy
import scipy.stats
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint
from statsmodels.stats.proportion import confint_proportions_2indep
import statsmodels.stats.api as sms
from google.colab import drive
drive.mount('/content/drive')

# read csv file
# AL = pd.read_csv('August 2018 Nationwide.2.csv')
AL = pd.read_csv('/content/drive/MyDrive/MSAAI - 501 Introduction to AI/Team 2 AAI 501/August 2018 Nationwide.csv')

# top records of the dataset
AL.head()

# checking for number of columns
AL.columns

# removing unnecessary columns, including Airport IDies Origin and Dest, cancelltion and cancellation code
AL = AL.drop(['CANCELLED', 'CANCELLATION_CODE', 'DEST_AIRPORT_ID', 'DEST_AIRPORT_SEQ_ID', 'DEST_CITY_MARKET_ID', 'ORIGIN_AIRPORT_ID', 'ORIGIN_AIRPORT_SEQ_ID',\
              'ORIGIN_CITY_MARKET_ID', 'DEP_DELAY', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY', 'Unnamed: 28', 'ARR_DELAY', 'ARR_DELAY_NEW'], axis=1)

# renam the column "OP_CARRIER_AIRLINE_ID" to "Airline_Name"
AL.rename(columns={"TAIL_NUM":"Airline_Name", "DEP_DELAY_NEW": "DELAY"}, inplace=True)

# confirm the change
AL.columns

# to check for the missing value
AL.isnull().sum()

# Remove Any Rows Containing Nulls
AL.dropna(inplace=True)

# to check for the missing value
AL.isnull().sum()

len(AL)

AL['DELAY'] = AL['DELAY'].astype('bool')

# check for information concerning dataset
AL.info()

AL.groupby("Airline_Name")["Airline_Name"].agg("count")

# check for the unique values in the column "Airline_Name"
AL['Airline_Name'].unique()

# to clean the column, replace this Tail numbers with unique values (airline_name)
AL["Airline_Name"] = AL["Airline_Name"].str.replace("215NV", "Allegiant Air")
AL["Airline_Name"] = AL["Airline_Name"].str.replace("216NV", "Allegiant Air")
AL["Airline_Name"] = AL["Airline_Name"].str.replace("217NV", "Allegiant Air")
AL["Airline_Name"] = AL["Airline_Name"].str.replace("218NV", "Allegiant Air")
AL["Airline_Name"] = AL["Airline_Name"].str.replace("219NV", "Allegiant Air")
AL["Airline_Name"] = AL["Airline_Name"].str.replace("N998AN", "American Airlines")
AL["Airline_Name"] = AL["Airline_Name"].str.replace("N998AT", "Delta Air Lines")
AL["Airline_Name"] = AL["Airline_Name"].str.replace("N998DL", "Delta Air Lines")
AL["Airline_Name"] = AL["Airline_Name"].str.replace("N998NN", "American Airlines")
AL["Airline_Name"] = AL["Airline_Name"].str.replace("N999DN", "Delta Air Lines")

# to confirm the change- trying to get full list of unique items!(any idea?!)
UI = AL["Airline_Name"].unique()
UI

# checking for outliers in the dataset
sns.boxplot(AL["CRS_DEP_TIME"])

sns.boxplot(AL["DEP_TIME"])

sns.boxplot(AL["CRS_ELAPSED_TIME"])

sns.boxplot(AL["ACTUAL_ELAPSED_TIME"])

# chechink for duplicate values
AL.duplicated()

from sklearn import preprocessing

categorical_columns = ['OP_CARRIER_AIRLINE_ID', 'Airline_Name', 'OP_CARRIER_FL_NUM', 'ORIGIN', 'DEST']

# label_encoder object knows how to understand word labels.
label_encoder = preprocessing.LabelEncoder()
  
# Encode labels in categorical columns.
for cat in categorical_columns:
  cat_le =  label_encoder.fit_transform(AL[cat])
  if 'ORIGIN' == cat:
    origin_name_mapping = dict(zip(cat_le, AL[cat]))
  elif 'DEST' == cat:
    dest_name_mapping = dict(zip(cat_le, AL[cat]))

  AL[cat] = cat_le

"""### Exploratory Data Analysis"""

## Determine Correlation Between Parameters and the Categorical Target, Delay
import scipy.stats as ss
from itertools import product

categorical_columns.append('DELAY')
categorical_columns.append('FL_DATE')
AL_cat = AL[categorical_columns]
AL_cat['FL_DATE'] = label_encoder.fit_transform(AL_cat['FL_DATE'])

AL_cat.head()

## Determine All Unique Products of the Categories to Determine Number of Chi-Squared
cat_var1 = AL_cat.columns
cat_var2 = AL_cat.columns
cat_var_prod = list(product(cat_var1,cat_var2, repeat = 1))
print(cat_var_prod)
print(len(cat_var_prod))

## Run Chi-Sqaured
result = []
for prod in cat_var_prod:
  if prod[0] != prod[1]: # Ignore Same Pairing Product
    result.append((prod[0],prod[1],list(ss.chi2_contingency(pd.crosstab(AL_cat[prod[0]], AL_cat[prod[1]])))[1]))

print(result)

chi_test_output = pd.DataFrame(result, columns = ['var1', 'var2', 'coeff'])
## Using pivot function to convert the above DataFrame into a crosstab
chi_test_output.pivot(index='var1', columns='var2', values='coeff')

## Determine Correlation Between Continous Features and the Categorical Target, Delay
import scipy.stats as ss
from itertools import product

cat_continous_columns = ['CRS_DEP_TIME', 'DEP_TIME', 'DELAY', 'ARR_TIME', 'CRS_ELAPSED_TIME', 'ACTUAL_ELAPSED_TIME']
AL_con_cat = AL[cat_continous_columns]
print(AL_con_cat.head())

con_var1 = ['CRS_DEP_TIME', 'DEP_TIME', 'ARR_TIME', 'CRS_ELAPSED_TIME', 'ACTUAL_ELAPSED_TIME']
cat_var1 = ['DELAY']
cat_con_prod = list(product(con_var1,cat_var1, repeat = 1))
print(cat_con_prod)
print(len(cat_con_prod))

## Find Correlation Between Categorical (Delay) and Continous Variables
result = []
for prod in cat_con_prod:
  result.append((prod[0],prod[1], AL_con_cat[prod[0]].corr(AL_con_cat[prod[1]])))

print(result)

corr_output = pd.DataFrame(result, columns = ['var1', 'var2', 'coeff'])
## Using pivot function to convert the above DataFrame into a crosstab
corr_output.pivot(index='var1', columns='var2', values='coeff')

## Adding Categorical Column Day of the Week
AL['Day_of_Week'] = pd.to_datetime(AL['FL_DATE']).dt.day_name()
print(AL.head())

## Label Encode
AL['Day_of_Week']= label_encoder.fit_transform(AL['Day_of_Week'])

print(AL.head())

# Preform Chi Squared on New Categorical Variable, Day of Week, with Delay
cat_var_1 = ['Day_of_Week']
cat_var_2 = ['DELAY']
result = list()
result.append((cat_var_1[0],cat_var_2[0],list(ss.chi2_contingency(pd.crosstab(AL[cat_var_1[0]], AL[cat_var_2[0]])))[1]))

corr_output = pd.DataFrame(result, columns = ['var1', 'var2', 'coeff'])
## Using pivot function to convert the above DataFrame into a crosstab
corr_output.pivot(index='var1', columns='var2', values='coeff')

## Add Weather Features and Check Correlation Between Them and Delay
# !pip install airportsdata
# !pip install meteostat
import airportsdata
from meteostat import Point, Daily
import datetime

airports = airportsdata.load('IATA')

def retrieve_weather_data(airport_code, date):
  # Convert String Date Time to Date Time Object
  date = datetime.datetime.strptime(date, '%Y-%m-%d')

  # Attempt to Get the Airport Statistics, If Failure Return None
  try:
      airport_stats = airports[airport_code]
  except KeyError:
    return None

  airport_lat = airport_stats['lat']
  airport_lon = airport_stats['lon']

  # Create Point for Airport
  airport_point = Point(airport_lat, airport_lon)

  # Get daily data for 2018
  data_airport = Daily(airport_point, date, date)
  data_airport = data_airport.fetch().reset_index()

  return data_airport

## Create Lookup Dictionary
unique_dates = AL['FL_DATE'].unique()

# Dictionary to Store Weather Features for Specific Date, Origin and Destination
date_airport_dict = dict()

for date in unique_dates:
  origin_dest = AL.loc[AL['FL_DATE'] == date, ['ORIGIN', 'DEST']]

  # Add Airport Names to a List to Be Used to Retreive Airport Latitude and Longitude
  origin_airports = list()
  for origin in origin_dest['ORIGIN']:
    origin_airports.append(origin_name_mapping[origin])

  dest_airports = list()
  for dest in origin_dest['DEST']:
    dest_airports.append(dest_name_mapping[dest])
  unique_airports = list(set(origin_airports + dest_airports)) # Remove Repeats of Airport Names

  # Create a Date Key in the Dictionary
  date_airport_dict[date] = {}
  # Extract Aiport Location for Weather Pull
  for airport_IATA in unique_airports:
    date_airport_dict[date][airport_IATA] = {}

    # Retreive the Weather Information for That Date and Specific Airport
    weather_data = retrieve_weather_data(airport_IATA, date)
    # Try Indexing the Weather Dictionary and Storing the Weather Information, If Unable to Index No Weather Information Exists for that Airport
    try:
      date_airport_dict[date][airport_IATA]['TAVG'] = weather_data.iloc[0]['tavg']
      date_airport_dict[date][airport_IATA]['SNOW'] = weather_data.iloc[0]['snow']
      date_airport_dict[date][airport_IATA]['PRCP'] = weather_data.iloc[0]['prcp']
      date_airport_dict[date][airport_IATA]['WSPD'] = weather_data.iloc[0]['wspd']
      date_airport_dict[date][airport_IATA]['PRES'] = weather_data.iloc[0]['pres']
    except:
      date_airport_dict[date][airport_IATA]['TAVG'] = None
      date_airport_dict[date][airport_IATA]['SNOW'] = None
      date_airport_dict[date][airport_IATA]['PRCP'] = None
      date_airport_dict[date][airport_IATA]['WSPD'] = None
      date_airport_dict[date][airport_IATA]['PRES'] = None

## Creation of the Weather Lists to Be Added to the DataFrame
origin_temp = list()
origin_wspd = list()
origin_snow = list()
origin_prcp = list()
origin_pres = list()

dest_temp = list()
dest_wspd = list()
dest_snow = list()
dest_prcp = list()
dest_pres = list()

for date, origin, dest in zip(AL['FL_DATE'], AL['ORIGIN'], AL['DEST']):
  origin_name = origin_name_mapping[origin]
  dest_name = dest_name_mapping[dest]

  ## Lookup the Date, Origin and Destination in the Previously Created Dictionary and Add the Appropriate Information to Their Respective Lists
  date_dict_origin = date_airport_dict[date][origin_name]
  date_dict_dest = date_airport_dict[date][dest_name]

  origin_temp.append(date_dict_origin['TAVG'])
  origin_wspd.append(date_dict_origin['WSPD'])
  origin_snow.append(date_dict_origin['SNOW'])
  origin_prcp.append(date_dict_origin['PRCP'])
  origin_pres.append(date_dict_origin['PRES'])

  dest_temp.append(date_dict_dest['TAVG'])
  dest_wspd.append(date_dict_dest['WSPD'])
  dest_snow.append(date_dict_dest['SNOW'])
  dest_prcp.append(date_dict_dest['PRCP'])
  dest_pres.append(date_dict_dest['PRES'])

# Update the DataFrame with the Additional Weather Features  

AL['ORIGIN_TAVG'] = origin_temp
AL['ORIGIN_WSPD'] = origin_wspd
AL['ORIGIN_SNOW'] = origin_snow
AL['ORIGIN_PRCP'] = origin_prcp
AL['ORIGIN_PRES'] = origin_pres

AL['DEST_TAVG'] = dest_temp
AL['DEST_WSPD'] = dest_wspd
AL['DEST_SNOW'] = dest_snow
AL['DEST_PRCP'] = dest_prcp
AL['DEST_PRES'] = dest_pres

print(AL.head())
## Check for Nulls
print(AL.isnull().sum())

## Drop Nulls
AL.dropna(inplace=True)

## Confirm Nulls Were Dropped
print(AL.isnull().sum())

## Determine Correlation Between Parameters and the Categorical Target, Delay
import scipy.stats as ss
from itertools import product

cat_continous_columns = ['ORIGIN_TAVG', 'ORIGIN_WSPD', 'ORIGIN_SNOW', 'ORIGIN_PRCP', 'ORIGIN_PRES', 'DEST_TAVG', 'DEST_WSPD', 'DEST_SNOW', 'DEST_PRCP', 'DEST_PRES', 'DELAY']
AL_con_cat = AL[cat_continous_columns]
print(AL_con_cat.head())

con_var1 = ['ORIGIN_TAVG', 'ORIGIN_WSPD', 'ORIGIN_SNOW', 'ORIGIN_PRCP', 'ORIGIN_PRES', 'DEST_TAVG', 'DEST_WSPD', 'DEST_SNOW', 'DEST_PRCP', 'DEST_PRES',]
cat_var1 = ['DELAY']
cat_con_prod = list(product(con_var1,cat_var1, repeat = 1))
print(cat_con_prod)
print(len(cat_con_prod))

# Get Correlation Between Weather Features and Delay
result = []
for prod in cat_con_prod:
  result.append((prod[0],prod[1], AL_con_cat[prod[0]].corr(AL_con_cat[prod[1]])))

print(result)

corr_output = pd.DataFrame(result, columns = ['var1', 'var2', 'coeff'])
## Using pivot function to convert the above DataFrame into a crosstab
corr_output.pivot(index='var1', columns='var2', values='coeff')

"""### Model Selection"""

from sklearn import svm, tree, naive_bayes, linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

def run_decision_tree(x_train, y_train, x_test, y_test):
  '''
  Function for Autonomous Running of a Decision Tree
  '''
 
  ## Create Decision Tree Object
  clf = tree.DecisionTreeClassifier(random_state=0)

  ## Fit clf2 with x_train_scaled and y_train_scaled
  clf.fit(x_train, y_train)

  ## Predict and Score
  predictions = clf.predict(x_test)
  score = accuracy_score(y_test, predictions)

  CM = confusion_matrix(y_test, predictions)

  TN = CM[0][0]
  FN = CM[1][0]
  TP = CM[1][1]
  FP = CM[0][1]

  confusion_dict = {'TN': TN, 'FN': FN, 'TP': TP, 'FP': FP}

  return score, confusion_dict

def run_random_forest(x_train, y_train, x_test, y_test):
  '''
  Function for Autonomous Running of the Random Forest Function
  '''
  ## Fitting the Model
  rf = RandomForestClassifier(n_estimators=500)
  rf.fit(x_train, y_train)

  ## Evaluating the Model
  predictions = rf.predict(x_test)
  score = accuracy_score(y_test, predictions)

  CM = confusion_matrix(y_test, predictions)

  TN = CM[0][0]
  FN = CM[1][0]
  TP = CM[1][1]
  FP = CM[0][1]

  confusion_dict = {'TN': TN, 'FN': FN, 'TP': TP, 'FP': FP}

  return score, confusion_dict

def run_naive_bayes(x_train, y_train, x_test, y_test):
  '''
  Function for Autonomous Running of a Naive Bayes Model
  '''

  ## Fitting the Model
  gnb = naive_bayes.GaussianNB()
  gnb.fit(x_train, y_train)

  ## Evaluating the Model
  predictions = gnb.predict(x_test)
  score = accuracy_score(y_test, predictions)

  CM = confusion_matrix(y_test, predictions)

  TN = CM[0][0]
  FN = CM[1][0]
  TP = CM[1][1]
  FP = CM[0][1]

  confusion_dict = {'TN': TN, 'FN': FN, 'TP': TP, 'FP': FP}

  return score, confusion_dict

def run_logistic_regression(x_train, y_train, x_test, y_test):
  '''
  Function for Autonomous Running of Logistic Regression
  '''
  ## Fitting the Model
  lr = linear_model.LogisticRegression(random_state=0)
  lr.fit(x_train, y_train)

  ## Evaluating the Model
  predictions = lr.predict(x_test)
  score = accuracy_score(y_test, predictions)

  CM = confusion_matrix(y_test, predictions)

  TN = CM[0][0]
  FN = CM[1][0]
  TP = CM[1][1]
  FP = CM[0][1]

  confusion_dict = {'TN': TN, 'FN': FN, 'TP': TP, 'FP': FP}

  return score, confusion_dict

# Run Models on Various Sized Training Sets

i = 10000

dt_list = []
rf_list = []
nb_list = []
lr_list = []

confusion_dict = dict()
confusion_dict['Initial Features'] = dict()

num_samples = []
while i <= 100000:
  ## Sample from Data Set Randomly of Size i
  AL_r = AL.sample(n=i, random_state=0)
  ## Split the Sample for Training and Testing
  x_train, x_test, y_train, y_test = train_test_split(AL_r[['OP_CARRIER_AIRLINE_ID', 'Airline_Name', 'OP_CARRIER_FL_NUM',
                                                            'ORIGIN', 'DEST', 'CRS_DEP_TIME', 'DEP_TIME', 'ARR_TIME', 'CRS_ELAPSED_TIME', 'ACTUAL_ELAPSED_TIME']], AL_r['DELAY'], random_state=0)
  # Run the Four Models with the Training and Testing Data
  dt_acc, dt_conf = run_decision_tree(x_train, y_train, x_test, y_test)
  rf_acc, rf_conf = run_random_forest(x_train, y_train, x_test, y_test)
  nb_acc, nb_conf = run_naive_bayes(x_train, y_train, x_test, y_test)
  lr_acc, lr_conf = run_logistic_regression(x_train, y_train, x_test, y_test);
  
  # Store the Accuracy from the Models to a List that Will be Added to a Results DataFrame
  dt_list.append(round(dt_acc*100, 2))
  rf_list.append(round(rf_acc*100, 2))
  nb_list.append(round(nb_acc*100, 2))
  lr_list.append(round(lr_acc*100, 2))

  # Store the Confusion Matrix Results of Each Model in a Dictionary for Later Result Comparison

  confusion_dict['Initial Features'][i] = dict()
  confusion_dict['Initial Features'][i]['Decision Tree'] = dt_conf
  confusion_dict['Initial Features'][i]['Random Forest'] = rf_conf
  confusion_dict['Initial Features'][i]['Naive Bayes'] = nb_conf
  confusion_dict['Initial Features'][i]['Logistic Regression'] = lr_conf

  # Samples Size is Appended to a List to Be Used as Index for the Results DataFrame
  num_samples.append(i)

  # Increment i
  i += 5000

samples_dict = {'Decision Tree Accuracy':dt_list, 'Random Forest Accuracy':rf_list, 'Naive Bayes (Gaussian) Accuracy': nb_list, 'Logistic Regression': lr_list}
samples_df_inital = pd.DataFrame(data=samples_dict, index=num_samples)

print(samples_df_inital)

i = 10000

dt_list = []
rf_list = []
nb_list = []
lr_list = []

confusion_dict['Reduced Features'] = dict()

num_samples = []
while i <= 100000:
  ## Sample from Data Set Randomly of Size i
  AL_r = AL.sample(n=i, random_state=0)
  ## Split the Sample for Training and Testing
  x_train, x_test, y_train, y_test = train_test_split(AL_r[['CRS_DEP_TIME', 'DEP_TIME', 'ARR_TIME', 'CRS_ELAPSED_TIME', 'ACTUAL_ELAPSED_TIME']], AL_r['DELAY'], random_state=0)

  dt_acc, dt_conf = run_decision_tree(x_train, y_train, x_test, y_test)
  rf_acc, rf_conf = run_random_forest(x_train, y_train, x_test, y_test)
  nb_acc, nb_conf = run_naive_bayes(x_train, y_train, x_test, y_test)
  lr_acc, lr_conf = run_logistic_regression(x_train, y_train, x_test, y_test);
  
  dt_list.append(round(dt_acc*100, 2))
  rf_list.append(round(rf_acc*100, 2))
  nb_list.append(round(nb_acc*100, 2))
  lr_list.append(round(lr_acc*100, 2))

  confusion_dict['Reduced Features'][i] = dict()
  confusion_dict['Reduced Features'][i]['Decision Tree'] = dt_conf
  confusion_dict['Reduced Features'][i]['Random Forest'] = rf_conf
  confusion_dict['Reduced Features'][i]['Naive Bayes'] = nb_conf
  confusion_dict['Reduced Features'][i]['Logistic Regression'] = lr_conf


  num_samples.append(i)

  i += 5000


samples_dict = {'Decision Tree Accuracy':dt_list, 'Random Forest Accuracy':rf_list, 'Naive Bayes (Gaussian) Accuracy': nb_list, 'Logistic Regression': lr_list}
samples_df_reduced_param = pd.DataFrame(data=samples_dict, index=num_samples)

print(samples_df_reduced_param)

## Sample from Data Set Randomly of Size i
i = 10000

dt_list = []
rf_list = []
nb_list = []
lr_list = []

confusion_dict['Day of Week Features'] = dict()

num_samples = []
while i <= 100000:
  AL_r = AL.sample(n=i, random_state=0)
  ## Split the Sample for Training and Testing
  x_train, x_test, y_train, y_test = train_test_split(AL_r[['CRS_DEP_TIME', 'DEP_TIME', 'ARR_TIME', 'CRS_ELAPSED_TIME', 'ACTUAL_ELAPSED_TIME', 'Day_of_Week']], AL_r['DELAY'], random_state=0)

  dt_acc, dt_conf = run_decision_tree(x_train, y_train, x_test, y_test)
  rf_acc, rf_conf = run_random_forest(x_train, y_train, x_test, y_test)
  nb_acc, nb_conf = run_naive_bayes(x_train, y_train, x_test, y_test)
  lr_acc, lr_conf = run_logistic_regression(x_train, y_train, x_test, y_test);
  
  dt_list.append(round(dt_acc*100, 2))
  rf_list.append(round(rf_acc*100, 2))
  nb_list.append(round(nb_acc*100, 2))
  lr_list.append(round(lr_acc*100, 2))

  confusion_dict['Day of Week Features'][i] = dict()
  confusion_dict['Day of Week Features'][i]['Decision Tree'] = dt_conf
  confusion_dict['Day of Week Features'][i]['Random Forest'] = rf_conf
  confusion_dict['Day of Week Features'][i]['Naive Bayes'] = nb_conf
  confusion_dict['Day of Week Features'][i]['Logistic Regression'] = lr_conf


  num_samples.append(i)

  i += 5000


samples_dict = {'Decision Tree Accuracy':dt_list, 'Random Forest Accuracy':rf_list, 'Naive Bayes (Gaussian) Accuracy': nb_list, 'Logistic Regression': lr_list}
samples_df_cat_days = pd.DataFrame(data=samples_dict, index=num_samples)

print(samples_df_cat_days)

## Sample from Data Set Randomly of Size i
i = 10000

dt_list = []
rf_list = []
nb_list = []
lr_list = []

confusion_dict['Weather Features'] = dict()

num_samples = []
while i <= 100000:
  AL_r = AL.sample(n=i, random_state=0)
  ## Split the Sample for Training and Testing

  x_train, x_test, y_train, y_test = train_test_split(AL_r[['CRS_DEP_TIME', 'DEP_TIME', 'ARR_TIME', 'CRS_ELAPSED_TIME', 'ACTUAL_ELAPSED_TIME', 'ORIGIN_PRCP', 'DEST_PRCP']], AL_r['DELAY'], random_state=0)

  dt_acc, dt_conf = run_decision_tree(x_train, y_train, x_test, y_test)
  rf_acc, rf_conf = run_random_forest(x_train, y_train, x_test, y_test)
  nb_acc, nb_conf = run_naive_bayes(x_train, y_train, x_test, y_test)
  lr_acc, lr_conf = run_logistic_regression(x_train, y_train, x_test, y_test);
  
  dt_list.append(round(dt_acc*100, 2))
  rf_list.append(round(rf_acc*100, 2))
  nb_list.append(round(nb_acc*100, 2))
  lr_list.append(round(lr_acc*100, 2))

  confusion_dict['Weather Features'][i] = dict()
  confusion_dict['Weather Features'][i]['Decision Tree'] = dt_conf
  confusion_dict['Weather Features'][i]['Random Forest'] = rf_conf
  confusion_dict['Weather Features'][i]['Naive Bayes'] = nb_conf
  confusion_dict['Weather Features'][i]['Logistic Regression'] = lr_conf


  num_samples.append(i)

  i += 5000

samples_dict = {'Decision Tree Accuracy':dt_list, 'Random Forest Accuracy':rf_list, 'Naive Bayes (Gaussian) Accuracy': nb_list, 'Logistic Regression': lr_list}
samples_df_weather = pd.DataFrame(data=samples_dict, index=num_samples)
print(samples_df_weather)

# Print the Differences Between the Initial Feature List and the Reduced Feature List Accuracies
i = 10000
idx = 0
while i <=100000:
  for model in samples_df_inital.columns:
    print(f'{model} w/ {i} Samples (No Additional Parameters): {samples_df_inital[model].iloc[idx]}%, {model} w/ {i} Samples (Reduced Features): {samples_df_reduced_param[model].iloc[idx]}%, Difference: {round(samples_df_inital[model].iloc[idx] - samples_df_reduced_param[model].iloc[idx], 2)}%')
  print()
  i += 5000
  idx += 1

# Print the Differences Between the Initial Feature List and the Additional Day of Week Feature w/ Redcued Feature List Accuracies
i = 10000
idx = 0
while i <=100000:
  for model in samples_df_inital.columns:
    print(f'{model} w/ {i} Samples (No Additional Parameters): {samples_df_inital[model].iloc[idx]}%, {model} w/ {i} Samples (Additional Day of Week Parameter): {samples_df_cat_days[model].iloc[idx]}%, Difference: {round(samples_df_inital[model].iloc[idx] - samples_df_cat_days[model].iloc[idx], 2)}%')
  print()
  i += 5000
  idx += 1

# Print the Differences Between the Initial Featue List and the Additional Weather Features w/ Reduced Feature List Accuracies
i = 10000
idx = 0
while i <=100000:
  for model in samples_df_inital.columns:
    print(f'{model} w/ {i} Samples (No Additional Parameters): {samples_df_inital[model].iloc[idx]}%, {model} w/ {i} Samples (Additional Weather Parameters): {samples_df_weather[model].iloc[idx]}%, Difference: {round(samples_df_inital[model].iloc[idx] - samples_df_weather[model].iloc[idx], 2)}%')
  print()
  i += 5000
  idx += 1

## Plot Histograms for Each Model
from matplotlib import rcParams

# figure size in inches
rcParams['figure.figsize'] = 20 , 20

for model in samples_df_inital.columns:

  # Need to Create Combined Data Frame Containing all the Models w/ Type of Algorithms
  indexes =  list(samples_df_inital.index.values) + list(samples_df_reduced_param.index.values) + list(samples_df_cat_days.index.values) + list(samples_df_weather.index.values)
  algo = ['No Additional Parameters'] * 19 + ['Reduced Parameters'] * 19 + ['Additional Day of Week Parameter'] * 19 + ['Additional Weather Parameters for Origin and Destination Airports'] * 19
  accurs = list(samples_df_inital[model]) + list(samples_df_reduced_param[model]) + list(samples_df_cat_days[model]) + list(samples_df_weather[model])

  conjoined_models = {'Indexes': indexes, 'Algorithm': algo, 'Accuracies': accurs}
  conjoined_model_df = pd.DataFrame(data=conjoined_models)
  sns.catplot(kind='bar', data=conjoined_model_df, x='Indexes', y='Accuracies', hue='Algorithm', height=8.27, aspect=11.7/8.27)

  plt.ylim(0,100)
  plt.title(model)

print(f'Percentage of Delayed Flights (Delay Greater than 1 Minute): {round(AL["DELAY"].sum() / len(AL["DELAY"])* 100, 2)}%')

FP_Decision = 0
FN_Decision = 0

FP_Random = 0
FN_Random = 0

FP_NB = 0
FN_NB = 0

FP_Log = 0
FN_Log = 0

samples = 0
for key, value in confusion_dict.items():
  for idx, algo in value.items():
    FP_Decision += algo['Decision Tree']['FP']
    FN_Decision += algo['Decision Tree']['FN']

    FP_Random += algo['Random Forest']['FP']
    FN_Random += algo['Random Forest']['FN']

    FP_NB += algo['Naive Bayes']['FP']
    FN_NB += algo['Naive Bayes']['FN']

    FP_Log += algo['Logistic Regression']['FP']
    FN_Log += algo['Logistic Regression']['FN']

    samples += (idx * .25)

  print(f'{key}:')

  print(f'Rate at Which Non-Delayed Flights Were Incorrectly Labeled as Delayed for Decision Trees: {round(FP_Decision/samples * 100, 2)}%')
  print(f'Rate at Which Delayed Flights Were Incorrectly Labeled as Not Delayed for Decision Trees: {round(FN_Decision/samples * 100, 2)}%\n')

  print(f'Rate at Which Non-Delayed Flights Were Incorrectly Labeled as Delayed for Random Forests: {round(FP_Random/samples * 100, 2)}%')
  print(f'Rate at Which Delayed Flights Were Incorrectly Labeled as Not Delayed for Random Forests: {round(FN_Random/samples * 100, 2)}%\n')

  print(f'Rate at Which Non-Delayed Flights Were Incorrectly Labeled as Delayed for Naive Bayes: {round(FP_NB/samples * 100, 2)}%')
  print(f'Rate at Which Delayed Flights Were Incorrectly Labeled as Not Delayed for Naive Bayes: {round(FN_NB/samples * 100, 2)}%\n')

  print(f'Rate at Which Non-Delayed Flights Were Incorrectly Labeled as Delayed for Logistic Regression: {round(FP_Log/samples * 100, 2)}%')
  print(f'Rate at Which Delayed Flights Were Incorrectly Labeled as Not Delayed for Logistic Regression: {round(FN_Log/samples * 100, 2)}%\n\n')

  samples = 0
  FP_Decision = 0
  FN_Decision = 0

  FP_Random = 0
  FN_Random = 0

  FP_NB = 0
  FN_NB = 0

  FP_Log = 0
  FN_Log = 0

def get_avgs(df):
  '''
  Function to Auto Print Means for Data Frame
  '''
  print(f"Decision Tree Avg: {round(df['Decision Tree Accuracy'].mean(), 2)}")
  print(f"Random Forest Avg: {round(df['Random Forest Accuracy'].mean(), 2)}")
  print(f"Naive Bayes Avg: {round(df['Naive Bayes (Gaussian) Accuracy'].mean(), 2)}")
  print(f"Logistic Regression Avg: {round(df['Logistic Regression'].mean(), 2)}\n")

print('Initial Featueres Average Accuracies:')
get_avgs(samples_df_inital)

print('Reduced Features Average Accuracies:')
get_avgs(samples_df_reduced_param)

print('Day of Week Additional Feature Average Accuracies:')
get_avgs(samples_df_cat_days)

print('Additional Weather Features Average Accuracies:')
get_avgs(samples_df_weather)