class ConfigsPlotXY:
    def __init__(self, x=[], y=[], custom_config={}):
        self.x = x
        self.y = y
        self.custom_config = custom_config
        # Mandatory settings
        if "x_title_text" not in custom_config:
            self.custom_config["x_title_text"] = "Souřadnice x [mm]"
        if "y_title_text" not in custom_config:
            self.custom_config["y_title_text"] = "Souřadnice y [mm]"
        if "graph_title" not in custom_config:
            self.custom_config["graph_title"] = "Scatter plot X,Y"
        if "display" not in custom_config:
            self.custom_config["display"] = False
        if "output" not in custom_config:
            self.custom_config["output"] = "fig"
        if "show_legend" not in custom_config:
            self.custom_config["show_legend"] = True
        if "include_js" not in custom_config:
            self.custom_config["include_js"] = False
        if "margin" not in custom_config:
            self.custom_config["margin"] = {"t":10, "r":10, "b":10, "l":10}
        if "height" not in custom_config:
            self.custom_config["height"] = 500
        if "line_color" not in custom_config:
            self.custom_config["line_color"] = "black"

    def get_config(self):
        config = {}
        config["body"] = \
            [
                [
                    {
                        "name": "X",
                        "x": self.x,
                        "y": self.y,
                        "mode": "lines",
                        "line": {
                            "color": self.custom_config["line_color"],
                            "width": 2
                        },
                        "opacity": 0.65,
                    },
                    {
                        "_config": {  # https://plotly.com/python/axes/
                            "update_xaxes": {
                                "title_text": self.custom_config["x_title_text"],
                                "showgrid": True,
                                "title_font": {"size": 28,
                                               "family": 'Georgia',
                                               "color": 'black'},
                                "showticklabels": True,
                                "tickangle": 0,
                                "tickfont": {
                                    "family": 'Georgia',
                                    "color": 'black',
                                    "size": 20
                                },
                                "scaleanchor": "y"
                            },
                            "update_yaxes": {
                                "title_text": self.custom_config["y_title_text"],
                                "showgrid": True,
                                "title_font": {"size": 28,
                                               "family": 'Georgia',
                                               "color": 'black'},
                                "showticklabels": True,
                                "tickangle": 0,
                                "tickfont": {
                                    "family": 'Georgia',
                                    "color": 'black',
                                    "size": 20
                                }
                            },
                            "update_annotations": {  # plotly bug, cannot update by row and col
                                "font": {
                                    "family": 'Georgia',
                                    "color": 'black',
                                    "size": 28
                                },
                                "text": self.custom_config["graph_title"],
                                "selector": {"text": "1"}
                            }
                        }
                    }
                ],
            ]

        config["global_config"] = {
            "subplots": {
                "rows": 1,
                "cols": 1,
                # "column_widths": [0.5, 0.5],
                "vertical_spacing": 0.14,
                "subplot_titles": ["1"]},
            "layout": {  # https://plotly.com/python/reference/layout/
                "showlegend": self.custom_config['show_legend'],
                "autosize": True,
                "height": self.custom_config["height"],
                # "title": "Časové řady",
                "margin": self.custom_config["margin"],
                "font": {
                    "family": "Georgia",
                    "size": 22,
                    "color": "black"
                },
                "legend": {
                    "orientation": "h",
                    "yanchor": "top",
                    "xanchor": "center",
                    "y": -0.1,
                    "x": 0.5},
                "paper_bgcolor": "rgb(255, 255, 255)",  # Background color for the entire plot area
                "plot_bgcolor": "rgb(245, 245, 220)",
            },
            "display": self.custom_config["display"],
            "output": self.custom_config["output"],
            "picture": {},
            "include_js": self.custom_config["include_js"],
        }
        return config
