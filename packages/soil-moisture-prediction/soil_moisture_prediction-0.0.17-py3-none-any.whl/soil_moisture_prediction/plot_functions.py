"""Module to plot predicition, etc.

This file regroups all functions used to plot the input data or the regression results
"""

import base64
import os
from io import BytesIO

import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import xycmap
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.ndimage import median_filter

mpl.use("agg")

CM_PER_INCH = 1 / 2.54


def convert_plt_to_base64(plt):
    """Convert matplot to base64 encoded image."""
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="svg", bbox_inches="tight")
    img_buffer.seek(0)
    content = base64.b64encode(img_buffer.read()).decode()
    return content


def set_axis(rfo_model):
    """
    Define the axis for plotting.

    Parameters:
    - rfo_model (object): Object containing geometric information.

    Returns:
    - tuple: Tuple containing the x-axis and y-axis values for plotting.
    """
    return (
        rfo_model.rect_geom.grid_x / 1000,
        rfo_model.rect_geom.grid_y / 1000,
    )


def plot_selection(rfo_model):
    """
    Plot visualizations defined by the input selection.

    Parameters:
    - rfo_model (object): Random forest regression model and results.

    This function plots various visualizations based on the input selection
    defined in the rfo_model object. It plots predictors, prediction correlation
    matrix, measurements, model predictions, and predictor importance for each
    time step if specified in what_to_plot attribute of rfo_model. Additionally,
    it can plot predictor importance across all days if specified.
    """
    output_dir = rfo_model.work_dir

    if rfo_model.what_to_plot["predictors"]:
        plot_predictors(rfo_model, output_dir=output_dir)

    if rfo_model.what_to_plot["pred_correlation"]:
        prediction_correlation_matrix(rfo_model, output_dir=output_dir)

    for time_step in range(len(rfo_model.input_data.soil_moisture_data.start_times)):
        if rfo_model.what_to_plot["day_measurements"]:
            plot_measurements(
                rfo_model,
                time_step,
                output_dir=output_dir,
            )
        if rfo_model.what_to_plot["day_prediction_map"]:
            plot_rfo_model(
                rfo_model,
                time_step,
                output_dir=output_dir,
            )
        if rfo_model.what_to_plot["day_predictor_importance"]:
            plot_predictor_importance(
                rfo_model,
                time_step,
                output_dir=output_dir,
            )
    if rfo_model.what_to_plot["alldays_predictor_importance"]:
        predictor_importance_along_days(rfo_model, output_dir=output_dir)


def plot_predictors(rfo_model, output_dir=None, return_base64_img=False):
    """
    Plot all predictors as color maps.

    Parameters:
    - rfo_model (object): Random forest regression model and results.
    - output_dir (str): Directory path to save the plot image file.
    - return_base64_img (bool): Whether to return the plot image as a base64 string.


    This function plots all predictors as color maps, with predictor name and
    unit displayed. It automatically adjusts the layout based on the number
    of predictors and shares the same axes for all subplots.
    """
    n_cols = np.ceil(len(rfo_model.input_data.predictors) / 2).astype(int)
    fig, ax = plt.subplots(
        nrows=2,
        ncols=n_cols,
        sharex=True,
        sharey=True,
        figsize=(17 * CM_PER_INCH, 9 * CM_PER_INCH),
    )
    xaxis, yaxis = set_axis(rfo_model)
    fig.subplots_adjust(wspace=0.4)
    plt.rcParams.update({"font.size": 5})
    axes_count = 0
    for pred_name, predictor in rfo_model.input_data.predictors.items():
        im = ax.flat[axes_count].pcolormesh(xaxis, yaxis, predictor[0], shading="auto")
        ax.flat[axes_count].set_title(pred_name)
        ax.flat[axes_count].set_aspect(1)
        divider = make_axes_locatable(ax.flat[axes_count])
        cax = divider.append_axes("right", size="5%", pad=0.15)
        cbar = plt.colorbar(im, cax=cax)
        cbar.ax.set_title(predictor[1])
        axes_count += 1

    if return_base64_img:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(output_dir, "predictors.svg")
    plt.savefig(fig_file_path, dpi=300)


