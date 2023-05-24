from typing import List
import cobra
from cobra import Model, Metabolite, Reaction
from diel_models.pipeline import Step


class StoragePoolGenerator(Step):

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
        self.metabolite_sp_ids: List[str] = []
        self.metabolite_names: List[str] = []

    def create_storage_pool_metabolites(self) -> None:
        """
        According to the given metabolite IDs,
        this function creates new metabolites for a new compartment: storage pool

        Raises:
            ValueError: If a metabolite ID is not present in the given model.
        """
        metabolite_objs: List[Metabolite] = []
        names: List[str] = []

        for identification in self.metabolites:
            if identification in self.model.metabolites:
                metabolite_sp_id: str = identification.replace(
                    self.model.metabolites.get_by_id(identification).compartment, "sp")
                names.append(self.model.metabolites.get_by_id(identification).name)
                self.metabolite_sp_ids.append(metabolite_sp_id)
            else:
                raise ValueError("Metabolite id not present in the model that was given.")
        for metabolite_sp_id in self.metabolite_sp_ids:
            metabolite = Metabolite(metabolite_sp_id)
            metabolite.compartment = "sp"
            metabolite_objs.append(metabolite)
        for idx, met in enumerate(metabolite_objs):
            met.name = names[idx]
            if "Day" in met.name:
                met.name = met.name.replace("Day", "")
            elif "Night" in met.name:
                met.name = met.name.replace("Night", "")
            self.metabolite_names.append(met.name)
        self.model.add_metabolites(metabolite_objs)
        self.model._compartments["sp"] = "Storage Pool"

    def create_exchange_reaction(self, metabolite_id: str, metabolite_sp_id: str, direction: str) -> Reaction:
        """
        It creates a Reaction object representing an exchange reaction
        for the specified metabolite in the specified direction.

        Parameters
        ----------
        metabolite_id
        metabolite_sp_id
        direction

        Returns
        -------
        Reaction object
        """

        met = self.model.metabolites.get_by_id(metabolite_sp_id)
        exchange_reaction = Reaction(f"{met.name}_{direction}_sp_exchange".replace(" ", ""))
        if direction == "Day" and "Day" in metabolite_id:
            exchange_reaction.add_metabolites({
                self.model.metabolites.get_by_id(metabolite_id): -1.0,
                self.model.metabolites.get_by_id(metabolite_sp_id): 1.0
            })
        if direction == "Night" and "Night" in metabolite_id:
            exchange_reaction.add_metabolites({
                self.model.metabolites.get_by_id(metabolite_sp_id): -1.0,
                self.model.metabolites.get_by_id(metabolite_id): 1.0
            })
        exchange_reaction.lower_bound = -1000.0
        exchange_reaction.upper_bound = 1000.0
        exchange_reaction.name = f"{met.name} {direction} storage pool exchange"
        return exchange_reaction

    def create_storage_pool_first_reactions(self) -> None:
        """
        According to the given metabolite IDs,
        this function creates the corresponding exchange reaction
        of the metabolite to the storage pool.
        """
        exchange_reactions: List[Reaction] = []

        for metabolite_id, metabolite_sp_id in zip(self.metabolites, self.metabolite_sp_ids):
            if "Day" in metabolite_id:
                exchange_reactions.append(self.create_exchange_reaction(metabolite_id, metabolite_sp_id, "Day"))
            if "Night" in metabolite_id:
                exchange_reactions.append(self.create_exchange_reaction(metabolite_id, metabolite_sp_id, "Night"))

        self.model.add_reactions(exchange_reactions)

    # def create_storage_pool_second_reactions(self) -> None:
    #     """
    #     According to the given metabolite IDs,
    #     this function creates the complementary reactions,
    #     i.e. if it previously created the Day <-> Storage Pool reaction,
    #     it now creates the Storage Pool <-> Night reaction and vice versa.
    #     """
    #     other_side_exchange_reactions: List[Reaction] = []
    #
    #     for metabolite_id, metabolite_sp_id in zip(self.metabolites, self.metabolite_sp_ids):
    #         if "Day" in metabolite_id:
    #             other_side_exchange_reactions.append(
    #                 self.create_exchange_reaction(metabolite_id, metabolite_sp_id, "Night"))
    #         if "Night" in metabolite_id:
    #             other_side_exchange_reactions.append(
    #                 self.create_exchange_reaction(metabolite_id, metabolite_sp_id, "Day"))
    #
    #     self.model.add_reactions(other_side_exchange_reactions)

    def run(self) -> Model:
        """
        Executes the methods of the class StoragePoolGenerator

        Returns
        Model
        """

        test = StoragePoolGenerator(self.model, self.metabolites)
        test.create_storage_pool_metabolites()
        test.create_storage_pool_first_reactions()
        # test.create_storage_pool_second_reactions()

        return self.model

    def validate(self) -> None:
        """
        Validates the model, since it has to have metabolites, reactions and a Day and Night compartments
        """

        for reaction in self.model.reactions:
            assert "_Day" in reaction.id or "_Night" in reaction.id, "The model does not have Day and Night reactions."
        for metabolite in self.model.metabolites:
            assert "_Day" in metabolite.id or "_Night" in metabolite.id, "The model does not have Day and Night " \
                                                                         "metabolites."
        for compartment in self.model.compartments:
            assert "_Day" in compartment or "_Night" in compartment, "The model does not have Day and Night " \
                                                                     "compartments."
