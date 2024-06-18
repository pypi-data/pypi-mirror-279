"""Load and process input data."""

import csv
import json
import logging
import math
import os
from collections import OrderedDict
from typing import Dict, List, Set

import numpy as np
from scipy import ndimage
from scipy.interpolate import griddata
from sklearn.decomposition import PCA

from soil_moisture_prediction.areaGeometry import RectGeom

logger = logging.getLogger(__name__)


class FileValidationError(Exception):
    """Exception raised when a file validation fails."""

    pass


class SoilMoistureData:
    """Class containing soil moisture measurements."""

    x: OrderedDict[str, np.ndarray]
    y: OrderedDict[str, np.ndarray]
    soil_moisture: OrderedDict[str, np.ndarray]
    number_measurements: OrderedDict[str, int]
    soil_moisture_dev_low: OrderedDict[str, np.ndarray]
    soil_moisture_dev_high: OrderedDict[str, np.ndarray]
    start_times: List[str]
    geom: RectGeom
    uncertainty: bool

    def __init__(self, soil_moisture_file, geom, uncertainty):
        """
        Initialize the SoilMoistureData object.

        Parameters:
        - soil_moisture_file (str): Path to the soil moisture file.
        - geom (RectGeom): RectGeom object defining the geometry.
        - uncertainty (bool): Whether uncertainty data is present.

        This method opens the soil moisture file and saves the data to NumPy arrays.
        """
        logger.info("Loading soil moisture data...")
        self.x = OrderedDict()
        self.y = OrderedDict()
        self.soil_moisture = OrderedDict()
        self.soil_moisture_dev_low = OrderedDict()
        self.soil_moisture_dev_high = OrderedDict()
        self.number_measurements = OrderedDict()
        self.geom = geom
        self.uncertainty = uncertainty

        self._parse_soil_moisture_file(soil_moisture_file)

    def _parse_soil_moisture_file(self, soil_moisture_file, sm_filtering=False):
        """
        Open the soil moisture file and save data to NumPy arrays.

        Parameters:
        - soil_moisture_file (str): Path to the soil moisture file.
        - sm_filtering (bool): whether apply a median filter on soil moisture data

        This method reads the soil moisture file line by line, parses the data,
        and updates the appropriate attributes accordingly.
        """
        parser = SoilMoistureParser(self.geom, self.uncertainty)
        with open(soil_moisture_file, "r") as soil_moisture_file:
            for row in parser.parse(soil_moisture_file):
                x, y, start_time, soil_moisture, err_low, err_high = row

                if self.uncertainty and err_low is None:
                    raise FileValidationError(
                        f"Uncertainty data is missing in file {soil_moisture_file}"
                    )

                if start_time not in self.number_measurements:
                    self._initiate_time(start_time)
                self.x[start_time].append(x)
                self.y[start_time].append(y)
                self.soil_moisture[start_time].append(soil_moisture)
                self.soil_moisture_dev_low[start_time].append(err_low)
                self.soil_moisture_dev_high[start_time].append(err_high)
                self.number_measurements[start_time] += 1

        self.start_times = list(self.number_measurements.keys())

        for start_time in self.start_times:
            self.x[start_time] = np.array(self.x[start_time])
            self.y[start_time] = np.array(self.y[start_time])
            self.soil_moisture[start_time] = np.array(self.soil_moisture[start_time])
            if self.uncertainty:
                self.soil_moisture_dev_low[start_time] = np.array(
                    self.soil_moisture_dev_low[start_time]
                )
                self.soil_moisture_dev_high[start_time] = np.array(
                    self.soil_moisture_dev_high[start_time]
                )

            if sm_filtering:
                self._soil_moisture_filtering(start_time)

    def _initiate_time(self, start_time):
        """
        Initialize lists to store soil moisture data for the given start time.

        Parameters:
        - start_time (str): Start time of the measurements.
        - uncertainty (bool): Whether uncertainty data is present.

        This method initializes empty lists to store soil moisture data for the
        specified start time.
        """
        self.number_measurements[start_time] = 0
        self.x[start_time] = []
        self.y[start_time] = []
        self.soil_moisture[start_time] = []
        self.soil_moisture_dev_low[start_time] = []
        self.soil_moisture_dev_high[start_time] = []

    def soil_moisture_filtering(self, start_time):
        """
        Apply median filter to the soil moisture measurements.

        Parameters:
        - start_time (str): Start time of the measurements.

        This method applies a median filter to the soil moisture measurements for
        the specified start time. It separates branches of measurements based on
        distance, applies the filter to each branch, and concatenates the
        filtered branches.
        """
        raise NotImplementedError("This method is old and must be reviewed")
        filter_size = 5
        x = self.x[start_time]
        y = self.y[start_time]
        branches = self.separate_branches(
            x / 1000, y / 1000, self.soil_moisture[start_time]
        )
        filtered_branches = [
            ndimage.median_filter(branch[:, 2], size=filter_size) for branch in branches
        ]
        self.soil_moisture[start_time] = np.concatenate(filtered_branches)

    def separate_branches(self, x, y, z, threshold_distance=1):
        """
        Identify branch transitions based on distance between consecutive points.

        Parameters:
        - x (numpy.ndarray): Array of x-coordinates.
        - y (numpy.ndarray): Array of y-coordinates.
        - z (numpy.ndarray): Array of z-coordinates (soil moisture measurements).
        - threshold_distance (float): Threshold distance for identifying branch
        transitions.

        Returns:
        - list: List of arrays representing separate branches.

        This method identifies branch transitions based on the distance between
        consecutive points (specified by threshold_distance) in the x-y plane.
        It splits the data into separate branches and returns them as a list
        of arrays.
        """
        # Threshold by time when time data input is added?
        distances = np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2)
        branch_transitions = np.where(distances > threshold_distance)[0] + 1
        branches = np.split(np.column_stack([x, y, z]), branch_transitions)
        return branches


