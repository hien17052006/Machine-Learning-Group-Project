RANDOM_SEED = 42

TEST_SIZE = 0.2
VAL_SIZE = 0.2

RAW_DATA_PATH = "data/raw/hour.csv"
PROCESSED_TRAIN_PATH = "data/processed/train.csv"
PROCESSED_VAL_PATH = "data/processed/val.csv"
PROCESSED_TEST_PATH = "data/processed/test.csv"

TARGET_COLUMN = "demand_level"
TARGET_SOURCE_COLUMN = "cnt"

DEMAND_LEVEL_LABELS = {0: "low", 1: "medium", 2: "high"}

LOW_THRESHOLD = 56.0
HIGH_THRESHOLD = 176.0

CYCLICAL_FEATURES = {
    "hr": 24,
    "mnth": 12,
    "weekday": 7,
}

ONE_HOT_FEATURES = ["season", "weathersit"]
ONE_HOT_COLUMNS = ["season_2", "season_3", "season_4", "weathersit_2", "weathersit_3", "weathersit_4"]

BINARY_FEATURES = ["holiday", "workingday"]

NUMERIC_FEATURES = ["atemp", "hum", "windspeed"]

LAG_FEATURES = ["lag_1h", "lag_mean_3h", "same_hour_prev"]

DROP_COLUMNS = ["instant", "dteday", "casual", "registered", "cnt", "yr", "temp"]

FEATURE_COLUMNS = (
    [f"{col}_sin" for col in CYCLICAL_FEATURES]
    + [f"{col}_cos" for col in CYCLICAL_FEATURES]
    + BINARY_FEATURES
    + NUMERIC_FEATURES
    + ONE_HOT_COLUMNS
    + LAG_FEATURES
)


def get_thresholds():
    if LOW_THRESHOLD is None or HIGH_THRESHOLD is None:
        raise ValueError("LOW_THRESHOLD and HIGH_THRESHOLD must be set after Person 1 computes them from the train set.")
    return LOW_THRESHOLD, HIGH_THRESHOLD


if __name__ == "__main__":
    print("Random seed:", RANDOM_SEED)
    print("Target column:", TARGET_COLUMN)
    print("Feature columns:", FEATURE_COLUMNS)
