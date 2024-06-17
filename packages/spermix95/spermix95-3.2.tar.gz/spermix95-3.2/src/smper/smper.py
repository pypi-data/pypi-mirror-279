import os
from PIL import Image
import IPython.display as display


class pict:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__), 'files')
        self.sklad = []
        self.themes = []
        self.files = []
        k = 0
        # print(os.listdir(self.path))
        for theme in os.listdir(self.path):
            if 'DS' not in theme and 'init' not in theme:
                self.themes += [theme]
                for file in os.listdir(f"{self.path}/{theme}"):
                    if '.jpg' in file:
                        self.files.append(file.replace('.jpg',''))
                        self.sklad.append({f"{theme} {file.replace('.jpg','')}": {'index':f".pics[{k}].resize([400,200])", 'path':f"{self.path}/{theme}/{file}"}})
                        k+=1

        self.pics = []
        for i in range(len(self.sklad)):
            theme = self.sklad[i]
            keys, values = zip(*theme.items())
            values = values[0]
            self.pics.append(Image.open(values['path']))

    def search(self, string):
        results = []
        for i in self.sklad:
            # print(i)
            if string in list(i.keys())[0]:
                key, values = zip(*i.items())
                values = values[0]
                key = key[0]
                results += [{key:values['index']}]
        return results



