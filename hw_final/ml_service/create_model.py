from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
import joblib

# Загружаем датасет diabetes
diabetes = load_diabetes()
X, y = diabetes.data, diabetes.target

# Обучаем простую модель
model = LinearRegression()
model.fit(X, y)

# Сохраняем модель
joblib.dump(model, 'model.pkl')
print("Model created and saved as model.pkl")
