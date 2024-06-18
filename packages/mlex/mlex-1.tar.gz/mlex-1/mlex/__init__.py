import pyperclip as pc
    
def imports():
    s = '''import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from sklearn.datasets import load_iris
from sklearn.datasets import load_diabetes
from sklearn.datasets import load_breast_cancer
from sklearn.datasets import load_wine
from sklearn.datasets import fetch_californ ia_housing

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Lasso
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

from sklearn.metrics import mean_absolute_error, r2_score, mean_absolute_percentage_error, mean_squared_error #регрессия
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix, classification_report, roc_curve, auc, roc_auc_score #классификация

from yellowbrick.model_selection import LearningCurve
from matplotlib.ticker import ScalarFormatter
    '''
    return pc.copy(s)
    
def cross_val_():
    s = '''
model.fit(X, y)
cv_results = cross_val_score(model,                  # модель
                             X,                      # матрица признаков
                             y,                      # вектор цели
                             cv = 3,                # тип разбиения (можно указать просто число фолдов cv = 3)
                             scoring = 'accuracy',   # метрика
                             n_jobs=-1)              # используются все ядра CPU

print("Кросс-валидация: ", cv_results)
print("Среднее по кросс-валидации: ", cv_results.mean())
print("Дисперсия по кросс-валидации: ", cv_results.std())
    '''
    return pc.copy(s)
    
def grid_search_():
    s = '''model = Lasso()
grid = {'alpha' : [1, 2, 10, 20]} #меняйте alpha на нужное для вашей модели, можно несколько параметров и числа свои
grid_model = GridSearchCV(estimator=model,
                        param_grid=grid,
                        scoring='neg_mean_squared_error', #GridSearch ищет наилучшую модель, а не наихудшую. Поэтому GridSearchCV добавляет знак "минус".
                        #Таким образом, neg_mean_squared_error - это метрика, которая минимизируется, чтобы найти модель с минимальным среднеквадратичным отклонением.
                        cv=5,
                        verbose=1)
grid_model.fit(X, y)
best_model = grid_model.best_estimator_ #возвращает лучшую модель 
    '''
    return pc.copy(s)

def all_metrics_():
    s = '''from sklearn.metrics import get_scorer_names
print(get_scorer_names())
    '''
    return pc.copy(s)
    
def train_test_split_():
    s = '''X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 50)
    '''
    return pc.copy(s)
    
def confusion_matrix_():
    s = '''    ax = sns.heatmap(confusion_matrix(y_test, y_predicted), annot = True, cmap = 'Blues', fmt = 'd')
    plt.xlabel('Предсказанные значения')
    plt.ylabel('Реальные значения ');
    ax.xaxis.set_ticklabels(['False','True'])
    ax.yaxis.set_ticklabels(['False','True'])
    plt.show()
    '''
    return pc.copy(s)

def roc_auc_():
    s = '''rf = RandomForestClassifier()
rf.fit(X_train, y_train)
y_predicted = rf.predict(X_test)
y_predicted_prob = rf.predict_proba(X_test)[:, 1]

fpr, tpr, thresholds = roc_curve(y_test, y_predicted_prob)
roc_auc = roc_auc_score(y_test, y_predicted_prob)

plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC кривая (площадь = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='green', lw=2, linestyle='--')
plt.xlim([-0.01, 1.01])
plt.ylim([-0.01, 1.01])
plt.xlabel('FP')
plt.ylabel('TP')
plt.title('кривая ROC')
plt.legend(loc="lower right")
plt.show()
#ROC-кривая показывает, что модель идеально различает положительные классы от отрицательных. Площадь под кривой = 1, что является очень высоким значением.
    '''
    return pc.copy(s)

def learning_curve_():
    s = '''from yellowbrick.model_selection import LearningCurve
train_sizes = [0.5, 0.6, 0.7, 0.8, 0.9]
visualizer = LearningCurve(RandomForestClassifier(), train_sizes = train_sizes, cv = 5).fit(X, y)

#если оси через e (числа e)
visualizer.ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
visualizer.ax.yaxis.get_major_formatter().set_scientific(False)

visualizer.show()
    '''
    return pc.copy(s)
    
