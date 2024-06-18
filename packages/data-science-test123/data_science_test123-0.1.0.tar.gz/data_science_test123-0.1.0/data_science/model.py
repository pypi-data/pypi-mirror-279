"""Trains ML model."""
import os
from dotenv import load_dotenv
from database.source import Source
import logging
from ds.data_science.preprocessing import create_preprocessor, drop_columns
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline


logger = logging.getLogger()

# Load environment variable from secrets.env
load_dotenv('secrets.env')

db = Source(connection_string=os.getenv("SOURCE"))
db.connect()

def load_data(query: str):
    """Loads data from DB to dataframe"""
    df = db.execute_to_dataframe(query=query, args=None)
    logger.info("Loaded data from database")
    return df

def train_and_serialize_model(X_train, y_train, numerical_features, categorical_features, cols_to_drop: list, model_path='linear_model.pkl'):
    """Train a model and serialize it to a file."""
    X_train = drop_columns(X_train, cols_to_drop)
    preprocessor = create_preprocessor(numerical_features, categorical_features)
    regressor = LinearRegression()
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', regressor)
    ])
    pipeline.fit(X_train, y_train)

    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)
    print(f"Model saved to {model_path}")
