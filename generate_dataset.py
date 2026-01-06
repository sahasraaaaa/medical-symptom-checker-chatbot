import pandas as pd
import numpy as np
import os

# 41 diseases
DISEASES = [
    'Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction',
    'Peptic ulcer diseae', 'AIDS', 'Diabetes', 'Gastroenteritis', 'Bronchial Asthma',
    'Hypertension', 'Migraine', 'Cervical spondylosis', 'Paralysis (brain hemorrhage)',
    'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A',
    'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis',
    'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
    'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
    'Osteoarthristis', 'Arthritis', '(vertigo) Paroymsal  Positional Vertigo',
    'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo'
]

# 132 symptoms
SYMPTOMS = [
    'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering',
    'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue',
    'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue',
    'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss',
    'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough',
    'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration',
    'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea',
    'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain',
    'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure',
    'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision',
    'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose',
    'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements',
    'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness',
    'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels',
    'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger',
    'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain',
    'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements',
    'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort',
    'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
    'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body',
    'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite',
    'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration',
    'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
    'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf',
    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring',
    'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
    'red_sore_around_nose', 'yellow_crust_ooze'
]

def generate_disease_symptom_mapping():
    """Generate mapping of diseases to their typical symptoms"""
    mapping = {
        'Fungal infection': ['itching', 'skin_rash', 'nodal_skin_eruptions', 'dischromic _patches'],
        'Allergy': ['continuous_sneezing', 'shivering', 'chills', 'watering_from_eyes'],
        'GERD': ['stomach_pain', 'acidity', 'ulcers_on_tongue', 'vomiting', 'cough', 'chest_pain'],
        'Chronic cholestasis': ['itching', 'vomiting', 'yellowish_skin', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes'],
        'Drug Reaction': ['itching', 'skin_rash', 'stomach_pain', 'burning_micturition', 'spotting_ urination'],
        'Peptic ulcer diseae': ['vomiting', 'loss_of_appetite', 'abdominal_pain', 'passage_of_gases', 'internal_itching'],
        'AIDS': ['muscle_wasting', 'patches_in_throat', 'high_fever', 'extra_marital_contacts'],
        'Diabetes': ['fatigue', 'weight_loss', 'restlessness', 'lethargy', 'irregular_sugar_level', 'blurred_and_distorted_vision', 'obesity', 'excessive_hunger', 'increased_appetite', 'polyuria'],
        'Gastroenteritis': ['vomiting', 'sunken_eyes', 'dehydration', 'diarrhoea'],
        'Bronchial Asthma': ['fatigue', 'cough', 'high_fever', 'breathlessness', 'family_history', 'mucoid_sputum'],
        'Hypertension': ['headache', 'chest_pain', 'dizziness', 'loss_of_balance', 'lack_of_concentration'],
        'Migraine': ['acidity', 'indigestion', 'headache', 'blurred_and_distorted_vision', 'excessive_hunger', 'stiff_neck', 'depression', 'irritability', 'visual_disturbances'],
        'Cervical spondylosis': ['back_pain', 'weakness_in_limbs', 'neck_pain', 'dizziness', 'loss_of_balance'],
        'Paralysis (brain hemorrhage)': ['vomiting', 'headache', 'weakness_of_one_body_side', 'altered_sensorium'],
        'Jaundice': ['itching', 'vomiting', 'fatigue', 'weight_loss', 'high_fever', 'yellowish_skin', 'dark_urine', 'nausea'],
        'Malaria': ['chills', 'vomiting', 'high_fever', 'sweating', 'headache', 'nausea', 'diarrhoea', 'muscle_pain'],
        'Chicken pox': ['itching', 'skin_rash', 'fatigue', 'lethargy', 'high_fever', 'headache', 'loss_of_appetite', 'mild_fever', 'swelled_lymph_nodes', 'malaise', 'red_spots_over_body'],
        'Dengue': ['skin_rash', 'chills', 'joint_pain', 'vomiting', 'fatigue', 'high_fever', 'headache', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'malaise', 'muscle_pain', 'red_spots_over_body'],
        'Typhoid': ['chills', 'vomiting', 'fatigue', 'high_fever', 'headache', 'nausea', 'constipation', 'abdominal_pain', 'diarrhoea', 'toxic_look_(typhos)', 'belly_pain'],
        'hepatitis A': ['joint_pain', 'vomiting', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellowing_of_eyes', 'muscle_pain'],
        'Hepatitis B': ['itching', 'fatigue', 'lethargy', 'yellowish_skin', 'dark_urine', 'loss_of_appetite', 'abdominal_pain', 'yellow_urine', 'yellowing_of_eyes', 'malaise', 'receiving_blood_transfusion', 'receiving_unsterile_injections'],
        'Hepatitis C': ['fatigue', 'yellowish_skin', 'nausea', 'loss_of_appetite', 'yellowing_of_eyes', 'family_history'],
        'Hepatitis D': ['joint_pain', 'vomiting', 'fatigue', 'high_fever', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes'],
        'Hepatitis E': ['joint_pain', 'vomiting', 'fatigue', 'high_fever', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes', 'acute_liver_failure', 'coma', 'stomach_bleeding'],
        'Alcoholic hepatitis': ['vomiting', 'yellowish_skin', 'abdominal_pain', 'swelling_of_stomach', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1'],
        'Tuberculosis': ['chills', 'vomiting', 'fatigue', 'weight_loss', 'cough', 'high_fever', 'breathlessness', 'sweating', 'loss_of_appetite', 'mild_fever', 'yellowing_of_eyes', 'swelled_lymph_nodes', 'malaise', 'phlegm', 'chest_pain', 'blood_in_sputum'],
        'Common Cold': ['continuous_sneezing', 'chills', 'fatigue', 'cough', 'high_fever', 'headache', 'swelled_lymph_nodes', 'malaise', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'loss_of_smell'],
        'Pneumonia': ['chills', 'fatigue', 'cough', 'high_fever', 'breathlessness', 'sweating', 'malaise', 'phlegm', 'chest_pain', 'fast_heart_rate', 'rusty_sputum'],
        'Dimorphic hemmorhoids(piles)': ['constipation', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus'],
        'Heart attack': ['vomiting', 'breathlessness', 'sweating', 'chest_pain'],
        'Varicose veins': ['fatigue', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'prominent_veins_on_calf'],
        'Hypothyroidism': ['fatigue', 'weight_gain', 'cold_hands_and_feets', 'mood_swings', 'lethargy', 'dizziness', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'depression', 'irritability', 'abnormal_menstruation'],
        'Hyperthyroidism': ['fatigue', 'mood_swings', 'weight_loss', 'restlessness', 'sweating', 'diarrhoea', 'fast_heart_rate', 'excessive_hunger', 'muscle_weakness', 'irritability', 'abnormal_menstruation'],
        'Hypoglycemia': ['vomiting', 'fatigue', 'anxiety', 'sweating', 'headache', 'nausea', 'blurred_and_distorted_vision', 'fast_heart_rate', 'drying_and_tingling_lips'],
        'Osteoarthristis': ['joint_pain', 'neck_pain', 'knee_pain', 'hip_joint_pain', 'swelling_joints', 'painful_walking'],
        'Arthritis': ['muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'painful_walking'],
        '(vertigo) Paroymsal  Positional Vertigo': ['vomiting', 'headache', 'nausea', 'spinning_movements', 'loss_of_balance', 'unsteadiness'],
        'Acne': ['skin_rash', 'pus_filled_pimples', 'blackheads', 'scurring'],
        'Urinary tract infection': ['burning_micturition', 'foul_smell_of urine', 'continuous_feel_of_urine'],
        'Psoriasis': ['skin_rash', 'joint_pain', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails'],
        'Impetigo': ['skin_rash', 'high_fever', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']
    }
    return mapping

def generate_medical_dataset(n_records=4920):
    """Generate synthetic medical dataset"""
    np.random.seed(42)
    disease_symptom_map = generate_disease_symptom_mapping()

    records = []

    for _ in range(n_records):
        # Select a random disease
        disease = np.random.choice(DISEASES)

        # Get primary symptoms for this disease
        primary_symptoms = disease_symptom_map.get(disease, [])

        # Create a record with symptoms
        record = {symptom: 0 for symptom in SYMPTOMS}

        # Set primary symptoms (80-100% of them appear)
        n_primary = max(1, int(len(primary_symptoms) * np.random.uniform(0.8, 1.0)))
        selected_primary = np.random.choice(primary_symptoms, n_primary, replace=False)
        for symptom in selected_primary:
            if symptom in record:
                record[symptom] = 1

        # Add some random noise (5-10% chance of other symptoms)
        for symptom in SYMPTOMS:
            if symptom not in selected_primary and np.random.random() < 0.05:
                record[symptom] = 1

        record['prognosis'] = disease
        records.append(record)

    df = pd.DataFrame(records)
    return df

if __name__ == '__main__':
    # Create data directory
    os.makedirs('data', exist_ok=True)

    # Generate dataset
    print("Generating medical dataset...")
    df = generate_medical_dataset()

    # Save dataset
    df.to_csv('data/medical_dataset.csv', index=False)

    print(f"Dataset generated successfully!")
    print(f"Total records: {len(df)}")
    print(f"Total diseases: {df['prognosis'].nunique()}")
    print(f"Total symptoms: {len(SYMPTOMS)}")
    print(f"\nDisease distribution:")
    print(df['prognosis'].value_counts())
