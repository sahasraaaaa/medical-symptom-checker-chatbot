import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd

class SymptomNER:
    """Named Entity Recognition for extracting symptoms from natural language"""

    def __init__(self):
        """Initialize NER with symptom vocabulary"""
        self.download_nltk_data()
        self.lemmatizer = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))

        # Load symptom vocabulary
        self.symptom_vocab = self._load_symptom_vocab()
        self.symptom_synonyms = self._create_symptom_synonyms()

    def download_nltk_data(self):
        """Download required NLTK data"""
        required_data = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}')
            except LookupError:
                try:
                    nltk.download(data, quiet=True)
                except:
                    pass

    def _load_symptom_vocab(self):
        """Load symptom vocabulary from dataset"""
        symptoms = [
            'itching', 'skin rash', 'nodal skin eruptions', 'continuous sneezing', 'shivering',
            'chills', 'joint pain', 'stomach pain', 'acidity', 'ulcers on tongue',
            'muscle wasting', 'vomiting', 'burning micturition', 'spotting urination', 'fatigue',
            'weight gain', 'anxiety', 'cold hands and feets', 'mood swings', 'weight loss',
            'restlessness', 'lethargy', 'patches in throat', 'irregular sugar level', 'cough',
            'high fever', 'sunken eyes', 'breathlessness', 'sweating', 'dehydration',
            'indigestion', 'headache', 'yellowish skin', 'dark urine', 'nausea',
            'loss of appetite', 'pain behind the eyes', 'back pain', 'constipation', 'abdominal pain',
            'diarrhoea', 'mild fever', 'yellow urine', 'yellowing of eyes', 'acute liver failure',
            'fluid overload', 'swelling of stomach', 'swelled lymph nodes', 'malaise', 'blurred and distorted vision',
            'phlegm', 'throat irritation', 'redness of eyes', 'sinus pressure', 'runny nose',
            'congestion', 'chest pain', 'weakness in limbs', 'fast heart rate', 'pain during bowel movements',
            'pain in anal region', 'bloody stool', 'irritation in anus', 'neck pain', 'dizziness',
            'cramps', 'bruising', 'obesity', 'swollen legs', 'swollen blood vessels',
            'puffy face and eyes', 'enlarged thyroid', 'brittle nails', 'swollen extremeties', 'excessive hunger',
            'extra marital contacts', 'drying and tingling lips', 'slurred speech', 'knee pain', 'hip joint pain',
            'muscle weakness', 'stiff neck', 'swelling joints', 'movement stiffness', 'spinning movements',
            'loss of balance', 'unsteadiness', 'weakness of one body side', 'loss of smell', 'bladder discomfort',
            'foul smell of urine', 'continuous feel of urine', 'passage of gases', 'internal itching', 'toxic look typhos',
            'depression', 'irritability', 'muscle pain', 'altered sensorium', 'red spots over body',
            'belly pain', 'abnormal menstruation', 'dischromic patches', 'watering from eyes', 'increased appetite',
            'polyuria', 'family history', 'mucoid sputum', 'rusty sputum', 'lack of concentration',
            'visual disturbances', 'receiving blood transfusion', 'receiving unsterile injections', 'coma', 'stomach bleeding',
            'distention of abdomen', 'history of alcohol consumption', 'blood in sputum', 'prominent veins on calf',
            'palpitations', 'painful walking', 'pus filled pimples', 'blackheads', 'scurring',
            'skin peeling', 'silver like dusting', 'small dents in nails', 'inflammatory nails', 'blister',
            'red sore around nose', 'yellow crust ooze', 'fever'
        ]
        return set(symptoms)

    def _create_symptom_synonyms(self):
        """Create synonym mapping for better symptom matching"""
        synonyms = {
            'temperature': 'fever',
            'hot': 'fever',
            'pyrexia': 'fever',
            'throw up': 'vomiting',
            'puke': 'vomiting',
            'sick': 'nausea',
            'queasy': 'nausea',
            'tired': 'fatigue',
            'exhausted': 'fatigue',
            'weak': 'fatigue',
            'itch': 'itching',
            'scratch': 'itching',
            'rash': 'skin rash',
            'hives': 'skin rash',
            'sneeze': 'continuous sneezing',
            'sneezing': 'continuous sneezing',
            'cold': 'chills',
            'shiver': 'shivering',
            'ache': 'pain',
            'hurt': 'pain',
            'sore': 'pain',
            'breathless': 'breathlessness',
            'short of breath': 'breathlessness',
            'can\'t breathe': 'breathlessness',
            'dizzy': 'dizziness',
            'vertigo': 'dizziness',
            'loose motions': 'diarrhoea',
            'loose stool': 'diarrhoea',
            'upset stomach': 'stomach pain',
            'tummy ache': 'stomach pain',
            'head ache': 'headache',
            'head pain': 'headache'
        }
        return synonyms

    def preprocess_text(self, text):
        """Preprocess input text"""
        # Convert to lowercase
        text = text.lower()

        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)

        # Normalize whitespace
        text = ' '.join(text.split())

        return text

    def extract_symptoms(self, text):
        """Extract symptoms from natural language text"""
        text = self.preprocess_text(text)
        detected_symptoms = []

        # First check for exact matches with multi-word symptoms
        for symptom in self.symptom_vocab:
            if symptom in text:
                detected_symptoms.append(symptom)

        # Check for synonyms
        for synonym, symptom in self.symptom_synonyms.items():
            if synonym in text and symptom not in detected_symptoms:
                if symptom in self.symptom_vocab:
                    detected_symptoms.append(symptom)
                else:
                    # Try to find similar symptom
                    for vocab_symptom in self.symptom_vocab:
                        if symptom in vocab_symptom:
                            detected_symptoms.append(vocab_symptom)
                            break

        # Tokenize and check individual words
        tokens = word_tokenize(text)

        # Check for body parts + pain/ache patterns
        body_parts = ['head', 'chest', 'stomach', 'back', 'joint', 'muscle', 'neck', 'knee', 'hip', 'belly', 'abdomen']
        pain_words = ['pain', 'ache', 'hurt', 'sore', 'discomfort']

        for i, token in enumerate(tokens):
            if token in body_parts:
                # Check if next word is pain-related
                if i + 1 < len(tokens) and tokens[i + 1] in pain_words:
                    symptom_phrase = f"{token} {tokens[i + 1]}"
                    for symptom in self.symptom_vocab:
                        if token in symptom and 'pain' in symptom and symptom not in detected_symptoms:
                            detected_symptoms.append(symptom)

        return list(set(detected_symptoms))  # Remove duplicates

    def format_symptoms_for_model(self, symptoms):
        """Convert symptom list to format expected by model"""
        # This will be used to create feature vector for the model
        symptom_vector = {}
        for symptom in self.symptom_vocab:
            # Convert spaces to underscores to match model format
            symptom_key = symptom.replace(' ', '_')
            symptom_vector[symptom_key] = 1 if symptom in symptoms else 0
        return symptom_vector


if __name__ == '__main__':
    # Test the NER
    ner = SymptomNER()

    test_sentences = [
        "I have a headache and fever",
        "I'm experiencing chest pain and difficulty breathing",
        "My stomach hurts and I feel nauseous",
        "I have itching and skin rash",
        "I've been vomiting and have diarrhea"
    ]

    print("Testing Symptom NER:\n")
    for sentence in test_sentences:
        symptoms = ner.extract_symptoms(sentence)
        print(f"Input: {sentence}")
        print(f"Detected symptoms: {symptoms}\n")
