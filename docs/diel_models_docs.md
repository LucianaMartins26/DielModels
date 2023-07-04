# Install and Run Diel Models

Para instalar este pacote através do pip, insira o seguinte comando:

```python
pip install DielModels==1.0.2
```

Este pacote contém vários submódulos, que podem ser usados separadamente *(day_night_creator, storage_pool_generator, photon_reaction_inhibitor, nitrate_uptake_ratio, biomass_adjuster)* ou aplicados consecutivamente por meio da função *diel_models_creator*, que executa todo o pipeline usando a classe *Pipeline*. Aqui está um exemplo:

```python
import cobra
import diel_models
from diel_models.diel_models_creator import diel_models_creator

model = cobra.io.read_sbml_model('../../desired_model.xml')

storage_pool_metabolites = ['Metabolite_ID_1', 'Metabolite_ID_2', 'Metabolite_ID_3']

diel_models_creator(model, storage_pool_metabolites, 'Photon_Reaction_ID',
                    'Biomass_Reaction_ID', 'Nitrate_Reaction_ID')
```