def prediction_correlation_matrix(rfo_model, output_dir=None, return_base64_img=False):
    """Plot the correlation matrix between all predictors, 2 by 2.

    Parameters:
    - rfo_model (object): Random forest regression model and results.
    - output_dir (str): Directory path to save the plot image file.
    - return_base64_img (bool): Whether to return the plot image as a base64 string.

    This function plots the correlation matrix between all predictors as a heatmap.
    Each cell represents the correlation coefficient between two predictors.
    The x-axis and y-axis labels show the names of the predictors.
    The color intensity indicates the strength and direction of correlation,
    ranging from -1 (strong negative correlation) to 1 (strong positive correlation).
    If return_base64_img is True, the function returns the base64-encoded
    image string. Otherwise, it saves the plot image as an SVG file in the
    specified output directory.
    """
    ticks = list(rfo_model.input_data.predictors.keys())
    plt.figure(figsize=(12 * CM_PER_INCH, 9 * CM_PER_INCH))
    plt.rcParams.update({"font.size": 5})
    correlation_matrix = rfo_model.input_data.compute_correlation_matrix()
    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="seismic",
        vmin=-1,
        vmax=1,
        xticklabels=ticks,
        yticklabels=ticks,
    )

    if return_base64_img:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(output_dir, "correlation_matrix.svg")
    plt.savefig(fig_file_path, dpi=300)


def draw_error_band_path(x, y, error):
    """
    Calculate normals via centered finite differences.

    Parameters:
    - x (numpy.ndarray): Array of x-coordinates.
    - y (numpy.ndarray): Array of y-coordinates.
    - error (numpy.ndarray): Array of error values corresponding to each point.

    Returns:
    - matplotlib.path.Path: Path object representing the error band.

    This function calculates the normals of a path using centered finite differences.
    It computes the components of the normals and extends the path in both directions
    based on the error values. The resulting path forms an error band around the
    original path.
    """
    dist_to_next_point_x_component = np.concatenate(
        [[x[1] - x[0]], x[2:] - x[:-2], [x[-1] - x[-2]]]
    )
    dist_to_next_point_y_component = np.concatenate(
        [[y[1] - y[0]], y[2:] - y[:-2], [y[-1] - y[-2]]]
    )
    dist_to_next_point = np.hypot(
        dist_to_next_point_x_component, dist_to_next_point_y_component
    )
    normal_x_component = dist_to_next_point_y_component / dist_to_next_point
    normal_y_component = -dist_to_next_point_x_component / dist_to_next_point

    scale_error_vector = 3
    x_error_end_point = x + normal_x_component * error * scale_error_vector
    y_error_end_point = y + normal_y_component * error * scale_error_vector

    vertices = np.block([[x_error_end_point, x[::-1]], [y_error_end_point, y[::-1]]]).T
    codes = np.full(len(vertices), Path.LINETO)
    codes[0] = Path.MOVETO
    return Path(vertices, codes)


def plot_measurements_vs_distance(
    rfo_model, time_step, output_dir=None, return_base64_img=False
):
    """Plot soil moisture measurements vs. cumulative driven distance.

    Includes the corresponding low and up standard deviations.
    """
    start_time = rfo_model.input_data.soil_moisture_data.start_times[time_step]

    plt.rcParams.update({"font.size": 7})
    cumulative_distance = [0]
    for measurement in range(
        rfo_model.input_data.soil_moisture_data.number_measurements[start_time] - 1
    ):
        cumulative_distance.append(
            (
                cumulative_distance[measurement]
                + np.sqrt(
                    (
                        rfo_model.input_data.soil_moisture_data.x_measurement[
                            start_time
                        ][measurement + 1]
                        - rfo_model.input_data.oil_moisture_data.x_measurement[
                            start_time
                        ][measurement]
                    )
                    ** 2
                    + (
                        rfo_model.input_data.soil_moisture_data.y_measurement[
                            start_time
                        ][measurement + 1]
                        - rfo_model.input_data.soil_moisture_data.y_measurement[
                            start_time
                        ][measurement]
                    )
                    ** 2
                )
                / 1000
            )
        )
    plt.figure()
    plt.plot(
        cumulative_distance,
        rfo_model.input_data.soil_moisture_data.soil_moisture[start_time],
        "g",
        label="Measurements",
    )
    if rfo_model.monte_carlo_soil_moisture or rfo_model.monte_carlo_predictor:
        plt.fill_between(
            cumulative_distance,
            rfo_model.input_data.soil_moisture_data.soil_moisture[start_time]
            - rfo_model.input_data.soil_moisture_data.soil_moisture_dev_low[start_time],
            rfo_model.input_data.soil_moisture_data.soil_moisture[start_time]
            + rfo_model.input_data.soil_moisture_data.soil_moisture_dev_high[
                start_time
            ],
            edgecolor="none",
            alpha=0.3,
            color="purple",
            label="Lower/upper SD",
        )
    plt.ylim([0.1, 0.8])
    plt.xlabel("Cumulative distance (km)")
    plt.ylabel("Gravimetric soil moisture (g/g)")
    plt.legend(loc="upper left")

    if return_base64_img:
        return convert_plt_to_base64(plt)
    fig_file_path = os.path.join(
        output_dir, "measurements_vs_distance_" + start_time + ".svg"
    )
    plt.savefig(fig_file_path, dpi=300)


