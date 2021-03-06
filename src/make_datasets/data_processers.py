import glob
import pandas as pd

def clean_header(df):
	"""
	This functions removes weird characters and spaces from column names, while keeping everything lower case
	"""
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')


def get_date_int(df, date_column):
	year = df[date_column].dt.year
	month = df[date_column].dt.month
	week = df[date_column].dt.week
	return year, month, week

def days_diff(df):
    df['days_since'] = (df['date_col2'] - df['date_col1']).dt.days


def calculate_time_difference(df, date_col2, date_col1):
	"""
	date_col2: name of the column with the signup date
	date_col1: name of the column with the last login
	"""
	event_year, event_month, event_week = get_date_int(df, event_date)
	lastevent_year, lastevent_month, lastevent_week = get_date_int(df, lastevent_activity)
	years_diff = lastevent_year - sign_year
	months_diff = lastlogin_month - sign_month
	weeks_diff = lastlogin_week - sign_week
	df['first_group'] = years_diff * 52 + weeks_diff + 1
	df['second_group'] = years_diff * 12 + months_diff + 1

def mass_edit(file_prefix, folder_path=''):
    """
    file_prefix: string that defines new file name
    folder_path: no need to declare it. string copied from file explorer to the folder where the files are
	"""
    if folder_path == '':
        folder_path = input('Please enter the path where the CSV files are:\n')
    folder_path = folder_path.replace("\\","/")
    if folder_path[:-1] != "/":
        folder_path = folder_path + "/"
		
	file_list = glob.glob(folder_path + '*.csv')

	for file in file_list:
		name_pos = file.rfind('\\')
		data = pd.read_csv(file)
		# changes go here!!
		data['seniority'] = data['seniority'] + 1 #in this case, i just needed to add 1 to this column in each file
		# until here!!
		data.to_csv(folder_path + file[name_pos+1:], index=False) #saving the file again with same name
		print(file+' ready!!')

# https://towardsdatascience.com/creating-python-functions-for-exploratory-data-analysis-and-data-cleaning-2c462961bd71
# -------------------------Missing values----------------------------
def check_nulls(df):
    '''
    Takes df
    Checks nulls
    '''
    if df.isnull().sum().sum() > 0:
        mask_total = df.isnull().sum().sort_values(ascending=False) 
        total = mask_total[mask_total > 0]

        mask_percent = df.isnull().mean().sort_values(ascending=False) 
        percent = mask_percent[mask_percent > 0] 

        missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    
        print(f'Total and Percentage of NaN:\n {missing_data}')
    else: 
        print('No NaN found.')

def view_columns_w_many_nans(df, missing_percent):
    '''
    Checks which columns have over specified percentage of missing values
    Takes df, missing percentage
    Returns columns as a list
    '''
    mask_percent = df.isnull().mean()
    series = mask_percent[mask_percent > missing_percent]
    columns = series.index.to_list()
    print(columns) 
    return columns

def drop_columns_w_many_nans(df, missing_percent):
    '''
    Takes df, missing percentage
    Drops the columns whose missing value is bigger than missing percentage
    Returns df
    '''
    series = view_columns_w_many_nans(df, missing_percent=missing_percent)
    list_of_cols = series.index.to_list()
    df.drop(columns=list_of_cols)
    print(list_of_cols)
    return df

# Alternatively, set a threshold for nans
def remove_null_values(df,threshold:int=0.8):
  pct_null = df.isnull().sum() / len(df)
  missing_features = pct_null[pct_null > threshold].index
  df.drop(missing_features, axis=1, inplace=True)
  df.fillna(0,inplace=True)



from sklearn.impute import SimpleImputer
imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
imp_mean.fit(df)from sklearn.ifrom sklearn.impute import SimpleImputermpute import SimpleImputer


###-------------------- Outliers-----------------------------------------------
#https://github.com/bhavikaG21/Credit-Consumption-Prediction/blob/master/Credit_Final_Model.ipynb

from scipy.stats.mstats import winsorize
from sklearn.preprocessing import Binarizer ,LabelEncoder
from sklearn.preprocessing import LabelEncoder,MinMaxScaler,StandardScaler

