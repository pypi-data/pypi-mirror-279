import pyperclip as pc
    
def imports():
    s = '''import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import *
    '''
    return pc.copy(s)
    
def zarembki():
    s = '''Y_gmean = gmean(Y)
print(Y_gmean)
Y_ = Y / Y_gmean

X_with_c = sm.add_constant(X)
model = sm.OLS(Y_, X_with_c)
result = model.fit()
result.summary()

ESS1 = sum(result.resid**2)
print(ESS1)

X_with_c = sm.add_constant(X)
model = sm.OLS(np.log(Y_), X_with_c)
result = model.fit()
result.summary()

ESS2 = sum(result.resid**2)
print(ESS2)

Z = np.abs(len(X)/2 * np.log(ESS1/ESS2))
print(Z)
print(chi2(1).isf(0.05))
    '''
    return pc.copy(s)
    
def bokskoks():
    s = '''l = {}
for lam in range(1, 1001):
    lambd = lam/1000
    Y_ = Y/gmean(Y)
    Y_bc = Y_**lambd / lambd
    X_bc = X**lambd / lambd

    X_with_c = sm.add_constant(X_bc)
    model = sm.OLS(Y_bc, X_with_c)

    result = model.fit()
    l[result.ssr] = lambd
    print(l[min(l.keys())])
#параметр λ→0, то функция принимает вид F=lny Выбираем полулогарифмическую модель
    '''
    return pc.copy(s)

def shwarz():
    s = '''X_with_c = sm.add_constant(X)
model = sm.OLS(Y, X_with_c)
result = model.fit()
ESS = result.ssr
BIC = np.log(ESS/len(X)) + np.log(len(X))/len(X) + 1 + np.log(2*np.pi)
print(BIC)

X_with_c = sm.add_constant(X)
model = sm.OLS(np.log(Y), X_with_c)
result = model.fit()
ESS = result.ssr
BIC = np.log(ESS/len(X)) + np.log(len(X))/len(X) + 1 + np.log(2*np.pi)
print(BIC)
#чем меньше по модулю число, тем лучше
    '''
    return pc.copy(s)
    
def akaike():
    s = '''X_with_c = sm.add_constant(X)
model = sm.OLS(Y, X_with_c)
result = model.fit()
ESS = result.ssr
AIC = np.log(ESS/len(X)) + 2/len(X) + 1 + np.log(2*np.pi)
print(AIC)

X_with_c = sm.add_constant(X)
model = sm.OLS(np.log(Y), X_with_c)
result = model.fit()
ESS = result.ssr
AIC = np.log(ESS/len(X)) + 2/len(X) + 1 + np.log(2*np.pi)
print(AIC)
#чем меньше по модулю число, тем лучше
    '''
    return pc.copy(s)
    
def mkwhitedavidson():
    s = '''X_with_c = sm.add_constant(X)
model = sm.OLS(Y, X_with_c)
result = model.fit()
Y_pred = result.predict(X_with_c)

X_with_c = sm.add_constant(X)
model = sm.OLS(np.log(Y), X_with_c)
result = model.fit()
LNY_pred = result.predict(X_with_c)

X_with_c = sm.add_constant(np.array(list(zip(X, (Y_pred-np.e**LNY_pred)))))
model = sm.OLS(np.log(Y), X_with_c)
result = model.fit()
result.summary()

X_with_c = sm.add_constant(np.array(list(zip(X, (LNY_pred - np.log(Y_pred))))))
model = sm.OLS(Y, X_with_c)
result = model.fit()
result.summary()

#Если theta1 = 0 не отвергается, а theta2 = 0 отвергается, выбирается полулогар модель
#Если theta2 = 0 не отвергается, а theta1 = 0 отвергается, выбирается линейная модель
    '''
    return pc.copy(s)

def logit_probit():
    s = '''X0 = sm.add_constant(X)
log_reg0 = sm.Logit(Y, X0)
result = log_reg0.fit()
result.summary()

prob = sm.Probit(Y, X0)
result_prob = prob.fit()
result_prob.summary() 

Y_pred = result.predict(X0)
Y_pred[Y_pred > 0.5] = 1
Y_pred[Y_pred < 0.5] = 0
accuracy_score(Y, Y_pred)
f1_score(Y, Y_pred)
    '''
    return pc.copy(s)

