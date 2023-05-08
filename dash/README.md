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

1. From the base folder of this repo, execute `python dash/main.py` or go to the available [live demo](https://duodrl-demo-app.onrender.com/).
2. Select one DUO data use permission concepts to annotate a dataset with a purpose for accessing.
3. Select zero/one/more DUO data use modifiers to restrict access to the dataset -- these will be added to the `odrl:Offer`.
4. Upon clicking the `Generate Offer` button, the generated policy will be displayed in the UI.
5. Next, an `odrl:Request` can be defined in the UI and matched against the specified offer `odrl:Offer`.
6. Upon clicking the `Generate Request & Match` button, the generated `odrl:Request` will be displayed and the result of the matching will be returned, stating if access to the resource is authorized or not according to its corresponding `odrl:Offer` and any duties that the requester must fulfill in case the access is authorized.

## Examples to test the demo

1. Select 'General Research Use' as the data use permission and create the Offer. Select 'Biomedical Research' as the purpose of the request and create the Request. Check the result of the matching and the Agreement.
2. Select 'No restriction' as the data use permission, 'research specific restrictions' as the data use modifier with 'Gender category research' as purpose on the 'Female' gender, and create the Offer. Select 'Gender category research' as the purpose of the request and create the Request. Check the result of the matching and the Agreement for research on 'Female' and 'Male'groups.
3. Select 'Health or Medical or Biomedical research' as the data use permission, 'publication required' as the data use modifier, and create the Offer. Select 'Research control' as the purpose of the request and create the Request. Check the result of the matching and the Agreement.
4. Select 'General Research Use' as the data use permission, the DPV-based data use modifier, and create the Offer. Select 'Biomedical Research' as the purpose of the request and create the Request. Check the result of the matching and the Agreement.