class tests:
    def __init__(self):

        self.sklad = {5: ['5. ARMA. 1)Скачать с любого сайта данные о дневных ценах закрытия выбранной Вами акции в период с 01.06.2021 по 01.06.2022. (ряд 1). 2. Рассчитать доходность акции за выбранный период. (ряд 2) (3 балла). 3)Ряды 1 и 2 проверить, соответствуют ли они определению стационарных рядов. (8 баллов). 5)Построить автокорреляционные функции. Построить их графики. Сделать аналитические выводы. Оценить порядок p и q в ARMA, где это возможно. (7 баллов).  6. Для ряда 2 построить: Модель AR(2), MA(4), ARMA(1,4)  и провести их сравнение. Сделать аналитические выводы. Также в случае определения параметров p и q с помощью коррелограммы, построить эту модели и сравнить с AR(2), MA(4), ARMA(1,4)  (12 баллов).', 
[
'''
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import *

import warnings
warnings.filterwarnings('ignore')
''',
'''
# данные с финама https://www.finam.ru/quote/moex/gazp/export/ за указанный период, 
# периодичность 1 день, нужен только y - CLOSE, t - 1...n, d = (y_тек - y_пред) / y_пред (со второго значения) вручную

data = pd.read_csv('arm.csv', delimiter=';', decimal=",") # y - акции, d - доходность

y = data['y'] # 1 ряд - акции
d = data['d']  # 2 ряд - доходность акций (y_тек - y_пред) / y_пред

plt.plot(y);
''',
'''
plt.plot(d);
''',
'''
# Проверим ряды на стационарность (тест Дики-Фуллера)
# H0: ряд нестационарен
# H1: ряд стационарен
# Проверка стационарности ряда 1 (акции)
result = adfuller(y)
print(f"ADF Statistic: {result[0]}")
print(f"p-value: {result[1]}")

# Проверка стационарности ряда 2 (доходность акций)
result = adfuller(d[1:])
print(f"ADF Statistic: {result[0]}")
print(f"p-value: {result[1]}")
''',
'''
# избавляемся от нестационарности 
data = (data.shift(1) - data).iloc[1:]
data

y = data.y
d = data.d[1:]
''',
'''
# автокорреляционные функции и выводы по наибольшим лагам
plot_acf(data.y);
plot_pacf(data.y);
''',
'''
# лучшие p и q по AIC для ряда 2
p_range = range(1, 5)
q_range = range(1, 5)

results = pd.DataFrame(index=['AR{}'.format(i) for i in p_range],
                       columns=['MA{}'.format(i) for i in q_range])

for p in p_range:
    for q in q_range:
        model = ARIMA(data.d, order=(p, 0, q))
        model_fit = model.fit()
        # AIC модели (для сравнений)
        results.loc['AR{}'.format(p), 'MA{}'.format(q)] = model_fit.aic

results = results.apply(pd.to_numeric)

# параметры модели с наименьшим AIC
best_model_q = results.min().idxmin()
best_model_p = results[best_model_q].idxmin()
print('Лучшая модель: AR{} MA{}'.format(best_model_p[2:], best_model_q[2:]))

print(results)
''',
'''
# Постройка моделей для ряда 2 (заданных, и по найденным выше p, q)
model_ar2 = ARIMA(d, order=(2,0,0)).fit()
model_ma4 = ARIMA(d, order=(0,0,4)).fit()
model_arm14 = ARIMA(d, order=(1,0,4)).fit()
model_arm21 = ARIMA(d, order=(2,0,1)).fit() 

# Сравнение моделей AR, MA и ARMA по AIC, BIC 
aic_ar2 = model_ar2.aic
aic_ma4 = model_ma4.aic
aic_arm14 = model_arm14.aic
aic_arm21 = model_arm21.aic

bic_ar2 = model_ar2.bic
bic_ma4 = model_ma4.bic
bic_arm14 = model_arm14.bic
bic_arm21 = model_arm21.bic

print(f"Модель AR(2): AIC = {aic_ar2}, BIC = {bic_ar2}")
print(f"Модель MA(4): AIC = {aic_ma4}, BIC = {bic_ma4}")
print(f"Модель ARMA(1,4): AIC = {aic_arm14}, BIC = {bic_arm14}")
print(f"Модель ARMA(2,1): AIC = {aic_arm21}, BIC = {bic_arm21}")
''',
'''
# Аналитические выводы
# Модель с наименьшими значениями AIC, BIC будет считаться лучшей для описания данных.
print(model_arm21.summary())   # выведем лучшую модель, спецификация типа 
                              # $ d_t = const + 0.3162d_{t-1} - 0.1118d_{t-2} - 0.9958u_{t-1} + \epsilon_t $
''',
'''
# прогноз по лучшей
forecast = model_arm21.forecast(5)

plt.figure(figsize=(12, 6))
plt.plot(data.d, label='Факт')
plt.plot(forecast, label='Прогноз')
plt.xlabel('Время')
plt.ylabel('Значение')
plt.title('Модель ARMA')
plt.legend()
plt.show()''']],
            6:['6. 1) Постройте спецификацию Логит и Пробит моделей для объясняющей переменной Default (6 баллов) 2)Постройте Логит и Пробит модели со значимыми факторами, определите их прогнозную достоверность. (10 баллов) 3)Определите долю каждого значимого фактора в моделях. (10 баллов) 4)Сделайте аналитические выводы. (4 балла)',[
            
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
import sympy as sp
import scipy.stats as sts
from sklearn.metrics import accuracy_score
""",
"""
data = pd.read_excel('')

data.dropna(axis = 1, inplace = True)
alpha = 0.05

data.info()
""",
"""
y = data.Default
#Сразу удалим незначимый регрессор Firm_ID
X = data.drop(['Default', 'Firm ID'], axis = 1)

#Заменим нули на единицы и единицы на нули и будем предсказывать
#вероятность отсутсвия DEFAULT по причине большего количества данных с меткой 0
y = y.replace({1:0, 0:1})

#Делим выборку на Train и Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify = y)
""",
"""
#Проверка на наличие мультиколлинеарности

#Хи-квадрат Тест на мультиколлинеарность
def chi2_test(X):
    cor_matrix = sp.Matrix(X.corr().to_numpy())
    det = sp.det(cor_matrix)
    n = X.shape[0]
    k = X.shape[1]
    FG = -(n - 1 - 1/6 * (2*k + 5)) * sp.ln(det)
    chi2_cr = sts.chi2(1/2*k*(k-1)).isf(0.05)
    print(f'FG: {FG}, chi2: {chi2_cr}')
    if FG > chi2_cr:
        print('Мультиколлинеарность есть')
    else:
        print('Мультиколлинеарности нет')

chi2_test(X_train)
""",
"""
### Пошаговый отбор
X_train = sm.add_constant(X_train)
logit_model = sm.Logit(y_train, X_train)
result = logit_model.fit()

print(result.summary())
""",
"""
Z_krit = sts.norm.isf(alpha/2)
Z_krit

#'S/TA' имеет наименьшее значение z-статистики и оно меньше Z-критического, следовательно удаляем его

#и тд смотрим каждый раз на то какая переменная имеет меньшую z статистику по модулю в таблице и убираем пока все кэфы не станут значимыми
""",
"""
# итоговая логит модель 
new_X_train = X_train.drop(['S/TA', 'WC/TA', 'EBIT/TA', 'RE/TA'], axis = 1)
logit_model = sm.Logit(y_train, new_X_train)
result = logit_model.fit()
print(result.summary())

#Оставшийся коэффициент значимый, пошаговый отбор закончен
""",
"""
#Спецификация логит модели:
$$ ln(\frac{P(y_i = 1)}{P(y_i = 0)}) = 5.4201 - 3.0605*ME/TL_i$$
$$\sigma_{b_{0}} = 1.765$$
$$\sigma_{b_{4}} = 1.435$$
""",
"""
Проверим статистическую значимость регрессии в целом
chi_2_cr = sts.chi2.isf(0.05, new_X_train.shape[1])
LR = result.llr
print('Уравнение значимо') if (LR > chi_2_cr) else print('Уравнение незначимо')
""",
"""
##Прогноз на тестовой выборке
#Коэффициент R^2_pseudo = 0.2516 (из таблицы там так и написано)
# оставшиеся значимые переменные
new_X_test = sm.add_constant(X_test)[['const', 'ME/TL']]
y_pred = result.predict(new_X_test)
""",
"""
ans = 0
max_acc = 0
for i in np.linspace(0, 1, 100):
    if accuracy_score(y_test, y_pred > i) >= max_acc:
        max_acc = accuracy_score(y_test, y_pred > i)
        ans = i
print(f'Порог равен: {ans}', f'Точность(accuracy_score) равна: {max_acc}')
""",
"""
#Определим долю каждого значимого фактора в модели.
print(result.get_margeff().summary())
""",
"""
# в таблице dy/dx = -0.2
#При увеличении ME/TL на 1 вероятность дефолта увеличивается на 20%
""",
"""
# Построение Пробит модели
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify = y)
# Произведем пошаговый отбор признаков
X_train = sm.add_constant(X_train)
probit_model = sm.Probit(y_train, X_train)
result_probit = probit_model.fit()

print(result_probit.summary())
""",
"""
#'S/TA' имеет наименьшее значение z-статистики и оно меньше Z-критического, следовательно удаляем его

#и тд смотрим каждый раз на то какая переменная имеет меньшую z статистику по модулю в таблице и убираем пока все кэфы не станут значимыми
Z_krit = sts.norm.isf(alpha/2)
Z_krit
""",
"""
new_X_train = X_train.drop(['S/TA', 'WC/TA', 'EBIT/TA', 'RE/TA'], axis = 1)
probit_model = sm.Probit(y_train, new_X_train)
result_probit = probit_model.fit()

print(result_probit.summary())
""",
"""
#Итоговая спецификация модели
$$P(Y_i = 1) = F(Z_i)$$ 
где
$$Zi = 2.7558 - 1.4744 * ME/TL_i$$
$$\sigma_{b_{0}} = 0.774$$
$$\sigma_{b_{4}} = 0.688$$
F(Z) - функция стандартного нормального распределения
""",
"""
#Проверим статистическую значимость регрессии в целом
#Воспользуюсь LR-статистикой
LR = result_probit.llr
chi_2_cr = sts.chi2.isf(0.05, new_X_train.shape[1])
print('Уравнение значимо') if (LR > chi_2_cr) else print('Уравнение незначимо')
""",
"""
#Прогноз на тестовой выборке
new_X_test = sm.add_constant(X_test)[['const', 'ME/TL']]
y_pred_2 = result.predict(new_X_test)
""",
"""
ans = 0
max_acc = 0
for i in np.linspace(0, 1, 100):
    if accuracy_score(y_test, y_pred_2 > i) >= max_acc:
        max_acc = accuracy_score(y_test, y_pred_2 > i)
        ans = i
print(f'Порог равен: {ans}', f'Точность(accuracy_score) равна: {max_acc}')
""",
"""
#Определим долю каждого значимого фактора в модели.
print(result_probit.get_margeff().summary())
#Пробит модель так же показала, что при увеличении ME/TL на 1 вероятность дефолта увеличивается на 20%
#в таблице dy/dy = -0.2
""",
"""
#Вывод
#Данных достаточно мало и присутствует сильный дисбаланс классов, в связи с этим модели чаще предсказывают мажоритарный класс и pseudo_R^2 достаточно низкий в обоих моделях, однако можно с уверенностью сказать, что модели выделяют сильную зависимость между вероятностью дефолта и показателем ME/TL. Логит и пробит модели показали похожие результаты и несмотря на проблему с исходными данными достаточно точно прогнозируют вероятность дэфолта.
"""]], 3: ['3. 1)Запишите структурную форму модели в матричном виде и проведите проверку идентифицируемости системы правилами ранга и порядка (8 баллов) 2)Какая оптимальная процедура оценивания системы, обоснуйте? Если система неидентифицируема, предложите способ для идентификации системы (5 баллов) 3)Оцените систему с помощью выбранной оптимальная процедуры, запишите оцененный вид спецификации. (10 баллов) 4)Проиллюстрируйте графически результаты моделирования, сделайте выводы о качестве модели и о ее применимости. (7 баллов)',
[
"""
import pandas as pd
import statsmodels.api as sm
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sts
from sklearn.model_selection import train_test_split
sp.init_printing()
""",
"""
### 1)Запишите структурную форму модели в матричном виде и проведите проверку идентифицируемости системы правилами ранга и порядка (8 баллов)
$y_1 = a_{11}y_2 + b_{11}x_2 + u_1 \\
y_2 = a_{21}y_3 + b_{21}x_1 + u_2 \\
y_3 = a_{31}y_1 + b_{31}x_1 + u_3$
Структурная форма в матричном виде:  
$AY_t + BX_t = U_t$
""",
"""
Необходимое условие идентифицируемости (порядковое)
# H_i - число эндогенных переменных в структурной форме i-ого уравнения
# D_i - число экзогенных переменных, отсут. в i-ом уравнении, но присут. в системе уравнений

H1 = 2
D1 = 1

H2 = 2
D2 = 1

H3 = 2
D3 = 1

""",
"""
if D1 == H1 - 1:
  eq1 = 'id'
elif D1 > H1- 1:
  eq1 = 'sid'
else:
  eq1 = 'nid'

if D2 == H2 - 1:
  eq2 = 'id'
elif D2 > H2- 1:
  eq2 = 'sid'
else:
  eq2 = 'nid'

if D3 == H3 - 1:
  eq3 = 'id'
elif D3 > H3- 1:
  eq3 = 'sid'
else:
  eq3 = 'nid'
""",
"""
if set({eq1, eq2, eq3}) == {'id'}:
  print('Необходимое условие выполняется, проверим достаточное условие.')
if 'sid' in (eq1, eq2, eq3):
  print('Система сверхидентифицируема.')
if  'nid' in (eq1, eq2, eq3):
  print('Система неидентифицируема.')
""",
"""
#Достаточное условие (ранговое).
**Достаточное условие идентифицируемости структурного уравнения:** ранг матрицы, составленной из коэффициентов (в других уравнениях) при переменных (и эндогенных и экзогенных), отсутствующих в данном уравнении, не меньше общего числа эндогенных переменных системы (N) минус единица.

$$y_1 = a_{11}y_2 + b_{11}x_2 + u_1 \\
y_2 = a_{21}y_3 + b_{21}x_1 + u_2 \\
y_3 = a_{31}y_1 + b_{31}x_1 + u_3
$$

**Матрица коэффициентов при всех переменных всех уравнений:**

$
\begin{array}{|c|c|}
\hline
 & y_1 & y_2 & y_3 & x_1 & x_2 \\
\hline
1 & -1 & a_{11} & 0 & 0 & b_{11}\\
\hline
2 & 0 & -1 & a_{21} & b_{21} & 0\\
\hline
3 & a_{31} & 0 & -1 & b_{31} & 0\\
\hline
\end{array}
$

**Для первого уравнения:**  
переменные, отсутствующие в данном уравнении:
$y_3, x_1$.  
Матрица коэффициентов при этих переменных:
$$
W_1 = \begin{pmatrix}
a_{21} & b_{21} \\
-1 & b_{31}
\end{pmatrix}
, \ rank(W_1) = 2 \geq N-1 = 2 \Rightarrow (1) \ идентифицируемо.
$$

**Для второго уравнения:**  
переменные, отсутствующие в данном уравнении:
$y_1, x_2$.  
Матрица коэффициентов при этих переменных:
$$
W_2 = \begin{pmatrix}
-1 & b_{11} \\
a_{31} & 0
\end{pmatrix}
, \ rank(W_2) = 2 \geq N-1 = 2 \Rightarrow (2) \ идентифицируемо.
$$

**Для третьего уравнения:**  
переменные, отсутствующие в данном уравнении:
$y_2, x_2$.  
Матрица коэффициентов при этих переменных:
$$
W_3 = \begin{pmatrix}
a_{11} & b_{11} \\
-1 & 0
\end{pmatrix}
, \ rank(W_3) = 2 \geq N-1 = 2 \Rightarrow (3) \ идентифицируемо.
$$  

Все три уравнения идентифицируемы $\Rightarrow$ система идентифицируема.

""",
"""
### 2)Какая оптимальная процедура оценивания системы, обоснуйте? Если система неидентифицируема, предложите способ для идентификации системы (5 баллов)
Система уравнений идентифицируема $⇒$ используем косвенный метод наименьших квадратов (КМНК) для оценки системы.
иначе не нужно применять если сверхидентифицируема
""",
"""
### 3)Оцените систему с помощью выбранной оптимальная процедуры, запишите оцененный вид спецификации. (10 баллов)
y1, y2, y3, x1, x2, x3, u1, u2, u3, a11, a21, a31, b11, b21, b31 = sp.symbols('y_1, y_2, y_3, x_1, x_2, x_3, u_1, u_2, u_3, a_11, a_21, a_31, b_11, b_21, b_31')

# Заносим в питон систему уравнений:
eq1 = sp.Eq(y1, a11*y2 + b11*x2)
eq2 = sp.Eq(y2, a21*y3 + b21*x1)
eq3 = sp.Eq(y3, a31*y1 + b31*x1)

# Строим приведенную форму модели (выражаем у1, y2, y3)
system = sp.solve([eq1, eq2, eq3], [y1, y2, y3])
system
""",
"""
delta11 = system[y1].subs({x1: 1, x2: 0})
delta12 = system[y1].subs({x1: 0, x2: 1})
delta21 = system[y2].subs({x1: 1, x2: 0})
delta22 = system[y2].subs({x1: 0, x2: 1})
delta31 = system[y3].subs({x1: 1, x2: 0})
delta32 = system[y3].subs({x1: 0, x2: 1})
""",
"""
Выделим часть данных на тестовую выборку, остальные оставим для оценки адекватности модели
""",
"""
df = pd.read_excel('data.xlsx', decimal=',', dtype='float')
df, df_test = train_test_split(df, test_size=0.1, shuffle=False)

Y1 = df["y1"]
X1 = df[["x1", "x2"]]
model1 = sm.OLS(Y1, X1).fit()
d11, d12 = model1.params[['x1', 'x2']]

Y2 = df["y2"]
X2 = df[["x1", "x2"]]
model2 = sm.OLS(Y2, X2).fit()
d21, d22 = model2.params[['x1', 'x2']]

Y3 = df["y3"]
X3 = df[["x1", "x2"]]
model3 = sm.OLS(Y3, X3).fit()
d31, d32 = model3.params[['x1', 'x2']]
""",
"""
[{a11 :1.38796572964232, a21 :0.529612840629745, a31 :3.18969197336254, b11:−0.19861194349823, b21:0.446035711273433, b31:−2.03506926594528}]
**Оцененный вид спецификации:**

$$
y_1 = 1.387 \cdot y_2 - 0.198 \cdot x_2 + u_1 \\
y_2 = 0.529 \cdot y_3 + 0.446 \cdot x_1 + u_2 \\
y_3 = 3.189 \cdot y_1 - 2.035 \cdot x_1 + u_3
$$
""",
"""
### 4)Проиллюстрируйте графически результаты моделирования, сделайте выводы о качестве модели и о ее применимости. (7 баллов)
# Перепишем наши уравнения для получения оценненых значений:
y1_hat = params[0][a11]*df["y2"] + params[0][b11]*df["x2"]
y2_hat = params[0][a21]*df["y3"] + params[0][b21]*df["x1"]
y3_hat = params[0][a31]*df["y1"] + params[0][b31]*df["x1"]

y1_pred = params[0][a11]*df_test["y2"] + params[0][b11]*df_test["x2"]
y2_pred = params[0][a21]*df_test["y3"] + params[0][b21]*df_test["x1"]
y3_pred = params[0][a31]*df_test["y1"] + params[0][b31]*df_test["x1"]
""",
"""
residuals = df['y1'] - y1_hat
sigma_squared = np.var(residuals)

X_test = df_test[["x1", "x2"]]
X = df[["x1", "x2"]]

z_score = sts.norm.ppf(1 - 0.05 / 2)

mean_se = (residuals**2).mean()

lower_bounds = y1_pred - z_score * mean_se
upper_bounds = y1_pred + z_score * mean_se
""",
"""
results = pd.DataFrame({
    'predictions': y1_pred,
    'lower_bound': lower_bounds,
    'upper_bound': upper_bounds
}, index = df_test.index, dtype='float')

plt.fill_between(results.index.get_level_values(0), results['lower_bound'], results['upper_bound'], color='blue', alpha=0.1, label='Доверительный интервал')
plt.plot(y1_pred, label='Спрогнозированные значения', color='red')
plt.plot(y1_hat, label='Оцененные значения', color='green')
plt.plot(pd.concat([df["y1"], df_test["y1"]]), label='Фактические значения')
plt.legend()
plt.show()
""",
"""
residuals = df['y2'] - y2_hat
sigma_squared = np.var(residuals)

X_test = df_test[["x1", "x2"]]
X = df[["x1", "x2"]]
X_mean_row = X.mean(axis=1)
X_mean_row_test = X_test.mean(axis=1)

sum_squares_X_test = np.sum((X_test.subtract(X_mean_row_test, axis=0))**2, axis=1)
sum_squares_X = np.sum((X.subtract(X_mean_row, axis=0))**2, axis=1)

mean_se = np.sqrt(sigma_squared * (1 + sum_squares_X_test / sum_squares_X))
""",
"""
z_score = sts.norm.ppf(1 - 0.05 / 2)

mean_se = (residuals**2).mean()

lower_bounds = y2_pred - z_score * mean_se
upper_bounds = y2_pred + z_score * mean_se


results = pd.DataFrame({
    'predictions': y2_pred,
    'lower_bound': lower_bounds,
    'upper_bound': upper_bounds
}, index = df_test.index, dtype='float')
""",
"""
plt.fill_between(results.index.get_level_values(0), results['lower_bound'], results['upper_bound'], color='blue', alpha=0.1, label='Доверительный интервал')
plt.plot(y2_pred, label='Спрогнозированные значения', color='red')
plt.plot(y2_hat, label='Оцененные значения', color='green')
plt.plot(pd.concat([df["y2"], df_test["y2"]]), label='Фактические значения')
plt.legend()
plt.show()
""",
"""
residuals = df['y3'] - y3_hat
sigma_squared = np.var(residuals)

X_test = df_test[["x1", "x2"]]
X = df[["x1", "x2"]]
X_mean_row = X.mean(axis=1)
X_mean_row_test = X_test.mean(axis=1)

sum_squares_X_test = np.sum((X_test.subtract(X_mean_row_test, axis=0))**2, axis=1)
sum_squares_X = np.sum((X.subtract(X_mean_row, axis=0))**2, axis=1)

mean_se = np.sqrt(sigma_squared * (1 + sum_squares_X_test / sum_squares_X))
""",
"""
z_score = sts.norm.ppf(1 - 0.05 / 2)

mean_se = (residuals**2).mean()

lower_bounds = y3_pred - z_score * mean_se
upper_bounds = y3_pred + z_score * mean_se


results = pd.DataFrame({
    'predictions': y3_pred,
    'lower_bound': lower_bounds,
    'upper_bound': upper_bounds
}, index = df_test.index, dtype='float')
""",
"""
plt.fill_between(results.index.get_level_values(0), results['lower_bound'], results['upper_bound'], color='blue', alpha=0.1, label='Доверительный интервал')
plt.plot(y3_pred, label='Спрогнозированные значения', color='red')
plt.plot(y3_hat, label='Оцененные значения', color='green')
plt.plot(pd.concat([df["y3"], df_test["y3"]]), label='Фактические значения')
plt.legend()
plt.show()
""",
"""
# Вывод
Исходя из графиков, на которых изображены прогнозные значения и доверительные интервалы, можно сделать вывод, что первое и второе уравнение системы довольно точно прогнозируют эндогенную переменную, ведь ее значения входят в доверительный интервал. Третье уравнение системы уже менее точно делает прогноз. В связи с этим можно сказать, что модели можно назвать качественными и применимыми.
""",
"""
# Вариант с сверхидентифицируемой системой
# Отличается от предыдущего варианта только тем что используется ДМНК

y1, y2, y3, x1, x2, x3, u1, u2, u3, a11, a21, a31, b11, b12, b21, b31 = sp.symbols('y_1, y_2, y_3, x_1, x_2, x_3, u_1, u_2, u_3, a_11, a_21, a_31, b_11, b_12, b_21, b_31')

# Заносим в питон систему уравнений:
eq1 = sp.Eq(y1, a11*y3 + b11*x2)
eq2 = sp.Eq(y2, a21*y1 + b21*x3)
eq3 = sp.Eq(y3, a31*y2 + b31*x1)

# Строим приведенную форму модели (выражаем у1, y2, y3)
system = sp.solve([eq1, eq2, eq3], [y1, y2, y3])
system
""",
"""
delta11 = system[y1].subs({x1: 1, x2: 0, x3: 0})
delta12 = system[y1].subs({x1: 0, x2: 1, x3: 0})
delta13 = system[y1].subs({x1: 0, x2: 0, x3: 1})
delta21 = system[y2].subs({x1: 1, x2: 0, x3: 0})
delta22 = system[y2].subs({x1: 0, x2: 1, x3: 0})
delta23 = system[y2].subs({x1: 0, x2: 0, x3: 1})
delta31 = system[y3].subs({x1: 1, x2: 0, x3: 0})
delta32 = system[y3].subs({x1: 0, x2: 1, x3: 0})
delta33 = system[y3].subs({x1: 0, x2: 0, x3: 1})
""",
"""
df = pd.read_excel('data_sverh.xlsx', decimal=',', dtype='float', names=['x1', 'x2', 'x3', 'y1', 'y2', 'y3'])
df, df_test = train_test_split(df, test_size=0.1, shuffle=False)

Y1 = df["y1"]
X1 = df[["x1", "x2", "x3"]]
model1 = sm.OLS(Y1, X1).fit()
d11, d12, d13 = model1.params[['x1', 'x2', "x3"]]

Y2 = df["y2"]
X2 = df[["x1", "x2", "x3"]]
model2 = sm.OLS(Y2, X2).fit()
d21, d22, d23 = model2.params[['x1', 'x2', 'x3']]

Y3 = df["y3"]
X3 = df[["x1", "x2", "x3"]]
model3 = sm.OLS(Y3, X3).fit()
d31, d32, d33 = model3.params[['x1', 'x2', 'x3']]
""",
"""
y1_hat = d11*df["x1"] + d12*df["x2"] + d13*df["x3"]
y2_hat = d21*df["x1"] + d22*df["x2"] + d23*df["x3"]
y3_hat = d31*df["x1"] + d32*df["x2"] + d33*df["x3"]

model1 = sm.OLS(df["y1"], pd.concat([y3_hat, df["x2"]], axis=1)).fit()
b11, b12 = model1.params

model2 = sm.OLS(df["y2"], pd.concat([y1_hat, df["x3"]], axis=1)).fit()
a21, b21 = model2.params

model3 = sm.OLS(df["y3"], pd.concat([y2_hat, df["x1"]], axis=1)).fit()
a31, b31 = model3.params
"""]], 1: ['1. Временные ряды 1)Предварительный анализ временных рядов. Построить график и провести визуальный анализ. Результаты описать. ',[

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t, f
""",
"""
df = pd.read_csv('Задача1.csv')
df = df.apply(lambda x: x.apply(lambda y: float(y.replace(',', '.')) if type(y) == str else y))
""",
"""
plt.plot(df['T'], df['EMPLDEC_Y тыс.чел'])
plt.ylabel('CNSTR_C_M млрд. руб.', fontsize=14)
plt.xlabel('t', fontsize=14)
plt.grid()
plt.show()
""",
"""
Визуально похоже на то, что присутсвует некий тренд, а также не похоже, что имеются аномальные значения
""",
"""
2.Провести выявление аномальных наблюдений с помощью использования распределения Стьюдента, Метода Ирвина. Написать выводы. Использовать один метод на выбор.
""",
"""
Поиск Аномалий с помощью распределения Стьюдента
""",
"""
n = df.shape[0]
y = df.iloc[:, -1]
y_star = y[np.argmax(abs(y - y.mean()))]
t_hat = (y_star - y.mean()) / y.std()
t_kr_05 = t(n - 2).ppf(1 - 0.05 / 2)
t_kr_001 = t(n - 2).ppf(1 - 0.001 / 2)
lower_bound = t_kr_05 * (n - 1) ** 0.5 / ((n - 2 + t_kr_05 ** 2) ** 0.5)
upper_bound = t_kr_001 * (n - 1) ** 0.5 / ((n - 2 + t_kr_001 ** 2) ** 0.5)

""",
"""
if t_hat <= lower_bound:
    print("Наблюдение нельзя считать аномальным")
elif lower_bound < t_hat <= upper_bound:
    print("Наблюдение можно считать аномальным, если в пользу этого имеются и другие выводы, например другие методы")
else:
    print("Наблюдение признается аномальным")
""",
"""
Особенностью применения метода является то, что данные, к которым применяется
метод, должны быть близки к нормальному распределению для наибольшей
эффективности. Однако часто данные не распределены нормально, из-за чего
распределение Стьюдента чувствительно к размеру выборки и не подходит для малых
объёмов (по центральной предельной теореме с увеличением выборки данные стремятся
к нормальному распределению)
""",
"""
# Метод Ирвина
S_y = y.std(ddof=1)
lmd_t = abs(y.diff().values) / S_y
""",
"""
alpha 0.05: crit_value = 2.8 для n = 2, 2.2 для n = 3, 1.5 для n = 10, 1.3 для n = 20, 1.2 n = 30, 1.1 n = 50, 1.0 n = 100, 
alpha 0.01: 3.7 для n = 2, 2.9 для n = 3, 2 для n = 10, 1.8 для n = 20, 1.7 n = 30, 1.6 n = 50, 1.5 n = 100
""",
"""
crit_value = 1.3
df['is_anomaly'] = lmd_t > crit_value
df 
""",
"""
df['is_anomaly'].sum() 
# У нас нет значений которые можно считать аномальными,
# в случае если бы они были, то необходимо было заменить значение на средние между двумя соседними
""",
"""
3)Провести проверку наличия тренда с помощью: Критерия серий, основанный на медиане,
Метода проверки разности средних уровней, Метода Фостера-Стьюарта. Использовать один метод на выбор.
""",
"""
# Критерий серий, основанный на медиане
med = np.median(y)
ser = []
for el in y:
    if el > med:
        ser.append('+')
    elif el < med:
        ser.append('-')
ser
mx, cnt, cnt_ser = 1, 1, 0
for i in range(len(ser) - 1):
    if ser[i] == ser[i + 1]:
        cnt += 1
    else:
        cnt_ser += 1
        mx = max(mx, cnt)
        cnt = 1
mx = max(mx, cnt)
cnt_ser += 1
mx, cnt_ser

""",
"""
if mx >= 3.3 * (np.log(n) + 1) or cnt_ser <= 1/2 * (n + 1 - 1.96 * np.sqrt(n - 1)):
    print('Ряд имеет тренд')
else:
    print('Ряд тренда не имеет')
#Данный метод стоит применять в совокупности с другими, если визуально тренд нельзя наблюдать.
""",
"""
# Метод проверки разности средних уровней
n1 = n // 2
n2 = n - n1
m1_ = y[: n1].mean()
m2_ = y[n1: ].mean()
v1_ = y[: n1].var(ddof=1)
v2_ = y[n1: ].var(ddof=1)
F = max(v1_, v2_) / min(v1_, v2_)
if F > f(n1 - 1, n2 - 1).isf(0.05):
    print("Метод не может дать ответа")
else:
    s = np.sqrt(((n1 - 1) * s1_ + (n2 - 1) * s2_) / (n1 + n2 - 2))
    t_hat = abs(m1_ - m2_) / (s * np.sqrt(1/n1 + 1/n2))
    if t_hat > t(n1 + n2 - 2).isf(0.05):
        print('Тренд присутсвует')
    else:
        print("Тренда нет")
""",
"""
Данный метод применим только для рядов с монотонной тенденцией. Помимо этого,
результат метода может зависить от разбиения на подвыборки в 1-ом пункте. Метод
подходит для малых выборок
""",
"""
# Метод Фостера-Стьарта
ki = np.array([int(y[i] > max(y[:i])) for i in range(1, n)])
li = np.array([int(y[i] < min(y[:i])) for i in range(1, n)])
s = sum(ki + li)
d = sum(ki - li)
mu = (1.69 * np.log(n) - 0.299) / (1 - 0.035 * np.log(n) + 0.0027 * np.log(n) ** 2)
s1 = np.sqrt(2 * np.log(n) - 3.4253)
s2 = np.sqrt(2 * np.log(n) - 0.8456)
ts = (s - mu) / s1
td = s / s2
if ts > t(n).isf(0.05):
    print('Тренд ряда присутсвует')
else:
    print('Тренд ряда отсутсвует')
if td > t(n).isf(0.05):
    print('Тренд дисперсии ряда присутсвует')
else:
    print('Тренддисперсии  ряда отсутсвует')
""",
"""
Данный метод является универсальным, даёт более надёжные результаты, чем остальные,
а также позволяет выявить тренд дисперсии.
""",
"""
4)Провести сглаживание временных рядов с помощью:  Взвешенной (средневзвешенной) скользящей средней,  а также провести Экспоненциальное сглаживание. Привести аналитические выводы.
""",
"""
weights = np.array([1, 1, 1]) 
y_smooth_slide = np.convolve(y, weights/sum(weights), 'valid')
y_smooth_slide[:3]
""",
"""
plt.plot(df['T'].iloc[2:-2], y_smooth_slide, label='Сглаженный ряд')
plt.plot(df.iloc[:, 0], df.iloc[:, 1], label='Исходный ряд')
plt.title('Взвешенная (средневзвешенная) скользящая средняя по 5 точкам');
plt.xlabel('t', fontsize=14)
plt.grid()
plt.legend()
plt.show()
""",
"""
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing
y_smooth_exp20 = SimpleExpSmoothing(y, initialization_method="heuristic").fit(
    smoothing_level=0.2, optimized=False).fittedvalues
y_smooth_exp42 = SimpleExpSmoothing(y, initialization_method="heuristic").fit(
    smoothing_level=0.42, optimized=False).fittedvalues
y_smooth_exp60 = SimpleExpSmoothing(y, initialization_method="heuristic").fit(
    smoothing_level=0.6, optimized=False).fittedvalues
y_smooth_exp[:3]
""",
"""
plt.plot(df['T'], y_smooth_exp20, label='Сглаженный ряд alpha = 0.2')
plt.plot(df['T'], y_smooth_exp42, label='Сглаженный ряд alpha = 0.42')
plt.plot(df['T'], y_smooth_exp60, label='Сглаженный ряд alpha = 0.6')
plt.plot(df.iloc[:, 0], df.iloc[:, 1], label='Исходный ряд')
plt.title('Экспоненциальное сглаживание');
plt.xlabel('t', fontsize=14)
plt.grid()
plt.legend()
plt.show()
""",
"""
Для выявления основной тенденции 
изменения исследуемой величины используют сглаживани, а значит нам подходит больше всего экспоненциальное сглаживание с параметрами 0.42 поскольку тренд остается тем же, но при этом уже нет мелких случайных колебаний 
"""]], 2: ['2. Кривая роста. 1)Провести прогнозирование с помощью кривой роста. Рассчитать точечный и интервальный прогноз на 6 периода вперед. (10 баллов). 2) Моделирование тренд-сезонных процессов. Применить Модель Хольта-Уинтерса. (10 баллов). 3)Выделение компонент тренд-сезонного временного ряда. Метод Четверикова: По заданным значениям временного ряда y_t .',
[
'''
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import warnings
import matplotlib.pyplot as plt
from scipy.stats import t
from numpy.polynomial.polynomial import Polynomial
from statsmodels.tsa.holtwinters import ExponentialSmoothing

warnings.filterwarnings("ignore")
''',

'''
data = pd.read_excel("Задача экзамен ПМ22-3.xlsx", sheet_name='Вариант21', usecols='a:b')

plt.plot(data.y);
''',

''' 
# выбор кривой роста
y = np.array(data.y)

def calculate_derivatives(data):
    delta_yt = (data[2:] - data[:-2]) / 2
    delta2_yt = (delta_yt[1:] - delta_yt[:-1]) / 2
    return delta_yt, delta2_yt

delta_yt, delta2_yt = calculate_derivatives(y)

# Функции для различных кривых роста
def poly_first_order(x, a, b):
    return a * x + b

def poly_second_order(x, a, b, c):
    return a * x**2 + b * x + c

def poly_third_order(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

def exponential(x, a, b):
    return a * np.exp(b * x)

def modified_exponential(x, a, b, c):
    return a * np.exp(b * x) + c

def gompertz_curve(x, a, b, c):
    return a * np.exp(-b * np.exp(-c * x))

def logistic_curve(x, a, b, c):
    return a / (1 + np.exp(-b * (x - c)))

# Список кривых и соответствующих функций
curves = {
    'Полином первого порядка': (poly_first_order, 2),
    'Полином второго порядка': (poly_second_order, 3),
    'Полином третьего порядка': (poly_third_order, 4),
    'Экспонента': (exponential, 2),
    'Модифицированная экспонента': (modified_exponential, 3),
    'Кривая Гомперца': (gompertz_curve, 3),
    'Логистическая кривая': (logistic_curve, 3)
}
''',

'''
best_fit = None
best_fit_name = ""
lowest_mse = np.inf
xdata = np.arange(len(y))

for name, (func, params_count) in curves.items():
    if len(y) >= params_count:
        try:
            # Находим параметры кривой методом наименьших квадратов
            popt, _ = curve_fit(func, xdata, y, maxfev=10000)
            
            # Вычисляем среднюю квадратическую ошибку
            residuals = y - func(xdata, *popt)
            mse = np.mean(residuals**2)
            
            # Сравниваем с лучшим результатом
            if mse < lowest_mse:
                lowest_mse = mse
                best_fit = popt
                best_fit_name = name
                print(lowest_mse)
        except Exception as e:
            print(f"Не удалось подобрать кривую {name}: {e}")

print(f"Лучшая кривая роста: {best_fit_name}")
print(f"Параметры: {best_fit}")\

''',

'''
plt.figure(figsize=(10, 6))  

plt.plot(y, color='black', linestyle='-', linewidth=1, marker='.', markersize=7, label='y')
plt.title('y', fontsize=14)
plt.xlabel('Время (ti)', fontsize=14)
plt.ylabel('Значение y', fontsize=14)
plt.xlim(0, len(y) - 1)
plt.ylim(min(y) - np.std(y), max(y) + np.std(y))
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

plt.show()
''',

'''
n = len(y)  # Количество наблюдений
time_index = np.arange(n) 

def poly1(t, a0, a1):
    return a0 + a1*t

def poly2(t, a0, a1, a2):
    return a0 + a1*t + a2*t**2

def poly3(t, a0, a1, a2, a3):
    return a0 + a1*t + a2*t**2 + a3*t**3

models = [
    (poly1, 'Полином 1-го порядка'),
    (poly2, 'Полином 2-го порядка'),
    (poly3, 'Полином 3-го порядка'),
]

# t-значения для 95% доверительного интервала
t_value = t.ppf(0.975, df=n-2)
time_index_extended = np.arange(n + 6) # на 6 периодов вперед


for i, (model_func, name) in enumerate(models, start=1):
    params, pcov = curve_fit(model_func, time_index, y)
    fitted_model = lambda t: model_func(t, *params)
    
    # Расчет доверительных интервалов для исходных данных
    y_pred = fitted_model(time_index)
    mean_x = np.mean(time_index)
    se = np.sqrt(1/n + (time_index - mean_x)**2 / np.sum((time_index - mean_x)**2))
    ci = t_value * np.sqrt(np.diag(pcov))[:, np.newaxis] * se
    lower_bound = y_pred - ci
    upper_bound = y_pred + ci
    
    # Расчет предсказаний на 6 шагов вперед
    future_pred = fitted_model(time_index_extended[-6:])
    future_se = np.sqrt(1/(n+4) + (time_index_extended[-6:] - mean_x)**2 / np.sum((time_index - mean_x)**2))
    future_ci = t_value * np.sqrt(np.diag(pcov))[:, np.newaxis] * future_se
    future_lower_bound = future_pred - future_ci
    future_upper_bound = future_pred + future_ci

    plt.figure(figsize=(10, 6))
    plt.plot(y, color='black', linestyle='-', linewidth=1, marker='.', markersize=7, label='y')

    plt.plot(time_index, y_pred, 'r-', label=name)
    plt.plot(time_index_extended[-6:], future_pred, 'g--',linewidth=1, marker='.', markersize=7,  label=name + ' (Прогноз)')
    plt.fill_between(time_index, lower_bound[0], upper_bound[0], color='pink', alpha=0.3, label='95% доверительный интервал')
    plt.fill_between(time_index_extended[-6:], future_lower_bound[0], future_upper_bound[0], color='lightgreen', alpha=0.3, label='95% доверительный интервал (Прогноз)')
    plt.title('y', fontsize=16)
    plt.xlabel('Время (t)', fontsize=14)
    plt.ylabel('Значение индекса', fontsize=14)
    plt.ylim(min(y) - np.std(y), max(y) + np.std(y))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(loc='upper left', fontsize=12)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

plt.tight_layout()
plt.show()
''',


'''
# применение модели Брауна
brown_model = ExponentialSmoothing(y, trend='additive').fit()

# Прогнозирование 6 следующих
brown_forecast = brown_model.forecast(6)
time_index_extended = np.arange(n + 6)

plt.figure(figsize=(10, 6)) 
plt.plot(y, color='black', linestyle='-', linewidth=1, marker='.', markersize=7, label='y')
plt.plot(time_index, y_pred, 'r-',  label=name)
plt.plot(time_index_extended[n:], brown_forecast, 'g--',linewidth=1, marker='.', markersize=7,  label='Прогноз Брауна')

plt.title('y', fontsize=16)
plt.xlabel('Время (t)', fontsize=14)
plt.ylabel('Значение индекса', fontsize=14)
plt.ylim(min(y) - np.std(y), max(y) + np.std(y))
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(loc='upper left', fontsize=12)
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

plt.tight_layout()
plt.show()
''',

'''
# применением адаптивной модели прогнозирования Хольта-Уинтерса с учетом тренда и сезонности
# Здесь предполагается, что у нас есть сезонные данные, и мы должны указать период сезонности.
# Например, если данные имеют годовую сезонность, period=12 для месячных данных.
holt_winters_model = ExponentialSmoothing(y, trend='additive', seasonal='additive', seasonal_periods=4).fit()

# Прогнозирование следующих 6 значений
holt_winters_forecast = holt_winters_model.forecast(24)
time_index_extended = np.arange(n + 24)

plt.figure(figsize=(10, 6))  # Размер фигуры
plt.plot(y, color='black', linestyle='-', linewidth=1, marker='.', markersize=7, label='y')
plt.plot(time_index_extended[n:], holt_winters_forecast, 'g--',linewidth=1, marker='.', markersize=7,  label='Прогноз Хольта-Уинтерса')
plt.title('y', fontsize=16)
plt.xlabel('Время (t)', fontsize=14)
plt.ylabel('Значение индекса', fontsize=14)
plt.ylim(min(y) - np.std(y), max(y) + np.std(y))
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(loc='upper left', fontsize=12)
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

plt.tight_layout()
plt.show()
''',

'''
# Этап 1: Предварительная оценка тренда (ср. хронологическое)
def preliminary_trend_estimation(y, T=4):
    n = len(y)
    trend_preliminary = np.array([(y[i] + y[i+1]) / 2 for i in range(n - 1)])
    start = 0
    end = n - 1
    return trend_preliminary, start, end


# Этап 2: Нормирование отклонений
def normalize_deviations(y, trend_preliminary, start, end, T=4):
    deviations = y[start:end] - trend_preliminary
    years = len(deviations) // T
    normalized_deviations = np.zeros_like(deviations)
    for i in range(years):
        year_slice = slice(i*T, (i+1)*T)
        sigma_i = np.std(deviations[year_slice])
        normalized_deviations[year_slice] = deviations[year_slice] / sigma_i if sigma_i != 0 else deviations[year_slice]
    return normalized_deviations


trend_preliminary, start, end = preliminary_trend_estimation(y)
normalized_deviations = normalize_deviations(y, trend_preliminary, start, end)

# Посмотрим на результаты до построения диаграмм
trend_preliminary[:5], normalized_deviations[:5], start, end
''',

'''
# Построение диаграммы исходного ряда и предварительного тренда

plt.figure(figsize=(14, 6))
plt.plot(y, label='Исходный ряд', color='blue')
trend_indexes = np.arange(start, end)
plt.plot(trend_indexes, trend_preliminary, label='Предварительный тренд', color='red', linestyle='--')

plt.title('Исходный ряд и предварительный тренд')
plt.xlabel('Время')
plt.ylabel('Значения')
plt.legend()
plt.grid(True)

plt.show()
''',

'''
t = np.arange(y.shape[0])

def preliminary_seasonal_wave(normalized_deviations, T=4):
    m = len(normalized_deviations) // T
    S_j1 = [np.mean(normalized_deviations[j::T]) for j in range(T)]
    return np.tile(S_j1, m), S_j1

def first_trend_estimate(y, S_j1, start, end, T=4):
    adjusted_len = end - start - 1  # -1 для вычитания второго элемента
    adjusted_y = y[start:end-1] - np.tile(S_j1[:T], (adjusted_len // T) + 1)[:adjusted_len]
    f_ij1 = np.array([(adjusted_y[i] + adjusted_y[i+1]) / 2 for i in range(len(adjusted_y) - 1)])
    return f_ij1

def second_trend_estimate(f_ij1, T=4):
    f_ij2 = np.convolve(f_ij1, np.ones(5)/5, mode='valid')
    return f_ij2
''',

'''
trend_preliminary, start, end = preliminary_trend_estimation(y)
normalized_deviations = normalize_deviations(y, trend_preliminary, start, end)
S_j1_full, S_j1 = preliminary_seasonal_wave(normalized_deviations)
f_ij1 = first_trend_estimate(y, S_j1, start, end)
f_ij2 = second_trend_estimate(f_ij1)

# Этап 6: Новые отклонения и окончательная средняя сезонная волна
f_ij2_full = np.pad(f_ij2, (start + 4, len(y) - (start + 4 + len(f_ij2))), 'edge')
seasonal_component_1 = np.tile(S_j1[:4], (len(y) + 3) // 4)[:len(y)]
residual = y - f_ij2_full - seasonal_component_1

# Этап 7: Вторая сезонная волна
deviations_after_first_trend = y - f_ij2_full
normalized_deviations_after_first_trend = normalize_deviations(deviations_after_first_trend, np.zeros_like(deviations_after_first_trend), 0, len(deviations_after_first_trend))
S_j2_full, S_j2 = preliminary_seasonal_wave(normalized_deviations_after_first_trend)
seasonal_component_2 = np.tile(S_j2[:4], (len(y) + 3) // 4)[:len(y)]

plt.figure(figsize=(18, 18))
plt.subplot(4, 1, 1)
plt.plot(y, label='Исходный ряд', color='blue')
plt.plot(f_ij2_full, label='Вторая оценка тренда', color='purple', linestyle='--')
plt.plot(f_ij1, label='Первая оценка тренда',  linestyle='--')
plt.title('Исходный ряд и тренды')
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(seasonal_component_1, label='Первая сезонная компонента', color='orange')
plt.title('Первая сезонная компонента')
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(seasonal_component_2, label='Вторая сезонная компонента', color='red')
plt.title('Вторая сезонная компонента')
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(residual, label='Остаточная компонента', color='green')
plt.title('Остаточная компонента')
plt.legend()

plt.tight_layout()
plt.show()''']],
4: ["""4. Построить  модель, используя панельные данные, для прогнозирования коэффициента рождаемости с учетом специфики регионов РФ.
1) составить спецификацию моделей (Pool, RE, FE (5 баллов), 2)построить три типа моделей панельных данных, провести аналитическое исследование качества модолей. (10 баллов) 3)провести сравнительный анализ моделей, используя тесты Фишера, Хаусмана,Бреуша-Пагана. Сделать выводы.(5 баллов) 4)Построить прогноз по лучшей модели (выбор обосновать). Результаты моделирования и прогнозирования изобразить на графике. (10 баллов) (или 4)Рассчитайте фиксированные эффекты для каждого представленного региона (10 баллов), но это есть внутри пункта 1 и 2)""",
[
r'''
import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, PooledOLS, RandomEffects
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
import seaborn as sns
v = 5 #свой варик
data = pd.read_excel('файл_своё_имя.xlsx', f'Вариант{v}')
''',
'''
data = data[list(filter(lambda x: 'Unnamed' not in x,data.columns))]
all_years = data['Год'].unique()
''',
'''
# если много данных или если не делаем прогноз на годы, которых нет в данных, то юзаем:
years_to_test = [2019]
test_data = data[data['Год'].isin(years_to_test)]
data = data[~data['Год'].isin(years_to_test)]
''',
'''
data = data.set_index(['Название региона', 'Год'])
data = data.sort_values(by=['Название региона', 'Год'])
data
''',
'''
y_perems = 'КОЭФ РОЖД НА 1000 ЧЕЛ'
X_perems = ['БЕЗРАБОТИЦА', 'СООТНОШЕНИЕ Б/Р', 'ИПЦ НА ЖИЛЬЕ', 'ИПЦ НА ПРОД ТОВАРЫ']
''',
'''
plt.figure(figsize=(14, 8))

regions = data.reset_index()['Название региона'].unique()

for region in regions:
    region_data = data.reset_index()[data.reset_index()['Название региона'] == region]

    # Линия фактических данных
    sns.lineplot(data=region_data.reset_index(), x='Год', y='КОЭФ РОЖД НА 1000 ЧЕЛ', marker='o', label=f'{region}')

plt.title('КОЭФ РОЖД НА 1000 ЧЕЛ по регионам')
plt.xlabel('Год')
plt.xticks(all_years)
plt.ylabel('КОЭФ РОЖД НА 1000 ЧЕЛ')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.show()
''',
'''
# вообще хз особо выводы не сделаешь, но мало ли
data.corr()
''',
'''
X = data[X_perems]
y = data[y_perems]
''',
'''
# Модель с общим эффектом (Pooled OLS, POOL)
model_pool = PooledOLS(y, X).fit()
model_pool.summary
# спецификация как лин рег
''',
'''
## Зависящая переменная
$ Y_{it} $ - имя таргета

## Независимые переменные
1)$ X_{1it} $ - имя_переменной_1
2)$ X_{2it} $ - имя_переменной_2
3)$ X_{3it} $ - имя_переменной_3
4)$ X_{4it} $ - имя_переменной_4

Коэффициент детерминации равен 0.9972, значимы все коэффициенты по t-статистике, высокая F-статистика. В итоге модель со случайными эффектами будет иметь вид:

$$
Y_{it} = 0.000 \cdot X_{1it} + 0.000 \cdot X_{2it} + 0.000 \cdot X_{3it} + 0.000 \cdot X_{4it} + \varepsilon_{it}
$$
''',
'''
# Модель со случайными эффектами (Random Effects, RE)
from linearmodels.panel import RandomEffects

model_re = RandomEffects(y, X).fit()
model_re.summary
''',

r'''
## Зависящая переменная
$ Y_{it} $ - имя таргета

## Независимые переменные
1)$ X_{1it} $ - имя_переменной_1
2)$ X_{2it} $ - имя_переменной_2
3)$ X_{3it} $ - имя_переменной_3
4)$ X_{4it} $ - имя_переменной_4

Коэффициент детерминации равен 0.9972, значимы все коэффициенты по t-статистике, высокая F-статистика. В итоге модель со случайными эффектами будет иметь вид:

$$
Y_{it} = \hat{\upsilon}_{it} + 0.000 \cdot X_{1it} + 0.000 \cdot X_{2it} + 0.000 \cdot X_{3it} + 0.000 \cdot X_{4it} + \varepsilon_{it}
$$

где $ \hat{\upsilon}_i $ - оцененные случайные эффекты для каждого региона. Ниже они представлены:
''',

'''
# Случайные эффекты
random_effects = model_re.estimated_effects
print(random_effects)
''',
'''
# Модель с фиксированными эффектами
from linearmodels.panel import PanelOLS

model_fe = PanelOLS(y, X, entity_effects=True).fit()
model_fe.summary
# спецификация как лин рег + FE.estimated_effects
''',
'''
## Зависящая переменная
$ Y_{it} $ - имя таргета

## Независимые переменные
1)$ X_{1it} $ - имя_переменной_1
2)$ X_{2it} $ - имя_переменной_2
3)$ X_{3it} $ - имя_переменной_3
4)$ X_{4it} $ - имя_переменной_4

Коэффициент детерминации равен 0.9972, значимы все коэффициенты по t-статистике, высокая F-статистика. В итоге модель со фиксированными эффектами будет иметь вид:

$$
Y_{it} = \hat{\mu}_{it} + 0.000 \cdot X_{1it} + 0.000 \cdot X_{2it} + 0.000 \cdot X_{3it} + 0.000 \cdot X_{4it} + \varepsilon_{it}
$$

где $ \hat{\mu}_{it} $ - оцененные константы для каждого региона. Ниже они представлены:

''',
'''
fixed_effects = model_fe.estimated_effects
print(fixed_effects)
''',
'''
# Тест Бреуша-Пагана (pool vs. RE)
from scipy.stats import f

RSSp = model_pool.resid_ss
RSSfe = model_fe.resid_ss

T = data.reset_index()['Год'].nunique()
k = len(X.columns)

n = len(y) / T
F = (RSSp - RSSfe) / (n - 1) / (RSSfe / (n * T - n - k))
F_cr = f(n - 1, n * T - n - k).isf(0.95)
F, F_cr
# если $F > F_{крит} \Rightarrow H_0$ отвергается, $\text{FE}$ лучше $\text{Pooled}$.
''',
'''
# Тест Бреуша-Пагана (pool vs. RE)
import statsmodels.stats.diagnostic as dg

_, _, _, pv = dg.het_breuschpagan(model_pool.resids, sm.add_constant(model_pool.model.exog.dataframe))

pv
# если pv < alpha, то остатки не гомоскедастичны (так как отвергается H_0), а значит RE лучше Pooled$.

''',
'''
# Тест Хаусмана (FE vs. RE)
import numpy.linalg as la
from scipy import stats

def hausman(fe, re):
    b = fe.params
    B = re.params
    v_b = fe.cov
    v_B = re.cov
    df = b.size
    chi2 = np.dot((b - B).T, la.inv(v_b - v_B).dot(b - B))
    pval = stats.chi2.sf(chi2, df)
    return chi2, pval

hausman(model_fe, model_re)

# если p-value < alpha, то есть достаточно высокого значения статистики хи-квадрат,
# оно попадает в критическую область и H_0 отвергается,
# поэтому между RE и FE лучше оказывается FE

''',
'''
# Это моделирование
future_predictions = model_re.predict()
future_predictions

# Прогноз теста, если он есть
# future_predictions = model_re.predict(exog=test_data[X_perems])
# print(future_predictions)


# если нужно тру предикт, то из тестов берём ar/arima/sarima/etc, отдельно предиктим все фичи для каждого региона в цикле, а потом коннектим это сюда и делаем прогноз, по нему не будет сравнения
''',
'''
# визуализация

import matplotlib.pyplot as plt
import seaborn as sns

# Получение уникальных регионов
regions = data.reset_index()['Название региона'].unique()

# Установка размеров фигуры и создание подграфиков
fig, axes = plt.subplots(len(regions)//2 + len(regions)%2, 2, figsize=(20, 8*len(regions)//2 + 8*len(regions)%2))
axes = axes.flatten()

for i, region in enumerate(regions):
    region_data = data.reset_index()[data.reset_index()['Название региона'] == region]

    # Линия фактических данных
    sns.lineplot(data=region_data.reset_index(), x='Год', y='КОЭФ РОЖД НА 1000 ЧЕЛ', marker='o', label=f'Фактические данные {region}', ax=axes[i])

    # Линия предсказанных данных
    #sns.lineplot(data=region_data.reset_index(), x='Время', y='Predicted', linestyle='--', marker='x', label=f'Прогноз {region}', ax=axes[i])

    # Прогнозные данные для будущих лет
    future_region_data = future_predictions.reset_index()[future_predictions.reset_index()['Название региона'] == region]
    axes[i].plot(future_region_data['Год'], future_region_data['fitted_values'], '--', marker='x', label=f'Будущий прогноз {region}')

    # Оформление графика
    axes[i].set_title(f'{region}')
    axes[i].set_xlabel('Год')
    axes[i].set_xticks(all_years)
    axes[i].set_ylabel('КОЭФ РОЖД НА 1000 ЧЕЛ')
    axes[i].legend(loc='upper left', bbox_to_anchor=(1, 1))

# Удаление пустых подграфиков, если количество регионов нечетное
if len(regions) % 2 != 0:
    fig.delaxes(axes[-1])

plt.tight_layout()
plt.show()
# идеи вывода:
# олег: ну напиши что данных мало хуево предиктит и тд…
# юрий: ну или типо наоборот что типо там тренд/сезонность продолжает еще че хз
''',
'''
# варик олега, но надо фиксить
import math

N = 3

num_plots = len(regions)
num_cols = N
num_rows = math.ceil(num_plots / num_cols)

fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 20))

for idx, reg in enumerate(regions):
    row = idx // num_cols
    col = idx % num_cols
    ax = axes[row, col] if num_rows > 1 else axes[col]

    temp_t = data.reset_index()[data.reset_index()['Название региона'] == reg]
    temp_p = test_data.reset_index()[test_data.reset_index()['Название региона'] == reg]

    ax.plot(temp_t['Год'], temp_t.values[:, 2], label='Истинное значение')
    ax.plot(temp_p['Год'], temp_p.values[:, 2], label='Прогноз')
    ax.set_xlabel('Год')
    ax.set_ylabel('Граница бедности')
    ax.legend()
    ax.set_title(f'Граница бедности, {reg}')
    ax.set_xticks(temp_t['Год'])
    ax.grid()

# Remove any empty subplots
for idx in range(num_plots, num_rows * num_cols):
    fig.delaxes(axes.flatten()[idx])

plt.tight_layout()
plt.show()
'''
        ]]}

        self.themes = [{values[0]:keys} for keys,values in self.sklad.items()]
    
    def search(self, text):
        ress = []
        for theme in self.themes:
            for key, value in theme.items():
                if text in key:
                    ress += [f"{key} : {value}"]
        return ress