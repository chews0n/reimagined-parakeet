from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import _pickle as cPickle
import numpy as np
import matplotlib.pyplot as plt
from catboost import CatBoostRegressor, Pool


class MLModel:

	def __init__(self, Xvals, Yvals, feature_names, testsize=0.20, randomstate=452):
		self.feature_list = Xvals
		self.target_list = Yvals
		self.feature_names = feature_names

		# instantiate model
		self.model = RandomForestRegressor(max_depth=15, min_samples_split=10, n_estimators=1000, oob_score=True,
										   random_state=randomstate, warm_start=True)
		self.scaler = StandardScaler()

		# split test/train
		dfX_train, dfX_test, dfy_train, dfy_test = train_test_split(self.feature_list, self.target_list,
																				test_size=testsize,
																				random_state=randomstate)

		self.X_train = self.scaler.fit_transform(dfX_train)
		self.X_test = self.scaler.transform(dfX_test)

		# kluge, not sure why nan values are showing up after scaling
		self.X_train[np.isnan(self.X_train)] = 0.0
		self.X_test[np.isnan(self.X_test)] = 0.0

		self.y_test = np.ravel(dfy_test.to_numpy())
		self.y_train = np.ravel(dfy_train.to_numpy())

		# train the model
		self.model.fit(self.X_train, self.y_train)

		# check the r2 scored
		self.r2_score_test = self.model.score(self.X_test, self.y_test)
		self.r2_score_train = self.model.score(self.X_train, self.y_train)

		# get feature importance
		self.feature_importance = self.model.feature_importances_

	def cross_validation(self, randomstate=452):

		# Define a range of hyperparameter values to search through
		n_estimators_values = [1200, 1400, 1600]
		depth_values = [10, 8, 6]
		min_impurity_decrease_values = [0.30, 0.35, 0.45]

		max_features_values = [3, 2, 1]
		min_samples_split_values = [4, 6, 8]

		best_score = 0  # Initialize the best score
		best_params = {}  # Initialize the best hyperparameters

		# Define cross-validation settings
		cv = KFold(n_splits=5, shuffle=True, random_state=42)

		# Initialize a list to store tuning progress
		tuning_progress = []

		# Perform hyperparameter tuning with cross-validation
		for max_features in max_features_values:
			for min_samples_split in min_samples_split_values:
				for n_estimators in n_estimators_values:
					for depth in depth_values:
						for min_impurity_decrease in min_impurity_decrease_values:
							# build model
							model = RandomForestRegressor(min_impurity_decrease=min_impurity_decrease, max_features=max_features, max_depth=depth, min_samples_split=min_samples_split, n_estimators=n_estimators, oob_score=True, random_state=randomstate, warm_start=False)

							# Perform cross-validation and get the mean r2 score
							r2_scores = []
							for train_index, val_index in cv.split(self.X_train):
								X_train, X_val = self.X_train[train_index], self.X_train[val_index]
								y_train, y_val = self.y_train[train_index], self.y_train[val_index]

								model.fit(X_train, y_train)

								r2 = model.score(X_val, y_val)
								r2_scores.append(r2)

							mean_r2 = sum(r2_scores) / len(r2_scores)

							# Update the best hyperparameters if a better score is found
							if mean_r2 > best_score:
								best_score = mean_r2
								best_params = {
									'n_estimators': n_estimators,
									'depth': depth,
									'min_impurity_decrease': min_impurity_decrease,
									'max_features': max_features,
									'min_samples_split': min_samples_split
								}

							# Append the progress to the list
							tuning_progress.append({
								'n_estimators': n_estimators,
								'Depth': depth,
								'min_impurity_decrease': min_impurity_decrease,
								'max_features': max_features,
								'min_samples_split': min_samples_split,
								'R2 Score': mean_r2
							})

		print(f'{best_params}')
		print(f'{best_score}')

		self.model = RandomForestRegressor(min_impurity_decrease=best_params['min_impurity_decrease'], max_features=best_params['max_features'],
									  max_depth=best_params['depth'], min_samples_split=best_params['min_samples_split'], n_estimators=best_params['n_estimators'],
									  oob_score=True, random_state=randomstate, warm_start=False)

		self.model.fit(self.X_train, self.y_train)

		# check the r2 scored
		self.r2_score_test = self.model.score(self.X_test, self.y_test)
		self.r2_score_train = self.model.score(self.X_train, self.y_train)

		print(f'r2 training: {self.r2_score_train}')
		print(f'r2 test: {self.r2_score_test}')





	def get_model_predictions(self, X_list):
		yvals = self.model.predict(self.scaler.transform(X_list))

		return yvals

	def plot_feature_importance(self):
		# sort features according to importance
		sorted_idx = np.argsort(self.feature_importance)
		pos = np.arange(sorted_idx.shape[0])

		# plot feature importances
		plt.barh(pos, self.feature_importance[sorted_idx], align="center")

		plt.yticks(pos, np.array(self.feature_names)[sorted_idx])
		plt.title("Feature Importance (MDI)")

		plt.savefig("feature_importance.jpg")
		plt.show()
		plt.close()

