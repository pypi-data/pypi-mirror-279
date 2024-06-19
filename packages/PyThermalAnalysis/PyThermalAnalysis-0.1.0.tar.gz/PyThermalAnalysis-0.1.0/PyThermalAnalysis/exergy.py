class ExergyAnalysis:
    def __init__(self, ambient_temperature, ambient_enthalpy, ambient_entropy):
        self.T0 = ambient_temperature
        self.h0 = ambient_enthalpy
        self.s0 = ambient_entropy

    def calculate_exergy(self, state):
        """
        Calculate the exergy of a given thermodynamic state.
        
        Parameters:
        state: ThermodynamicState - The state for which to calculate the exergy
        
        Returns:
        float - Specific exergy [kJ/kg]
        """
        return state.exergy(self.T0, self.h0, self.s0)

    def exergy_balance(self, states_in, states_out):
        """
        Perform exergy balance for a set of inlet and outlet states.
        
        Parameters:
        states_in: list of ThermodynamicState - List of inlet states
        states_out: list of ThermodynamicState - List of outlet states
        
        Returns:
        float - Total exergy destruction [kJ]
        """
        exergy_in = sum([self.calculate_exergy(state) for state in states_in])
        exergy_out = sum([self.calculate_exergy(state) for state in states_out])
        return exergy_in - exergy_out
