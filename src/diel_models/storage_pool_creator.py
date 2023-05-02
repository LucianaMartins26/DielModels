from typing import List
import cobra
from cobra import Model, Metabolite, Reaction


class StoragePoolCreator:

    def __init__(self, model: Model, metabolites: List[str]):
        """
        Constructor

        Parameters
        ----------
        model: cobra.Model
        metabolites: List[str]
        """
        self.model: Model = model
        self.metabolites: List[str] = metabolites
        self.new_ids: List[str] = []
        self.met_names: List[str] = []

    def sp_metabolites(self) -> None:
        """
        According to the given metabolite IDs,
        this function creates new metabolites for a new compartment: storage pool

        Raises:
            ValueError: If a metabolite ID is not present in the given model.
        """
        metabolite_objs: List[Metabolite] = []
        names: List[str] = []

        for id in self.metabolites:
            if id in self.model.metabolites:
                new_id: str = id.replace(self.model.metabolites.get_by_id(id).compartment, "sp")
                names.append(self.model.metabolites.get_by_id(id).name)
                self.new_ids.append(new_id)
            else:
                raise ValueError("Metabolite id not present in the model that was given.")
        for new_id in self.new_ids:
            metabolite = Metabolite(new_id)
            metabolite.compartment = "sp"
            metabolite_objs.append(metabolite)
        for idx, met in enumerate(metabolite_objs):
            met.name = names[idx]
            if "Day" in met.name:
                met.name = met.name.replace("Day", "")
            elif "Night" in met.name:
                met.name = met.name.replace("Night", "")
            self.met_names.append(met.name)
        self.model.add_metabolites(metabolite_objs)
        self.model._compartments["sp"] = "Storage Pool"

    def sp_first_reactions(self) -> None:
        """
        According to the given metabolite IDs,
        this function creates the corresponding exchange reaction
        of the metabolite to the storage pool.
        """
        exchanges_r: List[Reaction] = []

        for met_id, new_id in zip(self.metabolites, self.new_ids):
            if "Day" in met_id:
                met = self.model.metabolites.get_by_id(met_id)
                exchange_r = Reaction(f"{met_id}_exchange")
                exchange_r.add_metabolites({
                    self.model.metabolites.get_by_id(met_id): -1.0,
                    self.model.metabolites.get_by_id(new_id): 1.0
                })
                exchange_r.lower_bound = -1000.0
                exchange_r.upper_bound = 1000.0
                exchange_r.name = f"{met.name} exchange"
                exchanges_r.append(exchange_r)
            if "Night" in met_id:
                met = self.model.metabolites.get_by_id(met_id)
                exchange_r = Reaction(f"{met_id}_exchange")
                exchange_r.add_metabolites({
                    self.model.metabolites.get_by_id(new_id): -1.0,
                    self.model.metabolites.get_by_id(met_id): 1.0
                })
                exchange_r.lower_bound = -1000.0
                exchange_r.upper_bound = 1000.0
                exchange_r.name = f"{met.name} exchange"
                exchanges_r.append(exchange_r)
        self.model.add_reactions(exchanges_r)

    def sp_second_reactions(self) -> None:
        """
        According to the given metabolite IDs,
        this function creates the complementary reactions,
        i.e. if it previously created the Day <-> Storage Pool reaction,
        it now creates the Storage Pool <-> Night reaction and vice versa.
        """
        other_side_exchanges_r: List[Reaction] = []

        for met_id, new_id in zip(self.metabolites, self.new_ids):
            if "Day" in met_id:
                met = self.model.metabolites.get_by_id(met_id)
                other_side_exchange_r = Reaction(f"{met_id.replace('Day', 'Night')}_exchange")
                other_side_exchange_r.add_metabolites({
                    self.model.metabolites.get_by_id(new_id): -1.0,
                    self.model.metabolites.get_by_id(met_id.replace('Day', 'Night')): 1.0
                })
                other_side_exchange_r.lower_bound = -1000.0
                other_side_exchange_r.upper_bound = 1000.0
                other_side_exchange_r.name = f"{met.name.replace('Day', 'Night')} exchange"
                other_side_exchanges_r.append(other_side_exchange_r)
            if "Night" in met_id:
                met = self.model.metabolites.get_by_id(met_id)
                other_side_exchange_r = Reaction(f"{met_id.replace('Night', 'Day')}_exchange")
                other_side_exchange_r.add_metabolites({
                    self.model.metabolites.get_by_id(met_id.replace('Night', 'Day')): -1.0,
                    self.model.metabolites.get_by_id(new_id): 1.0
                })
                other_side_exchange_r.lower_bound = -1000.0
                other_side_exchange_r.upper_bound = 1000.0
                other_side_exchange_r.name = f"{met.name.replace('Night', 'Day')} exchange"
                other_side_exchanges_r.append(other_side_exchange_r)
        self.model.add_reactions(other_side_exchanges_r)
