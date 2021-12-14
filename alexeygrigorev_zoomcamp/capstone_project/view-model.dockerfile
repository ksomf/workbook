FROM tensorflow/serving:2.7.0

COPY view-model /models/view-model/1
ENV MODEL_NAME='view-model'
