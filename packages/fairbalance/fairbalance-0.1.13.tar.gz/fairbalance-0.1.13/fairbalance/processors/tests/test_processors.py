from fairbalance.processors import RandomOverSamplerProcessor, RandomUnderSamplerProcessor, SMOTENCProcessor
from fairbalance.tests.base_test import BaseSetUp
import pandas as pd
from pandas.testing import assert_frame_equal


def process_unprocess(dataset, target, sampler, cat=None, cont=None):
    X, y = sampler.process(dataset, target, cat, cont)
    X_final, y_final = sampler.unprocess(X, y)

    print(X_final["feature2"])
    print(dataset["feature2"])
    print(assert_frame_equal(X_final, dataset))
    assert dataset.equals(X_final)
    assert target.equals(y_final)


class TestRandomOverSamplerProcessor(BaseSetUp):

    def test_init(self):
        # no args
        assert RandomOverSamplerProcessor()

        # change prefix separator
        ros = RandomOverSamplerProcessor(prefix_sep="-")
        assert ros.prefix_sep == "-"
        # add kwargs
        ros = RandomOverSamplerProcessor(shrinkage=0.3, random_state=0)
        assert ros.shrinkage == 0.3
        assert ros.random_state == 0

    def test_process(self):
        self.setUp(multi=True)
        ros = RandomOverSamplerProcessor()

        X, y = ros.process(self.dataset, self.target)

        # assert no change
        assert self.dataset.equals(X)
        assert self.target.equals(y)

    def test_unprocess(self):
        self.setUp(multi=True)
        process_unprocess(self.dataset, self.target,
                          RandomOverSamplerProcessor())


class TestRandomUnderSamplerProcessor(BaseSetUp):

    def test_init(self):
        # no args
        assert RandomUnderSamplerProcessor()

        # change prefix separator
        rus = RandomUnderSamplerProcessor(prefix_sep="-")
        assert rus.prefix_sep == "-"
        # add kwargs
        rus = RandomUnderSamplerProcessor(random_state=0)
        assert rus.random_state == 0

    def test_process(self):
        self.setUp(multi=True)
        rus = RandomUnderSamplerProcessor()

        X, y = rus.process(self.dataset, self.target)

        # assert no change
        assert self.dataset.equals(X)
        assert self.target.equals(y)

    def test_unprocess(self):
        self.setUp(multi=True)
        process_unprocess(self.dataset, self.target,
                          RandomUnderSamplerProcessor())


class TestSMOTENCProcessor(BaseSetUp):
    def test_init(self):
        assert SMOTENCProcessor()

        # change prefix separator
        smotenc = SMOTENCProcessor(prefix_sep="-")
        assert smotenc.prefix_sep == "-"
        # add kwargs
        smotenc = SMOTENCProcessor(random_state=0)
        assert smotenc.random_state == 0

    def test_process(self):
        self.setUp()
        smotenc = SMOTENCProcessor()
        X, y = smotenc.process(self.dataset, self.target,
                               self.cat_columns, self.cont_columns)

        # assert that all the values in X are numerical (necessary for SMOTENC)
        types = X.dtypes
        for column in X.columns:
            assert types[column] is not object

    def test_unprocess(self):
        self.setUp()
        smotenc = SMOTENCProcessor()
        process_unprocess(self.dataset, self.target, smotenc,
                          self.cat_columns, self.cont_columns)
