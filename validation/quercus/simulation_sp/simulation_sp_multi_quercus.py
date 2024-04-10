import os

import cobra.io
import pandas as pd
from cobra.flux_analysis import pfba, flux_variability_analysis as fva

from src.diel_models.nitrate_uptake_ratio import NitrateUptakeRatioCalibrator


def load_model():
    model_path = 'C:\\Users\\lucia\\Desktop\\DielModels\\validation\\quercus\\(changed)diel_multi_quercus_model.xml'
    model = cobra.io.read_sbml_model(model_path)
    model.reactions.get_by_id("Total_biomass").bounds = (0.11, 0.11)
    model.reactions.EX_C00205__dra_Day.bounds = (-1000, 1000)
    model.objective = "EX_C00205__dra_Day"
    model.objective_direction = "max"
    nitrate_calibrator = NitrateUptakeRatioCalibrator(model, ["EX_C00244__dra_Day"], ["EX_C00244__dra_Night"])
    nitrate_calibrator.run()
    model = nitrate_calibrator.model
    model.reactions.get_by_id("EX_C00014__dra_Day").bounds = (0, 100000)
    model.reactions.get_by_id("EX_C00014__dra_Night").bounds = (0, 100000)
    return model


def simulate(model):
    solution = pfba(model).fluxes
    fva_solution = fva(model, [storage for storage in model.reactions if "Day_sp" in storage.id],
                       fraction_of_optimum=1.0, processes=os.cpu_count())
    # assert solution['Total_biomass'] == 0.000001
    assert round(solution['EX_C00244__dra_Day'] * 2, 4) == round(solution['EX_C00244__dra_Night'] * 3, 4)
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
    produced_at_day.to_excel(r'produced_at_day_multi_quercus.xlsx')
    produced_at_night.to_excel(r'produced_at_night_multi_quercus.xlsx')
    print(produced_at_day)
    print(produced_at_night)


if __name__ == '__main__':
    model = load_model()
    pfba, fva = simulate(model)
    analyze_solution(pfba, fva)
