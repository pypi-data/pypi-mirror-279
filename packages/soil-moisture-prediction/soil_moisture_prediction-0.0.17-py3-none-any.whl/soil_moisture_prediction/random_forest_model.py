"""Module for the main class for the module."""

import logging
import os
import random

import numpy as np
from scipy.stats import halfnorm, norm, qmc
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

from soil_moisture_prediction.areaGeometry import RectGeom
from soil_moisture_prediction.inputData import InputData
from soil_moisture_prediction.plot_functions import plot_selection

# TODO define private and public attribues and methods

logger = logging.getLogger(__name__)

RANDOM_SEED = 46
random.seed(RANDOM_SEED)


class RFoModel(object):
    """Class to store the output of the Random Forest regression.

    Support deterministic and probabilistic (Monte Carlo) predictions
    """

    random_forest_models = []
    n_trees = 40
    tree_depth = 8
    RF_prediction = np.empty(())
    predictor_importance = np.empty(())
    past_prediction_as_feature = False
    average_measurements_over_time = False
    rain_time_serie = ""
    monte_carlo_soil_moisture = False
    monte_carlo_predictor = False
    MC_mean = np.empty(())
    p5 = np.empty(())
    p25 = np.empty(())
    p75 = np.empty(())
    p95 = np.empty(())
    dispersion_coefficient = np.empty(())

    def __init__(
        self,
        *,
        input_parameters,
        work_dir,
        load_results=False,
    ):
        """Construct."""
        logger.info("Load model")
        self.work_dir = work_dir

        self.rect_geom = RectGeom(input_parameters.geometry)

        self.input_data = InputData(
            input_parameters,
            self.rect_geom,
            self.work_dir,
        )

        self.monte_carlo_soil_moisture = input_parameters.monte_carlo_soil_moisture
        self.monte_carlo_predictor = input_parameters.monte_carlo_predictor
        self.predictor_qmc_sampling = input_parameters.predictor_qmc_sampling
        # TODO add to pydantic
        if not self.monte_carlo_predictor and self.predictor_qmc_sampling:
            logging.warning(
                "Quasi-Monte Carlo sampling is only available for Monte Carlo predictor"
            )

        if self.monte_carlo_soil_moisture or self.monte_carlo_predictor:
            self.monte_carlo_iterations = input_parameters.monte_carlo_iterations
        else:
            self.monte_carlo_iterations = 1

        self.past_prediction_as_feature = input_parameters.past_prediction_as_feature
        self.average_measurements_over_time = (
            input_parameters.average_measurements_over_time
        )

        if (
            self.past_prediction_as_feature or self.average_measurements_over_time
        ) and self.input_data.rain_time_serie != "":
            self.reset_when_rain_occurs = True
        else:
            self.reset_when_rain_occurs = False

        self.what_to_plot = input_parameters.what_to_plot.model_dump()
        self.save_results = input_parameters.save_results

        if load_results:
            self.load_predictions()
        else:
            self.initiate_result_arrays()

    def initiate_result_arrays(self):
        """Initiate the arrays to store the results."""
        logger.info("Initiating result arrays...")
        self.RF_prediction = np.empty(
            (
                self.monte_carlo_iterations,
                len(self.input_data.soil_moisture_data.start_times),
                self.rect_geom.dim_x,
                self.rect_geom.dim_y,
            )
        )
        if self.monte_carlo_soil_moisture or self.monte_carlo_predictor:
            shape = (
                len(self.input_data.soil_moisture_data.start_times),
                self.rect_geom.dim_x,
                self.rect_geom.dim_y,
            )
            (
                self.MC_mean,
                self.p5,
                self.p25,
                self.p75,
                self.p95,
                self.dispersion_coefficient,
            ) = [np.empty(shape) for _ in range(6)]
        self.predictor_importance = np.zeros(
            (
                self.monte_carlo_iterations,
                len(self.input_data.soil_moisture_data.start_times),
                self.input_data.number_predictors,
            )
        )

    def compute(self, filter_measurements=False):
        """Build model and make predictions."""
        if self.average_measurements_over_time:
            number_timesteps_for_average = 3
            self.average_measurements(number_timesteps_for_average)

        for time_step, start_time in enumerate(
            self.input_data.soil_moisture_data.start_times
        ):
            self.random_forest_models = []
            if time_step > 0 and self.past_prediction_as_feature:
                self.add_prediction_to_feature(time_step)
            if filter_measurements:
                self.input_data.soil_moisture_filering(start_time)
            self.train_random_forest_models(start_time)
            self.apply_random_forest_models(time_step)
            if self.monte_carlo_soil_moisture or self.monte_carlo_predictor:
                self.compute_mc_stats(start_time, time_step)

        if self.save_results:
            self.save_predictions()

    def average_measurements(self, number_timesteps_for_average):
        """Average soil moisture measurements over the previous days."""
        if (
            len(self.input_data.soil_moisture_data.start_times)
            < number_timesteps_for_average
        ):
            logging.warning(
                "Will not apply average over time intervals. Not enough intervals!"
            )
            return
        soil_moisture_averaged = self.input_data.soil_moisture_data.soil_moisture
        for time_step, start_time in enumerate(
            self.input_data.soil_moisture_data.start_times
        ):
            if time_step > number_timesteps_for_average:
                number_timesteps_rainfall_reset = number_timesteps_for_average
                rain_occurs = False
                if self.reset_when_rain_occurs:
                    rain_occurs = self.input_data.check_rainfall_occurences(
                        number_timesteps_rainfall_reset,
                        time_step,
                        self.rain_time_serie,
                    )
                if not rain_occurs:
                    for past_time_step in range(1, number_timesteps_for_average + 1):
                        past_start_time = (
                            self.input_data.soil_moisture_data.start_times[
                                time_step - past_time_step
                            ]
                        )
                        soil_moisture_averaged[
                            start_time
                        ] += self.input_data.soil_moisture_data.soil_moisture[
                            past_start_time
                        ]
                    soil_moisture_averaged[start_time] /= (
                        number_timesteps_for_average + 1
                    )
        self.input_data.soil_moisture_data.soil_moisture = soil_moisture_averaged

    def add_prediction_to_feature(self, time_step):
        """Add the previous day's prediction to the features."""
        rain_occurs = False
        number_timesteps_rainfall_reset = 1
        if self.reset_when_rain_occurs:
            rain_occurs = self.input_data.check_rainfall_occurences(
                number_timesteps_rainfall_reset,
                time_step,
                self.rain_time_serie,
            )
        if not rain_occurs:
            self.input_data.predictors["past_prediction"] = (
                self.RF_prediction[0, time_step - 1, :, :],
                "g/g",
            )
        else:
            self.input_data.predictors["past_prediction"] = (
                np.zeros((self.rect_geom.dim_x, self.rect_geom.dim_y)),
                "g/g",
            )
        start_time = self.input_data.soil_moisture_data.start_times[time_step]
        self.input_data.set_training_predictors(start_time)

    def train_random_forest_models(self, start_time):
        """Train the random forest models.

        Iterates over measurements and iterations for Monte Carlo sampling.
        Trains random forest models for each iteration.

        Parameters:
        - start_time (str): Start time for training.
        """
        logger.info(f"[{start_time}] Training Random Forest models...")

        number_measurements = self.input_data.soil_moisture_data.number_measurements[
            start_time
        ]
        for iteration in range(self.monte_carlo_iterations):
            print("iteration", iteration)
            soil_moisture_labels = self.input_data.soil_moisture_data.soil_moisture[
                start_time
            ]

            if self.monte_carlo_soil_moisture:
                print("Monte Carlo soil moisture")
                for measurement in range(number_measurements):
                    soil_moisture_labels[measurement] = (
                        self.compute_uncertain_soil_moisture(
                            measurement, iteration, start_time
                        )
                    )

            print(f"soil_moisture_labels: {soil_moisture_labels}")
            if self.monte_carlo_predictor:
                print("Monte Carlo predictor")
                predictor_features = self.compute_uncertain_predictor(
                    start_time, rdm_seed=iteration, quase_mc=self.predictor_qmc_sampling
                )
            else:
                predictor_features = self.input_data.training_pred[start_time]
            print(f"predictor_features: {predictor_features}")
            self.random_forest_models.append(
                self.train_random_forest(
                    predictor_features,
                    soil_moisture_labels,
                    start_time,
                )
            )

    def compute_uncertain_soil_moisture(self, measurement, iteration, start_time):
        """
        Compute the uncertain soil moisture for the Monte Carlo simulation.

        Parameters:
        - measurement (int): Index of the soil moisture measurement.
        - iteration (int): Index of the Monte Carlo iteration.
        - start_time (str): Start time of the soil moisture data.

        Returns:
        - float: Uncertain soil moisture value.
        """
        soil_moisture = self.input_data.soil_moisture_data.soil_moisture[start_time][
            measurement
        ]
        soil_moisture_dev_low = (
            self.input_data.soil_moisture_data.soil_moisture_dev_low[start_time][
                measurement
            ]
        )
        soil_moisture_dev_high = (
            self.input_data.soil_moisture_data.soil_moisture_dev_high[start_time][
                measurement
            ]
        )
        lower_uncertainty = 2 * soil_moisture - float(
            halfnorm.rvs(
                soil_moisture,
                soil_moisture_dev_low,
                1,
                random_state=measurement * 100 + iteration,
            )
        )
        upper_uncertainty = float(
            halfnorm.rvs(
                soil_moisture,
                soil_moisture_dev_high,
                1,
                random_state=measurement * 100 + iteration,
            )
        )

        # TODO This random variable is not effected by the seed. So it is not
        # deterministic.
        random_binary = random.randint(0, 1)
        soil_moisture_uncertain = (
            random_binary * lower_uncertainty + (1 - random_binary) * upper_uncertainty
        )
        return soil_moisture_uncertain

    def compute_uncertain_predictor(self, start_time, rdm_seed, quase_mc=False):
        """Compute uncertain predictors at measurement locations.

        Returns np array with values of noisy predictors at measurement locations.

        Parameters:
        - start_time (str): Start time for computation.
        - rdm_seed (int): Random seed for reproducibility.
        - quase_mc (bool, optional): Whether to use Quasi-Monte Carlo sampling.
                Defaults to False.

        Returns:
            numpy.ndarray: Noisy predictor data at measurement locations.
        """
        self.noisy_predictors = self.input_data.predictors.copy()
        if quase_mc:
            self.sample_MultivariateNormalQMC(rdm_seed)
        else:
            for pred_name, pred_values in self.input_data.predictors.items():
                if pred_name in self.input_data.predictor_deviations:
                    noisy_predictor = self.sample_from_distribution(
                        pred_values[0], pred_name, rdm_seed
                    )
                    self.noisy_predictors[pred_name] = (noisy_predictor, pred_values[1])

        if "elevation" in self.input_data.predictors.keys():
            (
                self.noisy_predictors["slope"],
                self.noisy_predictors["aspect_we"],
                self.noisy_predictors["aspect_ns"],
            ) = self.input_data.compute_slope_aspect(
                self.noisy_predictors["elevation"][0]
            )

        noisy_predictor_train = np.empty(
            (
                self.input_data.soil_moisture_data.number_measurements[start_time],
                self.input_data.number_predictors,
            )
        )
        for coord_index, coord in enumerate(
            self.input_data.training_coordinates[start_time]
        ):
            noisy_predictor_train[coord_index] = [
                pred[0][coord[0], coord[1]] for pred in self.noisy_predictors.values()
            ]
        return noisy_predictor_train

    def sample_from_distribution(self, predictor, predictor_name, rdm_seed):
        """Sample from a distribution to add noise to predictor data.

        Generates noisy predictor data by sampling from a normal distribution
        with mean `predictor` and standard deviation obtained from the input data
        for the given predictor `pred_name`. The noise is added to each grid point
        defined by the geometry.

        Parameters:
        - predictor (float): Mean value of the predictor.
        - pred_name (str): Name of the predictor.
        - rdm_seed (int): Random seed for reproducibility.

        Returns:
        - numpy.ndarray: Noisy predictor data sampled from the distribution.
        """
        noisy_predictor = norm.rvs(
            predictor,
            self.input_data.predictor_deviations[predictor_name],
            size=self.rect_geom.grid_x.shape,
            random_state=rdm_seed,
        )
        return noisy_predictor

    def sample_MultivariateNormalQMC(self, rdm_seed):
        """Sample from a Multivariate Normal distribution using Quasi-Monte Carlo (QMC).

        This method generates samples from a Multivariate Normal distribution using
        Quasi-Monte Carlo (QMC) sampling technique. It constructs the covariance
        matrix based on the standard deviations of predictors and their correlations.
        The QMC sampling aims to improve the efficiency of sampling in high-dimensional
        spaces compared to traditional Monte Carlo methods.
        """
        noisy_predictor = {}
        pred_index = {}
        count = 0
        for pred_name in self.input_data.predictor_deviations.keys():
            pred_index[pred_name] = count
            count += 1
            noisy_predictor[pred_name] = np.empty(
                (self.rect_geom.dim_x, self.rect_geom.dim_y)
            )
        for x in range(self.rect_geom.dim_x):
            for y in range(self.rect_geom.dim_y):
                mean = []
                covariance = []
                for pred_name, pred_values in self.noisy_predictors.items():
                    if pred_name in self.input_data.predictor_deviations:
                        mean.append(pred_values[0][x][y])
                        covariance.append(
                            self.input_data.predictor_deviations[pred_name][x][y] ** 2
                        )
                covariance = np.diag(covariance)
                seed = rdm_seed * 1000000 + x * 1000 + y
                distribution = qmc.MultivariateNormalQMC(
                    mean=mean, cov=covariance, seed=seed
                )
                random_sample = distribution.random(1)
                for pred_name in self.input_data.predictor_deviations.keys():
                    noisy_predictor[pred_name][x, y] = random_sample[
                        0, pred_index[pred_name]
                    ]
        for pred_name, pred_values in self.input_data.predictors.items():
            if pred_name in self.input_data.predictor_deviations:
                self.noisy_predictors[pred_name] = (
                    noisy_predictor[pred_name],
                    pred_values[1],
                )

    def train_random_forest(self, features, labels, start_time):
        """Build and train a random forest regressor.

        Parameters:
        - features : array-like, shape = [n_samples, n_features]
            Training input samples.
        - labels : array-like, shape = [n_samples]
            Target values (Real soil moisture).
        - start_time : str
            Start time of the soil moisture data.

        Returns:
        - RandomForestRegressor: Trained random forest regressor.
        """
        # TODO random_state hard coded
        print("features", features)
        print("labels", labels)

        train_features, test_features, train_labels, test_labels = train_test_split(
            features, labels, test_size=0.3, random_state=40
        )
        train_labels = np.ravel(train_labels)
        test_labels = np.ravel(test_labels)

        random_forest = RandomForestRegressor(
            n_estimators=self.n_trees,
            max_depth=self.tree_depth,
            random_state=RANDOM_SEED,
        )
        random_forest.fit(train_features, train_labels)

        predictions = random_forest.predict(test_features)
        r2 = r2_score(test_labels, predictions)
        logger.info(f"[{start_time}] Random Forest R2: {round(r2, 3)}")
        rf_res = predictions - test_labels
        errors = abs(rf_res) ** 2
        mean_absolute_error = round(np.mean(errors), 6)
        logger.info(
            f"[{start_time}] Random Forest Mean Absolute Error: {mean_absolute_error} "
            f"with prediction mean value: {round(np.mean(predictions), 2)}"
        )

        return random_forest

    def apply_random_forest_models(self, time_step):
        """Apply the random forest on the full area and compute feature importance."""
        logger.info(
            f"[{self.input_data.soil_moisture_data.start_times[time_step]}] "
            "Applying Random Forest model(s)..."
        )

        for monte_carlo_iteration in range(self.monte_carlo_iterations):
            for line in range(self.rect_geom.dim_x):
                predictors = np.array(
                    [
                        predictor[0][line, :]
                        for predictor in self.input_data.predictors.values()
                    ]
                ).T
                if self.input_data.apply_pca:
                    predictors = self.input_data.pca.transform(predictors)
                self.RF_prediction[monte_carlo_iteration, time_step, line, :] = (
                    self.random_forest_models[monte_carlo_iteration].predict(predictors)
                )

            if self.input_data.has_mask:
                self.RF_prediction[
                    monte_carlo_iteration, time_step, :, :
                ] *= self.input_data.mask

            self.predictor_importance[monte_carlo_iteration, time_step] = (
                self.random_forest_models[monte_carlo_iteration].feature_importances_
            )

    def compute_mc_stats(self, start_time, time_step):
        """Compute mean and percentiles of the prediction for a given day.

        The function computes the 5th, 25th, 75th and 95th percentiles.
        """
        logger.info(f"[{start_time}] Computing Monte Carlo statistics.")

        self.MC_mean[time_step, :, :] = np.mean(
            self.RF_prediction[:, time_step, :, :], axis=0
        )
        (
            self.p5[time_step, :, :],
            self.p25[time_step, :, :],
            self.p75[time_step, :, :],
            self.p95[time_step, :, :],
        ) = [
            np.percentile(self.RF_prediction[:, time_step, :, :], q=perc, axis=0)
            for perc in [5, 25, 75, 95]
        ]
        self.dispersion_coefficient[time_step, :, :] = (
            self.p75[time_step, :, :] - self.p25[time_step, :, :]
        ) / (self.p75[time_step, :, :] + self.p25[time_step, :, :])

    def load_predictions(self):
        """
        Load prediction results and RF feature importance from files.

        If Monte Carlo is switched on, the mean and coefficient of dispersion
        are also loaded.
        """
        logger.info("Loading prediction results from files...")
        self.RF_prediction = np.load(os.path.join(self.work_dir, "RF_predictions.npy"))
        self.predictor_importance = np.load(
            os.path.join(self.work_dir, "RF_feat_importance.npy")
        )
        if self.monte_carlo_soil_moisture or self.monte_carlo_predictor:
            self.MC_mean = np.load(os.path.join(self.work_dir, "MC_mean.npy"))
            self.dispersion_coefficient = np.load(
                os.path.join(self.work_dir, "MC_coefficient_dispersion.npy")
            )

    def save_predictions(self):
        """
        Save the prediction results and RF feature importance to files.

        If Monte Carlo is switched on, the mean and coefficient of dispersion
        are also saved.
        """
        logger.info("Saving predictions to files...")
        np.save(os.path.join(self.work_dir, "RF_predictions"), self.RF_prediction)
        np.save(
            os.path.join(self.work_dir, "RF_feat_importance"),
            self.predictor_importance,
        )
        if self.monte_carlo_soil_moisture or self.monte_carlo_predictor:
            np.save(os.path.join(self.work_dir, "MC_mean"), self.MC_mean)
            np.save(
                os.path.join(self.work_dir, "MC_coefficient_dispersion"),
                self.dispersion_coefficient,
            )

    def plot_figure_selection(self):
        """Plot the selected figures."""
        logger.info("Computing selected figures to plot...")
        plot_selection(self)
