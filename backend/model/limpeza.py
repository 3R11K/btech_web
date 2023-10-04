import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path


user_superfit = pd.read_csv(Path.cwd() / 'backend' / 'model' / 'tabelas'/ 'user_superfit_inteli.csv')
superfit_copy = user_superfit.copy()

columns_to_drop = ['user_id', 'key']

# Strip leading/trailing whitespaces from column names
superfit_copy .columns = superfit_copy .columns.str.strip()

id_column = superfit_copy['user_id']
key_column = superfit_copy['key']

# Check if columns exist in the DataFrame before dropping
columns_to_drop = [col for col in columns_to_drop if col in superfit_copy.columns]
# Drop the specified columns
superfit_copy.drop(labels=columns_to_drop, inplace=True, axis=1)
lista1 = superfit_copy

standard = StandardScaler()
lista1

# Para normalizar os dados de 0 a 1
scaler = MinMaxScaler()
lista1 = scaler.fit_transform(lista1)
df_superfit_clean = pd.DataFrame(lista1, columns=['superfit_dis', 'superfit_sin', 'superfit_cur', 'superfit_int', 'superfit_eng', 'superfit_res'])
columns_to_check = ['superfit_dis', 'superfit_sin', 'superfit_cur', 'superfit_int', 'superfit_eng', 'superfit_res']
df_superfit_marked = df_superfit_clean.copy()

for column in columns_to_check:
    column_data = df_superfit_clean[column]  # Get the Series corresponding to the column
    Q1 = column_data.quantile(0.25)
    Q3 = column_data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Create a new column to mark outliers
    outlier_column = column + '_outlier'
    df_superfit_marked[outlier_column] = (column_data < lower_bound) | (column_data > upper_bound)

    # Replace outliers with the mean of the column
    df_superfit_marked.loc[df_superfit_marked[outlier_column], column] = df_superfit_clean[column].mean()

outlier_counts = df_superfit_marked[columns_to_check].sum()
superfit_copy = superfit_copy.reset_index(drop=True)
df_superfit_user = df_superfit_marked.drop(labels=['superfit_dis_outlier',	'superfit_sin_outlier',	'superfit_cur_outlier',	'superfit_int_outlier',	'superfit_eng_outlier',	'superfit_res_outlier' ], axis=1)
df_superfit_user['user_id'] = id_column.reset_index(drop=True)
df_superfit_user['key'] = key_column.reset_index(drop=True)

df_superfit_user = df_superfit_user[['user_id', 'superfit_dis', 'superfit_sin', 'superfit_cur', 'superfit_int', 'superfit_eng', 'superfit_res']].drop_duplicates(subset="user_id").sort_values(by="user_id")

df_superfit_user = df_superfit_user.rename(columns={"user_id": "id"})

user_objectives = pd.read_csv( Path.cwd() / 'backend' / 'model' / 'tabelas'/"user_interests_inteli.csv")
user_objectives = pd.get_dummies(user_objectives, columns = ["name"], prefix=[''])
user_objectives = user_objectives.rename(columns={'user_id':'id'})
user_objectives = user_objectives.groupby('id').sum().reset_index().rename(columns=lambda x: x.lstrip('_'))
user_id_obj = user_objectives['id']

df_job_superfit = pd.read_csv(Path.cwd() / 'backend' / 'model' / 'tabelas'/'job_opportunity_superfit_consolidates.csv')
columns_to_drop = ['id', 'job_opportunity_id', 'created_at', 'updated_at', 'average_distance']

id = df_job_superfit['id']
job_opp = df_job_superfit['job_opportunity_id']
created = df_job_superfit['created_at']
update = df_job_superfit['updated_at']

# Check if columns exist in the DataFrame before dropping
columns_to_drop = [col for col in columns_to_drop if col in df_job_superfit.columns]

# Drop the specified columns
df_job_drop = df_job_superfit.copy()
df_job_drop.drop(labels=columns_to_drop, inplace=True, axis=1)
lista2 = df_job_drop

standard = StandardScaler()
lista2

# Para normalizar os dados de 0 a 1
scaler = MinMaxScaler()
lista2 = scaler.fit_transform(lista2)
df_job_clean = pd.DataFrame(lista2, columns=['score_res',	'score_eng',	'score_int',	'score_cur',	'score_sin',	'score_dis'])
columns_to_check = ['score_res',	'score_eng',	'score_int',	'score_cur',	'score_sin',	'score_dis']
df_job_marked = df_job_clean.copy()