class InputData:
    """Class containing all input data, predictors and soil moisture measurements."""

    number_predictors = 0
    predictors = {}
    predictor_deviations = {}
    training_coordinates = {}
    training_pred = {}
    _correlation_matrix = np.empty((number_predictors, number_predictors))

    def __init__(
        self,
        input_parameters,
        geom,
        work_dir,
        apply_pca=False,
        has_mask=False,
    ):
        """
        Initialize the InputData object.

        Parameters:
        - input_parameters (InputParameters): Dictionary containing input parameters.
        - geom (RectGeom): RectGeom object defining the geometry.
        - apply_pca (bool): Whether to apply Principal Component Analysis (PCA).
        - has_mask (bool): Whether a mask is present in the data.

        This method initializes the input data and opens the soil moisture file.
        """
        soil_moisture_file = [
            os.path.join(work_dir, file_name)
            for file_name, days in input_parameters.soil_moisture_data.items()
        ][0]
        self.soil_moisture_data = SoilMoistureData(
            soil_moisture_file, geom, input_parameters.monte_carlo_soil_moisture
        )

        predictors_input = {}
        for file_name, predictor_data in input_parameters.predictors.items():
            type_name = predictor_data.type if predictor_data.type != "" else file_name
            if type_name == "rain":
                # This predictor "rain" would be a single value per day (height)
                # Used to reset the option "precipitation as feature"
                # if precipitation height are not null
                self.rain_time_serie = os.path.join(self.work_dir, file_name)
            else:
                predictors_input[type_name] = (
                    os.path.join(work_dir, file_name),
                    predictor_data.unit,
                    predictor_data.std_deviation,
                )

        self.pred_files = predictors_input
        self.monte_carlo_predictor = input_parameters.monte_carlo_predictor
        # TODO maybe delete?
        self.has_mask = has_mask
        self.apply_pca = apply_pca
        self._prepare_predictors(geom, input_parameters.past_prediction_as_feature)

    def _prepare_predictors(
        self, geom, past_prediction_as_feature, compute_slope_aspect=True
    ):
        """
        Prepare predictors for modeling.

        Parameters:
        - geom (RectGeom): RectGeom object defining the geometry.
        - compute_slope_aspect (bool): Whether to compute slope and aspect from
        elevation.
        - past_prediction_as_feature (bool): Whether to include past predictions as
        predictors.

        This method interpolates predictors to the project grid, computes slope
        and aspect, and extracts predictor values at the training locations.
        """
        logger.info("Preparing predictors")
        self._fit_predictors_to_grid(geom)

        self.uniformize_nan_across_predictors(geom)

        if compute_slope_aspect and "elevation" in self.predictors.keys():
            (
                self.predictors["slope"],
                self.predictors["aspect_we"],
                self.predictors["aspect_ns"],
            ) = self.compute_slope_aspect(self.predictors["elevation"][0])
        self.number_predictors = len(self.predictors)

        if past_prediction_as_feature:
            self.number_predictors += 1
            self.predictors["past_prediction"] = (
                np.zeros((geom.dim_x, geom.dim_y)),
                "g/g",
            )

        self.prepare_training_predictors(geom)

    def _fit_predictors_to_grid(self, geom):
        """
        Open predictor files and interpolate them to the project grid.

        Parameters:
        - geom (RectGeom): RectGeom object defining the geometry.

        This method reads predictor files, interpolates them to the project grid,
        and stores the interpolated arrays in the predictors dictionary.
        """
        logger.info("Loading predictors and interpolating them to project grid.")
        for name, information in self.pred_files.items():
            file_path, unit, read_std_deviation = information
            x, y, value, std_deviation = self.open_predictor_file(
                file_path, geom, read_std_deviation
            )
            values_on_nodes = griddata(
                (x, y), value, (geom.grid_x, geom.grid_y), method="linear"
            )

            self.predictors[name] = (values_on_nodes, unit)
            if self.monte_carlo_predictor and read_std_deviation:
                # method="nearest" to avoid nan not handled by norm.rvs
                # TODO find a better interpolation without nan?
                deviation_on_nodes = griddata(
                    (x, y),
                    std_deviation,
                    (geom.grid_x, geom.grid_y),
                    method="nearest",
                )
                self.predictor_deviations[name] = deviation_on_nodes

    def open_predictor_file(self, file_path, geom, read_std_deviation=False):
        """Open a predictor file and store information in a list.

        Parameters:
        - file_path (str): The path to the predictor file.
        - geom (RectGeom): The geometry object defining the area of interest.
        - read_std_deviation (bool): Whether to read the standard deviation.

        Returns:
        - Three lists: x-coordinates, y-coordinates, predictor values and standard
          deviation. If read_std_deviation is False, the standard deviation list is
          empty.

        This function reads data from a predictor file located at `file_path` and
        extracts x, y coordinates, and predictor values from each row. It filters
        the data based on whether each pixel falls within the area defined by `geom`,
        with a defined buffer width.
        """
        x = []
        y = []
        value = []
        std_deviation = []
        with open(file_path, "r") as file:
            for row in file:
                line = row.split(",")
                # TODO should be gloabal
                # TODO better idea to buffer
                buffer_width = 10
                if self.is_pixel_within_area(line, buffer_width, geom):
                    x.append(float(line[0]))
                    y.append(float(line[1]))
                    value.append(float(line[2]))
                    if read_std_deviation:
                        std_deviation.append(float(line[3]))

        return x, y, value, std_deviation

    def is_pixel_within_area(self, line, buffer_width, geom):
        """
        Check if the given predictor pixel is within the study area.

        Parameters:
        - line (list): List containing the x-coordinate, y-coordinate, and value
        of the predictor pixel.
        - buffer_width (float): Buffer width for extending the study area.
        - geom (RectGeom): RectGeom object defining the geometry of the study area.

        Returns:
        - bool: True if the pixel is within the study area, False otherwise.

        This method checks whether the given predictor pixel, represented by its
        coordinates (x, y) and value, falls within the study area defined by the
        geometry object geom, considering a buffer zone specified by buffer_width.

        It returns True if the pixel is within the study area and its value is
        greater than 0, otherwise it returns False.
        """
        pixel_inside = False
        if (
            geom.xi - buffer_width * geom.resolution
            <= float(line[0])
            <= geom.xf + buffer_width * geom.resolution
            and geom.yi - buffer_width * geom.resolution
            <= float(line[1])
            <= geom.yf + buffer_width * geom.resolution
            and float(line[2]) > 0
        ):
            pixel_inside = True
        return pixel_inside

    # Check how to deal with None
    def uniformize_nan_across_predictors(self, geom):
        """
        Replace NaN values in predictors with NaN for all predictors.

        Parameters:
        - geom (RectGeom): RectGeom object defining the geometry.

        This method replaces NaN values in predictors with NaN for all predictors
        to ensure consistency across the data.
        """
        nan_indexes = np.full((geom.dim_x, geom.dim_y), False)
        for pred_values in self.predictors.values():
            nan_indexes[np.isnan(pred_values[0])] = True
        for pred_name in self.predictors.keys():
            self.predictors[pred_name][0][nan_indexes] = np.nan

    def compute_slope_aspect(self, elevation, compute_aspect=True):
        """
        Compute slope and aspect from elevation data.

        Parameters:
        - elevation (numpy.ndarray): elevation dataset
        - compute_aspect (bool): Whether to compute aspect.

        Returns:
        - Three numpy.ndarray for the slope, the aspect in west-east direction and
        aspect in north-south direction.
        """
        logger.info("Computing slope and aspects from elevation dataset...")
        elev_dx, elev_dy = np.gradient(elevation)
        slope = (
            np.sqrt(elev_dx * elev_dx + elev_dy * elev_dy),
            "m/m",
        )
        if compute_aspect:
            aspect = np.arctan2(-elev_dx, elev_dy)
            aspect_we = (90 - 90 * np.sin(aspect), "degree")
            aspect_ns = (90 - 90 * np.cos(aspect), "degree")
        return (slope, aspect_we, aspect_ns)

    def compute_correlation_matrix(self):
        """
        Compute the correlation matrix between predictors.

        Returns:
        - numpy.ndarray: 2D array representing the correlation matrix.

        This method computes the correlation matrix between predictors and returns it.
        """
        # TODO : remove half computations since symmetric matrix
        if self._correlation_matrix.size != 0:
            return self._correlation_matrix
        logger.info("Computing correlation between predictors...")
        self._correlation_matrix = np.zeros(
            (self.number_predictors, self.number_predictors)
        )
        i = 0
        for pred1 in self.predictors.values():
            j = 0
            for pred2 in self.predictors.values():
                self._correlation_matrix[i, j] = self._compute_pred_correlation(
                    pred1[0], pred2[0]
                )
                j += 1
            i += 1
        return self._correlation_matrix

    def _compute_pred_correlation(self, arr1, arr2):
        """
        Compute the correlation coefficient between two 2D arrays.

        Parameters:
        - arr1 (numpy.ndarray): First 2D array.
        - arr2 (numpy.ndarray): Second 2D array.

        Returns:
        - float: Correlation coefficient.

        This method computes the correlation coefficient between two 2D arrays.
        """
        arr1_nonan = np.ma.array(arr1, mask=np.isnan(arr1))
        arr2_nonan = np.ma.array(arr2, mask=np.isnan(arr2))

        arr1_mean = np.sum(arr1_nonan) / np.size(arr1_nonan)
        arr2_mean = np.sum(arr2_nonan) / np.size(arr2_nonan)

        arr1_norm = arr1_nonan - arr1_mean
        arr2_norm = arr2_nonan - arr2_mean

        correlation_coeff = (arr1_norm * arr2_norm).sum() / math.sqrt(
            (arr1_norm * arr1_norm).sum() * (arr2_norm * arr2_norm).sum()
        )
        return correlation_coeff

    def prepare_training_predictors(self, geom):
        """
        Extract predictor values at training locations.

        Parameters:
        - geom (RectGeom): RectGeom object defining the geometry.

        This method extracts predictor values at training locations and saves
        them in an array.
        """
        for start_time in self.soil_moisture_data.start_times:
            self.training_coordinates[start_time] = np.zeros(
                ((self.soil_moisture_data.number_measurements[start_time]), 2),
                dtype=int,
            )
            self.training_coordinates[start_time] = geom.find_nearest_node(
                self.soil_moisture_data.x[start_time],
                self.soil_moisture_data.y[start_time],
            )
            self.set_training_predictors(start_time)

    def set_training_predictors(self, start_time):
        """
        Set the training predictors for the given start_time.

        Parameters:
        - start_time (str): Start time of the measurements.
        """
        self.training_pred[start_time] = np.empty(
            (
                self.soil_moisture_data.number_measurements[start_time],
                self.number_predictors,
            )
        )
        for coord_index, coord in enumerate(self.training_coordinates[start_time]):
            self.training_pred[start_time][coord_index] = [
                pred[0][coord[0], coord[1]] for pred in self.predictors.values()
            ]

    # TODO review the whole mask stuff
    def apply_mask(self, geom, mask):
        """Open and interpolate the mask file.

        Set all predictors to NaN following the mask given in argument
        Remove training points where predictors are NaN
        """
        with open(mask, "r") as ft:
            lines = ft.readlines()
            mask_xyz = np.zeros((len(lines), 3))
            for i, j in enumerate(lines):
                line = j.split()
                if line[2] == "urban" or line[2] == "water":
                    mask_xyz[i, :] = [float(line[0]), float(line[1]), np.nan]
                else:
                    mask_xyz[i, :] = [float(line[0]), float(line[1]), 1]
        mask_grid = griddata(
            (mask_xyz[:, 0], mask_xyz[:, 1]),
            mask_xyz[:, 2],
            (geom.grid_x, geom.grid_y),
            method="linear",
        )

        self.has_mask = True
        self.mask = mask_grid

        for k, p in self.predictors.items():
            self.predictors[k] = (p[0] * self.mask, p[1])

        idx_no_nan = []
        for i, pts in enumerate(self.pts_train):
            if np.isnan(mask[pts[0], pts[1]]) is False:
                idx_no_nan.append(i)

        self.x = self.x[idx_no_nan]
        self.y = self.y[idx_no_nan]
        self.pts_train = self.pts_train[idx_no_nan]
        self.feat_train = self.feat_train[idx_no_nan]
        self.n_pts = len(idx_no_nan)

        sm_no_nan = np.empty((self.number_time_intervals, self.n_pts))
        for time_step in range(self.number_time_intervals):
            sm_no_nan[time_step] = self.soil_moisture[time_step][idx_no_nan]
        self.soil_moisture = sm_no_nan

    # TODO review whole pca stuff
    def use_pca(self, n_components):
        """Apply a principal component analysis to reduce the number of features.

        n_components: Number of components to keep
        """
        pca = PCA(n_components=n_components)
        pca_feat = pca.fit_transform(self.feat_train)
        self.feat_train = pca_feat
        self.number_predictors = n_components
        self.pca = pca
        logger.info(f"PCA explained variance ration: {pca.explained_variance_ratio_}")

    def check_no_nan_in_training(self, start_time):
        """
        Check if any predictor value is NaN at each training location.

        If any predictor value is NaN at a training location, the measurement is
        discarded.

        Parameters:
        - start_time (str): Start time of the measurements.

        Raises:
        - ValueError: If NaN is found in a measurement.

        This method iterates over each training location for the given time and
        checks if any predictor value is NaN. If NaN is found in any predictor,
        it raises a ValueError.
        """
        for coord in self.training_coordinates[start_time]:
            for pred in self.predictors.values():
                if np.isnan(pred[0][coord[0], coord[1]]):
                    raise ValueError("NAN in measurement!")

    def check_rainfall_occurences(self, n_timesteps_reset, time_step, rain_time_serie):
        """
        Check if rainfall occurred in the previous days.

        Parameters:
        - n_timesteps_reset (int): Number of time steps to check for rainfall.
        - time_step (int): Current time step.
        - rain_time_serie (str): Path to the rainfall time series data.

        Returns:
        - bool: True if rainfall occurred in the previous days, False otherwise.

        This method checks if rainfall occurred in the previous n_timesteps_reset
        days based on the rainfall time series data.
        It returns True if rainfall occurred, otherwise False.
        """
        rain_occurs = False
        for past_time_step in range(n_timesteps_reset):
            start_time = self.soil_moisture_data.start_times[time_step - past_time_step]
            start_time_rainfall = self.get_start_time_rainfall(
                start_time, rain_time_serie
            )
            if start_time_rainfall > 0:
                rain_occurs = True
                break
        return rain_occurs

    def get_start_time_rainfall(self, start_time, rain_time_serie):
        """
        Get the rainfall value for the given start time.

        Parameters:
        - start_time (str): Start time for which rainfall value is required.
        - rain_time_serie (str): Path to the rainfall time series data.

        Returns:
        - int: Rainfall value for the given start time.

        This method retrieves the rainfall value for the specified start time
        from the rainfall time series data.
        """
        with open(rain_time_serie, "r") as json_file:
            rainfall_values = json.load(json_file)
        start_time_rainfall = rainfall_values[start_time]
        return start_time_rainfall


