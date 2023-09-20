import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from sklearn.metrics import accuracy_score, precision_score, f1_score
from itertools import combinations

# Load and preprocess the dataset
def preprocess_dataset(dataset_path):
    df = pd.read_csv(dataset_path)
    df['Symptoms'] = df['Symptoms'].str.lower()
    df['Medication'] = df['Medication'].str.lower()
    df['Allergies'] = df['Allergies'].str.lower()
    df['Chronic Health Issues'] = df['Chronic Health Issues'].str.lower()
    df['Blood Group'] = df['Blood Group'].str.lower()
    df['Genotype'] = df['Genotype'].str.lower()
    df['Patient_Data'] = df['Symptoms'] + ' ' + \
                         df['Age'].astype(str) + ' ' + \
                         df['Blood Group'] + ' ' + \
                         df['Genotype'] + ' ' + \
                         df['Allergies'] + ' ' + \
                         df['Gender'] + ' ' + \
                         df['Chronic Health Issues']
    return df

# Load and preprocess the training and validation datasets
training_df = preprocess_dataset('training_dataset.csv')
validation_df = preprocess_dataset('validation_dataset.csv')

# Vectorize patient data
vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 5), sublinear_tf=True)
X_train = vectorizer.fit_transform(training_df['Patient_Data'])
y_train = training_df['Medication']

# Train the model (content-based filtering)
nn_model = NearestNeighbors(n_neighbors=10, metric='cosine')
nn_model.fit(X_train)

# Serialize and save the trained model
joblib.dump(nn_model, 'content_based_model.pkl')

# Load the trained model
loaded_model = joblib.load('content_based_model.pkl')

# Function to recommend medication based on user data
def recommend_medication(user_data):
    user_text = ' '.join(map(str, user_data))
    user_vector = vectorizer.transform([user_text])
    similarity_scores = cosine_similarity(user_vector, X_train)[0]
    max_similarity_indices = similarity_scores.argsort()[::-1]
    recommended_medications = []
    for index in max_similarity_indices:
        if similarity_scores[index] > 0:
            medication = y_train.iloc[index]
            if medication not in recommended_medications:
                recommended_medications.append(medication)
        if len(recommended_medications) >= 3:
            break
    return recommended_medications


# Function to predict ailments based on symptoms and user data
def recommend_ailments(symptoms, user_data):
    user_symptoms_text = ' '.join(symptoms).lower()
    user_vector = vectorizer.transform([user_symptoms_text])
    symptom_matrix = vectorizer.transform(training_df['Symptoms'])
    symptom_similarity_scores = cosine_similarity(user_vector, symptom_matrix)[0]
    
    ailment_candidates = []
    for r in range(1, len(user_data) + 1):
        for combo in combinations(user_data, r):
            candidate_data = ' '.join(map(str, combo))  # Join the combo elements as strings
            ailment_candidates.append(candidate_data + ' ' + user_symptoms_text)
    
    ailment_matrix = vectorizer.transform(ailment_candidates)
    ailment_similarity_scores = cosine_similarity(ailment_matrix, symptom_matrix)
    
    # Calculate ailment_prediction_scores
    ailment_prediction_scores = ailment_similarity_scores.dot(symptom_similarity_scores)
    
    max_similarity_indices = ailment_prediction_scores.argsort()[::-1]
    predicted_ailments = []
    
    for index in max_similarity_indices:
        if ailment_prediction_scores[index] > 0:
            ailment = training_df.loc[index, 'Ailment']
            if ailment not in predicted_ailments:
                predicted_ailments.append(ailment)
        if len(predicted_ailments) >= 3:
            break
    
    return predicted_ailments

# Function to evaluate the model's performance
def evaluate_model(X_val, y_val):
    predictions = loaded_model.kneighbors(X_val, n_neighbors=1, return_distance=False)
    predicted_labels = [y_train.iloc[prediction[0]] for prediction in predictions]
    accuracy = accuracy_score(y_val, predicted_labels)
    precision = precision_score(y_val, predicted_labels, average='weighted')
    f1 = f1_score(y_val, predicted_labels, average='weighted')
    return accuracy, precision, f1

# Get input from the user
name = input("Enter name: ")
hospital_ID = input("Enter hospital ID: ")
symptoms = input("Enter symptoms (comma-separated): ").lower().split(',')
age = int(input("Enter age: "))
blood_group = input("Enter blood group: ").lower()
genotype = input("Enter genotype: ").lower()
allergies = input("Enter allergies (comma-separated): ").lower().split(',')
gender = input("Enter gender: ").lower()
chronic_issues = input("Enter chronic health issues (comma-separated): ").lower().split(',')

# Preprocess the validation dataset
validation_df['Patient_Data'] = validation_df['Symptoms'] + ' ' + \
                                validation_df['Age'].astype(str) + ' ' + \
                                validation_df['Blood Group'] + ' ' + \
                                validation_df['Genotype'] + ' ' + \
                                validation_df['Allergies'] + ' ' + \
                                validation_df['Gender'] + ' ' + \
                                validation_df['Chronic Health Issues']

# Split the validation data into features (X_val) and labels (y_val)
X_val = vectorizer.transform(validation_df['Patient_Data'])
y_val = validation_df['Medication']

# Evaluate the model's performance on the validation dataset
accuracy, precision, f1 = evaluate_model(X_val, y_val)

# Prepare user data
user_data = [symptoms, age, blood_group, genotype, allergies, gender, chronic_issues]

# Call the recommendation functions

recommended_medications = recommend_medication(user_data)
predicted_ailments = recommend_ailments(symptoms, user_data)

print("You are likely suffering from: ", ", ".join(predicted_ailments))
print("Recommended medications: ", ", ".join(recommended_medications))

