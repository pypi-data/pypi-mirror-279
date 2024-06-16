from NFuzMatrix import *
import pandas as pd
import pickle  # сохрание и загрузка состояния нейросети

df_train = pd.read_csv("Train.csv")
x = df_train[["AT", "V"]]
y = df_train["PE"]

nfm = NFM(x, y, level=logging.DEBUG)
nfm.defuzzification = "Simple"

AT = nfm.create_feature("Температура", "C", 0, 38, True)
V = nfm.create_feature("Разрежение выхлопных газов", "cm Hg", 25, 82, True)
PE = nfm.create_feature("Генерация электроэнергии", "MW", 430, 510, False)

p_AT_low = nfm.create_predicate(AT, 'Низкая', func=Points, params=[[0, 0], [4, 1], [9, 1]])
p_AT_normal1 = nfm.create_predicate(AT, 'Средняя1', func=Points, params=[[8, 0], [15, 1], [20, 0]])
p_AT_normal2 = nfm.create_predicate(AT, 'Средняя2', func=Points, params=[[17, 0], [20, 1], [23, 0]])
p_AT_high = nfm.create_predicate(AT, 'Высокая', func=Points, params=[[22, 0], [30, 1], [38, 0]])

p_V_normal = nfm.create_predicate(V, 'Среднее', func=Points, params=[[25, 0], [40, 1], [70, 0]])
p_V_high = nfm.create_predicate(V, 'Высокое', func=Points, params=[[60, 0], [70, 1], [82, 0]])

p_PE_450 = nfm.create_predicate(PE, 'Низкая', const=450)
p_PE_460 = nfm.create_predicate(PE, 'Средняя1', const=460)
p_PE_470 = nfm.create_predicate(PE, 'Средняя2', const=470)
p_PE_490= nfm.create_predicate(PE, 'Высокая1', const=490)
p_PE_500= nfm.create_predicate(PE, 'Высокая2', const=500)


r_1 = nfm.create_rule([p_AT_low], p_PE_500, 1)
r_2 = nfm.create_rule([p_AT_normal1], p_PE_490, 1)
r_3 = nfm.create_rule([p_AT_normal2, p_V_normal], p_PE_470, 1)
r_4 = nfm.create_rule([p_AT_normal2, p_V_high], p_PE_460, 1)
r_5 = nfm.create_rule([p_AT_high, p_V_normal], p_PE_460, 1)
r_6 = nfm.create_rule([p_AT_high, p_V_high], p_PE_450, 1)


# nfm.show_view(True)
nfm.train(epochs=5, k=0.1)
nfm.show_view(True)
nfm.show_errors(True)

# Коэффициент детерминации (R²)
y_mean = np.mean(y)
ss_res = np.sum((y - nfm.matrix_y) ** 2)
ss_tot = np.sum((y - y_mean) ** 2)
r2 = 1 - (ss_res / ss_tot)
print("r2: ", r2)

# сохранения состояния нейросети
with open('NeuFuzMatrix_model.pkl', 'wb') as f:
    pickle.dump(nfm, f)