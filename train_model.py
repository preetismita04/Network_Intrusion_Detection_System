import pandas as pd   #data handling and manipulation
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier    #main! builds multiple decision tree
from sklearn.preprocessing import LabelEncoder         #understand numbers
from sklearn.metrics import accuracy_score
import joblib                                         #save and load train model efficiently
 
# ✅ Step 1: Create a small demo dataset
data = {
    "proto": [6, 17, 6, 6, 1, 17, 6, 6, 1, 17],      # protocol numbers tcp =6, udp= 17, icmp = 1
    "src_port": [443, 53, 80, 8080, 0, 67, 22, 443, 0, 21],  #source port
    "dst_port": [51514, 62454, 60000, 49152, 8, 68, 50222, 60111, 3, 8081],  # destination post 
    "length": [60, 70, 120, 500, 200, 80, 150, 300, 400, 600],  # packet length in bytes
    "label": ["normal", "normal", "normal", "dos", "icmp_flood",
              "normal", "dos", "normal", "icmp_flood", "normal"]
}

#pandas is used here for data handling and manipulation
df = pd.DataFrame(data)

# ✅ Step 2: Encode the labels
le = LabelEncoder()
df["label"] = le.fit_transform(df["label"])

# ✅ Step 3: Split into features and target
X = df[["proto", "src_port", "dst_port", "length"]]
y = df["label"]

# ✅ Step 4: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Step 5: Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ✅ Step 6: Evaluate
y_pred = model.predict(X_test)
print("Model trained successfully! Accuracy:", accuracy_score(y_test, y_pred))

# ✅ Step 7: Save model
joblib.dump(model, "nids_model.pkl")
print("Model saved successfully as nids_model.pkl")