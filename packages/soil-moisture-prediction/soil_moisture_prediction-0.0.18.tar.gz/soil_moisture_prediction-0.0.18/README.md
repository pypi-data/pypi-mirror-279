# SOIL MOISTURE PREDICTION

## Description
This script performs soil moisture prediction using a Random Forest model based on soil properties. Additionally, it allows for incorporating soil moisture uncertainty in the input file and performs a probabilistic prediction using a Monte Carlo approach.

## Input Data
All input data must be given in the same coordinates system.
### Geometry
4 corner points and resolution. The program will compute the dense mesh-grid defined by the given corner points and resolution.

### Soil moisture file 
format: x y date soil\_moisture\_value lower\_error upper\_error  
`lower\_error` and `upper\_error` are optional and must be given as standard deviation values.  
If several days are provided, each day will be processed independently. Several options are available (see Algorithms section) to enforce some continuity between consecutive days. 

### Predictors 
One file per predictor, format: x y value  
The predictors will be regridded on the grid given in "geometry" (linear interpolation).
If "elevation" is given as predictor, slope and aspect are computed as additional predictors.  
The predictors are statics and cannot change in time.

## Algorithm
The algorithm trains a random forest regressor (RandomForestRegressor from scikit-learn) with the soil moisture data and the predictor values at the measurements locations.
The trained model is then applied on the whole densely gridded area. 
The output is the a numpy array with the soil moisture values at each grid node. 

Several option are available:  
*Monte Carlo*: if soil moisture values are provided with quantified uncertainty (standard deviations), 
the prediction can be included in a Monte Carlo scheme to propagate the soil moisture uncertainty and 
output a probabilistic prediction. At each Monte Carlo run, each soil moisture measurements is replaced by a randomly drawned sample from the distribution defined by the standard deviations. From all the prediction runs, the coefficient of dispersion is computed and
provided on addition to the mean prediction.  
*past\_prediction\_as\_feature*: in case of several days are provided, this option uses the prediction from the day before 
as a predictor for the prediction of the current day. This allows to stabilize the results over time.  
*average\_measurements\_over\_time*: in case of several days are provided, each day measurement dataset is replaced by the average of itself with
the 3 previous day measurements. This allows to stabilize the results over time.  
For both these options, there is the possibility not to use the previous days when it rains. 

## Visualization
In addition to the resulting array(s) (prediction only or prediction and coefficient of dispersion),
the programm offers to plot some results.  
*predictors*: plot all the predictors as color maps after re-gridding them to the project grid.  
*pred\_correlation*: compute and plot the correlation between each predictors and display them as a heatmap. The color intensity indicates the strength and direction of correlation,
ranging from -1 (strong negative correlation) to 1 (strong positive correlation). It can help to remove redundant predictors highly correlated between them.  
*day\_measurements*: plot soil moisture measurements as a scatter plot on an x-y mapfor each day. The measurements are colored according to their corresponding soil moisture values.
If Monte Carlo simulations are enabled, error bands representing the standard deviations are overlaid on the scatter plot.  
*day\_predictor\_importance*: plot histogram of the normalized predictor importances from the random forest model for each day.  
If Monte Carlo simulations are enabled, the plot shows the 5th, 50th (median), and 95th quantiles of the importance values.
*day\_prediction\_map*: plot the map of the densely modelled soil moisture on the project area. If uncertainty are provided
the coefficient of dispersion map is also provided.  
*alldays\_predictor\_importance*: if several days are provided, the predictor importance is computed for each day 
and a curve of the predictor importance along days is plotted for each predictor. The x-axis represents the days, and the y-axis represents the importance values.