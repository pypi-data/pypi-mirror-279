class PVTConstantSTP:
    """PVT Water at STP Class"""

    def __init__(self):
        self.pressure_max = 500e5
        self.pressure_min = 1e5
        self.temperature_max = 100 + 273.15
        self.temperature_min = 0 + 273.15

        self.RHOG = 1.976  # CO2 gas density (kg/m3)
        self.RHOL = 1000  # H2O Liquid density (kg/m3)
        self.GMF = 0  # gas mass fraction (-)
        self.VISG = 21.29e-6  # CO2 Gas viscosity (Pa.s)
        self.VISL = 1e-3  # H2O viscosity (Pa.s)
        self.CPG = 0.819e3  # CO2 heat capacity (J/Kg K)
        self.CPL = 4.2174e3  # H2O Heat capacity (J/Kg K)
        self.HG = 484.665  # CO2 Enthalpy (KJ/Kg)
        self.HL = 0.000612  # H2O Enthalpy ((KJ/Kg)
        self.TCG = 14.7e-3  # CO2 thermal conductivity (W/m K)
        self.TCL = 1.6  # H2O thermal conductivity (W/m K)
        self.SIGMA = 72.8e-3  # Water-CO2 surface tension (N/m)
        self.SG = 9381.68  # CO2 Entropy (K/Kg K)
        self.SL = 0  # H2O Entropy (K/Kg K)

    def get_pvt(self, P, T):
        """
        Function to calculate the PVT parameters based on pressure and temperature

        Parameters
        ----------
        P : float
            pressure (Pa)
        T : float
            temperature (K)

        Returns
        -------
        rho_g : float
            gas density (kg/m3)
        rho_l : float
            liquid density (kg/m3)
        gmf : float
            gas mass fraction (-)
        eta_g : float
            viscosity gas (Pa.s)
        eta_l : float
            viscosity liquid (Pa.s)
        cp_g : float
            heat capacity gas (J/Kg/K)
        cp_l : float
            heat capacity liquid (J/Kg/K)
        K_g : float
            thermal conductivity gas (W/m/K)
        K_l : float
            thermal conductivity liquid (W/m/K)
        sigma : float
            surface tension (N/m)
        """

        # Density of Gas, Oil & Water. rho_l is a psuedo density of liquid phase
        rho_g = self.RHOG  # density gas (kg/m3)
        rho_l = self.RHOL  # density liquid (kg/m3)

        # Gas mass fraction of gas + water
        gmf = self.GMF  # gas mass fraction (-)

        # Viscosity of Gas & Water
        eta_g = self.VISG  # viscosity gas (Pa.s)
        eta_l = self.VISL  # viscosity liquid (Pa.s)

        # Heat capacity of gas & liquid
        cp_g = self.CPG  # heat capacity gas (J/Kg/K)
        cp_l = self.CPL  # heat capacity liquid (J/Kg/K)

        # Thermal conductivity of gas & liquid
        K_g = self.TCG  # thermal conductivity gas (W/m/K)
        K_l = self.TCL  # thermal conductivity liquid (W/m/K)

        # Interfacial tension of Gas-Water & Gas-Oil interface
        sigma = self.SIGMA  # Surface tension (N/m)

        return rho_g, rho_l, gmf, eta_g, eta_l, cp_g, cp_l, K_g, K_l, sigma
