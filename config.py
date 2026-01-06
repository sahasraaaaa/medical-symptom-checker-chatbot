import os

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MODEL_PATH = 'models/disease_model.pkl'
    VECTORIZER_PATH = 'models/vectorizer.pkl'
    LABEL_ENCODER_PATH = 'models/label_encoder.pkl'
    DATASET_PATH = 'data/medical_dataset.csv'

    # Severity levels for symptoms
    CRITICAL_SYMPTOMS = [
        'chest pain', 'difficulty breathing', 'severe bleeding', 'unconsciousness',
        'severe headache', 'paralysis', 'seizures', 'stroke symptoms',
        'severe abdominal pain', 'coughing blood', 'confusion', 'severe burns'
    ]

    # Model parameters
    MODEL_ACCURACY = 0.89
    N_DISEASES = 41
    N_SYMPTOMS = 130
    TRAINING_RECORDS = 4920
