import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import limpeza as l
import sys
#Retirar cursos de empresas


target_user_id = l.user_objectives['id'].iloc[10]

if len(sys.argv) > 1:
    target_user_id = l.user_objectives['id'].iloc(int(sys.argv[1]))

df_cursos = l.df_cursos.rename(columns={'id': 'journey_id'})
df_cursos.sort_values(by='journey_id', ascending=True)

#Retirar cursos de empresas
df_cursos = df_cursos.rename(columns={'id': 'journey_id'})
df_cursos.sort_values(by='journey_id', ascending=True)


df_user_journeys = l.df_user_journeys
user_objectives = l.user_objectives.rename(columns={'id': 'user_id'})

user_course_data = pd.merge(user_objectives, df_user_journeys, on='user_id', how='inner')

pivot_df = pd.pivot_table(user_course_data, index='journey_id', columns='user_id', values=['Administrativo', 'Comercial / Vendas', 'Engenharia', 'Finanças / Contabilidade', 'Jurídico', 'Logistica / Supply Chain', 'Marketing / Comunicação', 'Produção / Operações', 'RH', 'Saúde', 'Tecnologia'], aggfunc='sum', fill_value=0)

# Calculate the sums of how many users from each area have completed each course
sums_by_area = pivot_df.groupby(level=0, axis=1).sum()

# Reset the index to have courses as rows
sums_by_area.reset_index(inplace=True)


#Normalização dos dados
journeys_id = sums_by_area['journey_id']
lista1 = sums_by_area.drop(labels='journey_id', axis=1)

journeys_id = sums_by_area['journey_id']
standard = StandardScaler()

# Para normalizar os dados de 0 a 1
scaler = MinMaxScaler()
lista1 = scaler.fit_transform(lista1)
df_relevance_courses = pd.DataFrame(lista1, columns=['Administrativo', 'Comercial / Vendas','Engenharia', 'Finanças / Contabilidade', 'Jurídico',
                                                     'Logistica / Supply Chain', 'Marketing / Comunicação', 'Produção / Operações', 'RH', 'Saúde', 'Tecnologia'
])

df_relevance_courses['journey_id'] = journeys_id.reset_index(drop=True)
df_relevance_courses = df_relevance_courses[['journey_id', 'Administrativo', 'Comercial / Vendas','Engenharia', 'Finanças / Contabilidade', 'Jurídico',
                                             'Logistica / Supply Chain', 'Marketing / Comunicação', 'Produção / Operações', 'RH', 'Saúde', 'Tecnologia'
]]

area_compet = df_cursos.merge(df_relevance_courses, left_on='journey_id', right_on='journey_id', how='inner')
area_compet = area_compet.sort_values(by='journey_id', ascending=True)


areas = ['Administrativo', 'Comercial / Vendas','Engenharia', 'Finanças / Contabilidade', 'Jurídico',
         'Logistica / Supply Chain', 'Marketing / Comunicação', 'Produção / Operações', 'RH', 'Saúde', 'Tecnologia']
areas_courses = {}

for target_area in areas:
  # Classifica o DataFrame pelo valor de relevância para a área alvo em ordem decrescente
  relevance_journey = df_relevance_courses[['journey_id', target_area]].sort_values(by=target_area, ascending=False)

  # Obtem os 10 cursos mais relevantes para a área alvo
  mosts_relevants = relevance_journey.head(10)

  # Combinar as informações de relevância com as informações de nome do curso
  mosts_relevants = mosts_relevants.merge(l.df_cursos_completo[['id', 'name']], left_on='journey_id', right_on='id')

  # Remover a coluna de ID redundante
  mosts_relevants = mosts_relevants.drop(columns=['id'])

  database_most_relevants = pd.DataFrame(mosts_relevants)

  areas_courses[target_area] = database_most_relevants

skills = ['improve_eng', 'improve_tech',	'improve_cur',	'improve_int', 'improve_dis',	'improve_neg',	'improve_sin',	'improve_res']
target_areas = []
list_result_journey = []

relevance_journey = df_relevance_courses[['journey_id', target_area]].sort_values(by=target_area, ascending=False)
relevance_journey = relevance_journey[['journey_id']]
watched_journey = df_user_journeys["journey_id"][df_user_journeys['user_id'] == target_user_id].to_list()

#printar tipo de watched_journey
# Descobre as áreas de interesse do usuário
for area in areas:
  target_area = int(user_objectives[area][user_objectives['user_id'] == target_user_id])
  if target_area == 1:
    target_areas.append(area)

quant = 10 % len(target_areas)


# Recomenda 10 cursos para cada usuário detre aqueles mais relevantes em sua área, um curso para cada habilidade desenvolvida
while len(list_result_journey) < 11:
  print(len(list_result_journey))
# for i in range (1, 10):
  # print(len(list_result_journey))
  for skill in skills:
    # print(skill)
    count_skill = 0
    for target_area in target_areas:
      count_area = 0
      # print(target_area)
      for journey_id in relevance_journey['journey_id'].to_list():
        if journey_id not in list_result_journey and journey_id not in watched_journey and count_skill < 1:
          list_result_journey.append(journey_id)
          count_skill += 1
          count_area += 1


print(list_result_journey) # saída = id dos cursos recomendados