class InputFileParser:
    """This abstract base class defines the common methods for parsing an input file."""

    comment_char = "#"

    file_information: Dict[str, str]

    def __init__(self, geom_area):
        """Set parse_geom_area so that every point added expands area."""
        self.input_geom_area = geom_area
        self.parse_geom_area = RectGeom(
            [float("inf"), -float("inf"), float("inf"), -float("inf"), 0], False
        )

    def _check_first_line(self):
        raise NotImplementedError("This method should be implemented in child class.")

    def _check_row(self):
        raise NotImplementedError("This method should be implemented in child class.")

    def _get_file_information(self):
        raise NotImplementedError("This method should be implemented in child class.")

    def _check_validty_area(self):
        raise NotImplementedError("This method should be implemented in child class.")

    def _check_coordinate(self, cell, row, row_index):
        try:
            coor = float(cell)
        except ValueError:
            raise FileValidationError(
                f"Cell ''{cell}'' is not a decimal number."
                f"Row number {row_index} '{','.join(row)}'."
            )
        return coor

    def parse(self, in_file_stream):
        """Parse, validate and yield rows of the input file.

        Rows are yielded if they contained in the RectGeom.
        Raises FileValidationError if the file is not valid.
        """
        in_file_stream.seek(0)
        # Guess the delimiter
        sniffer = csv.Sniffer()

        # Get first line with no comment char
        line = ""
        while line == "":
            try:
                line = in_file_stream.readline()
            except UnicodeDecodeError:
                raise FileValidationError("File is not a UTF-8 file.")

            line = in_file_stream.readline()
            if line[0] == self.comment_char:
                line = ""

        try:
            dialect = sniffer.sniff(line)
        except csv.Error as e:
            if str(e) == "Could not determine delimiter":
                raise FileValidationError(str(e))
        in_file_stream.seek(0)

        csv_reader = csv.reader(in_file_stream, dialect=dialect)

        first_line = next(csv_reader)

        row = self._check_first_line(first_line)
        if row:
            yield row

        for row_index, row in enumerate(csv_reader, start=2):
            row = self._check_row(row, row_index)
            if row:
                yield row

        self._check_validty_area()
        return self._get_file_information()


