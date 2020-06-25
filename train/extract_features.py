import pandas as pd
from config import Config

Config.FEATURE_PATH.mkdir(parents=True, exist_ok=True)

train_df = pd.read_csv(str(Config.DATASET_PATH / 'train.csv'))
test_df = pd.read_csv(str(Config.DATASET_PATH / 'test.csv'))

train_features = train_df['text']#.values()
test_features = test_df['text']#.values()

train_labels = train_df['target']#.values()
test_labels = test_df['target']#.values()

train_features.to_csv(str(Config.FEATURE_PATH / 'train_features.csv'), index=False)
test_features.to_csv(str(Config.FEATURE_PATH / 'test_features.csv'), index=False)

train_labels.to_csv(str(Config.FEATURE_PATH / 'train_labels.csv'), index=False)
test_labels.to_csv(str(Config.FEATURE_PATH / 'test_labels.csv'), index=False)