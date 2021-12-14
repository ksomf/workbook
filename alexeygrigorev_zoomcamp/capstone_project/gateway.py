import numpy      as np
import pandas     as pd
import tensorflow as tf

import re
import json
import os

from functools  import partial
from itertools  import filterfalse
from flask      import Flask, request, jsonify

import grpc
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

from proto import np_to_protobuf


spec_file  = 'keras_model_spec.json'
spec = json.load(open(spec_file,'r'))

def transcript_to_tokens(s):
    s =  list(map(lambda s: s.strip(), filter(len,s.split('\r'))))
    s = ' '.join(filterfalse(partial(re.match,'[0-9]+\:[0-9]+'),s))
    s = s.replace('.','').replace(',','').replace('!','').replace('?','').replace(':','').replace(';','').replace('"','').lower()
    emotes = re.findall('\(([^)]+)\)',s)
    speech = ' '.join(re.split('\(([^)]+)\)',s)).split()
    emotes = emotes + list(filter(lambda s: s in ['applause','laughter'],speech)) # Inconsistent annotation in transcript
    speech = list(filter(lambda s: not s in ['applause','laughter'],speech))
    return (emotes,speech)

def word_count(s):
    return len(pd.value_counts(s))

def translate_dict(d):
    emotes, words = transcript_to_tokens(d['transcript'])
    d['words'] = words
    d['emotes'] = emotes
    d['unique_words'] = word_count(words)
    df = pd.DataFrame([d])
    df['duration'] = pd.to_timedelta(df['duration']).dt.total_seconds()
    df['date_published'] = pd.to_datetime(df['date_published'])
    df['year_published'] = df['date_published'].dt.year
    df['month_published'] = df['date_published'].dt.month  

    for word in spec['trained_words']:
        df[f'num_{word}'] = df['words'].apply(lambda xs: xs.count(word))

    for emote in spec['trained_emotes']:
        df[f'times_{emote}'] = df['emotes'].apply(lambda xs: xs.count(emote))
    return df[spec['columns']]

host = os.getenv('TF_SERVING_HOST','localhost:8500')
channel = grpc.insecure_channel(host)
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

app = Flask('views')

@app.route('/predict', methods=['POST'])
def predict():
    talk = request.get_json()

    default_data = {'duration':'0:15:00', 'date_published':'01/01/2017'}
    default_data.update(talk)
    talk_df = translate_dict(default_data)[spec['columns']]

    #print(talk_df)
    #print(talk_df.values)
    #print(np_to_protobuf(talk_df.values))

    pb_request = predict_pb2.PredictRequest()
    pb_request.model_spec.name = 'view-model'
    pb_request.model_spec.signature_name = 'serving_default'
    pb_request.inputs['normalization_46_input'].CopyFrom(np_to_protobuf(talk_df.values))

    pb_response = stub.Predict(pb_request,timeout=20.0)
    preds = pb_response.outputs['dense_108'].float_val

    result = {
        'predicted_views': np.expm1(preds).tolist()[0]
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
