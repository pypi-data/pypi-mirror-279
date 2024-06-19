from fairbalance.tests.base_test import BaseSetUp
from fairbalance.metrics import DIR, SPD, PMI, balance, balance_index, CBS
import pytest
import math


class TestDatasetMetrics(BaseSetUp):

    def test_DIR(self):
        self.setUp()

        DIRs, RMSDIR = DIR(self.dataset, self.target,
                           self.protected_attributes[0], self.privileged_groups[self.protected_attributes[0]], 1)

        print(DIRs)

        assert DIRs["B"] == pytest.approx(0.6/0.7)
        assert RMSDIR == pytest.approx(0.6/0.7)

    def test_SPD(self):
        self.setUp()

        SPDs = SPD(self.dataset, self.target,
                   self.protected_attributes[0], self.privileged_groups[self.protected_attributes[0]], 1)

        assert SPDs["B"] == pytest.approx(0.6 - 0.7)

    def test_PMI(self):
        self.setUp()

        PMIs, PMIRs, RMSPMI = PMI(
            self.dataset, self.target, self.protected_attributes[0], self.privileged_groups[self.protected_attributes[0]], 1)

        P_A = .5
        P_B = .5
        P_0 = 7/20
        P_1 = 13/20
        # test PMIs
        assert PMIs["A"][1] == pytest.approx(
            math.log((7/20)/(P_A*P_1))/math.log((7/20)))
        assert PMIs["A"][0] == pytest.approx(
            math.log((3/20)/(P_A*P_0))/math.log((3/20)))
        assert PMIs["B"][1] == pytest.approx(
            math.log((6/20)/(P_B*P_1))/math.log((6/20)))
        assert PMIs["B"][0] == pytest.approx(
            math.log((4/20)/(P_B*P_0))/math.log((4/20)))

        # test PMIRs
        assert PMIRs["B"][0] == pytest.approx(PMIs["B"][0]/PMIs["A"][0])
        assert PMIRs["B"][1] == pytest.approx(PMIs["B"][1]/PMIs["A"][1])

        # test RMSPMI
        assert RMSPMI == pytest.approx(math.sqrt(
            (PMIs["A"][1]**2 + PMIs["A"][0]**2 + PMIs["B"][1]**2 + PMIs["B"][0]**2)/4))

    def test_balance(self):
        self.setUp()
        balances = balance(self.dataset, self.target,
                           self.protected_attributes[0], self.privileged_groups[self.protected_attributes[0]], 1)

        assert balances["A"] == 10
        assert balances["B"] == 10

    def test_balance_index(self):
        self.setUp()
        balance_index_val = balance_index(
            self.dataset, self.target, self.protected_attributes[0], self.privileged_groups[self.protected_attributes[0]], 1)

        assert balance_index_val == pytest.approx(1)

    def test_CBS(self):
        self.setUp()
        CBS_val = CBS(self.dataset, self.target,
                      self.protected_attributes[0], self.privileged_groups[self.protected_attributes[0]], 1)
        balance_index_val = balance_index(
            self.dataset, self.target, self.protected_attributes[0], self.privileged_groups[self.protected_attributes[0]], 1)
        _, _, RMSPMI = PMI(self.dataset, self.target,
                           self.protected_attributes[0], self.privileged_groups[self.protected_attributes[0]], 1)
        _, RMSDIR = DIR(self.dataset, self.target,
                        self.protected_attributes[0], self.privileged_groups[self.protected_attributes[0]], 1)

        assert CBS_val == pytest.approx(
            1 - math.sqrt(((balance_index_val - 1)**2 + (RMSDIR - 1)**2 + RMSPMI**2)/3))