def tobit_heckit():
    s = '''install.packages('AER')
data <- read.csv("tobit.csv", header = TRUE, stringsAsFactors = TRUE, sep=';')
``
require(ggplot2)
f <- function(x, var, bw = 20) {
  dnorm(x, mean = mean(var), sd(var)) * length(var)  * bw
}
p <- ggplot(data, aes(x = apt))
p + stat_bin(binwidth=10) + stat_function(fun = f, size = 1, args = list(var = data$apt))

train <- data[0:160, ]
test <- data[161:200, ]

library(AER)
model = tobit(apt ~ read + math +prog, data = train, right=800, left=200)

summary(model)

y_pred <- test['read'] * 2.54207 + test['math'] * 5.85932 + test['prog'] * 24.46143 + 152.52400

MSE <- sum((y_pred - test['apt'])**2)/40
MSE

R2 <- with(test, cor(y_pred, apt))
R2

plot <-plot(test$apt, col = "green", ylim = c(0, max(test$apt, y_pred$read)), xlab = "Наблюдения", ylab = "Значения")
points(y_pred, col = "black")
legend("topright", legend = c("Реальные значения", "Предсказанные значения"), col = c("green", "black"), pch = 1)

if (!require("sampleSelection")) {
  install.packages("sampleSelection")
  library("sampleSelection")
}

heckit <- heckit(data=data, selection = d ~ read + math + prog, outcome = apt ~ read + math +prog)
summary(heckit)

y_pred1 = 175.82327354 + 2.61170331*test['read'] + 5.25718171*test['math'] + 24.42492773 * test['prog']
MSE <- sum((y_pred1 - test['apt'])**2)/40
MSE

R2 <- with(test, cor(y_pred1, apt))
R2

plot <-plot(test$apt, col = "green", ylim = c(0, max(test$apt, y_pred1$read)), xlab = "Наблюдения", ylab = "Значения")
points(y_pred1, col = "black")
legend("topright", legend = c("Реальные значения", "Предсказанные значения"), col = c("green", "black"), pch = 1)

#Можно сделать вывод,
#что для нашего датасета лучше подойдет Tobit модель, так как она имеет более высокий R^2
#И значение MSE меньше, чем у heckit модели.
#Но так как разница в показателях минимальна, можно сказать, что спецификация модели heckit является очень схожей с моделью Tobit.
#Нужно делать дальнейшее исследование и строить новые модели.
    '''
    return pc.copy(s)

def kriteriy_seriy_median():
    s = '''
def func_me(x):
    if x > Me:
        return 1
    elif x < Me:
        return -1
    else:
        return 0

Y_t = df['EX_NON-CIS_Y'].copy().sort_values()
Me = np.median(Y_t)
Y_t_signs = Y_t.apply(func_me).sort_index()
Y_t_signs

i = 0
current = 2
max_lenght = 0
count_serias = 0
current_cnt = 0
while i < len(Y_t_signs):
    # print(Y_t_signs.iloc[i], current, max_lenght)
    if Y_t_signs.iloc[i] == current:
        current_cnt += 1
    else:
        current = Y_t_signs.iloc[i]
        count_serias += 1
        max_lenght = max(current_cnt, max_lenght)
        current_cnt = 1
    i += 1

print(max_lenght, count_serias)

max_lenght < 3.3 * (np.log(n) + 1) and count_serias > 0.5 * (n + 1 - 1.96*(n-1)**0.5)
#False => условие о случайности ряда не выполняется => можно говорить о наличии тренда
    '''
    return pc.copy(s)
    
def anomalii_student():
    s = '''data1 = data.copy()
ind = np.argmax(abs(data1['UNEMPL_Y_SH'] - data1['UNEMPL_Y_SH'].mean()))
y_m = data1.iloc[ind][1]
tau = abs(y_m - data1['UNEMPL_Y_SH'].mean()) / data1['UNEMPL_Y_SH'].std(ddof=0)
print(tau)

alpha = 0.05
n = len(data1)
tau_an = t.ppf(1 - alpha/2, n-2) * (n - 1)**0.5 / (n - 2 + t.ppf(1 - alpha/2, n-2)**2)**0.5
print(tau_an)

alpha = 0.001
n = len(data1)
tau_an = t.ppf(1 - alpha/2, n-2) * (n - 1)**0.5 / (n - 2 + t.ppf(1 - alpha/2, n-2)**2)**0.5
print(tau_an)
#Если наше tau меньше обоих, то не выброс
#Если между, то значение может быть не признанно аномалией, так как визуальный анализ говорит об адекватности данных.
#Если больше обоих, то выброс
    '''
    return pc.copy(s)
    
