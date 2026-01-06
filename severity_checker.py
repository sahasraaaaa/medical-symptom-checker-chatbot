from config import Config


class SeverityChecker:
    """Check symptom severity and provide emergency escalation"""

    def __init__(self):
        self.critical_symptoms = Config.CRITICAL_SYMPTOMS

        # Severity scoring
        self.severity_scores = {
            # Critical (10 points)
            'chest pain': 10,
            'difficulty breathing': 10,
            'breathlessness': 10,
            'severe bleeding': 10,
            'unconsciousness': 10,
            'coma': 10,
            'severe headache': 10,
            'paralysis': 10,
            'seizures': 10,
            'stroke symptoms': 10,
            'severe abdominal pain': 10,
            'coughing blood': 10,
            'blood in sputum': 10,
            'confusion': 10,
            'altered sensorium': 10,
            'severe burns': 10,
            'weakness of one body side': 10,
            'slurred speech': 10,
            'acute liver failure': 10,
            'stomach bleeding': 10,

            # High severity (7-8 points)
            'high fever': 8,
            'vomiting': 7,
            'dehydration': 8,
            'yellowing of eyes': 7,
            'yellowish skin': 7,
            'dark urine': 7,
            'bloody stool': 8,
            'severe pain': 8,
            'fast heart rate': 7,
            'palpitations': 7,

            # Moderate severity (4-6 points)
            'fever': 5,
            'nausea': 4,
            'diarrhoea': 5,
            'constipation': 4,
            'headache': 5,
            'fatigue': 4,
            'dizziness': 5,
            'back pain': 5,
            'abdominal pain': 6,
            'stomach pain': 6,
            'joint pain': 5,
            'muscle pain': 4,
            'cough': 4,
            'loss of appetite': 4,
            'weight loss': 5,

            # Low severity (1-3 points)
            'itching': 2,
            'skin rash': 3,
            'mild fever': 3,
            'runny nose': 2,
            'congestion': 2,
            'continuous sneezing': 2,
            'anxiety': 3,
            'restlessness': 2,
            'lethargy': 3,
            'bruising': 2,
        }

    def calculate_severity_score(self, symptoms):
        """Calculate total severity score for given symptoms"""
        total_score = 0
        for symptom in symptoms:
            score = self.severity_scores.get(symptom, 2)  # Default 2 points
            total_score += score
        return total_score

    def check_critical_symptoms(self, symptoms):
        """Check if any critical symptoms are present"""
        critical_found = []
        for symptom in symptoms:
            # Check both exact match and partial match
            for critical in self.critical_symptoms:
                if critical in symptom or symptom in critical:
                    critical_found.append(symptom)
                    break
        return critical_found

    def get_severity_level(self, score):
        """Get severity level based on score"""
        if score >= 15:
            return "CRITICAL"
        elif score >= 10:
            return "HIGH"
        elif score >= 5:
            return "MODERATE"
        else:
            return "LOW"

    def should_seek_emergency_care(self, symptoms):
        """Determine if user should seek emergency care"""
        critical_symptoms = self.check_critical_symptoms(symptoms)
        severity_score = self.calculate_severity_score(symptoms)

        # Emergency if critical symptoms or very high score
        if critical_symptoms or severity_score >= 15:
            return True, critical_symptoms, severity_score
        return False, [], severity_score

    def get_emergency_message(self, critical_symptoms):
        """Get emergency message with critical symptoms"""
        message = "⚠️ EMERGENCY ALERT ⚠️\n\n"
        message += "You have reported critical symptoms that require IMMEDIATE medical attention:\n"
        for symptom in critical_symptoms:
            message += f"  - {symptom.title()}\n"
        message += "\n🚨 Please call emergency services (911) or go to the nearest emergency room immediately.\n"
        message += "\nThis is a medical emergency and should not be delayed."
        return message

    def get_severity_advice(self, severity_level, score):
        """Get advice based on severity level"""
        advice = {
            "CRITICAL": {
                "message": "Your symptoms indicate a potentially serious condition.",
                "action": "Seek immediate medical attention at an emergency room or call 911.",
                "urgency": "URGENT - Do not delay"
            },
            "HIGH": {
                "message": "Your symptoms suggest you should see a doctor soon.",
                "action": "Schedule an appointment with your healthcare provider within 24 hours.",
                "urgency": "HIGH PRIORITY - Same day or next day"
            },
            "MODERATE": {
                "message": "Your symptoms warrant medical evaluation.",
                "action": "Consider scheduling an appointment with your healthcare provider within a few days.",
                "urgency": "MODERATE - Within 2-3 days"
            },
            "LOW": {
                "message": "Your symptoms appear to be mild.",
                "action": "Monitor your symptoms. If they worsen or persist, consult a healthcare provider.",
                "urgency": "LOW - Monitor and schedule if symptoms persist"
            }
        }
        return advice.get(severity_level, advice["MODERATE"])


if __name__ == '__main__':
    # Test severity checker
    checker = SeverityChecker()

    test_cases = [
        ['chest pain', 'breathlessness', 'sweating'],
        ['headache', 'fever', 'nausea'],
        ['itching', 'skin rash'],
        ['vomiting', 'diarrhoea', 'dehydration']
    ]

    print("Testing Severity Checker:\n")
    for symptoms in test_cases:
        print(f"Symptoms: {symptoms}")
        is_emergency, critical, score = checker.should_seek_emergency_care(symptoms)
        severity = checker.get_severity_level(score)
        print(f"Severity Score: {score}")
        print(f"Severity Level: {severity}")
        print(f"Emergency: {is_emergency}")
        if is_emergency:
            print(checker.get_emergency_message(critical))
        else:
            advice = checker.get_severity_advice(severity, score)
            print(f"Advice: {advice['message']}")
            print(f"Action: {advice['action']}")
        print("-" * 50 + "\n")
