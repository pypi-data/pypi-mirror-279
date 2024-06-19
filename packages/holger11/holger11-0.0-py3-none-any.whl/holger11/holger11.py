import pyperclip as pc

def hhelp():
    """в словаре название темы - название функции"""
    z = ''' во всех функциях (кроме импортов) аргументом является часть задания, если выводить функцию от 0, выведет общее условие
{'Импорты' : 'imports',
'пропуски' : 'skip_value',
'Визуал' : 'visual',
'Бинарная классификация' : 'bi_class',
'обучения с учителем' : 'teacher',
'регрессия' : 'reg',
'множественная классификация' : 'many_class',
'опорных векторов с линейным ядром' : 'r2_mae',
'модель бинарной линейной классификации' : 'bin_change',
'множественной классификации по методу опорных векторов' : 'svc_poly',
'регрессии с регуляризацией' : 'reg_regul',}'''
    pc.copy(z)


def imports():
    pc.copy('''
from sklearn import datasets
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt     
from sklearn.model_selection import train_test_split   
from sklearn.linear_model import LogisticRegression  
''')

def skip_value():
    pc.copy('''
# Импорт необходимых библиотек
from sklearn import datasets
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка набора данных "Ирисы"
iris = datasets.load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)

# Проверка на пропущенные значения
print("Количество пропущенных значений в каждом столбце:")
print(df.isnull().sum())

# Графическая визуализация пропущенных значений
plt.figure(figsize=(10, 5))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title('Графическое представление пропущенных значений')
plt.show()''')


def visual():
    pc.copy('''
# Импорт необходимых библиотек
from sklearn import datasets
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка набора данных "Диабет"
diabetes = datasets.load_diabetes()
df = pd.DataFrame(data=diabetes.data, columns=diabetes.feature_names)

# Выбор четырех признаков для визуализации
features = ['age', 'sex', 'bmi', 'bp']

# Визуализация распределения выбранных признаков
for feature in features:
    plt.figure(figsize=(10, 5))
    sns.histplot(df[feature], kde=True)
    plt.title(f'Распределение признака {feature}')
    plt.show()''')


def bi_class():
    pc.copy('''
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Загрузка набора данных "Рак груди"
cancer = datasets.load_breast_cancer()
X = cancer.data
y = cancer.target

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание и обучение модели логистической регрессии
model = LogisticRegression(max_iter=10000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test);y_pred
df = pd.DataFrame({'Теоретические значения': y_test[:10],\
                   'Эмпирические значения': y_pred[:10]})
df
''')


def teacher():
    pc.copy('''
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd

# Загрузка датасета
wine = datasets.load_wine()

# Создание DataFrame
df = pd.DataFrame(data=wine.data, columns=wine.feature_names)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(df, wine.target, test_size=0.2, random_state=42)

# Создание и обучение модели
model = LinearRegression()
model.fit(X_train, y_train)

# Вывод коэффициентов линейной модели
for feature_name, coef in zip(wine.feature_names, model.coef_):
    print(f'{feature_name}: {coef}')
''')

def reg():
    pc.copy('''
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Загрузка набора данных
data = fetch_california_housing()
X, y = data.data, data.target

# Разделение набора данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Определение сетки гиперпараметров для поиска
param_grid = {'fit_intercept': [True, False], 'normalize': [True, False]}

# Создание объекта GridSearchCV
grid_search = GridSearchCV(model, param_grid, cv=5)

# Обучение модели и поиск оптимальных гиперпараметров
grid_search.fit(X_train, y_train)

print("До подбора MSE: ", mean_squared_error(y_test, model.predict(X_test)))

# Вывод лучших гиперпараметров
print("Лучшие гиперпараметры: ", grid_search.best_params_)

# Предсказание на тестовой выборке
y_pred = grid_search.predict(X_test)

# Вывод ошибки MSE
print("После подбора MSE: ", mean_squared_error(y_test, y_pred))
''')


def many_class():
    pc.copy('''
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

# Загрузка набора данных
data = load_iris()
X, y = data.data, data.target

# Создание модели SVC
model = SVC(kernel='linear', C=1, random_state=42)

# Выполнение кросс-валидации
scores = cross_val_score(model, X, y, cv=5)

# Вывод результатов
print("Средняя точность: ", scores.mean())
''')


def many_class():
    pc.copy('''
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

# Загрузка набора данных
data = load_iris()
X, y = data.data, data.target

# Создание модели SVC
model = SVC(kernel='linear', C=1, random_state=42)

# Выполнение кросс-валидации
scores = cross_val_score(model, X, y, cv=5)

# Вывод результатов
print("Средняя точность: ", scores.mean())
''')


def r2_mae():
    pc.copy('''
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

# Загрузка набора данных
data = load_diabetes()
X, y = data.data, data.target

# Разделение набора данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели SVR с линейным ядром
model = SVR(kernel='linear', C=1)

# Обучение модели
model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred = model.predict(X_test)

# Оценка эффективности модели
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

# Вывод результатов
print("R2: ", r2)
print("MAE: ", mae)
print("RMSE: ", rmse)
print("MAPE: ", mape)
''')


def bin_change():
    pc.copy('''
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Загрузка датасета
data = load_breast_cancer()

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

# Создание модели логистической регрессии с нестандартными параметрами
model = LogisticRegression(penalty='l1', solver='liblinear', C=0.5, random_state=42)

# Обучение модели
model.fit(X_train, y_train)

# Проверка точности модели на тестовой выборке
accuracy = model.score(X_test, y_test)
print(f'Точность модели: {accuracy}')

В этом коде используется конструктор LogisticRegression с нестандартными 
параметрами. Вот их смысл:

penalty='l1': это тип регуляризации, который помогает предотвратить переобучение. 
L1-регуляризация также называется Lasso.

solver='liblinear': это алгоритм, который используется для оптимизации задачи. 
‘liblinear’ подходит для небольших датасетов.

C=0.5: это обратный коэффициент регуляризации. Меньшие значения указывают 
на более сильную регуляризацию.

random_state=42: это начальное значение для генератора случайных чисел. 
Это используется для воспроизводимости результатов. Пожалуйста, учтите, что параметры модели могут требовать настройки в зависимости от вашего конкретного датасета и задачи.
''')


def svc_poly():
    pc.copy('''
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Загрузка датасета
data = load_wine()

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

# Создание модели SVM с полиномиальным ядром
model = SVC(kernel='poly', degree=3, random_state=42)

# Обучение модели
model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred = model.predict(X_test)

# Оценка эффективности модели
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print(f'Точность (Accuracy): {accuracy}')
print(f'Точность (Precision): {precision}')
print(f'Полнота (Recall): {recall}')
print(f'F1-мера: {f1}')
''')


def reg_regul():
    pc.copy('''
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

# Загрузка датасета
data = fetch_california_housing()

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

# Создание модели Ridge регрессии с нестандартными параметрами
model = Ridge(alpha=0.5, solver='cholesky', random_state=42)

# Обучение модели
model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred = model.predict(X_test)

# Оценка эффективности модели
mse = mean_squared_error(y_test, y_pred)
print(f'Среднеквадратичная ошибка (MSE): {mse}')

alpha=0.5: это параметр регуляризации, который контролирует степень уменьшения весов для предотвращения переобучения. Большие значения alpha увеличивают регуляризацию и делают модель более устойчивой к переобучению.

solver='cholesky': это метод вычисления, который используется для оптимизации. ‘cholesky’ использует стандартный разложение Холецкого для матрицы Грама.

random_state=42: это начальное значение для генератора случайных чисел. Это используется для воспроизводимости результатов.
''')