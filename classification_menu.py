from get_keyword_textrank import df
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

data = df

### Label Encoding
Y_obj = data['label']
encoder = LabelEncoder()
encoder.fit(Y_obj)
Y = encoder.transform(Y_obj)

### TF-IDF Vectorizing
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data.text)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

### Using Logistic Regression
# LR = LogisticRegression(max_iter=10000, multi_class='ovr')
# LR.fit(x_train, y_train)
# y_pred = LR.predict(x_test)


### --- Accuracy :  0.8717002554640931
### --- F1 score : 0.6750885375443181
### --- ROC-AUC score : 0.9523113298703136
# print(f'Accuracy of Logistic Regression: {metrics.accuracy_score(y_test, y_pred)}')
# print(f'F1 score of Logistic Regression: {metrics.f1_score(y_test, y_pred, average='macro')}')
# print(f'ROC-AUC score of Logistic Regression: {metrics.roc_auc_score(y_test, LR.predict_proba(x_test), multi_class="ovr", average="macro")}')

### Using XGBoost Classifier
### --- Accuracy : 0.8807834232188476
### --- F1 score : 0.7133921555734579
### --- ROC-AUC score : 0.969850417048002
from xgboost import XGBClassifier

model = XGBClassifier(objective='multi:softprob', max_depth=7, alpha=0.6)
xgb_model = model.fit(x_train, y_train)
xgb_y_pred = xgb_model.predict(x_test)
xgb_y_pred_proba = xgb_model.predict_proba(x_test)
print(f'Accuracy of XGBoost Classifier : {metrics.accuracy_score(y_test, xgb_y_pred)}')
print(f'F1 score of Logistic Regression: {metrics.f1_score(y_test, xgb_y_pred, average='macro')}')
print(f'ROC-AUC score of XGBoost Classifier : {metrics.roc_auc_score(y_test, xgb_y_pred_proba, multi_class="ovr", average="macro")}')