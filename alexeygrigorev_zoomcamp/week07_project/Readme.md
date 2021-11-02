# Midterm Project: Analysis of askamanager.org Self Reported Salaries

A recent [tidy tuesday problem](https://github.com/rfordatascience/tidytuesday/tree/master/data/2021/2021-05-18) looked into the self-reported salaries of multiple thousand people on askamanager.com. The [data](https://www.askamanager.org/2021/04/how-much-money-do-you-make-4.html) was provided with the following caveat.

> The salary survey a few weeks ago got a huge response — 24,000+ people shared their salaries and other info, which is a lot of raw data to sift through. Reader Elisabeth Engl kindly took the raw data and analyzed some of the trends in it and here’s what she found. (She asked me to note that she did this as a fun project to share some insights from the survey, rather than as a paid engagement.)
> This data does not reflect the general population; it reflects Ask a Manager readers who self-selected to respond, which is a very different group (as you can see just from the demographic breakdown below, which is very white and very female).


In addition to salary and monetary compensation the survey took additional data, including; *age, experience, job sector, job title, country, gender, race and education*. Some part of the survey had free text inputs, leaving many fields unuseable, in this project, some attempt was made as wrangling these malformed inputs into their correct forms.

In this project I will analyse how the discussed parameters predict the salary compensation, finding the most relevant markers to predict earnings.

## Environment Setup 
The project dependencies are managed using **pipenv** to use this model first ensure you have installed pipenv 

>pip install pipenv 

and navigate to the directory of this project and run

>pipenv install
>pipenv shell

to install all dependencies.

## Model training

EDA and tuning is performed in the notebook [notebook.ipynb]{https://github.com/ksomf/workbook/blob/main/alexeygrigorev_zoomcamp/week07_project/notebook.ipynb}


The tuned final model can be trained using [train.py]{https://github.com/ksomf/workbook/blob/main/alexeygrigorev_zoomcamp/week07_project/train.py} by

>pipenv shell
>python train.py

after which docker or aws can be setup

### Docker Setup

To install the Docker instance navigate to the folder and run 

>docker build -t renumeration-prediction .

and to run the Docker instance run

>docker run -it -p 9696:9696 renumeration-prediction:latest

### AWS Elastic Beanstalk Deploy

To deploy eb app run (after *pipenv shell*)

>eb init -p docker -r region salary-serving 

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