def plot_measurements(rfo_model, time_step, output_dir=None, return_base64_img=False):
    """
    Plot measurements as scatter on a x-y map.

    Parameters:
    - rfo_model (object): Random forest regression model and results.
    - time_step (int): Index of the time step for which measurements are plotted.
    - output_dir (str, optional): Directory path to save the plot image file.
    - return_base64_img (bool, optional): Whether to return the plot image as a
      base64 string.

    This function plots measurements as a scatter plot on an x-y map. It uses
    the soil moisture measurements from the specified time step of the input
    data. The measurements are colored according to their corresponding soil
    moisture values. If Monte Carlo simulations are enabled, error bands
    representing the standard deviations are overlaid on the scatter plot.
    """
    start_time = rfo_model.input_data.soil_moisture_data.start_times[time_step]

    plt.figure()
    plt.gca().set_aspect(1)
    x = rfo_model.input_data.soil_moisture_data.x_measurement[start_time] / 1000
    y = rfo_model.input_data.soil_moisture_data.y_measurement[start_time] / 1000
    sc = plt.scatter(
        x,
        y,
        c=rfo_model.input_data.soil_moisture_data.soil_moisture[start_time],
        cmap="Spectral",
        s=5,
        vmin=0.1,
        vmax=0.6,
        zorder=2,
        label="Measurements",
    )
    if rfo_model.monte_carlo_soil_moisture or rfo_model.monte_carlo_predictor:
        plt.gca().add_patch(
            PathPatch(
                draw_error_band_path(
                    x,
                    y,
                    -rfo_model.input_data.soil_moisture_data.soil_moisture_dev_low[
                        start_time
                    ],
                ),
                alpha=0.3,
                color="purple",
                label="Lower/upper SD",
            )
        )
        plt.gca().add_patch(
            PathPatch(
                draw_error_band_path(
                    x,
                    y,
                    rfo_model.input_data.soil_moisture_data.soil_moisture_dev_high[
                        start_time
                    ],
                ),
                alpha=0.3,
                color="purple",
            )
        )
    plt.xlabel("Easting (km)")
    plt.ylabel("Northing (km)")
    plt.legend(loc="upper left")
    cbar = plt.colorbar(sc, shrink=0.55)
    cbar.set_label("Gravimetric soil moisture (g/g)")

    if return_base64_img:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(output_dir, "measurements_" + start_time + ".svg")
    plt.savefig(fig_file_path, dpi=300)


def plot_rfo_model(rfo_model, time_step, *args, **kwargs):
    """Plot random forest prediction as a color map."""
    if rfo_model.monte_carlo_soil_moisture or rfo_model.monte_carlo_predictor:
        return plot_rfo_model_with_dispersion(rfo_model, time_step, *args, **kwargs)
    else:
        return plot_rfo_model_no_dispersion(rfo_model, time_step, *args, **kwargs)


