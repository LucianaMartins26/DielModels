# Diel Models

### Compatibility

_diel_models_ is compatible with the following versions of Python:

```
Python 3.8
Python 3.9
Python 3.10
Python 3.11
Python 3.12
```

### Description
*diel_models* is a python package generated from this project and has its own [ReadtheDocs](https://dielmodels.readthedocs.io/) file.

Despite numerous successful studies, modeling plant metabolism remains challenging for several reasons, such as limited information, incomplete annotations, and dynamic changes in plant metabolism that occur under different conditions, including night and day.
In particular, the integration of these day-night cycles (diel cycles) is complex, laborious, and time-consuming.

With this in mind, this package aims to accelerate this process by being able to transform a non-diel model into a diel model.

### Table of contents:

- [Installation](#installation)
    - [Pip](#pip)
- [Getting Started](#getting-started)
- [Expanding the pipeline](#expanding-the-pipeline)
- [Where to find the publication results](#where-to-find-the-publication-results)

## Installation
### Pip

``` pip install diel_models==1.1.1 ```

## Getting Started
Using this package, you can handle generic or multi-tissue models by:

* Assigning day and night;
* Inserting specified metabolites into the storage pool allowing their transition between day and night, and vice versa; 
* Supressing the photon reaction flux at night; 
* Setting the flux of the nitrate reactions to 3:2 according to the literature; 
* (optional) Taking the day and night biomass reactions and creating a total biomass reaction resulting from the junctions of both. Supressing at the same time the flow of the individual reactions to zero and setting the total biomass reaction as the objective function.

If each method is to be applied individually it is essential that the first 3 steps are applied in that order specifically.

**Alternatively, it is possible to apply all methods to a given model, running the entire pipeline (where the arguments are all relative to the original model), as shown below:**

- Generic model:

```python
import cobra
from diel_models.diel_models_creator import diel_models_creator

model = cobra.io.read_sbml_model('.../.../desired_single_tissue_model.xml')

storage_pool_metabolites = ['Metabolite_ID_1', 'Metabolite_ID_2', 'Metabolite_ID_3']

diel_models_creator(model, storage_pool_metabolites, ['Photon_Reaction_ID'], ['Nitrate_Reaction_ID'], 'Biomass_Reaction_ID')
```

- Multi-tissue model:

```python
import cobra
from diel_models.diel_models_creator import diel_models_creator

model = cobra.io.read_sbml_model('.../.../desired_multi_tissue_model.xml')

storage_pool_metabolites = ['Metabolite_ID_1', 'Metabolite_ID_2', 'Metabolite_ID_3']

tissues = ['Tissue_ID_1', 'Tissue_ID_2']

diel_models_creator(model, storage_pool_metabolites, ['Photon_Reaction_ID'], ['Nitrate_Reaction_ID'], 'Biomass_Reaction_ID', tissues)
```

This is possible due to the created *Pipeline* class that derives from a *Step* class with abstract methods - both present in this package, in the [pipeline.py](src/diel_models/pipeline.py) file.

## Expanding the pipeline

It is possible to add other classes to the *diel_models_creator* function, if desired, for example to create a different adjustment that needs to be taken into account in the diel models.
To expand the pipeline, it is necessary to create a new class that inherits from the *Step* class and implement the abstract methods.
  
Considering a new hypothetical file **new_class.py**, this new class, in addition to the desired methods, would have to contain the two abstract methods of the *Step* class, *run* and *validate*, which, respectively, runs all the methods of the class returning the model and performs asserts to validate whether the class has been implemented successfully (or simply doesn't apply any if it doesn't make sense).

```python
from diel_models.pipeline import Step

class NewClass(Step):

  def __init__(self, model, param1):
    self.model = model
    self.param1 = param1

  def method1(self):
    pass

  def method2(self):
    pass

  def run(self):
    self.method1()
    self.method2()

    return self.model

  def validate(self):
    pass
```

Then you need to adjust the *diel_models_creator* function to integrate the new class. This function is in the [diel_models_creator.py](src/diel_models/diel_models_creator.py) file.

```python
from typing import List

from cobra import Model

from diel_models.new_class import NewClass

from diel_models.pipeline import Pipeline

def diel_models_creator(model: Model, storage_pool_metabolites: List[str], photon_reaction_id: List[str],
                        nitrate_exchange_reaction: List[str], param1, biomass_reaction_id: str = None, tissues: List[str] = None) -> Model:  
  
    storage_pool_metabolites_with_day = [metabolite + "_Day" for metabolite in storage_pool_metabolites]
    photon_reaction_id_night = [photon_night_reaction + "_Night" for photon_night_reaction in photon_reaction_id]
    # ...
    
    steps = [
             # ...
            NewClass(model, param1)
        ]

    pipeline = Pipeline(model, steps)
    pipeline.run()
    return pipeline.model
```

Finally, you can run the *diel_models_creator* function with the new class.

Just as you can expand methods in the pipeline, you can modify or remove others.

## Where to find the publication results

### AraGEM:

* Details about the fluxes in the AraGEM diel model reactions in the day and night phases, as well as in the original model where calculated in [aragem_reactions_fluxes.py](validation/arabidopsis/aragem_reactions_fluxes.py) file.
* Validation of the metabolites exchange reactions through simulation using pFBA where performed in [simulation_sp.py](validation/arabidopsis/simulation_sp/simulation_sp.py) file.
* [DFA file](DFA/differential_flux_analysis.py) and respective [Test file](tests/integration_tests/test_dfa.py).
* [Plot](tests/reconstruction_results/MODEL1507180028/results_troppo/DielModel/dfa/diel_model_DFA_pathway_result.png) from the pathway enrichment method representing the amount of differentially expressed reactions between day and night in each pathway.
* [PCA](PCA/gráfico_pca_df_filtrado.png) plot with the sampling values filtered by the differentially expressed reactions.

### _Quercus suber_:

* Details about the fluxes in the _Quercus suber_ diel model reactions in the day and night phases, as well as in the original model where calculated in [quercus_reactions_fluxes.py](validation/quercus/quercus_reactions_fluxes.py) file.
* Slight adjustments to the biomass reaction in the generated diel model can be found [here](validation/quercus/comparison/auxiliar_model_change.py).
* Validation of the metabolites exchange reactions through simulation using pFBA where performed in [simulation_sp_multi_quercus.py](validation/quercus/simulation_sp/simulation_sp_multi_quercus.py) file.
* The comparison between the flux of the biomass reaction for both diel multi-tissue models are in the [quercus_diel_models_comparison.py](validation/quercus/comparison/quercus_multi_tissue_diel_models_comparison.py) file.

### QY for the several models:

* The scripts for quantum yield and assimilation quotient calculation for the _Zea mays L._ (2011), _Arabidopsis thaliana_ (2010), _Populus trichocarpa_ (2020), _Solanum lycopersicum_ (2015), _Solanum lycopersicum_ (2022) and _Solanum tuberosum_ (2018) models can be found in the [QY](validation/QY) folder.