def ber_makaler():
    s = '''X_with_c = sm.add_constant(X)
model = sm.OLS(Y, X_with_c)
result = model.fit()
Y_pred = result.predict(X_with_c)

X_with_c = sm.add_constant(X)
model = sm.OLS(np.log(Y), X_with_c)
result = model.fit()
LNY_pred = result.predict(X_with_c)
#


X_with_c = sm.add_constant(X)
model = sm.OLS(np.e**LNY_pred, X_with_c)
result = model.fit()
v1 = result.resid
#

X_with_c = sm.add_constant(X)
model = sm.OLS(np.log(Y_pred), X_with_c)
result = model.fit()
v2 = result.resid
#

X_with_c = sm.add_constant(np.array(list(zip(X, v1))))
model = sm.OLS(np.log(Y), X_with_c)
result = model.fit()
result.summary()
#

X_with_c = sm.add_constant(np.array(list(zip(X, v2))))
model = sm.OLS(Y, X_with_c)
result = model.fit()
result.summary()
#
#Если $\theta_1 = 0$ не отвергается, а $\theta_2 = 0$ отвергается выбирается полулогарифмическая модель.
#Если $\theta_2 = 0$ не отвергается, а $\theta_1 = 0$ отвергается, выбирается линейная модель.
#Возникает проблема если обе гипотезы отвергаются или не отвергаются.
    '''
    return pc.copy(s)
    
def foster_stuart():
    s = '''plt.plot(data['Date'], data['Close'])
plt.grid()
plt.scatter(data['Date'], data['Is Outlier'] * 300, color='r')# 300 - среднее значение наших иксов 
#

data4 = data.copy()
#

Kt = [1]
Lt = [1]
arr = data4.Close.values
for i in range(1, len(arr)):
    if arr[i] >= max(arr[:i]):
        Kt.append(1)
    else:
        Kt.append(0)
        
        
    if arr[i] <= min(arr[:i]):
        Lt.append(1)
    else:
        Lt.append(0)

#
data4['Kt'] = Kt
data4['Lt'] = Lt
#
sigma1 = (2*np.log(len(arr)) - 3.4253)**0.5
sigma2 = (2*np.log(len(arr)) - 0.8456)**0.5
#
mu = (1.693872*np.log(len(arr)) - 0.299015) / (1-0.035092 * np.log(len(arr)) + 0.002705*np.log(len(arr))**2)
#
t_s = np.abs(s - mu) / sigma1
t_d = np.abs(d - 0)/sigma2
t_s, t_d
#
t_kr = t.ppf(1-0.05/2, len(arr) - 2)
t_kr
#
t_s > t_kr # если тру, то делаем вывод о наличии тренда ряда
t_d > t_kr #  если тру, то делаем вывод о наличии тренда дисперсии
    '''
    return pc.copy(s)

def ARMA():
    s = '''adfuller(Y)# ряд не стационарный
from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(Y, period=12)
Y_stac = result.resid.dropna()
plt.plot(result.resid)
adfuller(Y_stac) # ряд стал стационарным

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(Y_stac.diff().dropna().values.squeeze(), lags=25, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(Y_stac.diff().dropna(), lags=25, ax=ax2)

from statsmodels.tsa.arima.model import ARIMA

import warnings
warnings.filterwarnings("ignore")
best_model = None
best_params = [0, 0]
best_metrics = [1e9, 1e9]
for p in range(1, 5):
    for q in range(1, 5):
        model = ARIMA(Y_stac, order=(p, 0, q))
        results = model.fit()
        print(f'p={p}, q={q}, AIC={results.aic}, BIC={results.bic}')
        if (results.aic + results.bic)/2 < sum(best_metrics)/2:
            best_metrics = results.aic, results.bic
            best_model = model
            best_params = [p, q]

print(f'\n\n\nBEST MODEL\n')
print(f'p={best_params[0]}, q={best_params[1]}, AIC={best_metrics[0]}, BIC={best_metrics[1]}')

model = ARIMA(Y_stac, order=(best_params[0], 0, best_params[1]))

results = model.fit()
Y_pred = results.predict(len(X), len(X)+10)

plt.figure(figsize=(15, 6))
plt.plot(Y_stac.index, Y_stac)
plt.plot(Y_pred.index, Y_pred, 'r')
    '''
    return pc.copy(s)
    