def plot_rfo_model_no_dispersion(
    rfo_model,
    time_step,
    output_dir=None,
    return_base64_img=False,
):
    """
    Plot soil moisture prediction as a color map.

    Parameters:
    - rfo_model (object): Random forest regression model and results.
    - time_step (int): Index of the time step for which predictions are plotted.
    - output_dir (str, optional): Directory path to save the plot image file.
    - return_base64_img (bool, optional): Whether to return the plot image as a
      base64 string.
    """
    if not output_dir:
        output_dir = rfo_model.work_dir

    xaxis, yaxis = set_axis(rfo_model)
    start_time = rfo_model.input_data.soil_moisture_data.start_times[time_step]

    plt.rcParams.update({"font.size": 6})
    fig, ax = plt.subplots(figsize=(16 * CM_PER_INCH, 14 * CM_PER_INCH))
    im = plt.pcolormesh(
        xaxis,
        yaxis,
        rfo_model.RF_prediction[0, time_step, :, :],
        vmin=0.1,
        vmax=0.45,
        cmap="Spectral",
    )

    plt.scatter(
        rfo_model.input_data.soil_moisture_data.x_measurement[start_time] / 1000,
        rfo_model.input_data.soil_moisture_data.y_measurement[start_time] / 1000,
        c="black",
        s=0.5,
    )
    ax.set_title(start_time)
    ax.set_aspect(1)
    cbar = plt.colorbar(im)
    cbar.ax.tick_params(labelsize=14)
    if return_base64_img:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(output_dir, "RF_prediction_" + start_time + ".tif")
    plt.savefig(fig_file_path, dpi=300)


def plot_rfo_model_with_dispersion(
    rfo_model,
    time_step,
    output_dir=None,
    return_base64_img=False,
):
    """
    Plot soil moisture mean prediction and coefficient of dispersion maps.

    Parameters:
    - rfo_model (object): Random forest regression model and results.
    - time_step (int): Index of the time step for which predictions are plotted.
    - output_dir (str, optional): Directory path to save the plot image file.
    - return_base64_img (bool, optional): Whether to return the plot image as a
      base64 string.

    This function plots the mean prediction and coefficient of dispersion maps
    for soil moisture predictions. It uses the data from the specified time
    step of the random forest model. Measurement locations are overlaid on the
    plots. The first subplot displays the mean prediction map, while the second
    subplot displays the coefficient of dispersion map.
    """
    xaxis, yaxis = set_axis(rfo_model)
    start_time = rfo_model.input_data.soil_moisture_data.start_times[time_step]

    plt.rcParams.update({"font.size": 7})

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16 / 2.54, 10 / 2.54))
    axes[0].set_aspect(1)
    axes[1].set_aspect(1)

    divider = make_axes_locatable(axes[0])
    cax = divider.append_axes("right", size="5%", pad=0.15)
    im = axes.flat[0].pcolormesh(
        xaxis,
        yaxis,
        rfo_model.MC_mean[time_step],
        shading="auto",
        vmin=0.1,
        vmax=0.45,
        cmap="Spectral",
    )
    axes.flat[0].scatter(
        rfo_model.input_data.soil_moisture_data.x_measurement[start_time] / 1000,
        rfo_model.input_data.soil_moisture_data.y_measurement[start_time] / 1000,
        c="black",
        s=1,
    )
    axes.flat[0].set_title("Mean")
    plt.colorbar(im, cax=cax)

    im1 = axes.flat[1].pcolormesh(
        xaxis,
        yaxis,
        rfo_model.dispersion_coefficient[time_step],
        shading="auto",
        vmin=0,
        vmax=0.15,
        cmap="Reds",
    )
    axes.flat[1].set_title("Coefficient of dispersion")
    axes.flat[1].tick_params(axis="y", left=False, labelleft=False)
    divider = make_axes_locatable(axes[1])
    cax = divider.append_axes("right", size="5%", pad=0.15)
    plt.colorbar(im1, cax=cax)

    fig.suptitle(start_time)

    if return_base64_img:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(output_dir, "RF_prediction_" + start_time + ".svg")
    plt.savefig(fig_file_path, dpi=300)


