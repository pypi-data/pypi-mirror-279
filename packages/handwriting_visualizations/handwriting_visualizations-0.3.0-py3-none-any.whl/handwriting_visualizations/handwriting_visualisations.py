from .SimplePlots import *
from .AdvancedPlots import *


class HandwritingVisualisations:

    def __init__(self, input_data, custom_config={}):
        """Constructor with basic inicialisation"""
        self.input_data = input_data
        self.custom_config = custom_config if bool(custom_config) else {}
        self.simple_plots = SimplePlots(self.input_data, self.custom_config)
        self.advanced_plots = AdvancedPlots(self.input_data, self.custom_config)
