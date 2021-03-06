import utilities
import pickle
from sklearn.model_selection import KFold, GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from matplotlib import pyplot
from sklearn.metrics import mean_absolute_error


n_per_in = 5
n_per_out = 1
X, y = utilities.get_dataset(n_per_in, n_per_out)
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)


# create pipeline
rfe = utilities.get_feature_selector('gbr', n_per_in)
models = utilities.get_models(['dt', 'gbr'])
results, names = list(), list()
for name, model in models.items():
    cv = KFold(n_splits=5, shuffle=False)
    pipeline = Pipeline(steps=[('feature_selector', rfe), ('model', model['estimator'])])
    print("Creating pipeline with %s model..." % name)
    predictor = GridSearchCV(
        estimator=pipeline,
        param_grid=model['grid_params'],
        scoring='neg_mean_absolute_error',
        cv=cv,
        refit=True
    )
    predictor.fit(x_train, y_train)
    filename = 'model_%s_%d.sav' % (name, n_per_in)
    print("Writing %s model to file..." % name)
    pickle.dump(predictor, open(filename, 'wb'))
    # evaluate model
    print("Getting predictions for validation set")
    y_predicted = predictor.predict(x_test)
    print('MAE in validation set for %s: %.3f' % (name, mean_absolute_error(y_test, y_predicted)))
    score = predictor.best_score_
    results.append(score)
    names.append(name)
    # report performance
    print('>%s %.3f' % (name, score))
    pyplot.plot(y_predicted, label='Predicted')
    # Printing and plotting the actual values
    pyplot.plot(y_test, label='Actual')
    pyplot.title(f"Predicted vs Actual Daily Step Counts")
    pyplot.ylabel("Steps")
    pyplot.legend()
    pyplot.show()

pyplot.figure()
pyplot.title('CV MAE PER MODEL')
pyplot.xlabel("Algorithms")
pyplot.ylabel("MAE")
pyplot.bar(names, results)
pyplot.show()

# plot model performance for comparison
pyplot.figure()
pyplot.title('CV MAE PER MODEL')
pyplot.boxplot(results, labels=names, showmeans=True)
pyplot.show()
