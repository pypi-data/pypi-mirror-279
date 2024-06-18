from handwriting_features.features import HandwritingFeatures
from handwriting_sample import HandwritingSample
from .visualization_tools import *
from .Configs import *


class SimplePlots:

    def __init__(self, input_data, custom_config):
        self.input_data = input_data
        self.custom_config = custom_config

    def _control_input_data(self):
        """TODO: Check if input is Handwriting Features or numpy array and prepare the input data accordingly"""
        self.is_handwriting_features_obj = True if isinstance(self.input_data, HandwritingFeatures) else False

    def plot_x_y(self):
        return vizualize(ConfigsPlotXY(x=self.input_data["x"], y=self.input_data["y"], custom_config=self.custom_config).get_config()).values()

    def plot_on_surface(self, sample: HandwritingSample):
        """Plot the on_surface data of the handwriting sample"""

        # Get the on_surface data
        on_surface_strokes = sample.get_strokes(on_surface_only=True)

        # Prepare the empty config
        configs = []

        # Prepare the config for each stroke (x,y) and get global config
        for stroke in on_surface_strokes:
            configs.append(ConfigsPlotXY(x=stroke[1].x, y=stroke[1].y, custom_config=self.custom_config).get_config())

        # Create final config
        final_config = configs[0]

        # Go over each config in body and add only the x,y data
        for config in configs[1:]:
            final_config["body"][0].append(config["body"][0][0])

        return vizualize(final_config)

    def plot_in_air(self, sample: HandwritingSample):
        """Plot the on_surface data of the handwriting sample"""

        # Get the strokes data
        strokes = sample.get_strokes()

        # Prepare the empty config
        configs = []

        # Prepare the config for each stroke (x,y) and get global config
        for stroke in strokes:

            if stroke[0] == "on_surface":
                cfg = self.custom_config
                cfg["line_color"] = "black"
                configs.append(ConfigsPlotXY(x=stroke[1].x, y=stroke[1].y, custom_config=cfg).get_config())
            else:
                cfg = self.custom_config
                cfg["line_color"] = "#E91E63"
                configs.append(ConfigsPlotXY(x=stroke[1].x, y=stroke[1].y, custom_config=cfg).get_config())

        # Create final config
        final_config = configs[0]

        # Go over each config in body and add only the x,y data
        for config in configs[1:]:
            final_config["body"][0].append(config["body"][0][0])

        return vizualize(final_config)



