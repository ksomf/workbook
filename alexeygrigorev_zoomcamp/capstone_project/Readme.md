# Capstone Project: Non-NLP analysis of TED talk words

What gets people to view TED talks? Here we try to find compare the effects of words used and audience reaction. Using this we can figure out TED equivalent view counts from a transcript.

## Environment Setup
The project dependencies are managed using **pipenv** to use this model first ensure you have installed pipenv by running `pip install pipenv` and navigate to the directory of this project and run `pipenv install` to install all dependencies and launch the shell.

## Model training

Preparation EDA and tuning is performed in the notebook [notebook.ipynb](https://github.com/ksomf/workbook/blob/main/alexeygrigorev_zoomcamp/capstone_project/notebook.ipynb)

The tuned final model can be trained using [train.py](https://github.com/ksomf/workbook/blob/main/alexeygrigorev_zoomcamp/capstone_project/train.py) by

```bash
pipenv shell
python train.py
```

Using the resultant model or the supplied model in the project it can be deployed locally with either `docker-compose` or `kubectl` as described below and tested using [test.py](https://github.com/ksomf/workbook/blob/main/alexeygrigorev_zoomcamp/capstone_project/test.py).

## Docker Setup

The assumption is that you have docker already installed but need to install a few extra packages, links for instructions below:
 - **MacOSX:** [kind](https://kind.sigs.k8s.io/docs/user/quick-start/)
 - **Linux and Windows:** [docker-compose](https://docs.docker.com/compose/install/), [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/), and [kind](https://kind.sigs.k8s.io/docs/user/quick-start/)

To install the Docker instances navigate to the folder and run 

```bash
docker build -t view-gateway:dnnv1 -f view-gateway.dockerfile .
docker build -t view-model:dnnv1 -f view-model.dockerfile .
```

The docker isntances can be deployed by `docker-compose up` and tested with `python test.py`

## Kubernetes Setup

First make sure that you have a kind cluster running by running `kind create cluster`. Run the following commands below in order to load the docker images, the deployment,  services, and finally port forwarding it to the previous port.

```bash
kind load docker-image view-gateway:dnnv1
kind load docker-image view-model:dnnv1
kubectl apply -f kube-config/model-deployment.yaml
kubectl apply -f kube-config/model-service.yaml
kubectl apply -f kube-config/gateway-deployment.yaml
kubectl apply -f kube-config/gateway-service.yaml
kubectl prot-forward service/gateway 9696:80
```

After these commands have been run the service can be tested with the same test script `python test.py`
