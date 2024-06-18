import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

def drop_columns(df: pd.DataFrame, columns_to_drop):
    """Drop unnecessary columns from the dataframe."""
    return df.drop(columns=columns_to_drop, errors='ignore')

def create_preprocessor(numerical_features, categorical_features):
    """Create a preprocessing pipeline for numerical and categorical features."""
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', MinMaxScaler(), numerical_features),
            ('cat', OneHotEncoder(), categorical_features)
        ])
    return preprocessor