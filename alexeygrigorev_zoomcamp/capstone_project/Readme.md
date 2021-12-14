# Capstone Project: Non-NLP analysis of TED talk words

What gets people to view TED talks? Here we try to find compare the effects of words used and audience reaction. Using this we can figure out TED equivalent view counts from a transcript.

## Environment Setup
The project dependencies are managed using **pipenv** to use this model first ensure you have installed pipenv 

>pip install pipenv

and navigate to the directory of this project and run

>pipenv install
>pipenv shell

to install all dependencies.

## Model training

Preparation EDA and tuning is performed in the notebook [notebook.ipynb](https://github.com/ksomf/workbook/blob/main/alexeygrigorev_zoomcamp/capstone_project/notebook.ipynb)

The tuned final model can be trained using [train.py](https://github.com/ksomf/workbook/blob/main/alexeygrigorev_zoomcamp/capstone_project/train.py) by

>pipenv shell
>python train.py

after which docker or aws can be setup

### Docker Setup

The assumption is that you have docker already installed but need to install a few extra packages, links for instructions below:
 - **MacOSX:** [kind](https://kind.sigs.k8s.io/docs/user/quick-start/)
 - **Linux and Windows:** [docker-compose](https://docs.docker.com/compose/install/), [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/), and [kind](https://kind.sigs.k8s.io/docs/user/quick-start/)
To install the Docker instance navigate to the folder and run 

>docker build -t view-gateway:dnnv1 -f view-gateway.dockerfile .
>docker build -t view-model:dnnv1 -f view-model.dockerfile .

and to run the docer isntance run

>docker-compose up


>kind create cluster
>kind load docker-image view-gateway:dnnv1
>kind load docker-image view-model:dnnv1
>kubectl cluster-info --context kind-kind
>kubectl get deployment
>kubectl get pod
>kubectl port-forward <name> 9696:9696
>kubectl apply -f kube-config/model-deployment.yaml
>kubectl apply -f kube-config/model-service.yaml
>kubectl apply -f kube-config/gateway-deployment.yaml
>kubectl apply -f kube-config/gateway-service.yaml
>kubectl prot-forward service/gateway 9696:80
