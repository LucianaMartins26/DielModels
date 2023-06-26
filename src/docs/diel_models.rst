diel_models package
===================

Para instalar este pacote através do pip, insira o seguinte comando:

.. code-block:: python

    pip install DielModels==1.0.2

Submódulos
----------

Este pacote contém vários submódulos, que podem ser usados separadamente *(day_night_creator, storage_pool_generator, photon_reaction_inhibitor, nitrate_uptake_ratio, biomass_adjuster)* ou aplicados consecutivamente por meio da função *diel_models_creator*, que executa todo o pipeline usando a classe *Pipeline*. Aqui está um exemplo:

.. code-block:: python

    import cobra
    import diel_models
    from diel_models.diel_models_creator import diel_models_creator

    model = cobra.io.read_sbml_model('../../desired_model.xml')

    storage_pool_metabolites = ['Metabolite_ID_1', 'Metabolite_ID_2', 'Metabolite_ID_3']

    diel_models_creator(model, storage_pool_metabolites, 'Photon_Reaction_ID',
                        'Biomass_Reaction_ID', 'Nitrate_Reaction_ID')

diel_models.day_night_creator module
-----------------------------------

.. automodule:: diel_models.day_night_creator
   :members:
   :undoc-members:
   :show-inheritance:

diel_models.storage_pool_generator module
------------------------------------

.. automodule:: diel_models.storage_pool_generator
   :members:
   :undoc-members:
   :show-inheritance:

diel_models.photon_reaction_inhibitor module
--------------------------------------

.. automodule:: diel_models.photon_reaction_inhibitor
   :members:
   :undoc-members:
   :show-inheritance:

diel_models.nitrate_uptake_ratio module
--------------------------------------

.. automodule:: diel_models.nitrate_uptake_ratio
   :members:
   :undoc-members:
   :show-inheritance:

diel_models.biomass_adjuster module
--------------------------------------------

.. automodule:: diel_models.biomass_adjuster
   :members:
   :undoc-members:
   :show-inheritance:

diel_models.pipeline module
---------------------------

.. automodule:: diel_models.pipeline
   :members:
   :undoc-members:
   :show-inheritance:

diel_models.diel_models_creator module
-----------------------------------------

.. automodule:: diel_models.diel_models_creator
   :members:
   :undoc-members:
   :show-inheritance: