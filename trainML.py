import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import shap


# Load data
data = pd.read_csv("/Users/adhipraghunathan/Nova2025/Fetal Health Data.csv")
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

xgb = XGBClassifier(
    objective='multi:softprob',
    num_class=3,
    eval_metric='mlogloss',
    random_state=42
)

param_dist = {
    'n_estimators': np.arange(200, 800, 100),
    'max_depth': np.arange(3, 10),
    'learning_rate': np.linspace(0.01, 0.3, 10),
    'subsample': np.linspace(0.6, 1.0, 5),
    'colsample_bytree': np.linspace(0.6, 1.0, 5),
    'min_child_weight': np.arange(1, 10),
    'reg_lambda': np.linspace(0.5, 2.0, 5),
    'reg_alpha': np.linspace(0, 1.0, 5),
}

# # Train XGBoost model
# xgb = XGBClassifier(
#     use_label_encoder=False,
#     eval_metric='mlogloss',
#     learning_rate=0.1,
#     n_estimators=200,
#     max_depth=5,
#     subsample=0.8,
#     colsample_bytree=0.8,
#     random_state=42
# )

# xgb.fit(X_train, y_train)



cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
search = RandomizedSearchCV(
    estimator=xgb,
    param_distributions=param_dist,
    n_iter=120,  # number of random combinations
    scoring='f1_macro',
    cv=cv,
    verbose=1,
    n_jobs=-1,
    random_state=42
)

search.fit(X_train, y_train)
print("Best params:", search.best_params_)
print("Best score:", search.best_score_)
best_model = search.best_estimator_

y_pred = best_model.predict(X_test)


# Convert encoded labels back to original for readable evaluation
y_test_orig = le.inverse_transform(y_test)
y_pred_orig = le.inverse_transform(y_pred)

# Evaluate
print(confusion_matrix(y_test_orig, y_pred_orig))
print(classification_report(y_test_orig, y_pred_orig, digits=3))

best_model.save_model("xgb_model.json")


explainer = shap.Explainer(best_model.predict, X)
shap_values = explainer(X)
shap.plots.beeswarm(shap_values)