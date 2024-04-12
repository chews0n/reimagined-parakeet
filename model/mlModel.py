from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor


class MLModel:

	def __init__(self, Xvals, Yvals, testsize=0.33, randomstate=452, randomforest=True):
		self.feature_list = Xvals
		self.target_list = Yvals

		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.feature_list, self.target_list,
																				test_size=testsize,
																				random_state=randomstate)


		self.scaler = StandardScaler()
		self.X_train = self.scaler.fit_transform(self.X_train)
		self.X_test = self.scaler.transform(self.X_test)
		if randomforest:
			self.model = RandomForestRegressor()
		else:
			self.model = LogisticRegression()
		self.model.fit(self.X_train, self.y_train)

		self.accuracy = self.model.score(self.X_test, self.y_test)

	def get_model_predictions(self, X_list):
		yvals = self.model(X_list)

		return yvals


