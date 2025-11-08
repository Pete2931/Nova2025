import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier

# Load data
data = pd.read_csv("C:/Users/irisy/Desktop/nova/Nova2025/Fetal Health Data.csv")
X = data.drop("fetal_health", axis=1)
y = data["fetal_health"] -1

# Encode target labels to 0..n_classes-1 for XGBoost
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Scale features (optional for trees, but sometimes helps)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42
)

# Train XGBoost model
xgb = XGBClassifier(
    use_label_encoder=False,
    eval_metric='mlogloss',
    learning_rate=0.1,
    n_estimators=200,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

xgb.fit(X_train, y_train)
y_pred = xgb.predict(X_test)

# Convert encoded labels back to original for readable evaluation
y_test_orig = le.inverse_transform(y_test)
y_pred_orig = le.inverse_transform(y_pred)

# Evaluate
print(confusion_matrix(y_test_orig, y_pred_orig))
print(classification_report(y_test_orig, y_pred_orig, digits=3))