def panel_data():
    s = '''from linearmodels.panel import RandomEffects, PooledOLS, PanelOLS
data.set_index(['Reg', 'Year'], inplace=True)
data

exog_vars = ["X1", "X2", "X3", "X4", "X5", "X6", "t"]
exog = sm.add_constant(data[exog_vars])

mod = PooledOLS(data.Y, exog)
pooled_res = mod.fit()
pooled_res

mod = PanelOLS(data.Y, exog, entity_effects=True)
fe_res = mod.fit()
fe_res

mod = RandomEffects(data.Y, exog)
re_res = mod.fit()
re_res

#F-статистика
F_test = ((pooled_res.resid_ss - fe_res.resid_ss)/(len(data)-1)) / (fe_res.resid_ss / (len(data)*3-len(data)-7))
F_test
Так как F_test=51.485 > F_крит => делаем выбор в пользу модели FixedEffect


#Тест Хаусмана
def hausman_test(fixed, random):
    b = fixed.params
    B = random.params
    v_b = fixed.cov
    v_B = random.cov
    df = b[np.abs(b) < 1e8].size
    chi2 = np.dot((b - B).T, la.inv(v_b - v_B).dot(b - B))
    pval = stats.chi2.sf(chi2, df)
    return chi2, df, pval

hausman_results = hausman_test(fe_res, re_res)
print(f'Chi^2: {str(hausman_results[0])}')
print(f'Степени свободы: {str(hausman_results[1])}')
print(f'p-value: {str(hausman_results[2])}')
# Так как p-value < 0.05 => делаем выбор в пользу модели FixedEffect


#Тест Бреуша-Пагана
# Остатки и предсказанные значения из модели Pooled
pooled_residuals = pooled_res.resids
pooled_fitted = pooled_res.fitted_values
pooled_residuals; pooled_fitted

sigma2_u = re_res.variance_decomposition[1]; sigma2_u
exog = sm.add_constant(pooled_fitted)
exog = np.column_stack((exog, pooled_fitted**2))

from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(pooled_residuals, exog); bp_test
#Так как p-value < 0.05 => делаем выбор в пользу модели RandomEffect
    '''
    return pc.copy(s)
    
def topolog_regr():
    s = '''from sklearn.cluster import KMeans
y = data['data'][:, 0]
X = data['data'][:, 1:]
kmeans = KMeans(n_clusters=2, random_state=42, n_init="auto").fit(X)
kl_pred = kmeans.predict(X)
filtered_label0 = data['data'][kl_pred == 0]
plt.scatter(filtered_label0[:,1] , filtered_label0[:,0], color='red', marker='.')
filtered_label1 = data['data'][kl_pred == 1]
plt.scatter(filtered_label1[:, 1] , filtered_label1[:, 0], color='blue', marker='.')
plt.show()

y_0 = filtered_label0[:, 0]
X_0 = filtered_label0[:, 1:]

y_1 = filtered_label1[:, 0]
X_1 = filtered_label1[:, 1:]
X_0_c = sm.add_constant(X_0)
model_0 = sm.OLS(y_0, X_0_c).fit()
model_0.summary()
X_1_c = sm.add_constant(X_1)
model_1 = sm.OLS(y_1, X_1_c).fit()
model_1.summary()#должны быть значимыми коэффы
def Topolog_Regr(X, kmean_fit=kmeans, models=[]):
    classter_pred = kmean_fit.predict(X)
    if classter_pred[classter_pred == 0].shape[0] > classter_pred[classter_pred == 1].shape[0]:
        claster = 0
    else:
        claster = 1
        X = X[:, :-1]
        
    if X.shape[0] > 1:
        X_with_c = sm.add_constant(X)
        y_pred = models[claster].predict(X_with_c)
    else:
        X = pd.DataFrame(X)
        X['c']=1
        y_pred = models[claster].predict(X)
        
    result_model = {"R^2": round(models[claster].rsquared, 3),
                   "F": round(models[claster].fvalue, 3),
                   "t-значения": models[claster].tvalues}
    
    return claster, y_pred, result_model
Topolog_Regr(np.array([[2,10,0]]), kmean_fit=kmeans, models=[model_0, model_1])

y_pred0 = Topolog_Regr(X_0, kmean_fit=kmeans, models=[model_0, model_1])[1]
plt.plot(y_0)
plt.plot(y_pred0, color='r')
plt.legend(['data', 'predict'])
y_pred1 = Topolog_Regr(X_1, kmean_fit=kmeans, models=[model_0, model_1])[1]
plt.plot(y_1)
plt.plot(y_pred1, color='r')
plt.legend(['data', 'predict'])
    '''
    return pc.copy(s)
   
    
