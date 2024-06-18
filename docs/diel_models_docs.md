# Install and Run DielModels

### Description

Despite numerous successful studies, modeling plant metabolism remains challenging for several reasons, such as limited information, incomplete annotations, and dynamic changes in plant metabolism that occur under different conditions, including night and day.
In particular, the integration of these day-night cycles (diel cycles) is complex, laborious, and time-consuming.

With this in mind, this package aims to accelerate this process by being able to transform a non-diel model into a diel model.

### Installation

``` pip install DielModels==1.1.0 ```

### Getting Started
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

This is possible due to the created *Pipeline* class that derives from a *Step* class with abstract methods - both present in this package, in the pipeline.py file.

### Expanding the pipeline

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

Then you need to adjust the *diel_models_creator* function to integrate the new class. This function is in the diel_models_creator.py file.

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