import joblib
import pandas as pd
import numpy as np
from symptom_ner import SymptomNER
from severity_checker import SeverityChecker
from config import Config


class MedicalChatbot:
    """AI-powered medical symptom checker chatbot"""

    def __init__(self):
        """Initialize chatbot with trained model and components"""
        self.load_model()
        self.ner = SymptomNER()
        self.severity_checker = SeverityChecker()
        self.conversation_state = {
            'symptoms': [],
            'asked_questions': [],
            'predictions': None,
            'stage': 'initial'  # initial, clarifying, diagnosis, completed
        }
        self.medical_disclaimer = self._get_medical_disclaimer()

    def load_model(self):
        """Load trained model and encoders"""
        try:
            self.model = joblib.load(Config.MODEL_PATH)
            self.label_encoder = joblib.load(Config.LABEL_ENCODER_PATH)
            self.feature_names = joblib.load('models/feature_names.pkl')
            print("Model loaded successfully!")
        except FileNotFoundError:
            print("Error: Model files not found. Please train the model first.")
            raise

    def _get_medical_disclaimer(self):
        """Get medical disclaimer text"""
        return """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚕️  MEDICAL DISCLAIMER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This chatbot is an AI-powered tool designed for informational and
educational purposes only. It is NOT a substitute for professional
medical advice, diagnosis, or treatment.

⚠️  IMPORTANT:
• Always seek the advice of your physician or qualified healthcare
  provider with any questions about a medical condition
• Never disregard professional medical advice or delay seeking it
  because of information provided by this chatbot
• If you think you may have a medical emergency, call your doctor
  or 911 immediately
• This tool should not be used for diagnosing or treating health
  problems or diseases

Model Accuracy: 89% on test data
Training Data: 4,920 medical records
Diseases Covered: 41 common conditions
Symptoms Analyzed: 130+ medical symptoms

By using this chatbot, you acknowledge that you understand and
accept this disclaimer.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    def reset_conversation(self):
        """Reset conversation state for new session"""
        self.conversation_state = {
            'symptoms': [],
            'asked_questions': [],
            'predictions': None,
            'stage': 'initial'
        }

    def process_message(self, user_message):
        """Process user message and generate response"""
        # Extract symptoms from message
        detected_symptoms = self.ner.extract_symptoms(user_message)

        # Add new symptoms to the list
        for symptom in detected_symptoms:
            if symptom not in self.conversation_state['symptoms']:
                self.conversation_state['symptoms'].append(symptom)

        # Check for critical symptoms
        is_emergency, critical_symptoms, severity_score = \
            self.severity_checker.should_seek_emergency_care(self.conversation_state['symptoms'])

        if is_emergency:
            response = self.severity_checker.get_emergency_message(critical_symptoms)
            self.conversation_state['stage'] = 'completed'
            return response

        # Determine next step based on conversation stage
        if len(self.conversation_state['symptoms']) == 0:
            return self._ask_initial_symptoms()
        elif len(self.conversation_state['symptoms']) < 3:
            return self._ask_follow_up_questions()
        else:
            return self._make_diagnosis()

    def _ask_initial_symptoms(self):
        """Ask user to describe their symptoms"""
        return """Hello! I'm a medical symptom checker chatbot.

I can help identify possible conditions based on your symptoms, but please
remember that I cannot replace a real doctor's diagnosis.