def logit_probit_full():
    s = '''import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
import seaborn as sns
#специф логит $p(x)=\frac{1}{1+e^{-(\beta_0+\beta_1x}}$
#специф пробит $P(y_i = 1) = \Phi(z_i) = \Phi(\beta_1 + \beta_2x_i^{(2)} + ... + \beta_kx_i^{(k)})$
df = ...
X = ...
Y = ...
X_train, X_test, y_train, y_test = train_test_split(X, Y)
sns.heatmap(df.corr(), annot = True) #выбрать все, у которых высокая корреляция c Y
#если хотите VIF-test

X0 = sm.add_constant(X_train)
log_reg0 = sm.Logit(y_train, X0)
result = log_reg0.fit()
result.summary()

prob = sm.Probit(Y, X0)
result_prob = prob.fit()
result_prob.summary() 

Y_pred = result.predict(sm.add_constant(X_test)) #для пробита тоже сделать
Y_pred[Y_pred > 0.5] = 1
Y_pred[Y_pred < 0.5] = 0
#прогнозная достоверность
accuracy_score(y_test, Y_pred)

result.get_margeff().summary() #доля каждого фактора в модели
#dy/dx - насколько увеличивается вероятность принадлежности к классу при увеличении одного параметра на единицу
    '''
    return pc.copy(s)
    
def irvin():
    s = '''result = pd.DataFrame()  
y = df['EX_NON-CIS_Y']
n = len(y)
result['EX_NON-CIS_Y'] = y

# Вычисляем среднеквадратическое отклонение
S_y = np.sqrt(sum([(y[i] - y.mean()) ** 2 for i in range(n)]) / (n - 1))

# Вычисляем величину l_t для наблюдений
l_t = [0] + [abs(y[i] - y[i - 1]) / S_y for i in range(1, n)]
result['lambda'] = l_t

# Если величина l_t превышает табличный уровень, то значение y_t считается аномальным
difference = df['EX_NON-CIS_Y'].diff()
lamb = np.abs(difference)/S_y
l_kririch = 1.478*(n/10)**(-0.1767)

result_normal = result[result['lambda'] <= l_kririch]  # Убираем аномалии из таблицы

# Проводим анализ по методу Ирвина
anomalies = result[result['lambda'] > l_kririch]
num_anomalies = len(anomalies)

if num_anomalies == 0:
    print("Аномалий не обнаружено.")
else:
    print(f"Обнаружено {num_anomalies} аномалий:")
    print(anomalies)

# Отобразим таблицу без аномалий
print("\nТаблица без аномалий:")
print(result_normal)

#Используя метод Ирвина проанализировани датасет на аномальные значения. Таких не оказалось => Датасет оставляем без изменений.
    '''
    return pc.copy(s)
    
def mov_average():
    s = '''def mov_average(data, k = 5, a = 0.5, T = 12):
    #Принимает одномерный массив и параметры сглаживания
    #Возвращает 3 массива обычного, экспоненц, среднехронолог сглаживания

    # среднеарифметическая скользящая средняя по k точкам
    SMA = data.rolling(window=k).mean() 
    # экспоненц. среднее с a параметром сглаживания
    EMA = data.ewm(alpha=a).mean()

    # среднехронологическое с периодом T = 12 (год)
    sr_hronolog = np.array([0]*len(data))
    i = 0
    i_i = T//2
    while i_i <= len(data):
    try:
      sr_hronolog[i_i] = np.sum(np.sum(data.values[i+1:i+T]) + data.values[i]/2 + data.values[i+T+1]/2) / T
    except:
      pass
    i += 1
    i_i += 1
    return SMA, EMA, sr_hronolog
    '''
    return pc.copy(s)
    
def analiz_vrem_ryada():
    s = '''import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import *
df = ...
plt.plot(df['T'], df['EX_NON-CIS_Y'])
#1. Мультипликативная/аддитивная модель (аддитивная разброс не меняется (разброс примерно одинаково идет), мультипликативная разброс меняется)
#2. Тренд восходящий/убывающий/отсутствует (скорее всего, восходящий тренд)
#3. Нестационарный/стационарный (стационарный - хаотичные движения в окресности нуля, иначе нестационарный / будет нестационарный 99%)

#аномалии стьюдент - вызвать anomalii_student() / либо ирвин irvin()

#наличие тренда - критерий медиан kriteriy_seriy_median()

#сглаживание средним или экспоненциальным - mov_average()
#построить 2 графика для каждого вида сглаживания
#Вывод: экспоненциальное сглаживание лучше улавливает колебания, а скользящее среднее сглаживает все колебания ряда
    '''
    return pc.copy(s)
    