def print_coeffs_():
    s = '''model = ...
result = pd.DataFrame(index=model.classes_, columns = X.columns.tolist(), data=model.coef_)
#result['Intercept'] = model.intercept_
result.insert(0, 'Intercept', model.intercept_)
    '''
    return pc.copy(s)

def load_data_():
    s = '''from sklearn.datasets import load_wine
data = load_wine(as_frame=True)

X = data.data
y = data.target

df = pd.concat([X, y], axis=1)
    '''
    return pc.copy(s)

def raspredelenie_priznakov_():
    s = '''
fig, axs = plt.subplots(2, 2, figsize=(14, 8))
for i, x in enumerate(['age', 'sex', 's1', 's2']):
    sns.kdeplot(data=df, x=x, ax=axs[i//2, i%2])
plt.suptitle('Распределение признаков', fontsize=14, y=0.92)
plt.show()
    '''
    return pc.copy(s)
    
def regularization_():
    s = '''import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
from sklearn.datasets import load_wine

data = load_wine(as_frame=True)
X = data.data
y = data.target
df = pd.concat([X, y], axis=1)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Линейная регрессия без регуляризации
model_no_reg = LogisticRegression(max_iter = 10000)
model_no_reg.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred_no_reg = model_no_reg.predict(X_test)

# Оценка модели без регуляризации
mse_no_reg = accuracy_score(y_test, y_pred_no_reg)
print(f"ACCURACY без регуляризации: {mse_no_reg}")

# Линейная регрессия с L1-регуляризацией (Lasso)
model_l1 = LogisticRegression(penalty='l1', solver = 'saga', max_iter=10000)
model_l1.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred_l1 = model_l1.predict(X_test)

# Оценка модели с L1-регуляризацией
mse_l1 = accuracy_score(y_test, y_pred_l1)
print(f"ACCURACY с L1-регуляризацией: {mse_l1}")

# Линейная регрессия с L2-регуляризацией (Ridge)
model_l2 = LogisticRegression(penalty='l2', max_iter=10000)
model_l2.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred_l2 = model_l2.predict(X_test)

# Оценка модели с L2-регуляризацией
mse_l2 = accuracy_score(y_test, y_pred_l2)
print(f"ACCURACY с L2-регуляризацией: {mse_l2}")

# Вывод коэффициентов моделей
print(f"Коэффициенты модели без регуляризации: {model_no_reg.coef_}")
print(f"Коэффициенты модели с L1-регуляризацией: {model_l1.coef_}")
print(f"Коэффициенты модели с L2-регуляризацией: {model_l2.coef_}")
#Используйте solver='saga' для более быстрого обучения при использовании L1- или L2-регуляризации.
#Подберите гиперпараметры регуляризации (alpha) с помощью кросс-валидации, чтобы найти оптимальное значение для вашей задачи.
    '''
    return pc.copy(s)

def classification_plot():
    s = '''xx, yy = np.meshgrid(
    np.arange(X.min()[0], X.max()[0]+0.01, 0.01),
    np.arange(X.min()[1], X.max()[1]+0.01, 0.01))
XX = np.array(list(zip(xx.ravel(), yy.ravel()))).reshape((-1, 2))

Z = model.predict(XX).reshape(xx.shape)

plt.contourf(xx, yy, Z, alpha=0.4)
plt.scatter(X.iloc[:, 0][y==0], X.iloc[:, 1][y==0], marker="o", c='r', s=100)
plt.scatter(X.iloc[:, 0][y==1], X.iloc[:, 1][y==1], marker="x", c='b', s=100)
#plt.scatter(X.iloc[:, 0][y==2], X.iloc[:, 1][y==2], marker="o", c='g', s=100) 
#для новых классов добавлять строчку plt.scatter
plt.show()
    '''
    return pc.copy(s)
    
