# PyThermalAnalysis
Advanced Thermal Analysis Library

# PyThermalAnalysis

PyThermalAnalysis is a Python library for performing exergy analysis in thermodynamic systems.

## Features

- Calculate exergy of various thermodynamic states
- Analyze exergy destruction in components like heat exchangers and turbines

## Installation

You can install the library using pip:

```bash
pip install PyThermalAnalysis
```

**use**

```python
from PyThermalAnalysis import ExergyAnalysis, ThermodynamicState

# Define ambient conditions
T0 = 298.15  # K
h0 = 0.0     # kJ/kg
s0 = 0.0     # kJ/kg-K

# Create a thermodynamic state
state = ThermodynamicState(500, 101325, 2800, 6.8)

# Perform exergy analysis
exergy_analyzer = ExergyAnalysis(T0, h0, s0)
exergy = exergy_analyzer.calculate_exergy(state)
print(f"Exergy: {exergy} kJ/kg")
```