def kriv_rosta():
    s = '''import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import sklearn.metrics as m
import seaborn as sns
df = ...
plt.plot(df['Y'])
#Для выбора кривой роста
plt.plot(np.array(Y_new[1:]) - np.array(Y_new[:-1]))
#постоянна => линейная
#линейна => полином 2 порядка

temp = np.array(Y_new[1:]) - np.array(Y_new[:-1])
plt.plot(temp[1:] - temp[:-1])
#постоянна => линейная
#линейна => полином 3 порядка

plt.plot((np.array(Y_new[1:]) - np.array(Y_new[:-1]))/np.array(Y_new[1:]))
#постоянна => экспонента
#Для предсказываний
X = list(range(1, len(df) + 1))
X0 = sm.add_constant(X)

model = sm.OLS(df['CNSTR_C_M'], X0).fit()
model.summary()

#Линейная функция
for i in range(1, 5):
  print(f'Прогноз на {i} доп период: {a0 + (len(df) + i) * a1:.2f}')
  
def calculate_U_k(n, k, t_alpha, t_bar, epsilon, m):
    S_y_hat = np.sqrt(np.sum(epsilon**2) / (n - m - 1))
    
    sum_term = np.sum((np.arange(1, n + 1) - t_bar)**2)
    
    U_k = S_y_hat * t_alpha * np.sqrt(1 + 1/n + (n + k - t_bar)**2 / sum_term)
    return U_k
    
U_k = calculate_U_k(len(df), 4, 0.05, np.mean(X), model.resid, 1) #4 кол-во периодов прогноза, 1 - кол-во иксов
print("U(k):", U_k)  
 
for i in range(1, 5):
  print(f'Интервальный прогноз на {i} доп период: {(a0 + (len(df) + i) * a1) - U_k:.2f}, {(a0 + (len(df) + i) * a1) + U_k:.2f}')
    '''
    return pc.copy(s)
    
def braun():
    s = '''first8 = sm.OLS(df['Y'][:8], X0[:8]).fit()
first8.summary()

#ОТМЕТКА
model_params = [list(first8.params)] * 8
beta = 0.5 #random
df['t'] = list(range(1, len(df) + 1))
df['y'] = df['Y']

for i in range(8, len(df)):
    y_pred = model_params[-1][0] + model_params[-1][1] * df.iloc[i].t
    error = df.iloc[i].y - y_pred
    temp = [0, 0]
    temp[0] = model_params[-1][0] + model_params[-1][1] + (1 - beta) ** 2 * error
    temp[1] = model_params[-1][1] + (1 - beta) ** 2 * error
    model_params.append(temp)
    
model_params = np.array(model_params)
y_pred = model_params[:, 0] + model_params[:, 1] * df.t
plt.xlabel('t, период времени')
plt.ylabel('y')
plt.plot(df.t, y_pred)
plt.plot(df.t, df.y)
#КОНЕЦ ОТМЕТКИ

#ПОДБОР БЕТА
res = []
first8 = sm.OLS(df[:8].y, sm.add_constant(df[:8].t)).fit()
for beta in np.linspace(0, 1, 1000):
    model_params = [list(first8.params)] * 8
    for i in range(8, len(df)):
        y_pred = model_params[-1][0] + model_params[-1][1] * df.iloc[i].t
        error = df.iloc[i].y - y_pred
        temp = [0, 0]
        temp[0] = model_params[-1][0] + model_params[-1][1] + (1 - beta) ** 2 * error
        temp[1] = model_params[-1][1] + (1 - beta) ** 2 * error
        model_params.append(temp)
    model_params = np.array(model_params)
    y_pred = model_params[:, 0] + model_params[:, 1] * df.t
    res.append(np.sum((df.y - y_pred) ** 2))
print(np.argmin(res) / 1000, min(res)) #подобрали бета
#проделываем то же самое от отметки, меняя бета на подобранную
    '''
    return pc.copy(s)

def chetverikov_func():
    s = '''
def Chetverikov(t, y, L):
    y_reshaped = np.array(y).reshape(-1, L)
    chrono_mean = (0.5 * y_reshaped[:, 0] + np.sum(y_reshaped[:, 1:-1], axis=1) + 0.5 * y_reshaped[:, -1]) / L
    l1 = y_reshaped - chrono_mean[[[i]*L for i in range(len(chrono_mean))]]
    l1_2 = l1 ** 2
    sigma1 = np.sqrt((np.sum(l1_2, axis=1) - np.sum(l1, axis=1) ** 2 / L) / (L - 1))
    l1_norm = l1 / sigma1[[[i]*L for i in range(len(chrono_mean))]]
    s1 = np.mean(l1_norm, axis=0)

    f1 = y_reshaped - s1[[list(range(0, L)) for i in range(len(y_reshaped))]] * sigma1[[[i]*L for i in range(len(chrono_mean))]]
    f2 = [np.nan] * (int(0.5 * L) - 1)

    for i in range(int(0.5 * L), len(f1.reshape(-1)) + 1):
        f2.append(np.mean(f1.reshape(-1)[i - int(0.5 * L): i]))
    for i in range(int(0.5 * L) - 1):
        f2[i] = f1[i, 0]
    
    f2 = np.array(f2).reshape(-1, L)

    l2 = y_reshaped - f2

    l2_2 = l2 ** 2

    sigma2 = np.sqrt((np.sum(l2_2, axis=1) - np.sum(l2, axis=1) ** 2 / L) / (L - 1))
    l2_norm = l2 / sigma2[[[i]*L for i in range(len(chrono_mean))]]

    s2 = np.mean(l2_norm, axis=0)

    eps = l2 - s2[[list(range(0, L)) for i in range(len(y_reshaped))]] * sigma2[[[i]*L for i in range(len(chrono_mean))]]

    k = np.sum(l2_2 * eps, axis=1) / np.sum(eps ** 2, axis=1)

    return {'chrono_mean': chrono_mean[[[i]*L for i in range(len(chrono_mean))]].reshape(-1),  
            'f1': f1.reshape(-1), 
            'f2': f2.reshape(-1), 
            's1': s1, 
            's2': s2, 
            'eps': eps.reshape(-1)}
    '''
    return pc.copy(s)
    