def plot_monte_carlo_iteration(
    rfo_model,
    time_step,
    iteration_index,
    output_dir=None,
    return_base64_img=False,
):
    """Plot the Monte Carlo itration for the given RFO model and time step.

    Parameters:
    - rfo_model (object): The RFO model containing prediction data.
    - time_step (int): The time step index for plotting.
    - iteration_index (int): The iteration index for Monte Carlo simulation.
    - output_dir (str, optional): Directory to save the plot. Defaults to
                                rfo_model.work_dir.
    return_base64_img (bool, optional): If True, returns the plot as a base64
                                        string. Defaults to False.
    """
    if not output_dir:
        output_dir = rfo_model.work_dir

    xaxis, yaxis = set_axis(rfo_model)
    start_time = rfo_model.input_data.soil_moisture_data.start_times[time_step]

    plt.rcParams.update({"font.size": 6})
    fig, ax = plt.subplots(figsize=(16 * CM_PER_INCH, 14 * CM_PER_INCH))
    im = plt.pcolormesh(
        xaxis,
        yaxis,
        rfo_model.RF_prediction[iteration_index, time_step, :, :],
        vmin=0.1,
        vmax=0.45,
        cmap="Spectral",
    )
    plt.scatter(
        rfo_model.input_data.soil_moisture_data.x_measurement[start_time] / 1000,
        rfo_model.input_data.soil_moisture_data.y_measurement[start_time] / 1000,
        c="black",
        s=0.5,
    )
    ax.set_title(start_time)
    ax.set_aspect(1)
    cbar = plt.colorbar(im)
    cbar.ax.tick_params(labelsize=14)

    if return_base64_img:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(
        output_dir,
        "RF_prediction_" + start_time + "_iteration_" + iteration_index + ".svg",
    )
    plt.savefig(fig_file_path, dpi=300)


def plot_predictor_importance(
    rfo_model,
    time_step,
    output_dir=None,
    return_base64_img=False,
):
    """
    Plot predictor importance from the random forest model.

    This function plots the predictor importance from the random forest model
    for the specified time step. It displays the importance values as bars for
    each predictor. If Monte Carlo simulations were performed, the function
    shows the 5th, 50th (median), and 95th quantiles of the importance values.
    Otherwise, it displays the raw importance values. The x-axis represents the
    predictors, and the y-axis represents the importance values.
    """
    start_time = rfo_model.input_data.soil_moisture_data.start_times[time_step]

    plt.rcParams.update({"font.size": 7})
    x = np.arange(rfo_model.input_data.number_predictors)
    plt.figure(figsize=(16 / 2.54, 7 / 2.54))
    if rfo_model.monte_carlo_soil_moisture or rfo_model.monte_carlo_predictor:
        plt.bar(
            rfo_model.input_data.predictors.keys(),
            np.percentile(
                rfo_model.predictor_importance[:, time_step, :],
                95,
                axis=0,
            ),
            color="deepskyblue",
            label="q95",
        )
        plt.bar(
            rfo_model.input_data.predictors.keys(),
            np.percentile(
                rfo_model.predictor_importance[:, time_step, :],
                50,
                axis=0,
            ),
            color="blue",
            label="median",
        )
        plt.bar(
            rfo_model.input_data.predictors.keys(),
            np.percentile(
                rfo_model.predictor_importance[:, time_step, :],
                5,
                axis=0,
            ),
            color="navy",
            label="q5",
        )
        plt.legend()
    else:
        plt.bar(
            rfo_model.input_data.predictors.keys(),
            rfo_model.predictor_importance[0, time_step, :],
        )
    plt.xticks(x, rfo_model.input_data.predictors.keys())
    plt.title(start_time)

    if return_base64_img:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(
        output_dir, "predictor_importance_" + start_time + ".svg"
    )
    plt.savefig(fig_file_path, dpi=300)


