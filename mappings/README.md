# Expressing DUO concepts as ODRL policies

Each DUO concept is expressed as an `odrl:Set` representing a collection of permissions, prohibitions, and duties over the dataset (as an asset or resource). For valid policies that require specific instances to be mentioned, we use the notion of a placeholder _template_ concept that is replaced with the actual value when the ODRL policy is generated for a specific dataset.

- [`./duo-odrl-vocab.ttl`](./duo-odrl-vocab.ttl) contains the ad-hoc vocabulary for providing concepts necessary to create ODRL rules
- `DUO_00000XX*.ttl` contains the equivalent ODRL rules for `XX` concept in DUO

## Overview

### Process

For each concept in DUO, we first sought to identify the constraints or
conditions by interpreting the textual description and identifying
whether it related to a permission, prohibition, or obligation, and the
specific context of how those are to be applied. In doing this, we
observed duplicity and overlap between DUO’s data use permissions and
modifiers as both contained *purpose-based conditions* without a clear
distinction between their semantics and interpretation, and regarding
permission or prohibition of that purpose as an indication of *consent*.
For example, `DUO_0000011` represents permission and `DUO_0000044`
represents prohibition for “population origins or ancestry research”,
with the former being a data user permission and the latter a data use
modifier.

We suggest restructuring the taxonomies in DUO to address this by
considering a single purpose-based taxonomy specifying research concepts
that either have variants for permission and prohibition (i.e. two
distinct concepts), or to explicitly provide a data use modifier concept
representing permission or prohibition that is applied over a specified
research purpose. This is based on DUOS’s data collection input forms
and ADA-M’s concepts where each research purpose can be individually
consented (or restricted) to, with possible implications arising from
lack of any permission or prohibition.

After analysing DUO’s concepts and identifying inherent conditions, we
formulated the relevant ODRL rules for expressing those conditions.
Where this was not possible because of ODRL lacking the required
concept, we created proposed extensions of its concepts to enable rule
expressions. For each concept, we constructed an `odrl:Set` instance
representing the specific rules, that can be consolidated into an 
`odrl:Offer` representing a collective singular policy for a dataset.

### Challenges

We faced challenges in interpreting specific phrases such as “*is
limited to*” which imply that usage is permitted within and only within
that specific scope. If this interpretation is correct, then DUO should
clarify how potential conflicts should be resolved, for example between
rules expressing exclusive limitations and other permissive expressions
(e.g. “*is allowed for*”). Our suggestion is to take advantage of ODRL’s
ability to express these rules as code through which it can identify
when a given collection of rules associated with a single dataset are
contradictory or impossible to satisfy, e.g. by checking the
satisfiability of a policy against itself.

Currently, DUO concepts are limited to representing conditions for data
use, with suggestions referring to external ontologies for additional
concepts required for expressing scope or restrictions. For example,
`DUO_0000007` represents permission for disease-specific research, with
recommendation to use MONDO ontology for specifying diseases. Other
specific concepts mentioned in the textual descriptions but not modelled
explicitly include codes inherited from predecessors, such as *CC* for
Clinical Care Use, or *GRU* for General Research Use. Expressing ODRL
rules requires these concepts to be explicitly defined e.g. as *Disease*
for the disease-specific research, upon which permissions or
prohibitions are then expressed.

For our implementation, we identified and collected such ‘missing terms’
into an ad-hoc vocabulary to permit ODRL rules to be expressed correctly
for each DUO concept. We recommend DUO to adopt these or to create a
similar vocabulary for explicitly providing the concepts and their
descriptions separate from the data use conditions in which they are
used. This also has the added advantage of providing better
documentation of information represented by those concepts. For e.g. by
modelling *IRB* as a concept representing Ethics Review Board approval,
it is possible to add information about what processes and requirements
are needed in such reviews. It also permits further rules pertaining to
ethics approvals to be semantically associated with a base concept, e.g.
to indicate it must be carried out prior to data use, or periodically,
or before publishing any outcomes.

### Table of Interpreted ODRL Rules

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

## Example `DUO:0000022` GS

```turtle
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX : <https://w3id.org/duodrl#>

:DUO_0000022 a odrl:Set ;
    rdfs:label "DUO_0000022: This data use modifier indicates that use is limited to within a specific geographic region. (GS - geographical restriction)" ;
    skos:exactMatch obo:DUO_0000022 ;
    odrl:permission [
        odrl:target :TemplateDataset ;
        odrl:constraint [
            odrl:leftOperand odrl:spatial ;
            odrl:operator odrl:eq ;
            odrl:rightOperand :TemplateLocation
        ]
    ] .
```