def chetverikov():
    s = '''#сначала импортируем chetverikov_func()
res = Chetverikov(df.t, df.y, 12) #если кварталы то 4, месяцы - 12
plt.figure(figsize=(8, 8))
plt.suptitle('Диаграммы тренда')
plt.subplots_adjust(hspace=0.5)
titles = ['Исходный ряд', 'Предварительная оценка тренда', 'Первая оценка тренда', 'Вторая оценка тренда']
for i, col in enumerate([df.y, res['chrono_mean'], res['f1'], res['f2']]):
    plt.subplot(4, 1, i + 1)
    plt.title(titles[i])
    if i == 3:
        plt.xlabel('t, период времени')
    plt.grid(alpha=0.5, linestyle='--')
    plt.plot(df.t, col, c=('orange' if i else 'blue'))
    
plt.figure(figsize=(10, 7))
plt.suptitle('Диаграммы сезонной волны')
plt.subplots_adjust(hspace=0.5)
titles = ['Первая оценка сезонности', 'Вторая оценка сезонности']
for i, col in enumerate([res['s1'], res['s2']]):
    plt.subplot(3, 1, i + 1)
    if i < 2:
        plt.plot(np.arange(1, 13), col, c=('red' if i else 'lightgreen'), linewidth=1) #если кварталы то вместо 13 ставим 5
    else:
        plt.plot(np.arange(1, 13), col[0], c='red', linewidth=1)
        plt.plot(np.arange(1, 13), col[1], c='lightgreen', linewidth=1)
        
plt.figure(figsize=(10, 5))
plt.title('Остаточная компонента')
plt.grid()
plt.plot(df.t, res['eps'], c='g')
    '''
    return pc.copy(s)
    
def holt_w():
    s = '''import sklearn.metrics as m
def HolterWinter(y, alpha, beta, gamma, L, data_offset=None):
    a = [y[0]]
    b = [0]
    F = [1] * L

    for i in range(1, L):
        a_temp = alpha * (y[i] / 1) + (1 - alpha) * (a[i - 1] + b[i - 1])
        b_temp = beta * (a_temp - a[i - 1]) + (1 - beta) * b[i - 1]

        a.append(a_temp)
        b.append(b_temp)
    
    for i in range(L, len(y[:data_offset])):
        a_temp = alpha * (y[i] / F[i - L]) + (1 - alpha) * (a[i - 1] + b[i - 1])
        b_temp = beta * (a_temp - a[i - 1]) + (1 - beta) * b[i - 1]
        F_temp = gamma * (y[i] / a_temp) + (1 - gamma) * F[i - L]

        a.append(a_temp)
        b.append(b_temp)
        F.append(F_temp)

    return map(np.array, [a, b, F])

alpha, beta, gamma = 0.5, 0.5, 0.5 #от пизды
a, b, F = HolterWinter(df.y, alpha, beta, gamma, 4)

y_pred = (a + b) * F
y_pred, len(y_pred)

plt.figure(figsize=(10, 5))
plt.title(f'Модель Холтера-Уинторса ({alpha=}, {beta=}, {gamma=})')
plt.xlabel('t, период времени')
plt.ylabel('y')
plt.plot(df.t, y_pred, c='orange')
plt.plot(df.t, df.y, c='blue')

m.r2_score(y_pred, df.y) #хороший r^2
    '''
    return pc.copy(s)
    
