import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

def load_data(filepath):
    data = pd.read_csv(filepath)
    return data

def preprocess_data(data):
    # Удаляем ненужные столбцы
    cols_to_drop = ["Id", "PoolQC", "MiscFeature", "Alley", "Fence"]
    data = data.drop(columns=cols_to_drop)
    
    # Заполнение пропусков
    data["LotFrontage"].fillna(data["LotFrontage"].median(), inplace=True)
    categorical_cols = ["GarageType", "GarageFinish", "GarageQual", "GarageCond", 
                        "BsmtExposure", "BsmtFinType2", "BsmtFinType1", "BsmtCond", "BsmtQual", "MasVnrType"]
    for col in categorical_cols:
        data[col].fillna("None", inplace=True)
    
    numerical_cols = ["GarageYrBlt", "GarageArea", "GarageCars", "BsmtFinSF1", "BsmtFinSF2", 
                      "BsmtUnfSF", "TotalBsmtSF", "BsmtFullBath", "BsmtHalfBath", "MasVnrArea"]
    for col in numerical_cols:
        data[col].fillna(0, inplace=True)
    
    data["Electrical"].fillna(data["Electrical"].mode()[0], inplace=True)
    data["FireplaceQu"].fillna("None", inplace=True)
    
    return data

def explore_data(data):
    # Гистограмма SalePrice
    plt.figure(figsize=(10, 5))
    sns.histplot(data['SalePrice'], bins=30, kde=True, color='blue')
    plt.title("Распределение SalePrice")
    plt.show()
    
    # Корреляция признаков с SalePrice
    corr_matrix = data.corr(numeric_only=True)
    top_corr_features = corr_matrix['SalePrice'].abs().sort_values(ascending=False).head(11)[1:]
    print("Топ-10 признаков по корреляции с SalePrice:\n", top_corr_features)
    
    return top_corr_features.index.tolist()

def train_models(X_train, X_test, y_train, y_test):
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=10),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=10)
    }
    
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
        rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
        results[name] = (rmse_train, rmse_test)
        print(f"{name}: RMSE Train = {rmse_train:.2f}, RMSE Test = {rmse_test:.2f}")
    
    return results

def main():
    filepath = "train.csv"
    data = load_data(filepath)
    data = preprocess_data(data)
    selected_features = explore_data(data)
    
    X = data[selected_features]
    y = data["SalePrice"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)
    
    results = train_models(X_train, X_test, y_train, y_test)
    
    best_model = min(results, key=lambda k: results[k][1])
    print(f"Лучшая модель: {best_model} с RMSE {results[best_model][1]:.2f}")

if __name__ == "__main__":
    main()