from typing import List

from cobra import Model

from diel_models.day_night_creator import DayNightCreator
from diel_models.storage_pool_generator import StoragePoolGenerator
from diel_models.photon_reaction_inhibitor import PhotonReactionInhibitor
from diel_models.biomass_adjuster import BiomassAdjuster
from diel_models.nitrate_uptake_ratio import NitrateUptakeRatioCalibrator
from diel_models.pipeline import Pipeline


def diel_models_creator(model: Model, storage_pool_metabolites: List[str], photon_reaction_id: List[str],
                        nitrate_exchange_reaction: List[str], biomass_reaction_id: str = None, tissues: List[str] = None,
                        day_ratio_value: int = 3, night_ratio_value: int = 2) -> Model:
    """
    Function that allows you to run the pipeline in one go,
    returning the resulting model, where the arguments are all relative to the original model.

    Parameters
    ----------
    model: cobra.Model
        Metabolic model
    storage_pool_metabolites: List[str]
        list with all the metabolites for storage pool
    photon_reaction_id: List[str]
        id or ids for photon reaction(s) - in case of multi tissues models for example.
    nitrate_exchange_reaction: List[str]
        id for nitrate exchange reaction(s) - in case of multi tissues models for example.
    biomass_reaction_id: str, optional
        id for biomass_reaction, defaults to None in case no biomass reaction defined.
    tissues: List[str], optional
            List of tissues in the multi-tissue model, defaults to None for generic models.
    day_ratio_value: int, optional
        The ratio of nitrate uptake during the day, default is 3.
    night_ratio_value: int, optional
        The ratio of nitrate uptake during the night, default is 2.

    Returns
    -------
    cobra.Model
    """
    storage_pool_metabolites_with_day = [metabolite + "_Day" for metabolite in storage_pool_metabolites]
    photon_reaction_id_night = [photon_night_reaction + "_Night" for photon_night_reaction in photon_reaction_id]
    nitrate_exchange_reaction_night = [nitrate_reaction + "_Night" for nitrate_reaction in nitrate_exchange_reaction]
    nitrate_exchange_reaction_day = [nitrate_reaction + "_Day" for nitrate_reaction in nitrate_exchange_reaction]

    if biomass_reaction_id is not None:
        biomass_day_id = biomass_reaction_id + "_Day"
        biomass_night_id = biomass_reaction_id + "_Night"

        steps = [
            DayNightCreator(model),
            StoragePoolGenerator(model, storage_pool_metabolites_with_day, tissues),
            PhotonReactionInhibitor(model, photon_reaction_id_night),
            BiomassAdjuster(model, biomass_day_id, biomass_night_id),
            NitrateUptakeRatioCalibrator(model, nitrate_exchange_reaction_day, nitrate_exchange_reaction_night,
                                         day_ratio_value=day_ratio_value, night_ratio_value=night_ratio_value)
        ]

    else:
        steps = [
            DayNightCreator(model),
            StoragePoolGenerator(model, storage_pool_metabolites_with_day, tissues),
            PhotonReactionInhibitor(model, photon_reaction_id_night),
            NitrateUptakeRatioCalibrator(model, nitrate_exchange_reaction_day, nitrate_exchange_reaction_night,
                                         day_ratio_value=day_ratio_value, night_ratio_value=night_ratio_value)
        ]

    pipeline = Pipeline(model, steps)
    pipeline.run()
    return pipeline.model
