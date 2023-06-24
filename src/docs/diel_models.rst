diel\_models package
====================

To install this package throught *pip* please insert:

.. code-block:: python
    pip install DielModels==1.0.2
Submodules
----------
Several methods are present in this package, which can be used separately *(day_night_creator, storage_pool_generator, photon_reaction_inhibitor, nitrate_uptake_ratio, biomass_adjuster)* or alternatively be applied consecutively through the *diel_models_creator* function that runs the entire pipeline through the *Pipeline* class.
Here is an example:

.. code-block:: python
    import cobra
    import diel_models
    from diel_models.diel_models_creator import diel_models_creator

    model = cobra.io.read_sbml_model('../../desired_model.xml')

    storage_pool_metabolites = ['Metabolite_ID_1', 'Metabolite_ID_2', 'Metabolite_ID_3']

    diel_models_creator(model, storage_pool_metabolites, 'Photon_Reaction_ID', 'Biomass_Reaction_ID', 'Nitrate_Reaction_ID')
diel\_models.biomass\_adjuster module
-------------------------------------

.. automodule:: diel_models.biomass_adjuster
   :members:
   :undoc-members:
   :show-inheritance:

diel\_models.day\_night\_creator module
---------------------------------------

.. automodule:: diel_models.day_night_creator
   :members:
   :undoc-members:
   :show-inheritance:

diel\_models.diel\_models\_creator module
-----------------------------------------

.. automodule:: diel_models.diel_models_creator
   :members:
   :undoc-members:
   :show-inheritance:

diel\_models.nitrate\_uptake\_ratio module
------------------------------------------

.. automodule:: diel_models.nitrate_uptake_ratio
   :members:
   :undoc-members:
   :show-inheritance:

diel\_models.photon\_reaction\_inhibitor module
-----------------------------------------------

.. automodule:: diel_models.photon_reaction_inhibitor
   :members:
   :undoc-members:
   :show-inheritance:

diel\_models.pipeline module
----------------------------

.. automodule:: diel_models.pipeline
   :members:
   :undoc-members:
   :show-inheritance:

diel\_models.storage\_pool\_generator module
--------------------------------------------

.. automodule:: diel_models.storage_pool_generator
   :members:
   :undoc-members:
   :show-inheritance:

Module contents
---------------

.. automodule:: diel_models
   :members:
   :undoc-members:
   :show-inheritance:
