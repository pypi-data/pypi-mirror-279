from gemini_model.model_abstract import Model
from gemini_model.well.correlation.techo import Techo
from gemini_model.well.correlation.beggsbrill import BeggsBrill
from gemini_model.well.correlation.temperaturedrop import TemperatureDrop
import numpy as np


class VLP(Model):
    """ Class of VLP

    Class to calculate pressure drop and temperature along the well with multiple sections
    """

    def __init__(self):
        self.parameters = {}
        self.output = {}
        self.PVT = None

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

        # preparing input
        Ngrid = len(self.parameters['depth'])  # Number of grid cells (-)
        theta_rad = self.parameters['angle'] * np.pi / 180  # Inclinations of cells (rad)
        Lcel = self.parameters['depth']  # Length of 1 cell
        Dtube = self.parameters['diameter']  # diameter of cells (m)
        Atube = np.pi / 4 * Dtube ** 2  # area of cells (m2)
        SAtube = np.pi * Dtube * Lcel  # surface area of cell (m2)
        Krough = 0.01e-3 * np.ones(Ngrid)  # roughness of cells (m2)
        Uvalue = 10 * np.ones(Ngrid)  # Heat transfer coefficient (W/m2.K)

        direction = u['direction']
        pressure = u['pressure_input'] * 1e5  # convert to Pa
        temperature = u['temperature_input'] + 273.15  # convert to K
        mtot = u['mass_flowrate']
        T_ambient = u['temperature_ambient'] + 273.15  # convert to K

        if direction == 'down':
            krange = range(1, Ngrid + 1)
        elif direction == 'up':
            krange = range(Ngrid, 0, -1)

        for k in krange:
            rho_g, rho_l, gmf, eta_g, eta_l, cp_g, cp_l, K_g, K_l, sigma = self.PVT.get_pvt(
                pressure,
                temperature)

            ml = (1 - gmf) * mtot
            mg = gmf * mtot

            if mg == 0:
                model = 1  # mg = 0, using techo model
            else:
                model = 2  # using beggs & brill model

            us_l = (ml / rho_l) / Atube[k - 1]  # superficial gas velocity [m/s]
            us_g = (mg / rho_g) / Atube[k - 1]  # superficial liquid velocity [m/s]

            if model == 1:
                dp_friction, dp_grav = Techo.calculate_dp(us_l,
                                                          rho_l,
                                                          theta_rad[k - 1],
                                                          eta_l, Dtube[k - 1],
                                                          Krough[k - 1],
                                                          Lcel[k - 1])
            elif model == 2:
                dp_friction, dp_grav = BeggsBrill.calculate_dp(us_g,
                                                               us_l, rho_g,
                                                               rho_l,
                                                               theta_rad[k - 1],
                                                               eta_g,
                                                               eta_l, sigma,
                                                               Dtube[k - 1],
                                                               Krough[k - 1],
                                                               Lcel[k - 1])

            else:
                dp_friction = 0
                dp_grav = 0

            dT = TemperatureDrop.calculate_dt(temperature, Uvalue[k - 1],
                                              ml, mg, cp_l, cp_g,
                                              SAtube[k - 1], T_ambient)

            if direction == 'down':
                pressure = max(0.001, pressure + dp_friction + dp_grav)
                temperature = temperature + dT
            elif direction == 'up':
                pressure = max(0.001, pressure - dp_friction - dp_grav)
                temperature = temperature - dT

        self.output['pressure_output'] = pressure / 1e5
        self.output['temperature_output'] = temperature - 273.15

    def get_output(self):
        """get output of the model"""
        return self.output
