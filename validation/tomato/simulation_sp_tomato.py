import os

import cobra.io
import pandas as pd
from cobra.flux_analysis import pfba, flux_variability_analysis as fva
from tests import TEST_DIR

from src.diel_models.nitrate_uptake_ratio import NitrateUptakeRatioCalibrator


def load_model():
    model_path = os.path.join(TEST_DIR, 'data', 'diel_tomato_model.xml')
    model = cobra.io.read_sbml_model(model_path)
    model.reactions.get_by_id("Biomass_Total").upper_bound = 100
    model.reactions.get_by_id("Biomass_Total").lower_bound = 100
    model.objective = "Biomass_Total"
    model.objective_direction = "min"
    nitrate_calibrator = NitrateUptakeRatioCalibrator(model, ["EX_x_NO3_Day"], ["EX_x_NO3_Night"])
    nitrate_calibrator.run()
    model = nitrate_calibrator.model
    model.reactions.get_by_id("EX_x_NH4_Day").bounds = (0, 100000)
    model.reactions.get_by_id("EX_x_NH4_Night").bounds = (0, 100000)
    return model


def simulate(model):
    solution = pfba(model).fluxes
    fva_solution = fva(model, [storage for storage in model.reactions if "Day_sp" in storage.id],
                       fraction_of_optimum=1.0, processes=os.cpu_count())
    assert solution['Biomass_Total'] == 100
    assert round(solution['EX_x_NO3_Day'] * 2, 4) == round(solution['EX_x_NO3_Night'] * 3, 4)
    return solution, fva_solution


def analyze_solution(pfba_solution, fva_solution):
    produced_at_day = pfba_solution.loc[(pfba_solution.index.str.contains('Day_sp')) & (round(pfba_solution, 5) > 0)]
    produced_at_night = pfba_solution.loc[(pfba_solution.index.str.contains('Day_sp')) & (round(pfba_solution, 5) < 0)]
    produced_at_day = pd.concat([produced_at_day, fva_solution.loc[produced_at_day.index, ['minimum', 'maximum']]],
                                axis=1)
    produced_at_night = pd.concat(
        [produced_at_night, fva_solution.loc[produced_at_night.index, ['minimum', 'maximum']]], axis=1)
    ### add column called robust, that is true if both minimum and maximum have the same sign
    produced_at_day['robust'] = produced_at_day.apply(lambda x: True if x['minimum'] * x['maximum'] > 0 else False,
                                                      axis=1)
    ### same for night
    produced_at_night['robust'] = produced_at_night.apply(lambda x: True if x['minimum'] * x['maximum'] > 0 else False,
                                                          axis=1)
    produced_at_day.to_excel(r'produced_at_day_tomato.xlsx')
    produced_at_night.to_excel(r'produced_at_night_tomato.xlsx')
    print(produced_at_day)
    print(produced_at_night)


if __name__ == '__main__':
    model = load_model()
    pfba, fva = simulate(model)
    analyze_solution(pfba, fva)