def check_outliers(df):
    col = list(df)
    outliers = pd.DataFrame(columns=['columns','Outliers'])
    
    for column in col:
        if column in df.select_dtypes(include=np.number).columns:
            q1 = df[column].quantile(0.25) 
            q3 = df[column].quantile(0.75)
            below = q1 - (1.5*q3 - q1)
            above = q3 + (1.5*q3 - q1)
            outliers = outliers.append({'columns':column,'Outliers':df.loc[(df[column] < below) | (df[column] > above)].shape[0]},ignore_index=True)
    return outliers


# separate the num columns and cat data columns
X_cols = X.columns
num_cols = X.select_dtypes(exclude=['object','category']).columns
cat_cols = [i for i in X_cols if i not in X[num_cols].columns]
for i in cat_cols:
    X[i] = X[i].astype('category')

#function for removing outliers
def removing_outliers(dataframe):
    cols = list(dataframe)
    for col in cols:
        if col in dataframe.select_dtypes(include=np.number).columns:
            dataframe[col] = winsorize(dataframe[col], limits=[0.1, 0.1],inclusive=(True, True))
    
    return dataframe

dataframe[col_name].map("current": 'new', fem.': "female"})

def histograms_numeric_columns(df, numerical_columns):
    '''
    Takes df, numerical columns as list
    Returns a group of histagrams
    '''
    f = pd.melt(df, value_vars=numerical_columns) 
    g = sns.FacetGrid(f, col='variable',  col_wrap=4, sharex=False, sharey=False)
    g = g.map(sns.distplot, 'value')
    return g

def heatmap_numeric_w_dependent_variable(df, dependent_variable):
    '''
    Takes df, a dependant variable as str
    Returns a heatmap of all independent variables' correlations with dependent variable 
    '''
    plt.figure(figsize=(8, 10))
    g = sns.heatmap(df.corr()[[dependent_variable]].sort_values(by=dependent_variable), 
                    annot=True, 
                    cmap='coolwarm', 
                    vmin=-1,
                    vmax=1) 
    return g

def categorical_to_ordinal_transformer(categories):
    '''
    Returns a function that will map categories to ordinal values based on the
    order of the list of `categories` given. Ex.
    If categories is ['A', 'B', 'C'] then the transformer will map 
    'A' -> 0, 'B' -> 1, 'C' -> 2.
    '''
    return lambda categorical_value: categories.index(categorical_value)

# Plot multiple columns seaborn
df = data[columns]
n=len(df.columns)
fig,ax = plt.subplots(1,n, figsize=(12,n*2), sharex=True)
for i in range(n):
    plt.sca(ax[i])
    col = df.columns[i]
    sns.countplot(x=None, y=df[col].values,data=df)
    plt.title(f'Title based on {col}')

fig, ax = plt.subplots(2,2, figsize=(12,10))
# jitter = [[False, 1], [0.5, 0.2]]

for j in range(len(ax)):
    for i in range(len(ax[j])):
        ax[j][i].tick_params(labelsize=15)
        ax[j][i].set_xlabel('label', fontsize=17, position=(.5,20))
        ax[j][i].set_ylabel('label', fontsize=17)
        # x as Hindernisabstand hinzufügen 
        ax[j][i] = sns.stripplot(x="Sex", y="SidestepDist", jitter=jitter[j][i], data=daten_csv, ax=ax[j][i])
fig.suptitle('Categorical Features Overview', position=(.5,1.1), fontsize=20)
fig.tight_layout()

fig.show()
#transform categorical features into numerical (ordinal) features:
#Step 1 - output a function, i.e. a transformer, that will transform 
# each str in a list into a int, where the int is the index of that element
# in the list.
#Step 2 - ingest a dictionary and turn it into a a tranformer to map onto dataframe
def transform_categorical_to_numercial(df, categorical_numerical_mapping):
    '''
    Transforms categorical columns to numerical columns
    Takes a df, a dictionary 
    Returns df
    '''
    transformers = {k: categorical_to_ordinal_transformer(v) 
                    for k, v in categorical_numerical_mapping.items()}
    new_df = df.copy()
    for col, transformer in transformers.items():
        new_df[col] = new_df[col].map(transformer).astype('int64')
    return new_df


# https://towardsdatascience.com/automate-boring-tasks-with-your-own-functions-a32785437179
# https://www.datacamp.com/community/tutorials/moving-averages-in-pandas
# https://stackabuse.com/scikit-learn-save-and-restore-models/
# https://stackabuse.com/tensorflow-neural-network-tutorial/\
# https://queirozf.com/entries/pandas-dataframe-groupby-examples#group-by-and-change-aggregation-column-name