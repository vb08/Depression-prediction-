import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

BASE = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE, "depression.csv")
SAVE_PATH = os.path.join(BASE, "depression_rf_model.pkl")

# Read CSV
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"{CSV_PATH} not found. Place your dataset at this path.")

df = pd.read_csv(CSV_PATH, encoding="latin1")
df.columns = df.columns.str.strip()

df = df.rename(columns={
    '1. Age': 'your_age',
    '2. Gender': 'your_gender',
    '5. Academic Year': 'your_academic_year',
    '6. Current CGPA': 'your_cgpa',
    '7. Did you receive a waiver or scholarship at your university?': 'got_scholarship',
    '1. In a semester, how often have you had little interest or pleasure in doing things?': 'q1',
    '2. In a semester, how often have you been feeling down, depressed or hopeless?': 'q2',
    '3. In a semester, how often have you had trouble falling or staying asleep, or sleeping too much?': 'q3',
    '4. In a semester, how often have you been feeling tired or having little energy?': 'q4',
    '5. In a semester, how often have you had poor appetite or overeating?': 'q5',
    '6. In a semester, how often have you been feeling bad about yourself - or that you are a failure or have let yourself or your family down?': 'q6',
    '7. In a semester, how often have you been having trouble concentrating on things, such as reading the books or watching television?': 'q7',
    '8. In a semester, how often have you moved or spoke too slowly for other people to notice? Or you\'ve been moving a lot more than usual because you\'ve been restless?': 'q8',
    '9. In a semester, how often have you had thoughts that you would be better off dead, or of hurting yourself?': 'q9',
    'Depression Label': 'label'
})

# Age: extract first number from ranges like "18-22"
df['your_age'] = df['your_age'].astype(str).str.split('-').str[0]
df['your_age'] = pd.to_numeric(df['your_age'], errors='coerce').fillna(df['your_age'].median())

# Gender: convert categories to numeric codes
df['your_gender'] = df['your_gender'].astype(str).str.strip()
df['your_gender'] = pd.Categorical(df['your_gender']).codes
df['your_gender'] = df['your_gender'].replace({-1:0})

# Scholarship to 0/1
df['got_scholarship'] = df['got_scholarship'].astype(str).str.strip().map(lambda x: 1 if x.lower().startswith('y') else 0)

# CGPA numeric
df['your_cgpa'] = pd.to_numeric(df['your_cgpa'], errors='coerce')
df['your_cgpa'] = df['your_cgpa'].fillna(df['your_cgpa'].median())

# Features & label
X = df[['your_age','your_gender','got_scholarship','your_cgpa',
        'q1','q2','q3','q4','q5','q6','q7','q8','q9']].copy()

y = df['label']

# Fill any remaining NaNs
X = X.fillna(X.median())

# Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))

joblib.dump(model, SAVE_PATH)
print("Model saved at:", SAVE_PATH)
