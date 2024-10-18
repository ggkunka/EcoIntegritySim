import pandas as pd

def load_toniot_weather_data(file_path):
    """
    Loads and preprocesses the ToNIoT weather dataset.
    """
    data = pd.read_csv(file_path)
    # Data preprocessing: Handle missing values, normalize features, etc.
    data = data.dropna()
    # Normalize features (assuming numeric columns are the features)
    for col in data.columns:
        if data[col].dtype == 'float64':
            data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
    return data
