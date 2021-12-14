import numpy             as np
import pandas            as pd
import matplotlib.pyplot as pl
import seaborn           as sns
import tensorflow        as tf

import re
import json

from functools        import partial
from itertools        import filterfalse
from wordcloud        import WordCloud
from tensorflow       import keras
from tensorflow.keras import layers

df = pd.read_csv('data.csv')
columns = ['speaker','headline','description','event','duration','date_published','views_as_of_06162017','tags','transcript']
df = df[columns]
df['duration'] = pd.to_timedelta(df['duration']).dt.total_seconds()
df['date_published'] = pd.to_datetime(df['date_published'])
df = df.rename(columns={'views_as_of_06162017':'views'})
df = df.dropna()
wc = WordCloud()

def transcript_to_tokens(s):
    s =  list(map(lambda s: s.strip(), filter(len,s.split('\r'))))
    s = ' '.join(filterfalse(partial(re.match,'[0-9]+\:[0-9]+'),s))
    s = s.replace('.','').replace(',','').replace('!','').replace('?','').replace(':','').replace(';','').replace('"','').lower()
    emotes = re.findall('\(([^)]+)\)',s)
    speech = ' '.join(re.split('\(([^)]+)\)',s)).split()
    emotes = emotes + list(filter(lambda s: s in ['applause','laughter'],speech)) # Inconsistent annotation in transcript
    speech = filter(lambda s: not s in ['applause','laughter'],speech)
    speech = list(filter(lambda s: s not in wc.stopwords, speech))
    return (emotes,speech)

def word_count(s):
    return len(pd.value_counts(s))

def translate_df(df):
    emotes, words = zip(*df['transcript'].apply(transcript_to_tokens).to_list())
    df.loc[:,'emotes'] = list(emotes)
    df.loc[:,'words'] = list(words)
    df['unique_words'] = df['words'].apply(word_count)
    df['year_published'] = df['date_published'].dt.year
    df['month_published'] = df['date_published'].dt.month
    return df

df = translate_df(df)
all_words = [ x for xs in df['words'].to_list() for x in xs ]
word_counts = pd.value_counts(all_words)

all_emotes = [ x for xs in df['emotes'] for x in xs ]
emote_counts = pd.value_counts(all_emotes)

n_words_analyse = 50
for word in word_counts.head(n=n_words_analyse).keys():
    df[f'num_{word}'] = df['words'].apply(lambda xs: xs.count(word))

n_emotes_analyse = 2
for emote in emote_counts.head(n=n_emotes_analyse).keys():
    df[f'times_{emote}'] = df['emotes'].apply(lambda xs: xs.count(emote))

val_frac   = 0.2
test_frac  = 0.2
train_frac = 1.0 - val_frac - test_frac

df_model = df[numerical_columns]

df_full_train = df_model.sample(frac=train_frac + val_frac,random_state=0)
df_test       = df_model.drop(df_full_train.index)

y_full_train = np.log1p(df_full_train.pop('views'))
y_test       = np.log1p(df_test      .pop('views'))

def train_NN(df_train,y_train,df_val,y_val,inner_layers=[64],learning_rate=0.1,droprate=None,input_droprate=None):
    normalizer = tf.keras.layers.Normalization(axis=-1)
    normalizer.adapt(np.asarray(df_train))

    model = tf.keras.Sequential()
    model.add(normalizer)
    if input_droprate:
        model.add(layers.Dropout(droprate))
    for layer_size in inner_layers:
        model.add(layers.Dense(layer_size, activation='relu'))
        if droprate:
            model.add(layers.Dropout(droprate))
    model.add(layers.Dense(units=1))
    model.summary()

    model.compile(optimizer=tf.optimizers.Adam(learning_rate=learning_rate)
                    ,loss='mean_squared_error')
    history = model.fit(df_train,y_train,epochs=200,validation_data=(np.asarray(df_val),y_val))
    return history

best_ddn2_layer_size = [16,16]
best_ddn2_learning_rate = 0.33
best_ddn2_droprate = 0.4
best_ddn2_input_droprate = 0.0

best = train_NN(df_full_train,y_full_train,df_test,y_test
               ,inner_layers=best_ddn2_layer_size
               ,droprate=best_ddn2_droprate
               ,learning_rate=best_ddn2_learning_rate
               ,input_droprate=best_ddn2_input_droprate)

#best.model.save('keras_model')
tf.saved_model.save(best.model, 'view-model')
model_spec = { 'columns': df[numerical_columns].columns.to_list(),
               'trained_words': word_counts.head(n=n_words_analyse).keys().to_list(),
               'trained_emotes': emote_counts.head(n=n_emotes_analyse).keys().to_list()}

open('keras_model_spec.json','w+').write(json.dumps(model_spec))