Could you please describe the symptoms you're experiencing?
For example: "I have a headache and fever" or "I'm experiencing chest pain"
"""

    def _ask_follow_up_questions(self):
        """Ask follow-up questions to gather more information"""
        current_symptoms = self.conversation_state['symptoms']

        # Generate follow-up questions based on current symptoms
        questions = self._generate_follow_up_questions(current_symptoms)

        if questions:
            question = questions[0]
            self.conversation_state['asked_questions'].append(question)
            return f"I understand you have: {', '.join(current_symptoms)}\n\n{question}"
        else:
            # Proceed to diagnosis if no more questions
            return self._make_diagnosis()

    def _generate_follow_up_questions(self, symptoms):
        """Generate contextual follow-up questions"""
        questions = []

        # Check what symptoms we have and ask related questions
        symptom_str = ' '.join(symptoms)

        if 'fever' in symptom_str and 'duration' not in ' '.join(self.conversation_state['asked_questions']):
            questions.append("How long have you had the fever? Are you experiencing any other symptoms like chills, sweating, or body aches?")

        if 'pain' in symptom_str and 'intensity' not in ' '.join(self.conversation_state['asked_questions']):
            questions.append("Can you describe the pain? Is it sharp, dull, or throbbing? How severe is it on a scale of 1-10?")

        if 'cough' in symptom_str and 'cough type' not in ' '.join(self.conversation_state['asked_questions']):
            questions.append("Is your cough dry or are you coughing up phlegm? Do you have any shortness of breath?")

        if 'stomach' in symptom_str or 'abdominal' in symptom_str:
            if 'digestive' not in ' '.join(self.conversation_state['asked_questions']):
                questions.append("Are you experiencing any nausea, vomiting, diarrhea, or constipation?")

        if 'headache' in symptom_str and 'headache type' not in ' '.join(self.conversation_state['asked_questions']):
            questions.append("Where is the headache located? Is it accompanied by any visual disturbances or sensitivity to light?")

        # Generic follow-up if we have less than 3 symptoms
        if len(symptoms) < 3 and 'other symptoms' not in ' '.join(self.conversation_state['asked_questions']):
            questions.append("Are you experiencing any other symptoms such as fatigue, loss of appetite, or changes in body temperature?")

        return questions

    def _make_diagnosis(self):
        """Make disease prediction based on symptoms"""
        if len(self.conversation_state['symptoms']) == 0:
            return "I need more information about your symptoms to make a prediction. Please describe what you're experiencing."

        # Create feature vector
        feature_vector = self._create_feature_vector(self.conversation_state['symptoms'])

        # Make prediction
        prediction_proba = self.model.predict_proba([feature_vector])[0]
        top_3_indices = np.argsort(prediction_proba)[-3:][::-1]

        predictions = []
        for idx in top_3_indices:
            disease = self.label_encoder.inverse_transform([idx])[0]
            confidence = prediction_proba[idx] * 100
            predictions.append({
                'disease': disease,
                'confidence': confidence
            })

        self.conversation_state['predictions'] = predictions
        self.conversation_state['stage'] = 'diagnosis'

        # Calculate severity
        severity_score = self.severity_checker.calculate_severity_score(self.conversation_state['symptoms'])
        severity_level = self.severity_checker.get_severity_level(severity_score)
        severity_advice = self.severity_checker.get_severity_advice(severity_level, severity_score)

        # Format response
        response = self._format_diagnosis_response(predictions, severity_level, severity_advice)
        return response

    def _create_feature_vector(self, symptoms):
        """Create feature vector for model prediction"""
        feature_vector = []
        for feature in self.feature_names:
            # Check if symptom is present (handle both formats)
            symptom_normalized = feature.replace('_', ' ')
            is_present = 0

            for symptom in symptoms:
                symptom_check = symptom.replace('_', ' ')
                if symptom_normalized == symptom_check or symptom_normalized in symptom_check or symptom_check in symptom_normalized:
                    is_present = 1
                    break

            feature_vector.append(is_present)

        return feature_vector

    def _format_diagnosis_response(self, predictions, severity_level, severity_advice):
        """Format diagnosis response with predictions and advice"""
        response = "\n" + "="*60 + "\n"
        response += "📋 DIAGNOSIS RESULTS\n"
        response += "="*60 + "\n\n"

        response += f"Based on your symptoms: {', '.join(self.conversation_state['symptoms'])}\n\n"

        response += "🔍 Possible Conditions (ranked by probability):\n\n"
        for i, pred in enumerate(predictions, 1):
            confidence_bar = "█" * int(pred['confidence'] / 5) + "░" * (20 - int(pred['confidence'] / 5))
            response += f"{i}. {pred['disease']}\n"
            response += f"   Confidence: [{confidence_bar}] {pred['confidence']:.1f}%\n\n"

        response += f"\n⚕️  SEVERITY ASSESSMENT:\n"
        response += f"   Level: {severity_level}\n"
        response += f"   {severity_advice['message']}\n\n"

        response += f"📌 RECOMMENDATION:\n"
        response += f"   {severity_advice['action']}\n"
        response += f"   Urgency: {severity_advice['urgency']}\n\n"

        response += "="*60 + "\n"
        response += "⚠️  Remember: This is an AI prediction and not a definitive diagnosis.\n"
        response += "Always consult with a qualified healthcare professional.\n"
        response += "="*60 + "\n"

        return response

    def get_disclaimer(self):
        """Get medical disclaimer"""
        return self.medical_disclaimer


if __name__ == '__main__':
    # Test chatbot
    try:
        chatbot = MedicalChatbot()
        print(chatbot.get_disclaimer())
        print("\n" + "="*60)
        print("Medical Chatbot - Test Mode")
        print("="*60 + "\n")

        # Test conversation
        test_messages = [
            "I have a headache and high fever",
            "I also have body aches and chills",
            "Yes, and I'm feeling very tired"
        ]

        for msg in test_messages:
            print(f"User: {msg}")
            response = chatbot.process_message(msg)
            print(f"\nBot: {response}\n")
            print("-"*60 + "\n")

    except FileNotFoundError:
        print("\nModel not found. Please run train_model.py first to train the model.")
