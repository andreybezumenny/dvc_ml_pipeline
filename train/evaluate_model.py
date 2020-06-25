from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import json
import pickle
import pandas as pd
from config import Config
from train_model import setup_data


def evaluate(test_features_original, test_labels, model_save_path, metrics_path):
    model = pickle.load(open(model_save_path, 'rb'))
    test_features = setup_data(test_features_original.copy()).dropna()
    X_test = test_features['sentence']
    y_test = test_labels.astype(int)

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_pred, y_test)
    report = classification_report(y_test, y_pred, output_dict=True)

    with open(metrics_path, 'w') as outfile:
        json.dump(report, outfile)

    print('Accuracy on control data %s' % acc)
    print(report)

    for_save = pd.DataFrame()
    for_save['sentence'] = test_features_original['sentence'].to_list()
    for_save['label'] = y_test
    for_save['predict'] = y_pred

    for_save.to_csv(
        'assets/data/train_report.csv',
        index=False)


if __name__ == '__main__':
    test_features_df = pd.read_csv(str(Config.FEATURE_PATH / 'test_features.csv'))
    test_labels_df = pd.read_csv(str(Config.FEATURE_PATH / 'test_labels.csv'))
    test_features_df.columns = ['sentence']
    model_path = str(Config.MODELS_PATH / 'tfidf_model.pickle')
    metrics_path = str(Config.METRICS_FILE_PATH)
    evaluate(test_features_df, test_labels_df, model_path, metrics_path)
