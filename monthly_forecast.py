import pandas as pd
import joblib

def get_dip_risk():
    """
    Loads the trained model and the cleaned dataset,
    and returns a formatted string with the dip risk forecast.
    """

    # Load model + features
    pipe = joblib.load("files/dip_detector_model.pkl")
    FEATURES = joblib.load("files/feature_list.pkl")

    # Load cleaned dataset
    df = pd.read_csv("Data/bitcoin_cleaned_with_features.csv")

    # Drop any NaNs that may still exist
    df = df.dropna(subset=FEATURES)

    # Get latest features (last row)
    latest_features = df[FEATURES].iloc[[-1]]

    # Predict probabilities
    proba = pipe.predict_proba(latest_features)[0]

    # proba[1] = probability of dip
    return f"Risk of a 20% dip in the next 30 days is: {proba[1]*100:.2f}%"



# print(get_dip_risk())