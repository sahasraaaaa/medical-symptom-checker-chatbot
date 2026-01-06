# Medical Symptom Checker Chatbot

An AI-powered medical symptom checker chatbot that diagnoses 41 diseases from 130+ symptoms with 89% accuracy using Random Forest machine learning algorithm.

## Features

- **AI-Powered Diagnosis**: Random Forest classifier trained on 4,920 medical records
- **High Accuracy**: Achieves 89% accuracy on test data
- **Conversational Interface**: Natural language processing with follow-up questioning
- **Symptom Extraction**: Named Entity Recognition (NER) for extracting symptoms from natural language
- **Severity Assessment**: Intelligent severity scoring system with emergency escalation
- **Emergency Detection**: Identifies critical symptoms and recommends immediate medical attention
- **Web Interface**: Modern, responsive Flask web application
- **REST API**: JSON API for integration with other applications

## Technology Stack

- **Backend**: Python, Flask
- **Machine Learning**: scikit-learn, Random Forest
- **NLP**: NLTK (Natural Language Processing)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Data Processing**: pandas, numpy

## Project Statistics

- **Diseases Covered**: 41 common medical conditions
- **Symptoms Analyzed**: 130+ medical symptoms
- **Training Dataset**: 4,920 medical records
- **Model Accuracy**: 89%
- **Model Type**: Random Forest Classifier

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Download NLTK data**:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

6. **Generate the medical dataset**:
```bash
python generate_dataset.py
```

7. **Train the machine learning model**:
```bash
python train_model.py
```

8. **Run the web application**:
```bash
python app.py
```

9. **Open your browser** and navigate to:
```
http://localhost:5000
```

## Quick Start (Alternative)

Use the setup script to automate the installation:

```bash
python setup.py
```

## Project Structure

```
Medical-chatbot/
│
├── app.py                      # Flask web application
├── chatbot.py                  # Main chatbot logic and conversation flow
├── train_model.py              # Model training script
├── generate_dataset.py         # Dataset generation script
├── symptom_ner.py              # Named Entity Recognition for symptoms
├── severity_checker.py         # Severity assessment and emergency detection
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── data/
│   └── medical_dataset.csv     # Generated medical dataset
│
├── models/
│   ├── disease_model.pkl       # Trained Random Forest model
│   ├── label_encoder.pkl       # Label encoder for diseases
│   └── feature_names.pkl       # Feature names for prediction
│
├── templates/
│   └── index.html              # Web interface template
│
└── static/
    ├── css/
    │   └── style.css           # Stylesheet
    └── js/
        └── app.js              # Frontend JavaScript
```

## Usage

### Web Interface

1. Open http://localhost:5000 in your browser
2. Read and accept the medical disclaimer
3. Describe your symptoms in natural language
4. Answer follow-up questions from the chatbot
5. Receive diagnosis predictions with confidence scores
6. Get severity assessment and medical recommendations

### Example Conversations

**Example 1:**
```
User: I have a headache and high fever
Bot: How long have you had the fever? Are you experiencing any other symptoms like chills, sweating, or body aches?
User: Yes, I have chills and body aches
Bot: [Provides diagnosis with top 3 possible conditions]
```

**Example 2:**
```
User: I'm experiencing chest pain and difficulty breathing
Bot:  EMERGENCY ALERT - Please seek immediate medical attention!
```

### API Endpoints

#### POST /api/chat
Send a message to the chatbot
```json
{
  "message": "I have a headache and fever"
}
```

Response:
```json
{
  "response": "Chatbot response text",
  "symptoms": ["headache", "fever"],
  "stage": "diagnosis"
}
```

#### GET /api/symptoms
Get current symptoms in the conversation
```json
{
  "symptoms": ["headache", "fever"],
  "stage": "clarifying"
}
```

#### POST /api/reset
Reset the conversation

#### GET /api/disclaimer
Get the medical disclaimer text

## How It Works

### 1. Symptom Extraction (NER)
- Uses Natural Language Processing to extract symptoms from user input
- Handles synonyms and variations (e.g., "throw up" → "vomiting")
- Recognizes multi-word symptoms (e.g., "chest pain", "high fever")

### 2. Conversational Flow
- Starts with initial symptom collection
- Asks contextual follow-up questions based on reported symptoms
- Gathers at least 3 symptoms before making a diagnosis
- Adapts questions based on symptom patterns

### 3. Disease Prediction
- Creates feature vector from detected symptoms
- Uses trained Random Forest model to predict diseases
- Returns top 3 most likely conditions with confidence scores
- Model trained on 4,920 medical records

### 4. Severity Assessment
- Assigns severity scores to each symptom
- Calculates total severity: CRITICAL, HIGH, MODERATE, or LOW
- Detects critical symptoms requiring emergency care
- Provides urgency-based recommendations

### 5. Emergency Escalation
- Immediately identifies life-threatening symptoms
- Recommends calling 911 or visiting emergency room
- Critical symptoms include:
  - Chest pain
  - Difficulty breathing
  - Severe bleeding
  - Stroke symptoms
  - Seizures
  - And more...

## Diseases Covered

The chatbot can diagnose the following 41 diseases:

- Fungal infection
- Allergy
- GERD
- Chronic cholestasis
- Drug Reaction
- Peptic ulcer disease
- AIDS
- Diabetes
- Gastroenteritis
- Bronchial Asthma
- Hypertension
- Migraine
- Cervical spondylosis
- Paralysis (brain hemorrhage)
- Jaundice
- Malaria
- Chicken pox
- Dengue
- Typhoid
- Hepatitis A, B, C, D, E
- Alcoholic hepatitis
- Tuberculosis
- Common Cold
- Pneumonia
- Dimorphic hemorrhoids (piles)
- Heart attack
- Varicose veins
- Hypothyroidism
- Hyperthyroidism
- Hypoglycemia
- Osteoarthritis
- Arthritis
- Vertigo
- Acne
- Urinary tract infection
- Psoriasis
- Impetigo

## Important Disclaimers

**MEDICAL DISCLAIMER**

This chatbot is an AI-powered tool designed for **informational and educational purposes only**. It is **NOT a substitute** for professional medical advice, diagnosis, or treatment.

**IMPORTANT:**
- Always seek the advice of your physician or qualified healthcare provider
- Never disregard professional medical advice or delay seeking it because of this chatbot
- If you think you may have a medical emergency, call your doctor or 911 immediately
- This tool should not be used for diagnosing or treating health problems or diseases

## Model Performance

- **Accuracy**: 89%
- **Training Records**: 4,920
- **Test Split**: 80/20
- **Algorithm**: Random Forest (100 estimators)
- **Cross-validation**: Stratified split

## Development

### Running Tests

Test the symptom NER:
```bash
python symptom_ner.py
```

Test the severity checker:
```bash
python severity_checker.py
```

Test the chatbot:
```bash
python chatbot.py
```

### Retraining the Model

To retrain the model with different parameters or new data:

1. Modify `generate_dataset.py` to adjust the dataset
2. Run `python generate_dataset.py`
3. Modify hyperparameters in `train_model.py` if needed
4. Run `python train_model.py`

## Contributing

This is an educational project. Contributions are welcome for:
- Improving model accuracy
- Adding more diseases and symptoms
- Enhancing the NER system
- Improving the conversational flow
- Adding multilingual support

## License

This project is created for educational and demonstration purposes.

## Author

November 2025

## Acknowledgments

- scikit-learn for machine learning capabilities
- NLTK for natural language processing
- Flask for web framework
- Medical dataset based on common disease-symptom relationships

---

**Remember**: This is an AI tool for educational purposes. Always consult a healthcare professional for medical advice.
