import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os


def train_disease_prediction_model():
    """Train Random Forest model for disease prediction"""

    print("Loading dataset...")
    # Load dataset
    df = pd.read_csv('data/medical_dataset.csv')

    print(f"Dataset loaded: {len(df)} records")
    print(f"Diseases: {df['prognosis'].nunique()}")
    print(f"Features: {len(df.columns) - 1}")

    # Separate features and target
    X = df.drop('prognosis', axis=1)
    y = df['prognosis']

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    print(f"\nTraining set size: {len(X_train)}")
    print(f"Testing set size: {len(X_test)}")

    # Train Random Forest model
    print("\nTraining Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # Evaluate model
    print("\nEvaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nModel Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

    # Detailed classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_, zero_division=0))

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nTop 10 Most Important Symptoms:")
    print(feature_importance.head(10))

    # Create models directory
    os.makedirs('models', exist_ok=True)

    # Save model and encoders
    print("\nSaving model and encoders...")
    joblib.dump(model, 'models/disease_model.pkl')
    joblib.dump(label_encoder, 'models/label_encoder.pkl')

    # Save feature names
    feature_names = X.columns.tolist()
    joblib.dump(feature_names, 'models/feature_names.pkl')

    print("\nModel training completed successfully!")
    print(f"Model saved to: models/disease_model.pkl")
    print(f"Label encoder saved to: models/label_encoder.pkl")
    print(f"Feature names saved to: models/feature_names.pkl")

    return model, label_encoder, accuracy


if __name__ == '__main__':
    # Check if dataset exists
    if not os.path.exists('data/medical_dataset.csv'):
        print("Dataset not found. Generating dataset...")
        from generate_dataset import generate_medical_dataset
        os.makedirs('data', exist_ok=True)
        df = generate_medical_dataset(4920)
        df.to_csv('data/medical_dataset.csv', index=False)
        print("Dataset generated successfully!")

    # Train model
    model, encoder, accuracy = train_disease_prediction_model()
