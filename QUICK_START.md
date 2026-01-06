# Quick Start Guide

## For Absolute Beginners

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
python setup.py
python app.py
```

**macOS/Linux:**
```bash
python3 setup.py
python3 app.py
```

### Option 2: Use Quick Start Scripts

**Windows:**
Double-click `run.bat` or run:
```bash
run.bat
```

**macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

### Option 3: Manual Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Download NLTK data:**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

3. **Generate dataset:**
```bash
python generate_dataset.py
```

4. **Train model:**
```bash
python train_model.py
```

5. **Run application:**
```bash
python app.py
```

6. **Open browser:**
Navigate to http://localhost:5000

## Testing Individual Components

### Test Symptom NER
```bash
python symptom_ner.py
```

### Test Severity Checker
```bash
python severity_checker.py
```

### Test Chatbot Logic
```bash
python chatbot.py
```

## Common Issues

### Issue: ModuleNotFoundError
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Model not found
**Solution:** Train the model
```bash
python generate_dataset.py
python train_model.py
```

### Issue: NLTK data not found
**Solution:** Download NLTK data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### Issue: Port 5000 already in use
**Solution:** Change port in app.py (last line):
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Changed to 8000
```

## Project Overview

```
Setup Time: ~5-10 minutes
Dataset Generation: ~30 seconds
Model Training: ~1-2 minutes
```

## What Gets Created

- `data/medical_dataset.csv` - 4,920 medical records
- `models/disease_model.pkl` - Trained Random Forest model
- `models/label_encoder.pkl` - Label encoder
- `models/feature_names.pkl` - Feature names

## After Setup

1. Application runs on: http://localhost:5000
2. API available at: http://localhost:5000/api/*
3. Health check: http://localhost:5000/health

## Example API Usage

### Using curl:
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a headache and fever"}'
```

### Using Python:
```python
import requests

response = requests.post(
    'http://localhost:5000/api/chat',
    json={'message': 'I have a headache and fever'}
)
print(response.json())
```

## Need Help?

1. Check README.md for detailed documentation
2. Ensure Python 3.8+ is installed
3. Make sure all dependencies are installed
4. Verify model files exist in models/ directory

## Stop the Server

Press `CTRL+C` in the terminal where the app is running.
