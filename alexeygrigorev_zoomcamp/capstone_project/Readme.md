# Capstone Project: Non-NLP analysis of TED talk words

What gets people to view TED talks? Here we try to find compare the effect of various effects like: 

- **Publication date:** Maybe TED talks as a whole become more and less popular over time
- **Common description and title words:** Presumable people browsing TED videos and looking at ones that catch their interest
- **Talk transcript contents:** Presumably word of mouth and/or algorithms

## Environment Setup 
The project dependencies are managed using **pipenv** to use this model first ensure you have installed pipenv 

>pip install pipenv 

and navigate to the directory of this project and run

>pipenv install
>pipenv shell

to install all dependencies.

## Model training

Preparation EDA and tuning is performed in the notebook [notebook.ipynb]()


The tuned final model can be trained using [train.py]() by

>pipenv shell
>python train.py

after which docker or aws can be setup

### Docker Setup

To install the Docker instance navigate to the folder and run 

>docker build -t ted-prediction .

and to run the Docker instance run

>docker run -it -p 9696:9696 ted-prediction

### AWS Elastic Beanstalk Deploy

To deploy eb app run (after *pipenv shell*)

>eb init -p docker -r region ted-prediction-serving 

for instance with **region** replaced with **us-west-1**. To test locally you can run 
    
>eb local run --port 9696
    
and in another terminal window
    
>pipenv shell
>python predict-test-local.py
    
To deploy on aws run
    
>eb create salary-serving-env

## Deployed Model Test

As the trained model is deployed on AWS you can interface directly with it by running

>python predict-test-remote.py

which will access the AWS instance for a query
