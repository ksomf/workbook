import pickle 

import pandas  as pd
import numpy   as np
import xgboost as xgb

from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection    import train_test_split

output_file = 'model.bin'

print('Reading data')
df_raw = pd.read_csv('survey.csv')

print('Wrangling Data')
string_columns = df_raw.columns[(df_raw.dtypes == 'object')]
for col in string_columns:
    df_raw[col] = df_raw[col].str.lower().str.replace(' ','_')
df_raw = df_raw[~df_raw.industry.isnull()]
underrepresented_industries = df_raw.industry.value_counts()[(df_raw.industry.value_counts() == 1)].index.to_list()
df_raw.industry[df_raw.industry.isin(underrepresented_industries)] = 'other'
df_raw.highest_level_of_education_completed = df_raw.highest_level_of_education_completed.fillna('None')
df_raw.job_title[df_raw.job_title == 'manager,_[department_name]'] = 'manager'
single_represented_jobs = df_raw.job_title.value_counts()[df_raw.job_title.value_counts() == 1].index.to_list()
df_raw.job_title[ df_raw.job_title.isin(single_represented_jobs) ] = 'singular_job_title'
df_raw.gender = df_raw.gender.fillna('other_or_prefer_not_to_answer')
df_raw.gender[df_raw.gender == 'prefer_not_to_answer'] = 'other_or_prefer_not_to_answer'
df_raw.country[df_raw.country.isin(['united_states','usa','us','u.s.','united_states_of_america','united__states'])] = 'united_states'
df_raw.country[df_raw.country.isin(['uk','united_kingdom','england,_gb','england,_uk.','united_kindom','united_kingdom_(england)','wales_(united_kingdom)','u.k.','uk_(england)'])] = 'united_kingdom'
df_raw.country[df_raw.country.isin(['canada,_ottawa,_ontario'])] = 'canada'
df_raw.other_monetary_comp = df_raw.other_monetary_comp.fillna(0)
df_raw.currency_other = df_raw.currency_other.fillna(df_raw.currency)
df_raw = df_raw[df_raw.currency != 'other'].reset_index(drop=True)
df_raw.state = df_raw.state.fillna('na')
df_raw.state = df_raw.state.str.replace(',_*','')
df_raw.city = df_raw.city.fillna('none_supplied')
single_represented_cities = df_raw.city.value_counts()[df_raw.city.value_counts() == 1].index.to_list()
df_raw.city[ df_raw.city.isin(single_represented_cities) ] = 'singular_represented_city'
df_raw.race = df_raw.race.fillna('another_option_not_listed_here_or_prefer_not_to_answer')
df_currency = pd.DataFrame({
    'CAD'     : 0.81
,   'GBP'     : 1.37
,   'EUR'     : 1.16
,   'AUD/NZD' : 0.74 #Rough average
,   'CHF'     : 1.10
,   'SEK'     : 0.12
,   'JPY'     : 0.0088
,   'ZAR'     : 0.065
,   'HKD'     : 0.13
}.items(),columns=['currency','exchange_rate'])
df_currency.currency = df_currency.currency.str.lower()

df = df_raw.merge(df_currency,on='currency')
df['renumeration'] = df.annual_salary + df.other_monetary_comp
df['renumeration'] = df['renumeration'] * df['exchange_rate']

del df['timestamp']
del df['currency']
del df['currency_other']
del df['additional_context_on_job_title']
del df['additional_context_on_income']
del df['exchange_rate']
del df['state']
del df['race']

categorical_columns = df.columns[df.dtypes=='object' ].values
numerical_columns   = df.columns[df.dtypes=='float64'].values

print('Splitting Dataset')
seed = 1
prop_test  = 0.2
df_full_train, df_test = train_test_split(df, test_size=prop_test, random_state=seed)

def setup_tensors(df):
    df = df.reset_index(drop=True)
    y  = np.log1p(df.renumeration.values)
    for col in numerical_columns:
        del df[col]
    return df, y

df_full_train, y_full_train = setup_tensors(df_full_train)
df_test      , y_test       = setup_tensors(df_test      )

print('Setting encoding')
dv = DictVectorizer(sparse=False)
def transform_set(columns, df,fit=False):
    dicts = df[columns].to_dict(orient='records')
    if fit:
        X = dv.fit_transform(dicts)
    else:
        X = dv.transform(dicts)
    return dicts, X

fit_columns = categorical_columns 
_               , _            = transform_set(fit_columns, df           , fit=True)
dicts_full_train, X_full_train = transform_set(fit_columns, df_full_train)
dicts_test      , X_test       = transform_set(fit_columns, df_test      )
dv.get_feature_names()

dtrain_full = xgb.DMatrix(X_full_train, label=y_full_train, feature_names=dv.get_feature_names())
dtest       = xgb.DMatrix(X_test      , label=y_test      , feature_names=dv.get_feature_names())

print('Training')
watchlist = [(dtrain_full, 'full_train'), (dtest, 'test')]
xgb_params = { 'eta':0.2, 'max_depth':25, 'min_child_weight':1, 'objective':'reg:squarederror', 'nthread':2, 'seed':1, 'verbosity':1 }
model = xgb.train(xgb_params, dtrain_full, num_boost_round=100,verbose_eval=5,evals=watchlist)

print('Saving Model')
with open(output_file,'w+b') as f:
	pickle.dump((dv,model),f)