class PredParser(InputFileParser):
    """
    Parses an input file containing predictor data.

    This class extends InputFileParser and provides specific functionality for
    validation of predictor data. At the end, a global check is performed so
    that the predictor file must cover the input GeomArea completely, including
    a margin.

    Methods:
        parse(file_path, out_file_path):
            Parses the input file and writes valid predictor data to
            the output file.

    Attributes:
        file_information (dict):
            Information about the file contents (type, unit, std_deviation).
    """

    # A margin of 5 times the resolution is used to check if a point is inside the area.
    MARGIN_MULTI_RESOLUTION = 5

    file_information = {"type": "", "unit": ""}

    def _check_first_line(self, comments):
        if not comments[0][0] == "#":
            row = self._check_row(comments, 1)
        else:
            information = {
                info.split("=")[0]: info.split("=")[1]
                for info in comments[0][2:].split()
            }
            if information.keys() != self.file_information.keys():
                raise FileValidationError(
                    f"Unkown predictor information in comment line.<br>{comments}"
                )
            else:
                self.file_information = information
            row = None

        return row

    def _check_row_length(self, row, row_index):
        row_length = 3
        if len(row) != row_length:
            raise FileValidationError(
                f"Row number {row_index} '{','.join(row)}' has not correct number "
                f"of columns {row_length}."
            )

    def _check_predictor(self, cell, row, row_index):
        try:
            predictor = float(cell)
        except ValueError:
            raise FileValidationError(
                f"Cell '{cell}' is not a decimal number. "
                f"Row number {row_index} '{','.join(row)}'."
            )

        return predictor

    def _check_row(self, row, row_index):
        self._check_row_length(row, row_index)
        x = self._check_coordinate(row[0], row, row_index)
        y = self._check_coordinate(row[1], row, row_index)
        self._check_predictor(row[2], row, row_index)

        if self.input_geom_area.contain(
            x, y, margin_multi_resolution=self.MARGIN_MULTI_RESOLUTION
        ):
            self.parse_geom_area.expand(x, y)
            return row

    def _get_file_information(self):
        return self.file_information

    def _check_validty_area(self):
        if not self.input_geom_area.covered_by(self.parse_geom_area):
            raise FileValidationError(
                "The file does not cover the user defined area completely"
            )