def predictor_importance_along_days(
    rfo_model,
    apply_pca=False,
    output_dir=None,
    return_base64_img=False,
):
    """
    Plot predictor importance from the RF model along the days.

    This function plots the predictor importance from the random forest model
    over the days. It displays the mean importance values for each predictor
    across all days. If PCA was applied, it plots the importance values for
    each PCA component. The x-axis represents the days, and the y-axis
    represents the importance values.
    """
    number_predictors = rfo_model.input_data.number_predictors
    start_times = rfo_model.input_data.soil_moisture_data.start_times
    predictor_importance = rfo_model.predictor_importance
    predictors = rfo_model.input_data.predictors

    plt.rcParams.update({"font.size": 7})
    fig, ax = plt.subplots(
        number_predictors,
        sharex=True,
        figsize=(17 / 2.54, 16 / 2.54),
    )
    if not apply_pca:
        if number_predictors == 1:
            ax.plot(
                range(len(start_times)),
                np.mean(predictor_importance[:, :, 0], axis=0),
                label=list(predictors.keys())[0],
            )
            ax.set_ylim(0, 1)
            ax.legend(loc="right")
        else:
            for pred_index, predictor_name in enumerate(predictors.keys()):
                ax[pred_index].plot(
                    range(len(start_times)),
                    np.mean(predictor_importance[:, :, pred_index], axis=0),
                    label=predictor_name,
                )
                ax[pred_index].set_ylim(0, 1)
                ax[pred_index].legend(loc="right")
    else:
        for predictor_index in range(number_predictors):
            ax[predictor_index].plot(
                range(len(start_times)),
                np.mean(predictor_importance[:, :, predictor_index], axis=0),
                label="PCA comp. " + str(predictor_index),
            )
            ax[predictor_index].set_ylim(0, 1)
            ax[predictor_index].legend(loc="right")

    if return_base64_img:
        return convert_plt_to_base64(plt)

    fig_file_path = os.path.join(output_dir, "predictor_importance_vs_days.svg")
    plt.savefig(fig_file_path, dpi=300)


# Update!
def plot_section_sm_with_pred(rfo_model, x_axis, y, pred, day):
    """Plot SM mean together with predictor values along this section.

    Plot SM mean prediction and percentiles along a horizontal or vertical map section,
    together with predictor values along this section

    rfo_model : rfo_model object
    x_axis        : 1D array with the coordinates along the section
    y             : scalar, fix coordinate of the section
    pred          : dictionary with predictor values along this section
    day             : int, day number
    """
    raise NotImplementedError

    rf_stats = [
        rfo_model.p5[day],
        rfo_model.p25[day],
        rfo_model.m[day],
        rfo_model.p75[day],
        rfo_model.p95[day],
    ]
    p5_mid, p25_mid, p50_mid, p75_mid, p95_mid = [
        np.empty(len(x_axis)) for k in range(5)
    ]
    for j in range(len(x_axis)):
        idx_x = j
        p5_mid[j], p25_mid[j], p50_mid[j], p75_mid[j], p95_mid[j] = [
            perc[idx_x, y] for perc in rf_stats
        ]

    plt.rcParams.update({"font.size": 14})
    fig, ax1 = plt.subplots(figsize=(23, 5))
    ax1.plot(x_axis, p50_mid, "r", label="Median")
    ax1.fill_between(x_axis, p5_mid, p95_mid, color="blue", alpha=0.3, label="5-95%")
    ax1.fill_between(x_axis, p25_mid, p75_mid, color="blue", alpha=0.7, label="25-75%")
    ax1.set_ylim([0.2, 0.5])
    ax1.set_ylabel("Gravimetric soil moisture (g/g)")
    ax2 = ax1.twinx()
    for k, v in pred.items():
        ax2.plot(x_axis, v[0][:, y], label=k)
    ax2.legend()


# Update!
def plot_section_all_iters(rfo_model, x_axis, y, day):
    """Plot all SM RF predictions along a horizontal or vertical map section.

    rfo_model : rfo_model object
    x_axis        : 1D array with the coordinates along the section
    y             : scalar, fix coordinate of the section
    day             : int, day number
    """
    raise NotImplementedError
    plt.rcParams.update({"font.size": 14})
    plt.figure()
    plt.ylim([0.2, 0.5])
    for i in range(rfo_model.n_iters):
        plt.plot(x_axis, rfo_model.RF_prediction[i, day, :, y])


