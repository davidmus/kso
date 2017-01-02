import unittest
from django.test.testcases import TestCase
from modelTests.ComposerTest import ComposerTest
from modelTests.ConductorTest import ConductorTest
from modelTests.PieceTest import PieceTest
from viewTests.ConcertViewTest import ConcertViewTest


class ConcertsTestSuite(TestCase):
    def suite(self):
        testSuite = unittest.TestSuite([
            unittest.TestLoader().loadTestsFromModule(ComposerTest),
            unittest.TestLoader().loadTestsFromModule(PieceTest),
            unittest.TestLoader().loadTestsFromModule(ConductorTest),
            unittest.TestLoader().loadTestsFromModule(ConcertViewTest),
        ])
        return testSuite