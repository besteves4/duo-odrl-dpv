# ODRL Policy Editor for DUO Concepts

## Requirements
(recommended to use `pyenv`)

1. Python3
2. dash (python-lib)
3. rdflib (python-lib)

## Usage

1. From base folder of this repo, execute `python dash/main.py`.
2. Select DUO concepts to annotate a dataset with
3. A file containing the generated `odrl:Offer` will be stored at `dash/offer.ttl`
4. Simultaneously the generated policy will be displayed in the UI
5. An `odrl:Request` can be defined in the UI and matched against the specified offer `odrl:Offer`
6. The result of the matching will be returned, stating if access to the resource is authorized or not according with its corresponding `odrl:Offer` and any duties that the requester must fulfil in case the access is authorized

## Live demo

Live demo available at [https://duodrl-demo-app.onrender.com/](https://duodrl-demo-app.onrender.com/)

A response delay of up to 30 seconds might happen for the first request that comes in after a period of inactivity.