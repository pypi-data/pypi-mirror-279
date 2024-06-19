## Thermodynamic analysis for given system
## In short future going to add some more methods

class ThermodynamicState:
    def __init__(self, temperature, pressure, specific_enthalpy, specific_entropy):
        self.temperature = temperature
        self.pressure = pressure
        self.specific_enthalpy = specific_enthalpy
        self.specific_entropy = specific_entropy

    def exergy(self, T0, h0, s0):
        """
        Calculate the specific physical exergy.
        
        Parameters:
        T0: float - Ambient temperature (reference temperature) [K]
        h0: float - Specific enthalpy at ambient conditions [kJ/kg]
        s0: float - Specific entropy at ambient conditions [kJ/kg-K]
        
        Returns:
        float - Specific physical exergy [kJ/kg]
        """
        return (self.specific_enthalpy - h0) - T0 * (self.specific_entropy - s0)
