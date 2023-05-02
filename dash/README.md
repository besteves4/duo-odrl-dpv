# ODRL Policy Editor for DUO Concepts

## Requirements
(recommended to use `pyenv`)

1. Python3
2. dash (python-lib)
3. rdflib (python-lib)
4. datetime (python-lib)

## Live demo

Live demo available at [https://duodrl-demo-app.onrender.com/](https://duodrl-demo-app.onrender.com/)

A response delay of up to 30 seconds might happen for the first request that comes in after a period of inactivity.

## Usage

1. From base folder of this repo, execute `python dash/main.py` or go to the  available [live demo](https://duodrl-demo-app.onrender.com/).
2. Select one DUO data use permission concepts to annotate a dataset with a purpose for accessing.
3. Select zero/one/more DUO data use modifiers to restrict access to the dataset -- these will be added to the `odrl:Offer`.
4. Upon clicking the `Generate Offer` button, the generated policy will be displayed in the UI.
5. Next, an `odrl:Request` can be defined in the UI and matched against the specified offer `odrl:Offer`.
6. Upon clicking the `Generate Request & Match` button, the generated `odrl:Request` will be displayed and the result of the matching will be returned, stating if access to the resource is authorized or not according with its corresponding `odrl:Offer` and any duties that the requester must fulfil in case the access is authorized.
