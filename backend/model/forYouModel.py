import sys
import json
import limpeza as l
import pandas as pd


user_index = 10

if len(sys.argv) > 1:
    user_index = int(sys.argv[1])

df_job_info = pd.merge(l.df_job_superfit,l.df_job_details, on='job_opportunity_id', how='inner')
def remove_prefix(column_name):
    if column_name.startswith('score_'):
        return column_name[len('score_'):]
    else:
        return column_name
df_job_info = df_job_info.rename(columns=remove_prefix)

#Junção das tabelas atráves do id e separação das áreas de cada vaga/gestor
df_user_info = pd.merge(l.df_superfit_user,l.user_objectives, on = "id", how = "inner")
def remove_prefix(column_name):
    if column_name.startswith('superfit_'):
        return column_name[len('superfit_'):]
    else:
        return column_name

df_user_info = df_user_info.rename(columns=remove_prefix)

def remove_prefix(column_name):
    if column_name.startswith('improve_'):
        return column_name[len('improve_'):]
    else:
        return column_name

df_cursos = l.df_cursos.rename(columns=remove_prefix)

df_cursos_for_you = df_cursos.drop(columns = ["plataforma",	"neg",	"emp",	"tech"])
#_______________________________________________________________________________________________________________________
#recomendação

usuario = df_user_info.iloc[user_index].to_dict()
area_usuario = [area for area, valor in usuario.items() if valor == 1]
recomendacoes_por_area = {}

usuario = df_user_info.iloc[10].to_dict()
area_usuario = [area for area, valor in usuario.items() if valor == 1]
recomendacoes_por_area = {}

#abrir json com as importancias das competencias
with open('backend/model/feature_importance.json') as json_file:
    feature_importance_dict = json.load(json_file)
# Calcula as recomendações para cada área do usuário
for area in area_usuario:
    importancias_area = feature_importance_dict.get(area, {})  # Competências mais importantes para a área específica

    recomendacoes = []
    for caracteristica, importancia in importancias_area.items():
      limite_recomendacao = importancia * 5
      if usuario.get(caracteristica, 0) < limite_recomendacao:  # Se a pontuação do usuário na competência for menor do que a definida
            recomendacoes.append(caracteristica)


    recomendacoes_por_area[area] = recomendacoes
#Define quais competências
recomendar = {}
for area in recomendacoes_por_area:
    recomendar[area] = {
        "dis": 0,
        "int": 0,
        "eng": 0,
        "res": 0,
        "cur": 0,
        "sin": 0
    }

recomendacoes_sum = 0

for area, recomendacoes in recomendacoes_por_area.items():
    for recomendacao in recomendacoes:
        recomendar[area][recomendacao] += 1
        recomendacoes_sum += 1
df_recomendar = pd.DataFrame(recomendar).T

#Calcula as áreas de prefêrencia do usuário

user_area_preferences = df_recomendar.sum()

# Calcula a relevância de cada curso para a área
course_area_relevance = df_cursos_for_you.drop(columns=['id'])  # Remove the 'id' column
course_area_relevance = course_area_relevance * user_area_preferences  # Multiply by user preferences
# Calcula valores dos cursos
course_scores = course_area_relevance.sum(axis=1)

# Organiza e recomenda cursos
recommended_courses = df_cursos_for_you[['id']].copy()  # Create a new DataFrame with the 'id' column
recommended_courses['score'] = course_scores
recommended_courses = recommended_courses.sort_values(by='score', ascending= False)

melhorias = []

recomendations = recommended_courses["id"].to_list()

resp = []

for i in recomendations:
    name = l.df_cursos_name[l.df_cursos_name["id"] == i]["name"].to_string(index=False)
    resp.append(name)

print(resp)

