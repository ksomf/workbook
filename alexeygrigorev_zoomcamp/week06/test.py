import xgboost as xgb
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection    import train_test_split
from sklearn.metrics            import roc_auc_score
from sklearn.tree               import DecisionTreeRegressor, export_text
from sklearn.ensemble           import RandomForestRegressor


print('Wrangling')
columns = [
    'neighbourhood_group', 'room_type', 'latitude', 'longitude',
    'minimum_nights', 'number_of_reviews','reviews_per_month',
    'calculated_host_listings_count', 'availability_365',
    'price'
]

train_columns = list(filter(lambda x: x != 'price',columns))
df = pd.read_csv('AB_NYC_2019.csv', usecols=columns)
df.reviews_per_month = df.reviews_per_month.fillna(0)

df.price = np.log1p(df.price)

prop_val   = 0.2
prop_test  = 0.2
prop_train = 1.0 - prop_test - prop_val
seed = 1

df_full_train, df_test = train_test_split(df           , test_size=prop_test                          , random_state=seed)
df_train, df_val       = train_test_split(df_full_train, test_size=prop_val / (prop_train + prop_test), random_state=seed)

def setup_tensors(df):
    df = df.reset_index(drop=True)
    y  = df.price.values
    del df['price']
    return df, y

df_full_train, y_full_train = setup_tensors(df_full_train)
df_train     , y_train      = setup_tensors(df_train     )
df_val       , y_val        = setup_tensors(df_val       )
df_test      , y_test       = setup_tensors(df_test      )

print('One hot encoding')
dv = DictVectorizer(sparse=False)
def transform_set(columns, df):
    dicts = df[columns].to_dict(orient='records')
    X     = dv.fit_transform(dicts)
    return dicts, X

dicts_train, X_train = transform_set(train_columns, df_train)
dicts_val  , X_val   = transform_set(train_columns, df_val  )
dv.get_feature_names()

print('features')
features = dv.get_feature_names()

print('dtain')
dtrain   = xgb.DMatrix(X_train, label=y_train, feature_names=features)
print('dval')
dval     = xgb.DMatrix(X_val  , label=y_val  , feature_names=features)
print('watchlist')

watchlist = [(dtrain, 'train'), (dval, 'val')]
