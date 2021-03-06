# explore the algorithm wrapped by RFECV
from sklearn.model_selection import KFold
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from matplotlib import pyplot
import pickle

import utilities

n_per_in = 5
n_per_out = 1
initial_n_features = 53


# get a list of models to evaluate
def get_selectors(X, y):
    selectors = dict()
    # # lr
    # print('Training Linear Regression wrapper....')
    # rfe_models = RFECV(estimator=LinearRegression(), step=n_per_in, cv=KFold(shuffle=False),
    #               scoring='neg_mean_absolute_error',
    #               min_features_to_select=n_per_in, n_jobs=-1)
    # rfe_models.fit(X, y)
    # filename = 'rfecv_lr_'+str(n_per_in)+'.sav'
    # pickle.dump(rfe_models, open(filename, 'wb'))
    # selectors['lr'] = rfe_models
    # # dt
    # print('Training Decision Tree wrapper....')
    # rfe_models = RFECV(estimator=DecisionTreeRegressor(), step=n_per_in, cv=KFold(shuffle=False),
    #               scoring='neg_mean_absolute_error',
    #               min_features_to_select=n_per_in, n_jobs=-1)
    # rfe_models.fit(X, y)
    # filename = 'rfecv_dt_'+str(n_per_in)+'.sav'
    # pickle.dump(rfe_models, open(filename, 'wb'))
    # selectors['dt'] = rfe_models
    # # rf
    # print('Training Random Forest wrapper....')
    # rfe_models = RFECV(estimator=RandomForestRegressor(), step=n_per_in, cv=KFold(shuffle=False),
    #               scoring='neg_mean_absolute_error',
    #               min_features_to_select=n_per_in, n_jobs=-1)
    # rfe_models.fit(X, y)
    # filename = 'rfecv_rf_'+str(n_per_in)+'.sav'
    # pickle.dump(rfe_models, open(filename, 'wb'))
    # selectors['rf'] = rfe_models
    # gbr
    print('Training GBRegressor wrapper....')
    params = {'criterion': 'mae', 'loss': 'ls', 'max_depth': 7, 'max_features': 'log2'}
    rfecv = RFECV(estimator=GradientBoostingRegressor(**params), step=n_per_in, cv=KFold(shuffle=False),
                  scoring='neg_mean_absolute_error',
                  min_features_to_select=n_per_in, n_jobs=-1)
    rfecv.fit(X, y)
    filename = 'rfecv_gbr_'+str(n_per_in)+'.sav'
    pickle.dump(rfecv, open(filename, 'wb'))
    selectors['gbr'] = rfecv
    return selectors


# define dataset
X, y = utilities.get_dataset_without_outliers(n_per_in, n_per_out)
# get the models to evaluate
selectors = get_selectors(X, y)
# evaluate the models and store results
results, names = list(), list()
for name, selector in selectors.items():
    score = selector.grid_scores_.max()
    n_features = selector.n_features_
    results.append(-score)
    names.append(name)
    print('>%s %.3f %d' % (name, score, n_features))
# plot model performance for comparison
pyplot.figure()
pyplot.title('BEST MAE PER BASE MODEL FOR RFE')
pyplot.xlabel("Base model used")
pyplot.ylabel("Best MAE")
pyplot.bar(names, results)
pyplot.show()

i = (initial_n_features * n_per_in) + (initial_n_features - 1)
n_of_features = []
while i > n_per_in:
    n_of_features.append(i)
    i -= n_per_in
n_of_features.append(n_per_in)
n_of_features.reverse()
for name, selector in selectors.items():
    pyplot.figure()
    pyplot.title('%s | Best CV MAE: %.3f | Features: %d' % (name.upper(), selector.grid_scores_.max(), selector.n_features_))
    pyplot.xlabel("Number of features selected")
    pyplot.ylabel("Cross validation score")
    pyplot.plot(n_of_features, selector.grid_scores_)
    pyplot.show()
