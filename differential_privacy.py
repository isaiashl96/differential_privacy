import pandas as pd
import numpy as np
from scipy.stats import pearsonr

data = pd.read_csv('BARRANCA-BARRANCA-LIMA-5.csv', sep=',', header=0)
#rint data.dtypes

matriz_tmp = pd.pivot_table(data, values=['MONTO_RATING'], index=['CLIENTE1'], columns=['CODCOMERCIO'])
matriz_tmp = matriz_tmp.fillna(0)
matriz_ratings = matriz_tmp.values

usuario = matriz_ratings[0,:]


'''GROUPING PHASE'''

def calc_probability(usuario, matriz_ratings, epsilon):

    lista_usuarios = matriz_ratings[1:,]
    #print len(lista_usuarios)

    probability_list = []
    for u_t in lista_usuarios:
        a = np.exp(epsilon*pearsonr(usuario, u_t)[0]/2)

        lista_den = []
        for i in range(0, len(matriz_ratings)):
            lista_den.append(np.exp(epsilon*pearsonr(u_t, matriz_ratings[i,:])[0]/2))
        b = np.sum(lista_den)

        probability = a/b
        probability_list.append(probability)

    return probability_list

lista_probabilidades = calc_probability(usuario, matriz_ratings, 1)
lista_probabilidades /= np.sum(lista_probabilidades)

indices = list(range(len(lista_probabilidades)))
selected_indexes = np.random.choice(indices,20, p=lista_probabilidades)

selected_users = list()
for index in selected_indexes:
    selected_users.append(matriz_ratings[index,:])

#print selected_users

rating_pool = list()
lista_rating_pool = list()
for user in selected_users:

    for rating in user:
        if rating != 0:
            rating_pool.append(rating)
    lista_rating_pool.append(rating_pool)
    rating_pool = list()

print lista_rating_pool

'''MODIFICATION PHASE'''
friends_list = list()
for i in range(len(matriz_ratings)):
    friends_list.append(np.random.randint(100, size=np.random.randint(100, size=1)))

friends_dictionary = dict()
indices_friends = list(range(len(friends_list)))
for i in range(len(indices_friends)):
    friends_dictionary[indices_friends[i]] = friends_list[i]

#print friends_dictionary

#def calc_probability2(rating_usuario, alpha, rating_pool):