class SoilMoistureParser(InputFileParser):
    """Parser for soil moisture data."""

    time_steps: Set = set()
    data_points: int = 0

    def __init__(self, geom_area: RectGeom, uncertainty: bool):
        """Set uncertainty flag."""
        super().__init__(geom_area)
        self.uncertainty = uncertainty

    def _check_first_line(self, headers):
        self._check_row_length(headers, 1)

        try:
            return self._check_row(headers, 1)
        except FileValidationError:
            return None

    def _check_row_length(self, row, row_index):
        if self.uncertainty:
            row_length = 6
        else:
            row_length = 4

        if len(row) != row_length:
            raise FileValidationError(
                f"Row number {row_index} '{','.join(row)}' has not correct number "
                f"of columns {row_length}."
            )

    def _check_soil_moisture(self, cell, row, row_index, negativ):
        min_soil_moisture = 0
        max_soil_moisture = 1

        try:
            if negativ:
                soil_moisture = abs(float(cell))
            else:
                soil_moisture = float(cell)
        except ValueError:
            raise FileValidationError(
                f"Cell '{cell}' is not a decimal number. "
                f"Row number {row_index} '{','.join(row)}'."
            )
        if soil_moisture < min_soil_moisture or soil_moisture >= max_soil_moisture:
            raise FileValidationError(
                f"Cell '{cell}' needs to be between {min_soil_moisture} and"
                f"{max_soil_moisture}. "
                f"Row number {row_index} '{','.join(row)}'."
            )

        return soil_moisture

    def _check_time_step(self, cell, row, row_index):
        return row[2]

    def _check_row(self, row, row_index):
        self._check_row_length(row, row_index)
        x = self._check_coordinate(row[0], row, row_index)
        y = self._check_coordinate(row[1], row, row_index)
        time_step = self._check_time_step(row[2], row, row_index)
        if self.uncertainty:
            soil_moisture = self._check_soil_moisture(row[3], row, row_index, False)
            err_low = self._check_soil_moisture(row[4], row, row_index, True)
            err_high = self._check_soil_moisture(row[5], row, row_index, False)
        else:
            self._check_soil_moisture(row[3], row, row_index, True)
        if self.input_geom_area.contain(x, y):
            self.parse_geom_area.expand(x, y)
            self.time_steps.add(time_step)
            self.data_points += 1
            return x, y, time_step, soil_moisture, err_low, err_high

    def _get_file_information(self):
        return list(self.time_steps)

    def _check_validty_area(self):
        if self.data_points == 0:
            raise FileValidationError(
                "No CRN measurments are in the user defined area!"
            )