for column in columns_to_check:
    column_data = df_job_clean[column]  # Get the Series corresponding to the column
    Q1 = column_data.quantile(0.25)
    Q3 = column_data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Create a new column to mark outliers
    outlier_column = column + '_outlier'
    df_job_marked[outlier_column] = (column_data < lower_bound) | (column_data > upper_bound)

    # Replace outliers with the mean of the column
    df_job_marked.loc[df_job_marked[outlier_column], column] = df_job_clean[column].mean()

outlier_counts = df_job_marked[columns_to_check].sum()

columns_drop =['score_res_outlier', 'score_eng_outlier', 'score_int_outlier', 'score_cur_outlier', 'score_sin_outlier', 'score_dis_outlier']
df_job_marked.drop(columns=columns_drop, inplace=True, axis=1)

df_job_marked['job_opportunity_id'] = job_opp
df_job_marked['created_at'] = created
df_job_marked['updated_at'] = update
df_job_superfit = df_job_marked[['job_opportunity_id', 'score_res',	'score_eng',	'score_int',	'score_cur',	'score_sin',	'score_dis']]

df_job_details = pd.read_csv(Path.cwd() / 'backend' / 'model' / 'tabelas'/"job_opportunity_details.csv")
df_job_details = df_job_details.drop(columns = ["descricao_vaga_area",	"inicio_inscricoes",	"termino_inscricoes",	"setor_empresa",	"name"])
df_job_details = pd.get_dummies(df_job_details, columns=['Interesses'])
df_job_details = df_job_details.rename(columns=lambda x: x.lstrip('Interesses_'))

columns_to_update = [
    'Administrativo', 'Comercial / Vendas', 'Engenharia', 'Juridico',
    'Logística / Supply Chain', 'Marketing / Comunicação', 'Produção / Operações',
    'RH', 'Saúde', 'Tecnologia'
]
df_subset = df_job_details[columns_to_update]

# Usar pd.get_dummies para converter True e False em 1 e 0
df_subset = df_subset.astype(int)

# Concatenar o DataFrame convertido de volta com o DataFrame original
df_job_details = pd.concat([df_job_details, df_subset], axis=1)

# Remover a coluna 'ALL'
df_job_details = df_job_details.drop("ALL", axis=1)

#tornar colunas true e false em 1 e 0 com get_dumies em columns to update
df_job_details = df_job_details.groupby('job_opportunity_id').sum().reset_index()

#Limpando dados dos cursos oferecidos
#Transformação das classificações categóricas das competências em colunas numéricas
df_cursos = pd.read_csv(Path.cwd() / 'backend' / 'model' / 'tabelas'/'journeys_inteli.csv')
df_cursos_completo = df_cursos
df_cursos_name = df_cursos[["name","id"]]
df_cursos.competencias.value_counts()

#Cria uma cópia do DF para não modificar dados originais
df_encoded = df_cursos.copy()

# Extrai competências únicas do dataset
all_categories = set()
for categories_str in df_encoded['competencias']:
    if pd.notna(categories_str):
        all_categories.update(category.strip() for category in categories_str.split(' - '))

# Cria colunas numéricas com valor 0 para cada categoria 0
for category in all_categories:
    df_encoded[category] = 0

# Preenche as colunas numéricas de acordo com a presença da competência no curso ou não
for index, row in df_encoded.iterrows():
    categories_list = []
    if pd.notna(row['competencias']):
        categories_list = [category.strip() for category in row['competencias'].split(' - ')]
    for category in categories_list:
        df_encoded.at[index, category] = 1

# Drop na coluna original de competências
df_encoded.drop(columns = ["competencias", "name",	"type",	"category_type",	"average_rating",	"ratings_count"], axis=1, inplace=True)


# Filtrar os valores desejados
df_cursos = df_encoded[df_encoded["emp"]!=1]
df_cursos = df_cursos[df_cursos["plataforma"]!=1]
df_user_journeys = pd.read_csv(Path.cwd() / 'backend' / 'model' / 'tabelas'/"user_journeys_inteli.csv")
df_user_journeys = df_user_journeys.drop(labels='finish_time', axis=1)