def plot_rfo_model_as_bivariate(rfo_model, day, smooth_data=False):
    """Create a bivariate map based on a 2D colormap (saturation of a given colormap).

    rfo_model : rfo_model object
    """
    if smooth_data:
        mc_mean = median_filter(rfo_model.MC_mean[day], size=3, mode="nearest")
        disp_coeff = median_filter(rfo_model.disp_coeff[day], size=3, mode="nearest")

    cmap = saturation_xycmap(mpl.cm.get_cmap("Spectral"), "white", n=(9, 3))
    colors = xycmap.bivariate_color(
        sx=mc_mean.flatten(),
        sy=disp_coeff.flatten(),
        cmap=cmap,
        xlims=(0.2, 0.5),
        ylims=(0.2, 0.55),
    )
    color = colors.to_numpy().reshape(mc_mean.shape).T
    bi_map = np.empty((color.shape[0], color.shape[1], 4))  # 4 for rgba
    for i in range(color.shape[0]):
        for j in range(color.shape[1]):
            bi_map[i, j, 0] = color[i, j][0]
            bi_map[i, j, 1] = color[i, j][1]
            bi_map[i, j, 2] = color[i, j][2]
            bi_map[i, j, 3] = color[i, j][3]
    plt.rcParams.update({"font.size": 13})
    fig, axs = plt.subplots(1, 2)
    axs[0].imshow(
        bi_map,
        origin="lower",
        extent=[
            rfo_model.geom.xi / 1000,
            rfo_model.geom.xf / 1000,
            rfo_model.geom.yi / 1000,
            rfo_model.geom.yf / 1000,
        ],
    )
    axs[0].scatter(
        rfo_model.input_data.x_crns / 1000,
        rfo_model.input_data.y_crns / 1000,
        c="black",
        s=1,
    )
    axs[0].set_ylabel("Northing (km)")
    axs[0].set_xlabel("Easting (km)")
    xycmap.bivariate_legend(
        ax=axs[1],
        sx=mc_mean.flatten(),
        sy=disp_coeff.flatten(),
        cmap=cmap,
        xlims=(0.2, 0.5),
        ylims=(0.2, 0.55),
    )
    axs[1].set_xlabel("Gravimetric soil moisture (g/g)")
    axs[1].set_ylabel("Coefficient of dispersion")


def saturation_xycmap(xcmap, color, n):
    """Create a 2D colormap by saturation of a given colormap.

    Args:
        xcmap: Matplotlib colormap along the x-axis.
        color: Color used for the colormap saturation along the y-axis.
        n    : Tuple containing the number of columns and rows (x, y).
    Returns:
        Custom two-dimensional colormap in np.ndarray.
    Raises:
        ValueError: If less than two columns or rows are passed.
    """
    xn, yn = n
    if xn < 2 or yn < 2:
        raise ValueError("Expected n >= 2 categories.")

    sy, sx = np.mgrid[0:yn, 0:xn]
    scale = sy / (yn - 1)

    xvals = np.array(
        255 * (sx - sx.min()) / (sx.max() - sx.min()), dtype=int
    )  # Rescale the mock series into the colormap range (0, 255).

    xcolors = np.asarray(xcmap(xvals))
    ycolors = np.empty((yn, xn, 4))
    for i in range(yn):
        for j in range(xn):
            ycolors[i, j, :] = np.array(colors.to_rgba(color)) * scale[i, j]
            # xcolors[i,j,:] = xcolors[i,j,:]*min(1.5*(1-scale[i,j]),1)
            xcolors[i, j, :] = xcolors[i, j, :] * (1 - scale[i, j])

    return xcolors + ycolors