def ARIMA():
    s = '''from statsmodels.tsa.stattools import adfuller
print(adfuller(data)) # не стационарный, pvalue большое

# доходность 
data2 = (data[1:].values - data[:-1].values)/data[:-1].values
print(adfuller(data2)) # стационарный, pvalue маленькое
 
fig = plt.figure(figsize=(15, 10))
ig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
# график автокореляционной функции
fig = sm.graphics.tsa.plot_acf(data2, lags=25, ax=ax1) 
ax2 = fig.add_subplot(212)
# график частной автокореляционной функции
fig = sm.graphics.tsa.plot_pacf(data2, lags=25, ax=ax2)
plt.show()

def autocovariance(x, lag):
    n = len(x)
    mean = np.mean(x)
    cov = np.sum((x[:n-lag] - mean) * (x[lag:] - mean)) / n
    return cov

lags = np.arange(20)  # Вычисление автоковариации для 20 лагов
autocovariances = [autocovariance(data2, lag) for lag in lags]
plt.figure(figsize=(10, 5))
plt.stem(lags, autocovariances, use_line_collection=True)
plt.show()

# расчёт AR(1), AR(2), ARMA(1, 1)
from statsmodels.tsa.arima.model import ARIMA
arma1 = ARIMA(data2, order = (1, 0, 0)).fit()
arma2 = ARIMA(data2, order = (2, 0, 0)).fit()
arma3 = ARIMA(data2, order = (1, 0, 1)).fit()
arma1.bic, arma2.bic, arma3.bic
arma1.aic, arma2.aic, arma3.aic
# Выбирается та, где меньше aic и bic по модулю

# перебор параметров ARMA для нахождения лучшей
best_params = (0, 0)
best_aic_bic = 10000

for p in range(1, 5):
  for q in range(1, 5):
    arma = ARIMA(data2, order = (p, 0, q))
    arma = arma.fit()
    if (arma.aic + arma.bic) / 2 <  best_aic_bic:
      best_params = (p, q)
      best_aic_bic = (arma.aic + arma.bic) / 2

    '''
    return pc.copy(s)
    
def check_rank():
    s = '''
def check(mat, endog=2):
    """
    Проверка матрицы на идентифицируемост

    Args:
        mat (матрица): Матрица коэфициентов
        endog (int, optional): Количество Y. Defaults to 2.

    Returns:
        bool: Является ли идентифицируемой
    """    
    for i in range(mat.shape[0]):
        pos0 = np.where(np.array(mat[i, :])[0] == 0)[0]
        v = list(range(mat.shape[0]))
        v.remove(i)
        submat = mat[v, list(pos0)]
        print(submat, f"rang = {submat.shape[0]}")
        if submat.shape[0] < endog - 1:
            return False
    return True
check(mat, 2)
    '''
    return pc.copy(s)
    
def pravilo_poryadka():
    s = '''$𝐴𝐷𝐼𝐷𝐴𝑆=𝑎_0+𝑎_1 𝑡+ 𝑎_2 𝑡^2+𝑎_3 𝑃𝑈𝑀𝐴+𝑢_1$
#k - кол-во всех иксов во всех уравнениях (в том числе константа)
#p - кол-во Y конкретно в этом уравнении
#q - кол-во иксов конкретно в этом уравнении из всех иксов     
𝑘 = 4, 𝑝 = 2, 𝑞 = 3    
𝑘− 𝑝 ≥ 𝑞 − 1     
4 − 2 ≥ 3 − 1 (идентифицируемо если =, если > то сверхидентифицируемо)
    '''
    return pc.copy(s)
 
def pravilo_ranga():
    s = '''a0, a1, a2, a3,  b0, b1, b2, b3, c0, c1, c2, c3, u1, u2, u3 = symbols('a0 a1 a2 a3 b0 b1 b2 b3 c0 c1 c2 c3 u1 u2 u3')
A = Matrix([[1, 0, -a3], [-b2, 1, 0], [-c2, -c3, 1]])
B = Matrix([[-a0, -a1, 0, -a2], [-b0, -b1, 0, 0], [-c0, 0, -c1, 0]])
AB = Matrix.hstack(A, B)
AB

R1 = Matrix([[0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0]])
R2 = Matrix([[0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]])

AB * R2.T

m = 3 #кол-во всех Y

print((AB*R1.T).rank(), (AB*R2.T).rank(), m - 1) #если все равны то норм
    '''
    return pc.copy(s)
    
def gretl():
    s = '''
system
    equation Apple const SP500 Microsoft t
    equation Nvidia const  SP500 t
    equation Microsoft const Apple Microsoft t
    equation SP500 const Apple Nvidia Microsoft t
end system
    '''
    return pc.copy(s)