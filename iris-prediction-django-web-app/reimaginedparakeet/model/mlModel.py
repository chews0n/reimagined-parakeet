from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import _pickle as cPickle
import numpy as np
import matplotlib.pyplot as plt


class MLModel:

	def __init__(self, Xvals, Yvals, feature_names, testsize=0.30, randomstate=452):
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
		self.r2_score = self.model.score(self.X_test, self.y_test)

		# get feature importance
		self.feature_importance = self.model.feature_importances_

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

