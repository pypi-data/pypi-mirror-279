#!/usr/bin/env python

"""Tests for `carbatpy` package."""

import os
import unittest
import numpy as np
import pandas as pd

import carbatpy as cbp


class TestCarbatpy(unittest.TestCase):
    """Tests for `carbatpy` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_pareto_opt_screened(self):
        """Test the pareto function within utils.optimize."""

        directory = cbp._CARBATPY_BASE_DIR
        filename = directory + r"\\tests\\test_files\\"
        filename += r"test_data_ProEthPenBut\2024-02-05-08-37-ProEthPenBut.csv"
        objectives = objectives_act = ['p_ratio', 'T_glide_h', 'COP_is']
        sense = ["min", "min", "max"]
        obj_sense = [objectives_act, sense]
        optimal_values = cbp.utils.optimize.pareto(filename, obj_sense)
        self.assertTrue(len(optimal_values) > 0)

    def test_001_simple_orc(self):
        """Test the simple orc calculation with two storages and 
        heat transfer to the environment."""
        FLUID = "Propane * Butane * Pentane * Hexane"
        comp = [.75, 0.05, 0.15, 0.05]
        comp = [0.4,	0.3,	0.3, 0.0]  # [0.164,.3330,.50300,0.0]

        FLS = "Water"  # Storage fluid
        FLCOLD = "Methanol"  # Storage fluid for low T
        FLENV = "Water"  #

        flm = cbp.fprop.FluidModel(FLUID)
        myFluid = cbp.fprop.Fluid(flm, comp)

        secFlm = cbp.fprop.FluidModel(FLS)
        secFluid = cbp.fprop.Fluid(secFlm, [1.])

        coldFlm = cbp.fprop.FluidModel(FLCOLD)
        coldFluid = cbp.fprop.Fluid(coldFlm, [1.])

        envFlm = cbp.fprop.FluidModel(FLENV)
        envFluid = cbp.fprop.Fluid(secFlm, [1.])

        # Condenser(c) and storage (s), secondary fluids fix all, temperatures(T in K),
        # pressures (p in Pa)
        _ETA_S_ = 0.67  # interesting when changed from 0.69 to 0.65, the efficiency
        # decreases, the reason is the low quality along throtteling then
        _ETA_S_P_ = 0.6  # pump
        _STORAGE_T_OUT_ = cbp._T_SURROUNDING
        _COLD_STORAGE_T_OUT_ = cbp._T_SURROUNDING
        _ENV_T_IN_ = cbp._T_SURROUNDING
        _ENV_T_OUT_ = cbp._T_SURROUNDING + 5.
        _STORAGE_T_IN_ = 363.  # 395.0
        _COLD_STORAGE_T_IN_ = 260.15
        _STORAGE_P_IN_ = 5e5
        _COLD_STORAGE_P_IN_ = 5e5
        _ENV_P_IN_ = 5e5
        _Q_DOT_MIN_ = 1e3  # and heat_flow rate (W)
        _D_T_SUPER_ = 5  # super heating of working fluid
        _D_T_MIN_ = 4.  # minimum approach temperature (pinch point)
        _COP_CHARGING = 3.14  # needed to calculate Q_env_discharging
        _T_REDUCTION_EVAP = -27  # if the curves cross in the evaporator this parameter may help

        # environment for heat transfer
        state_env_out = envFluid.set_state([_ENV_T_OUT_, _ENV_P_IN_], "TP")
        state_env_in = envFluid.set_state([_ENV_T_IN_, _ENV_P_IN_], "TP")

        # high T-storages
        state_sec_out = secFluid.set_state(
            [_STORAGE_T_OUT_, _STORAGE_P_IN_], "TP")
        state_sec_in = secFluid.set_state(
            [_STORAGE_T_IN_, _STORAGE_P_IN_], "TP")

        #  low T sorages:
        state_cold_out = coldFluid.set_state(
            [_COLD_STORAGE_T_OUT_, _COLD_STORAGE_P_IN_], "TP")
        state_cold_in = coldFluid.set_state(
            [_COLD_STORAGE_T_IN_, _COLD_STORAGE_P_IN_], "TP")

        # working fluid

        state_satv_evap = myFluid.set_state(
            [_STORAGE_T_IN_-_D_T_MIN_-_D_T_SUPER_+_T_REDUCTION_EVAP, 1.], "TQ")  # find high pressure
        p_high = state_satv_evap[1]

        T_OUT = _STORAGE_T_IN_ - _D_T_MIN_
        # Evaporator input comes from the pump-output

        state_out_evap = myFluid.set_state([p_high,
                                            T_OUT], "PT")
        # low pressure, condenser # BA 2023-11-14 three points needed: low, environment and slightly higher
        T_SATL = _COLD_STORAGE_T_IN_ + _D_T_MIN_
        state_out_cond = myFluid.set_state(
            [T_SATL, 0.], "TQ")  # find low pressure
        p_low = state_out_cond[1]
        # BA changed 2023-12-13 the fixed starting point for the cycle is the  fluid
        # state before the pump now.

        # the other states in the condenser are fixed by the expander outlet and
        # the Q_total : Q_low_stored ratio    eventually p_low must be varied until
        # the balance is fulfilled, since m_dot_w is fixed by the evaporator!

        FIXED_POINTS = {"eta_s": _ETA_S_,  # expander
                        "eta_s_p": _ETA_S_P_,  # pump
                        "p_low": p_low,
                        "p_high": p_high,
                        "T_hh": _STORAGE_T_IN_,
                        "h_h_out_sec": state_sec_out[2],
                        "h_h_out_w": state_out_evap[2],
                        "h_l_out_cold": state_cold_out[2],
                        "h_l_out_w": state_out_cond[2],
                        "h_env_in": state_env_in[2],
                        "h_env_out": state_env_out[2],
                        "T_hl": _STORAGE_T_OUT_,
                        "T_lh": _COLD_STORAGE_T_OUT_,
                        "T_ll": _COLD_STORAGE_T_IN_,  # 256.0,
                        "Q_dot_h": _Q_DOT_MIN_,
                        "d_temp_min": _D_T_MIN_,
                        "cop_charging": _COP_CHARGING  # needed to calculate Q_env_discharging
                        }

        orc0 = cbp.orc_simple.OrganicRankineCycle(
            [myFluid, secFluid, envFluid, coldFluid], FIXED_POINTS)
        eta_dis = orc0.calc_orc(False)
        self.assertAlmostEqual(0.053007094612255716, eta_dis, places=14)

    def test_002_combine_fluid_screening_data_frames(self):
        """Test the combination of two dataframes function within
        utils.optimize."""

        directory = cbp._CARBATPY_BASE_DIR
        directory += "\\tests\\test_files\\"

        filename1 = directory + r"test_data_ProEthPenBut\2024-02-06-16-51-ProEthPenBut.csv"
        filename2 = directory + \
            r"test_data_ProEthPenBut\2024-02-06-16-51-ProEthPenBut-compressor-Roskosch.csv"
        combined_data = cbp.utils.property_eval_mixture.combine([filename1,
                                                                filename2],
                                                                filename_out="automatic")

        self.assertTrue(len(combined_data) > 0)

    def test_003_plot_data_frame(self):
        """Tplot the columns of a dataframe within
        utils.optimize."""

        directory = cbp._CARBATPY_BASE_DIR
        directory += "\\tests\\test_files\\"

        filename = directory + r"test_data_ProEthPenBut\2024-02-06-16-51-ProEthPenBut.csv"
        what = {"x": 'spec_Volume_sup', "y": 'COP_is80', "hue": 'T_glide_h',
                "size": 'p_ratio', 'style': 'Temperature_hplt'}
        success = cbp.utils.property_eval_mixture.data_plot(filename, what,
                                                            filename_out="automatic")

        self.assertTrue(success)

    def test_004_evaluate_data_(self):
        """Evaluate the data in the dataFrame, when the isentropic efficiencies
        are calculated. Typically using '-combined'-files"""

        directory = cbp._CARBATPY_BASE_DIR
        directory += "\\tests\\test_files\\"
        filename = directory + r"test_data_ProEthPenBut\2024-02-06-16-51-ProEthPenBut-combined.csv"
        data = pd.read_csv(filename)
        initial =len(data.columns)

        data_combined = cbp.utils.property_eval_mixture.eval_is_eff_roskosch(data,
                                                                        file_out=directory+"fluid-re-eval.csv")
        self.assertTrue(len(data_combined.columns) > initial)
        
    def test_005_curve_dist_find(self):
        """Evaluate the data in the dataFrame, when the isentropic efficiencies
        are calculated. Typically using '-combined'-files"""

        x_val = np.linspace(1, 12)
        # test points
        y_val = -5*np.sin(x_val) + 5 * x_val + 4 - 100/x_val
        values_act = np.array([x_val, y_val])
        solution_below = cbp.curve_min_distance_finder.find_min_approach(values_act, True)
        solution_above = cbp.curve_min_distance_finder.find_min_approach(values_act, False)
        self.assertTrue(solution_below["success"])
        self.assertTrue(solution_above["success"])
        self.assertAlmostEqual(solution_below["integral"],
                               356.82447354719505, places=14)


if __name__ == "__main__":
    unittest.main()
