# duo-odrl-dpv

The Global Alliance for Genomics and Health is an international consortium that is developing the Data Use Ontology (DUO) as a standard providing machine-readable codes for automation in data discovery and responsible sharing of genomics data. DUO concepts, which are OWL classes, only contain textual descriptions regarding the conditions for data use they represent, which limits their usefulness in automated systems.

We present the use of the Open Digital Rights Language (ODRL) to make these conditions explicit as rules, and combine them to create policies that can be attached to datasets, and used to identify compatibility with a data request.

To associate the use of DUO and the ODRL policies with concepts relevant to privacy and data protection law, we use the Data Privacy Vocabulary (DPV). Through this, we show how policies can be declared in a jurisdiction-agnostic manner, and extended as needed for specific laws like the GDPR. Our work acknowledges the socio-technical importance of DUO and therefore is intended to be complimentary to it rather than a replacement. To assist in the improvement of DUO, we provide ODRL rules for all of its concepts, an implementation of the matching algorithm, and a demonstration showing it in practice. 

Permanent URL for this work: [https://w3id.org/duodrl/repo](https://w3id.org/duodrl/repo)

To read more about this work, see the article (accepted for publishing at the Semantic Web Journal): ["Enhancing Data Use Ontology (DUO) for Health-Data Sharing by Extending it with ODRL and DPV" by H. J. Pandit and B. Esteves](https://doi.org/10.3233/SW-243583).

> Relevant links: [DUO](http://purl.obolibrary.org/obo/duo); [ODRL](https://www.w3.org/TR/odrl-model/); [DPV](https://w3id.org/dpv)

**Table of Contents**

- [duo-odrl-dpv](#duo-odrl-dpv)
  * [Repository Contents](#repository-contents)
  * [Overview of ODRL expression for DUO Concepts](#overview-of-odrl-expression-for-duo-concepts)
  * [Namespaces](#namespaces)
  * [Examples of ODRL Rules for DUO](#examples-of-odrl-rules-for-duo)
    + [`odrl:Set` for representing rules in DUO Concepts](#odrlset-for-representing-rules-in-duo-concepts)
    + [`odrl:Offer` for representing policy over a Dataset](#odrloffer-for-representing-policy-over-a-dataset)
    + [`odrl:Request` for requesting investigation](#odrlrequest-for-requesting-investigation)
    + [`odrl:Agreement` for indicating decision regarding data use](#odrlagreement-for-indicating-decision-regarding-data-use)
  * [Examples of DPV use for Legal Concepts](#examples-of-dpv-use-for-legal-concepts)
    + [Mapping between DPV and ODRL concepts](#mapping-between-dpv-and-odrl-concepts)
    + [Jurisdiction-Agnostic Policy](#jurisdiction-agnostic-policy)
    + [GDPR-specific Policy](#gdpr-specific-policy)


## Repository Contents

The repository contains the following work:

- [`./DUO`](./DUO) folder contains a copy of the DUO ontology from [http://purl.obolibrary.org/obo/duo](http://purl.obolibrary.org/obo/duo) or [https://github.com/EBISPOT/DUO](https://github.com/EBISPOT/DUO)
- [`./mappings`](./mappings) contains the ODRL policies for each DUO concept
- [`./docs`](./docs) contains the ad-hoc ontology TTL and HTML files
- [`./dash`](./dash) contains a Policy Editor UI/UX as a proof-of-concept demonstration for creating ODRL policies from selected DUO concepts

## Overview of ODRL expression for DUO Concepts

| **Concept**    | **Code**            | **Rule Type** | **Constraint**                                               | **Placeholder**      |
|----------------|---------------------|---------------|--------------------------------------------------------------|----------------------|
| **DUO0000001** | Data Use Permission |
| **DUO0000042** | GRU                 | Permission    | Purpose is :GRU                                              | ~                    |
| **DUO0000006** | HMB                 | Permission    | Purpose is :HMB and not :POA                                 | ~                    |
| **DUO0000007** | DS                  | Permission    | Purpose is :DS and mondo:0000001                             | :TemplateDisease     |
| **DUO0000004** | NRES                | Permission    | Purpose is odrl:Purpose                                      | ~                    |
| **DUO0000011** | POA                 | Permission    | Purpose is :POA                                              | ~                    |
| **DUO0000011** | POA                 | Prohibition   | Purpose is not :POA                                          | ~                    |
| **DUO0000017** | Data Use Modifier   |
| **DUO0000043** | CC                  | Permission    | Purpose is :CC                                               | ~                    |
| **DUO0000020** | COL                 | Duty          | Action is :CollaborateWithStudyPI before policy event        | ~                    |
| **DUO0000021** | IRB                 | Duty          | Action is :ProvideEthicalApproval                            | ~                    |
| **DUO0000016** | GSO                 | Permission    | Purpose is :GS (GeneticStudies) and :GSG (Genotype)          | ~                    |
| **DUO0000016** | GSO                 | Prohibition   | Purpose is :GS and not :GSG                                  | ~                    |
| **DUO0000022** | GS                  | Permission    | Spatial is less than or equal to specified Location          | :TemplateLocation    |
| **DUO0000022** | GS                  | Prohibition   | Spatial is greater than specified :Location                  | :TemplateLocation    |
| **DUO0000028** | IS                  | Permission    | Assignee is :ApprovedInstitution                             | :TemplateInstitution |
| **DUO0000028** | IS                  | Prohibition   | Assignee is not :ApprovedInstitution                         | :TemplateInstitution |
| **DUO0000015** | NMDS                | Prohibition   | Purpose is :MDS                                              | ~                    |
| **DUO0000018** | NPUNCU              | Permission    | Assignee is :NotForProfitOrganisation and Purpose is :NCU    | ~                    |
| **DUO0000018** | NPUNCU              | Prohibition   | Assignee is :ForProfitOrganisation and Purpose is :NCU       | ~                    |
| **DUO0000018** | NPUNCU              | Prohibition   | Assignee is :NotForProfitOrganisation and Purpose is not :NCU| ~                    |
| **DUO0000046** | NCU                 | Permission    | Purpose is :NCU                                              | ~                    |
| **DUO0000046** | NCU                 | Prohibition   | Purpose is not :NCU                                          | ~                    |
| **DUO0000045** | NPU                 | Permission    | Assignee is :NotForProfitOrganisation                        | ~                    |
| **DUO0000045** | NPU                 | Prohibition   | Assignee is :ForProfitOrganisation                           | ~                    |
| **DUO0000044** | NPOA                | Prohibition   | Purpose is :POA                                              | ~                    |
| **DUO0000027** | PS                  | Permission    | Project is :ApprovedProject                                  | :TemplateProject     |
| **DUO0000027** | PS                  | Prohibition   | Project is not :ApprovedProject                              | :TemplateProject     |
| **DUO0000024** | MOR                 | Prohibition   | Action is odrl:distribute ResultsOfStudies before Date       | :TemplateDateTime    |
| **DUO0000019** | PUB                 | Duty          | Action is odrl:distribute :ResultsOfStudies                  | ~                    |
| **DUO0000012** | RS                  | Permission    | Purpose is specified :Research                               | :TemplateResearch    |
| **DUO0000012** | RS                  | Prohibition   | Purpose is not specified :Research                           | :TemplateResearch    |
| **DUO0000029** | RTN                 | Duty          | Action is :ReturnDerivedOrEnrichedData                       | ~                    |
| **DUO0000025** | TS                  | Permission    | Temporal validity is less than specified Time                | :TemplateDateTime    |
| **DUO0000026** | US                  | Permission    | Assignee is :ApprovedUser                                    | :TemplateUser        |
| **DUO0000026** | US                  | Prohibition   | Assignee is not :ApprovedUser                                | :TemplateUser        |
| **OBI0000066** | Investigation       |             
| **DUO0000034** |                     | Permission    | Purpose is :AgeCategoryResearch for specified :AgeCategory   | :TemplateAgeCategory |
| **DUO0000033** | ~                   | Permission    | Purpose is :POA                                              |                      |
| **DUO0000037** | ~                   | Permission    | Purpose is :HMB                                              |                      |
| **DUO0000040** | ~                   | Permission    | Purpose is :DS and mondo:0000001                             | :TemplateDisease     |
| **DUO0000039** | ~                   | Permission    | Purpose is :DrugDevelopment                                  |                      |
| **DUO0000038** | ~                   | Permission    | Purpose is :GS                                               |                      |
| **DUO0000035** | ~                   | Permission    | Purpose is :GenderCategoryResearch for specified :Gender     | :TemplateGender      |
| **DUO0000031** | ~                   | Permission    | Purpose is :MDS                                              |                      |
| **DUO0000032** | ~                   | Permission    | Purpose is :PopulationGroupResearch for specified :Group     | :TemplatePopulation  |
| **DUO0000036** | ~                   | Permission    | Purpose is :ResearchControl                                  |                      |

## Namespaces

|**Prefix**|**Namespace**                              |
|----------|-------------------------------------------|
|xsd       |http://www.w3.org/2001/XMLSchema#          |
|owl       |http://www.w3.org/2002/07/owl#             |
|vann      |http://purl.org/vocab/vann/                |
|skos      |http://www.w3.org/2004/02/skos/core#       |
|rdf       |http://www.w3.org/1999/02/22-rdf-syntax-ns#|
|rdfs      |http://www.w3.org/2000/01/rdf-schema#      |
|dcterms   |http://purl.org/dc/terms/                  |
|odrl      |http://www.w3.org/ns/odrl/2/               |
|obo       |http://purl.obolibrary.org/obo/            |
|dpv       |https://w3id.org/dpv#                      |
|legal-eu  |https://w3id.org/dpv/legal/eu#             |
|eu-gdpr   |https://w3id.org/dpv/legal/eu/gdpr#        |
|ex        |https://example.com/                       |
|          |https://w3id.org/duodrl#                   |

## Examples of ODRL Rules for DUO

### `odrl:Set` for representing rules in DUO Concepts

An `odrl:Set` representing `DUO_0000011` regarding Population Origins or Ancestry research (POA). The permission and prohibition over the same purpose are based on the interpretation of the phrase _is limited to_ to indicate use is permitted only for that research

```turtle
:DUO_0000011 a odrl:Set ;
    odrl:uid :DUO_0000011 ;
    rdfs:label "DUO_0000011" ;
    rdfs:comment "This data use permission indicates that use of the data is limited to the study of population origins or ancestry (POA - population origins or ancestry research only)" ;
    skos:exactMatch obo:DUO_0000042 ;
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

### `odrl:Offer` for representing policy over a Dataset

```turtle
ex:offer_for_GRU_TS_COL a odrl:Offer ;
    odrl:uid ex:offer_for_GRU_TS_COL ;
    rdfs:label "Offer to use dataset for GRU within time limits while collaborating with the primary study investigator" ;
    odrl:target <https://example.com/Dataset> ;
    odrl:action odrl:use ;
    odrl:assigner <https://example.com/SomeDepositor> ;
    dcterms:source :DUO_0000042, :DUO_0000025, :DUO_0000020 ;
    dcterms:dateSubmitted "2022-04-30"^^xsd:date ;
    odrl:permission [
        odrl:duty [ odrl:action :CollaborateWithStudyPI ] ] ;
    odrl:permission [
        odrl:constraint [ 
            odrl:leftOperand odrl:elapsedTime ;
            odrl:operator odrl:lteq ;
            odrl:rightOperand "2022-12-31"^^xsd:date ] ] ;
    odrl:permission [
        odrl:constraint [ 
            odrl:leftOperand odrl:purpose ;
            odrl:operator odrl:isA ;
            odrl:rightOperand :GRU ] ] .
```

### `odrl:Request` for requesting investigation

```turtle
ex:request_for_GS a odrl:Request ;
    odrl:uid ex:request_for_GS ;
    rdfs:label "A request for GS (DUO_0000038)" ;
    rdfs:comment "Request for biomedical research concerning genetics (i.e., the study of genes, genetic variations and heredity)" ;
    dcterms:source :DUO_0000038 ;
    dcterms:dateSubmitted "2022-05-01"^^xsd:date ;
    odrl:permission [
        odrl:action odrl:use ;
        odrl:target :TemplateDataset ;
        odrl:assignee <https://example.com/SomeRequestor> ;
        odrl:constraint [
            odrl:leftOperand odrl:purpose ;
            odrl:operator odrl:isA ;
            odrl:rightOperand :GS ] ] .
```

### `odrl:Agreement` for indicating decision regarding data use

```turtle
ex:agreement a odrl:Agreement ;
    odrl:uid ex:agreement ;
    dcterms:dateAccepted "2022-05-31"^^xsd:date ;
    odrl:permission [
        odrl:action odrl:use ;
        odrl:target <https://example.com/Dataset> ;
        odrl:assigner <https://example.com/SomeDepositor> ;
        odrl:assignee <https://example.com/SomeRequestor> ;
        odrl:constraint [
            odrl:leftOperand odrl:purpose ;
            odrl:operator odrl:isA ;
            odrl:rightOperand :GS ] ] .
```

## Examples of DPV use for Legal Concepts

### Mapping between DPV and ODRL concepts

| **DPV Concept**                           | **ODRL Concept** | **Relationship** |
|-------------------------------------------|------------------|------------------|
| **dpv:Entity**                            | odrl:Party       | subclass         |
| **dpv:Purpose**                           | odrl:Purpose     | subclass         |
| **dpv:Processing**                        | odrl:Action      | subclass         |
| **dpv:PersonalData**                      | odrl:Asset       | subclass         |
| **dpv:LegalAgreement**                    | odrl:Policy      | subclass         |
| **dpv:hasTechnicalOrganisationalMeasure** | odrl:LeftOperand | instance         |
| **dpv:hasLocation**                       | odrl:LeftOperand | instance         |
| **dpv:hasJurisdiction**                   | odrl:LeftOperand | instance         |
| **dpv:hasApplicableLaw**                  | odrl:LeftOperand | instance         |
| **dpv:hasLegalBasis**                     | odrl:LeftOperand | instance         |
| **dpv:hasRecipient**                      | odrl:LeftOperand | instance         |
| **dpv:hasRight**                          | odrl:LeftOperand | instance         |
| **dpv:hasRisk**                           | odrl:LeftOperand | instance         |

### Jurisdiction-Agnostic Policy

```turtle
ex:offer_dpv a odrl:Offer ;
    odrl:uid ex:offer_dpv ;
    rdfs:label "Offer to use dataset using Consent, and requiring an Impact Assessment" ;
    odrl:target <https://example.com/Dataset> ;
    odrl:action dpv:Use ;
    odrl:assigner <https://example.com/SomeDepositor> ;
    odrl:permission [
        odrl:constraint [ 
            odrl:leftOperand dpv:hasLegalBasis ;
            odrl:operator odrl:isA ;
            odrl:rightOperand dpv:Consent ] ] ;
    odrl:permission [
        odrl:constraint [ 
            odrl:leftOperand dpv:hasOrganisationalMeasure ;
            odrl:operator odrl:isA ;
            odrl:rightOperand dpv:ImpactAssessment ] ] .
```

### GDPR-specific Policy

```turtle
ex:offer_dpv_gdpr a odrl:Offer ;
    odrl:uid ex:offer_dpv_gdpr ;
    rdfs:label "Offer to use dataset using GDPR's Explicit Consent, and requiring a DPIA" ;
    odrl:target <https://example.com/Dataset> ;
    odrl:action dpv:Use ;
    odrl:assigner <https://example.com/SomeDepositor> ;
    dpv:hasApplicableLaw legal-eu:law-GDPR ;
    odrl:permission [
        odrl:constraint [ 
            odrl:leftOperand dpv:hasLegalBasis ;
            odrl:operator odrl:isA ;
            odrl:rightOperand eu-gdpr:A6-1-a-explicit-consent ] ] ;
    odrl:permission [
        odrl:constraint [ 
            odrl:leftOperand dpv:hasOrganisationalMeasure ;
            odrl:operator odrl:isA ;
            odrl:rightOperand dpv:DPIA ] ] .
```
