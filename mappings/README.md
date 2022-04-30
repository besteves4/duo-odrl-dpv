# duo-odrl-dpv

Convert DUO restrictions (in [csv](https://github.com/EBISPOT/DUO/blob/master/duo.csv) and in [owl](https://github.com/EBISPOT/DUO/blob/master/duo.owl)) to ODRL+DPV policies.

Example:
 - DUO:0000004 - No restriction	(NRES): This data use permission indicates there is no restriction on use.

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX dpv: <http://www.w3.org/ns/dpv#>
PREFIX oac: <https://w3id.org/oac/>
PREFIX : <http://example.com>

:DUO_0000004 a odrl:Policy ;
    odrl:profile oac: ;
    rdfs:label "DUO_0000004: this data use permission indicates there is no restriction on use (NRES)" ;
    odrl:permission [
        a odrl:Permission ;
        odrl:assigner [ a oac:DataSubject ; dpv:hasName "Jane Doe" ] ;
        odrl:action odrl:use ;
        odrl:target </jane-doe/data/> ;
    ] .
```
