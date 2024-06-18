import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots


def school_round(x):
    return round(x + 1e-15)


def iterate(subplots, idx):
    idx += 1
    rows = subplots["rows"]
    cols = subplots["cols"]
    if idx == 1:
        return 1, 1
    # iterating through end of the lines
    if (cols / idx) >= 1:  # still first line
        return 1, idx
    if (cols / idx) < 1:  # idx is not on the first line anymore
        row = school_round((idx / cols))  # round always up
        col = cols if (idx % cols) == 0 else (idx % cols)
        return row, col


def vizualize(config):
    global_config = config["global_config"]
    display = global_config["display"]
    output = global_config["output"]
    picture = global_config["picture"]
    subplots = global_config["subplots"]
    layout = global_config["layout"]
    body = config["body"]

    response = {}

    fig = make_subplots(**subplots)
    # Go through each plot config and render data
    for idx, plot_config in enumerate(body):
        row, col = iterate(subplots, idx)
        # Go through each data trajectory and add it to the current graph
        for axis_config in plot_config:
            if "x" in axis_config:
                fig.add_trace(go.Scatter(**axis_config), row=row, col=col)
            if "_config" in axis_config:
                fig.update_xaxes(**axis_config["_config"]["update_xaxes"], row=row, col=col)
                fig.update_yaxes(**axis_config["_config"]["update_yaxes"], row=row, col=col)
                fig.update_annotations(**axis_config["_config"]["update_annotations"])
    # update layout after each graph ready
    fig.update_layout(**layout)
    # update annotations
    if display:
        plot(fig)
    if "div" in output:
        response["div"] = plot(fig, output_type='div', include_plotlyjs=global_config["include_js"], show_link=False, link_text="")
    if "fig" in output:
        response["fig"] = fig
    if picture:
        fig.write_image(**picture)
    return response
