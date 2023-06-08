from diel_models.day_night_creator import DayNightCreator
from diel_models.storage_pool_generator import StoragePoolGenerator
from diel_models.photon_reaction_inhibitor import PhotonReactionInhibitor
from diel_models.biomass_adjuster import BiomassAdjuster
from diel_models.nitrate_uptake_ratio import NitrateUptakeRatioCalibrator
from diel_models.pipeline import Pipeline


def diel_models_creator(model, storage_pool_metabolites, photon_reaction_id, biomass_reaction_id,
                        nitrate_exchange_reaction):
    """
    Function that allows you to run the pipeline in one go,
    returning the resulting model, where the arguments are all relative to the original model.

    Parameters
    ----------
    model: cobra.Model
        Metabolic model
    storage_pool_metabolites: List[str]
        list with all the metabolites for sp
    photon_reaction_id: str
        id for photon reaction
    biomass_reaction_id: str
        id for biomass_reaction
    nitrate_exchange_reaction: str
        id for nitrate exchange reaction

    Returns
    -------
    Metabolic model after pipeline
    """
    storage_pool_metabolites_with_day = [metabolite + "_Day" for metabolite in storage_pool_metabolites]
    photon_reaction_id_night = photon_reaction_id + "_Night"
    biomass_day_id = biomass_reaction_id + "_Day"
    biomass_night_id = biomass_reaction_id + "_Night"
    nitrate_exchange_reaction_night = nitrate_exchange_reaction + "_Night"
    nitrate_exchange_reaction_day = nitrate_exchange_reaction + "_Day"

    steps = [
        DayNightCreator(model),
        StoragePoolGenerator(model, storage_pool_metabolites_with_day),
        PhotonReactionInhibitor(model, photon_reaction_id_night),
        BiomassAdjuster(model, biomass_day_id, biomass_night_id),
        NitrateUptakeRatioCalibrator(model, nitrate_exchange_reaction_day, nitrate_exchange_reaction_night)
    ]

    pipeline = Pipeline(model, steps)
    pipeline.run()
    return pipeline.model
