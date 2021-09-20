#!/bin/bash

# Instructions according to https://github.com/alexeygrigorev/mlbookcamp-code/blob/master/course-zoomcamp/01-intro/06-environment.md
conda create -n ml-zoomcamp python=3.8
source activate ml-zoomcamp
conda install numpy pandas scikit-learn seaborn jupyter

pip install xgboost
pip install tensorflow
