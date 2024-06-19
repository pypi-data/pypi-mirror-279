import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyThermalAnalysis.thermodynamics import ThermodynamicState

class TestThermodynamicState(unittest.TestCase):
    def test_creation(self):
        state = ThermodynamicState(500, 101325, 2800, 6.8)
        self.assertEqual(state.temperature, 500)
        self.assertEqual(state.pressure, 101325)
        self.assertEqual(state.specific_enthalpy, 2800)
        self.assertEqual(state.specific_entropy, 6.8)

if __name__ == '__main__':
    unittest.main()
