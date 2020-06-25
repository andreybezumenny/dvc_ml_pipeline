import gdown
import numpy as np
import pandas as pd
from config import Config
from train.download_shareable_link import download_file_from_google_drive
from sklearn.model_selection import train_test_split

np.random.seed(Config.RANDOM_SEED)

Config.ORIGINAL_DATASET_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
Config.DATASET_PATH.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(str(Config.ORIGINAL_DATASET_FILE_PATH))

train_df, test_df = train_test_split(df, test_size=0.2, random_state=Config.RANDOM_SEED)

train_df.to_csv(str(Config.DATASET_PATH / 'train.csv'), index=False)
test_df.to_csv(str(Config.DATASET_PATH / 'test.csv'), index=False)

