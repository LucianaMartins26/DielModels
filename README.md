# DielModels

### Description
In this context, *DielModels* is a python package generated from this project [HERE](https://github.com/LucianaMartins26/DielModels.git).

Despite numerous successful studies, modeling plant metabolism remains challenging for several reasons, such as limited information, incomplete annotations, and dynamic changes in plant metabolism that occur under different conditions, including night and day.
In particular, the integration of these day-night cycles (diel cycles) is complex, laborious, and time-consuming.

With this in mind, this package aims to accelerate this process by being able to transform a non-diel model into a diel model.

### Table of contents:

- [Installation](#installation)
    - [Pip](#pip)
- [Getting Started](#getting-started)
- [Documentation](#documentation)

## Installation
### Pip

``` pip install DielModels==1.0.2 ```

## Getting Started
Through this package, you can:

* Assign day and night to the non-diel model;
* Insert specified metabolites into the storage pool allowing their transition between day and night, and vice versa; 
* Block the photon reaction flow at night; 
* Set the flux of the nitrate reactions to 3:2 according to the literature; 
* Takes the day and night biomass reactions and creates a total biomass reaction resulting from the junctions of both. It also blocks the flow of the individual reactions to zero. Sets the total biomass reaction as the objective function.

If each method is to be applied individually it is essential that the first 3 steps are applied in that order specifically.

**Alternatively, it is possible to apply all methods to a given model, running the entire pipeline using:**

```python
import cobra
import diel_models
from diel_models.diel_models_creator import diel_models_creator

model = cobra.io.read_sbml_model('../../desired_model.xml')

storage_pool_metabolites = ['Metabolite_ID_1', 'Metabolite_ID_2', 'Metabolite_ID_3']

diel_models_creator(model, storage_pool_metabolites, 'Photon_Reaction_ID', 'Biomass_Reaction_ID', 'Nitrate_Reaction_ID')
```

It is possible due to the created *Pipeline* class that derives from a *Step* class with abstract methods - both present in the package.

## Documentation

For extra documentation, you can check this [ReadTheDocs](http://dielmodels.readthedocs.io/).