def normalize_():
    s = '''from sklearn.preprocessing import MinMaxScaler, StandardScaler
# 1. MinMaxScaler - нормализация к диапазону [0, 1]
#    (x - min) / (max - min)
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)
print("MinMaxScaler:\n", scaled_data)

# 2. StandardScaler - стандартизация (центрирование и масштабирование)
#    (x - mean) / std
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)
print("StandardScaler:\n", scaled_data)

#для датафрейма
scaler = MinMaxScaler()
scaled_data = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    '''
    return pc.copy(s)
    
def isnull_plot():
    s = '''df.info()
df.isna().sum()
sns.heatmap(df.isnull(), yticklabels=False, cbar=False)
plt.show()
    '''
    return pc.copy(s)

def under_over_sampling():
    s = '''from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

#Oversampling
oversampler = SMOTE(sampling_strategy='auto', random_state=42)
X_oversampled, y_oversampled = oversampler.fit_resample(df[['magnesium', 'ash']], df['target'])

#Undersampling с помощью RandomUnderSampler
undersampler = RandomUnderSampler(sampling_strategy='auto', random_state=42)
X_undersampled, y_undersampled = undersampler.fit_resample(df[['magnesium', 'ash']], df['target'])

# Вывод результатов
print("Исходные данные:")
print(df['target'].value_counts())

print("\nOversampling:")
print(pd.Series(y_oversampled).value_counts())

print("\nUndersampling:")
print(pd.Series(y_undersampled).value_counts())
    '''
    return pc.copy(s)
    
def clustering():
    s = '''# Импорт необходимых библиотек 
import matplotlib.pyplot as plt 
from sklearn import datasets 
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans 
 
# Загрузка набора данных "ирисы" 
iris = datasets.load_iris() 
X = iris.data 
y = iris.target 
 
# Применение PCA для уменьшения размерности до 2D для визуализации 
pca = PCA(n_components=2) 
X_reduced = pca.fit_transform(X) 
 
# Создание модели KMeans и обучение её данным 
kmeans = KMeans(n_clusters=3, random_state=42) 
kmeans.fit(X) 
 
# Получение предсказанных меток кластеров 
y_kmeans = kmeans.predict(X) 
 
# Визуализация кластеров 
plt.figure(figsize=(12, 6)) 
 
# Визуализация исходных данных с истинными метками 
plt.subplot(1, 2, 1) 
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y, cmap='viridis', edgecolor='k', s=50) 
plt.title('Исходные данные с истинными метками') 
plt.xlabel('Компонента 1') 
plt.ylabel('Компонента 2') 
 
# Визуализация данных с предсказанными метками кластеров 
plt.subplot(1, 2, 2) 
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y_kmeans, cmap='viridis', edgecolor='k', s=50) 
plt.scatter(pca.transform(kmeans.cluster_centers_)[:, 0], pca.transform(kmeans.cluster_centers_)[:, 1],  
            s=200, c='red', marker='X', label='Центроиды') 
plt.title('Кластеризация KMeans') 
plt.xlabel('Компонента 1') 
plt.ylabel('Компонента 2') 
plt.legend() 
plt.show()
    '''
    return pc.copy(s)
    
def get_dummies_():
    s = '''df = ...
df_dummies = pd.get_dummies(df)
    '''
    return pc.copy(s)    

def one_hot_encoder_():
    s = '''from sklearn.preprocessing import OneHotEncoder
# Создаем DataFrame с текстовыми признаками
data = {'color': ['red', 'green', 'blue', 'green', 'red'],
        'size': ['S', 'M', 'L', 'M', 'S']}
df = pd.DataFrame(data)
# Инициализируем OneHotEncoder
encoder = OneHotEncoder(sparse=False)
# Преобразуем признаки
encoded_data = encoder.fit_transform(df)
# Преобразуем массив в DataFrame для наглядности
encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(df.columns))
print(encoded_df)
    '''
    return pc.copy(s) 