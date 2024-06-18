"""Pydantic models for the input parameters of the model."""

from typing import Dict, List

from pydantic import BaseModel, Field, conlist


class PredictorData(BaseModel):
    """Data model for the predictor data."""

    type: str = Field(
        ..., description="Will be used as a name in plots (can be an empty string)."
    )
    unit: str = Field(
        ..., description="Unit of the predictor (can be an empty string)."
    )
    std_deviation: bool = Field(
        ...,
        description="Whether the csv has a fourth column with the standard deviation.",
    )


class WhatToPlot(BaseModel):
    """List of which plotting functions should be used."""

    # TODO - Add descriptions to the fields
    alldays_predictor_importance: bool
    day_measurements: bool
    day_prediction_map: bool
    day_predictor_importance: bool
    pred_correlation: bool
    predictors: bool


class Predictors(BaseModel):
    """A dictionary with keys as filenames or paths and values as predictor information."""  # noqa

    data: Dict[str, PredictorData]


class InputParameters(BaseModel):
    """Data model for the input parameters."""

    geometry: conlist(float, min_length=5, max_length=5) = Field(
        ...,
        description="A list of five numbers representing the bounding box. [xmin, xmax, ymin, ymax, resolution].",  # noqa
    )
    soil_moisture_data: Dict[str, List[str]] = Field(
        ...,
        description="A dictionary with keys as filenames or paths to the CRNS data and values as a list of timesteps (list can be an empty string).",  # noqa
    )
    predictors: Dict[str, PredictorData] = Field(
        ...,
        description="A dictionary with keys as filenames or paths to the predictor data and values as a dictonary of preditor information (type and unit can be an empty string).",  # noqa
    )
    monte_carlo_soil_moisture: bool = Field(
        ...,
        description="Whether to use a Monte Carlo Simulation to predict uncertainty for soil moisture.",  # noqa
    )
    monte_carlo_predictor: bool = Field(
        ...,
        description="Whether to use a Monte Carlo Simulation to predict uncertainty for the predictors.",  # noqa
    )
    monte_carlo_iterations: int = Field(
        ..., description="Number of iterations for the Monte Carlo Simulation."
    )
    predictor_qmc_sampling: bool
    past_prediction_as_feature: bool = Field(
        ..., description="Whether to use the past prediction as a feature."
    )
    average_measurements_over_time: bool = Field(
        ..., description="Whether to average the measurements over time."
    )
    what_to_plot: WhatToPlot = Field(
        ..., description="List of which plotting functions should be used."
    )  # noqa
    save_results: bool = Field(..., description="Dump random as numpy arrays.")