def plot_rfo_model_and_percentiles(
    rfo_model,
    day,
):
    """Plot SM mean prediction with 5th and 95th percentiles maps.

    Measurement locations are overlaid.
    """
    xaxis, yaxis = set_axis(rfo_model)
    day_string = rfo_model.input_data.days[day]

    plt.rcParams.update({"font.size": 13})
    fig, axes = plt.subplots(nrows=1, ncols=3)
    axes[0].set_aspect(1)
    axes[1].set_aspect(1)
    axes[2].set_aspect(1)
    fig.subplots_adjust(wspace=0.3)

    divider = make_axes_locatable(axes[0])
    cax = divider.append_axes("right", size="5%", pad=0.15)
    im = axes.flat[0].pcolormesh(
        xaxis,
        yaxis,
        rfo_model.MC_mean[day],
        shading="auto",
        vmin=0.2,
        vmax=0.5,
        cmap="Spectral",
    )
    axes.flat[0].scatter(
        rfo_model.input_data.x_crns[day_string] / 1000,
        rfo_model.input_data.y_crns[day_string] / 1000,
        c="black",
        s=1,
    )
    axes.flat[0].set_title("Mean", fontsize=13)
    plt.colorbar(im, cax=cax)

    im = axes.flat[1].pcolormesh(
        xaxis,
        yaxis,
        rfo_model.p5[day],
        shading="auto",
        vmin=0.2,
        vmax=0.5,
        cmap="Spectral",
    )
    axes.flat[1].set_title("5% percentile", fontsize=13)
    axes.flat[1].tick_params(axis="y", left=False, labelleft=False)
    divider = make_axes_locatable(axes[1])
    cax = divider.append_axes("right", size="5%", pad=0.15)
    plt.colorbar(im, cax=cax)

    im = axes.flat[2].pcolormesh(
        xaxis,
        yaxis,
        rfo_model.p95[day],
        shading="auto",
        vmin=0.2,
        vmax=0.5,
        cmap="Spectral",
    )
    axes.flat[2].set_title("95% percentile", fontsize=13)
    axes.flat[2].tick_params(axis="y", left=False, labelleft=False)
    divider = make_axes_locatable(axes[2])
    cax = divider.append_axes("right", size="5%", pad=0.15)
    plt.colorbar(im, cax=cax)

    fig.suptitle(day_string)


def mc_iterations_histogram(rfo_model, time_step, point_x, point_y):
    """
    Plot histogram of predicted soil moisture values after n_iters MC runs.

    point_x (int): point coordinate on the x axis
    point_y (int): point coordinate on the y axis
    """
    plt.figure()
    plt.hist(
        rfo_model.RF_prediction[:, time_step, point_x, point_y],
        bins=30,
        range=(0.15, 0.6),
    )


# Update!
def relative_frequency_3d_section(rfo_model, day):
    """Plot parallel 3D sections over the study area."""
    raise NotImplementedError

    if rfo_model.monte_carlo_soil_moisture or rfo_model.monte_carlo_predictor:
        nb_hist_class = 15
        sections_hist = np.empty((nb_hist_class, 4, rfo_model.rect_geom.dim_y))
        sections_loc = np.linspace(
            10, rfo_model.rect_geom.dim_x - 10, 4, dtype=int
        )  # 4 sections along the x-axis
        for section_id, section_coord in enumerate(sections_loc):
            for y_coord in range(rfo_model.rect_geom.dim_y):
                sections_hist[:, section_id, y_coord], bin_edges = np.histogram(
                    rfo_model.RF_prediction[:, day, section_coord, y_coord],
                    bins=nb_hist_class,
                    range=(0, 1),
                )

        ax = plt.figure().add_subplot(projection="3d")
        x = rfo_model.rect_geom.grid_x[:, 0] / 1000
        y = rfo_model.rect_geom.grid_y[0, :] / 1000
        ax.set_box_aspect(
            (np.ptp(x), np.ptp(y), 20 * np.ptp(np.linspace(0, 1.2, nb_hist_class)))
        )
        ax.set_xlim(x[0], x[-1])
        ax.set_ylim(y[0], y[-1])
        norm = mpl.colors.Normalize(
            vmin=np.min(sections_hist[np.nonzero(sections_hist)]),
            vmax=np.max(sections_hist),
        )
        mapper = mpl.cm.ScalarMappable(norm=norm, cmap="Reds")
        mapper.cmap.set_under("w", alpha=0)
        x_pos = np.linspace(x[0], x[-1], 4)
        for section_id, i in enumerate(x_pos):
            z = 0
            for class_id in range(nb_hist_class):
                zcol = np.array(
                    [
                        (mapper.to_rgba(v))
                        for v in sections_hist[class_id, section_id, :]
                    ]
                )
                ax.bar3d(i, y, z, dx=0.5, dy=0.5, dz=1.2 / nb_hist_class, color=zcol)
                z += 1 / nb_hist_class
        plt.colorbar(mapper, extend="min", shrink=0.8)
    else:
        raise RuntimeError(
            "The figure can only be plot when Monte Carlo approach is used."
        )
