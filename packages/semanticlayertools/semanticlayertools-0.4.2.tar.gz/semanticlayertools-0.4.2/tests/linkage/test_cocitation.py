import os
import tempfile
import unittest
from pathlib import Path

import pandas as pd
from semanticlayertools.linkage.citation import Couplings

basePath = Path(__file__).resolve().parents[1]
testfiles = Path(basePath, "testdata", "cocite").glob("*.json")
testchunk = pd.read_json(next(testfiles), lines=True)


class TestCocitationCreation(unittest.TestCase):

    def setUp(self):
        self.outdir = tempfile.TemporaryDirectory()
        self.cociteinit = Couplings(
            Path(basePath, "testdata", "cocite"), self.outdir, "reference",
            numberProc=2,
        )

    def test_getCombinations(self):
        res = self.cociteinit._getCombinations(testchunk)
        assert (type(res[0]) == tuple)

