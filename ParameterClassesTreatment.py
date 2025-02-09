from enum import Enum
import numpy as np
import scipy.stats as stat
import math as math
import InputDataTreatment as Data
import scr.MarkovClasses as MarkovCls
import scr.RandomVariantGenerators as Random
import scr.ProbDistParEst as Est


class HealthStats(Enum):
    """ health states of patients with Stroke """
    WELL = 0
    STROKE = 1
    POSTSTROKE = 2
    STROKEDEATH = 3

class Therapies(Enum):
    """ No therapy versus Anticoag therapy """
    NOTHERAPY=0
    ANTICOAG=1


class ParametersFixed():
    def __init__(self, therapy):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

        # calculate the adjusted discount rate
        self._adjDiscountRate = Data.DISCOUNT * Data.DELTA_T

        # initial health state
        self._initialHealthState = HealthStats.WELL

        # annual treatment cost
        if self._therapy == Therapies.NOTHERAPY:
            self._annualTreatmentCost = Data.NOTHERAPY_COST
        else:
            self._annualTreatmentCost = Data.ANTICOAG_COST

        # transition probability matrix of the selected therapy
        self._prob_matrix = []
        # treatment relative risk
        self._notreatmentRR = 0

        # calculate transition probabilities between hiv states
        #self._prob_matrix = calculate_prob_matrix()

        # update the transition probability matrix if combination therapy is being used
        #if self._therapy == Therapies.COMBO:
            # treatment relative risk
        #    self._treatmentRR = Data.TREATMENT_RR
            # calculate transition probability matrix for the combination therapy
        #    self._prob_matrix = calculate_prob_matrix_combo(
        #       matrix_mono=self._prob_matrix, combo_rr=Data.TREATMENT_RR)

        # annual state costs and utilities
        self._annualStateCosts = Data.ANNUAL_STATE_COST
        self._annualStateUtilities = Data.ANNUAL_STATE_UTILITY

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_adj_discount_rate(self):
        return self._adjDiscountRate

    def get_transition_prob(self, state):
        return Data.TRANS_MATRIX[state.value]

    def get_annual_state_cost(self, state):
        if state == HealthStats.STROKEDEATH:
            return 0
        else:
            return self._annualStateCosts[state.value]

    def get_annual_state_utility(self, state):
        if state == HealthStats.STROKEDEATH:
            return 0
        else:
            return self._annualStateUtilities[state.value]

    def get_annual_treatment_cost(self):
        return self._annualTreatmentCost


