from gemini_model.model_abstract import Model


class IPR(Model):
    """ Class of IPR

        Class to calculate reservoir inflow performance
    """

    def __init__(self):
        """ Model initialization
        """
        self.parameters = {}
        self.output = {}

    def update_parameters(self, parameters):
        """ To update model parameters

        Parameters
        ----------
        parameters: dict
            parameters dict as defined by the model
        """
        for key, value in parameters.items():
            self.parameters[key] = value

    def initialize_state(self, x):
        """ generate an initial state based on user parameters """
        pass

    def update_state(self, u, x):
        """update the state based on input u and state x"""
        pass

    def calculate_output(self, u, x):
        """calculate output based on input u and state x"""
        # get input
        flow = u['flow']

        if self.parameters['type'] == 'production_reservoir':
            Pbh = self.parameters['reservoir_pressure'] - flow / self.parameters[
                'productivity_index']
        elif self.parameters['type'] == 'injection_reservoir':
            Pbh = self.parameters['reservoir_pressure'] + flow / self.parameters[
                'injectivity_index']

        self.output['pressure_bottomhole'] = Pbh

    def get_output(self):
        """get output of the model"""
        return self.output
