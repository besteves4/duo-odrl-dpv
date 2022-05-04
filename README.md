# duo-odrl-dpv

The Global Alliance for Genomics and Health is an international consortium that is developing the Data Use Ontology (DUO) as a standard providing machine-readable codes for automation in data discovery and responsible sharing of genomics data. DUO concepts, which are OWL classes, only contain textual descriptions regarding the conditions for data use they represent, which limits their usefulness in automated systems.

We present use of the Open Digital Rights Language (ODRL) to make these conditions explicit as rules, and combine them to create policies that can be attached to datasets, and used to identify compatibility with a data request.
To associate the use of DUO and the ODRL policies with concepts relevant to privacy and data protection law, we use the Data Privacy Vocabulary (DPV). Through this, we show how policies can be declared in a jurisdiction-agnostic manner, and extended as needed for specific laws like the GDPR. Our work acknowledges the socio-technical importance of DUO, and therefore is intended to be complimentary to it rather than a replacement. To assist in the improvement of DUO, we provide ODRL rules for all of its concepts, an implementation of the matching algorithm, and a demonstration showing it in practice. 

Permanent url for this work: https://w3id.org/duodrl/repo.

To read more about this work, see article (under-review): ["Enhancing Data Use Ontology (DUO) for Health-Data Sharing by Extending it with ODRL and DPV" by H. J. Pandit and B. Esteves](http://www.semantic-web-journal.net/content/enhancing-data-use-ontology-duo-health-data-sharing-extending-it-odrl-and-dpv).

## Repository Contents

The repository contains the following work:

- [`./DUO`](./DUO) folder contains a copy of the DUO ontology from [http://purl.obolibrary.org/obo/duo](http://purl.obolibrary.org/obo/duo) or [https://github.com/EBISPOT/DUO](https://github.com/EBISPOT/DUO)
- [`./mappings`](./mappings) contains the ODRL policies for each DUO concept
- [`./dash`](./dash) contains a Policy Editor UI/UX as a proof-of-concept demonstration for creating ODRL policies from selected DUO concepts

## Overview of ODRL expression for DUO Concepts

| **Concept**    | **Code**            | **Rule Type** | **Constraint**                                               | **Placeholder**      |
|----------------|---------------------|---------------|--------------------------------------------------------------|----------------------|
| **DUO0000001** | Data Use Permission |
| **DUO0000042** | GRU                 | Permission    | Purpose is :GRU                                              | ~                    |
| **DUO0000006** | HMB                 | Permission    | Purpose is :HMB                                              | ~                    |
| **DUO0000006** | HMB                 | Prohibition   | Purpose is not :POA                                          | ~                    |
| **DUO0000007** | DS                  | Permission    | Purpose is :DS and mondo:0000001                             | :TemplateDisease     |
| **DUO0000004** | NRES                | Permission    | Purpose is odrl:Purpose                                      | ~                    |
| **DUO0000011** | POA                 | Permission    | Purpose is :POA                                              | ~                    |
| **DUO0000011** | POA                 | Prohibition   | Purpose is not :POA                                          | ~                    |
| **DUO0000017** | Data Use Modified   |
| **DUO0000043** | CC                  | Permission    | Purpose is :CC                                               | ~                    |
| **DUO0000020** | COL                 | Duty          | Action :COL                                                  | ~                    |
| **DUO0000021** | IRB                 | Duty          | Action :IRB                                                  | ~                    |
| **DUO0000016** | GSO                 | Permission    | Purpose is :GeneticStudies                                   | ~                    |
| **DUO0000016** | GSO                 | Permission    | Purpose is :GeneticStudies and :PhenotypeResearch            | ~                    |
| **DUO0000016** | GSO                 | Prohibition   | Purpose is :PhenotypeResearch and not :GeneticStudies        | ~                    |
| **DUO0000022** | GS                  | Permission    | Spatial is equal to specified :Location                      | :TemplateLocation    |
| **DUO0000022** | GS                  | Permission    | Spatial is not equal to specified :Location                  | :TemplateLocation    |
| **DUO0000028** | IS                  | Permission    | Assignee is :ApprovedInstitution                             | :TemplateInstitution |
| **DUO0000028** | IS                  | Prohibition   | Assignee is not :ApprovedInstitution                         | :TemplateInstitution |
| **DUO0000015** | NMDS                | Prohibition   | Purpose is :MDS                                              | ~                    |
| **DUO0000018** | NPUNCU              | Permission    | Assignee is :NotForProfitOrg and Purpose is :NotForProfit    | ~                    |
| **DUO0000018** | NPUNCU              | Prohibition   | Assignee not :NotForProfitOrg or Purpose not :NotForProfit   | ~                    |
| **DUO0000046** | NCU                 | Permission    | Purpose is :NotForProfit                                     | ~                    |
| **DUO0000046** | NCU                 | Prohibition   | Purpose is not :NotForProfit                                 | ~                    |
| **DUO0000045** | NPU                 | Permission    | Assignee is :NotForProfitOrg                                 | ~                    |
| **DUO0000045** | NPU                 | Prohibition   | Assignee is not :NotForProfitOrg                             | ~                    |
| **DUO0000044** | NPOA                | Prohibition   | Purpose is not :POA                                          | ~                    |
| **DUO0000027** | PS                  | Permission    | Project is :ApprovedProject                                  | :TemplateProject     |
| **DUO0000027** | PS                  | Prohibition   | Project is not :ApprovedProject                              | :TemplateProject     |
| **DUO0000024** | MOR                 | Duty          | Action odrl:distribute :ResultsOfStudies with odrl:dateTime  | :TemplateDateTime    |
| **DUO0000019** | PUB                 | Duty          | Action odrl:distribute for :ResultsOfStudies                 | ~                    |
| **DUO0000012** | RS                  | Permission    | Purpose is specified :Research                               | :TemplateResearch    |
| **DUO0000012** | RS                  | Prohibition   | Purpose is not specified :Research                           | :TemplateResearch    |
| **DUO0000029** | RTN                 | Duty          | Action :ReturnDerivedOrEnrichedData                          | ~                    |
| **DUO0000025** | TS                  | Permission    | Time is less than specified :TemplateDateTime                | :TemplateDateTime    |
| **DUO0000026** | US                  | Permission    | Assignee type is :ApprovedUser                               | :TemplateUser        |
| **DUO0000026** | US                  | Prohibition   | Assignee type is not :ApprovedUser                           | :TemplateUser        |
| **OBI0000066** | Data Use Permission |
| **DUO0000034** |                     | Permission    | Purpose is :AgeCategoryResearch for specified age categories | :TemplateAgeCategory |
| **DUO0000033** | ~                   | Permission    | Purpose is :POA                                              |                      |
| **DUO0000037** | ~                   | Permission    | Purpose is :HMB                                              |                      |
| **DUO0000040** | ~                   | Permission    | Purpose is :DS                                               |                      |
| **DUO0000039** | ~                   | Permission    | Purpose is :DrugDevelopment                                  |                      |
| **DUO0000038** | ~                   | Permission    | Purpose is :GeneticStudies                                   |                      |
| **DUO0000035** | ~                   | Permission    | Purpose is :GenderCategoryResearch for specified categories  | :TemplateGender      |
| **DUO0000031** | ~                   | Permission    | Purpose is :MDS                                              |                      |
| **DUO0000032** | ~                   | Permission    | Purpose is :PopulationResearch for specified population      | :TemplatePopulation  |
| **DUO0000036** | ~                   | Permission    | Purpose is :ResearchControl                                  |                      |

## Examples

### `DUO_0000011` POA

An `odrl:Set` representing `DUO_0000011` regarding Population Origins or Ancestry research (POA). The permission and prohibition over the same purpose is based on interpretation of the phrase _is limited to_ to indicate use if permitted only for that research

```turtle
:DUO_0000011 a odrl:Set ;
    rdfs:label "DUO_0000011" ;
    rdfs:comment "This data use permission indicates that use of the data is limited to the study of population origins or ancestry (POA - population origins or ancestry research only)" ;
    dct:source obo:DUO_0000011 ;
    odrl:permission [
        odrl:action odrl:use ;
        odrl:target :TemplateDataset ;
        odrl:constraint [
            odrl:leftOperand odrl:purpose ;
            odrl:operator odrl:isA ;
            odrl:rightOperand :POA ] ] ;
    odrl:prohibition [
        odrl:action odrl:use ;
        odrl:target :TemplateDataset ;
        odrl:constraint [
            odrl:leftOperand odrl:purpose ;
            odrl:operator :isNotA ;
            odrl:rightOperand :POA ] ] .
```