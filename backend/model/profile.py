import limpeza as l
import pandas as pd
import sys
user_index = 10

if len(sys.argv) > 1:
    user_index = int(sys.argv[1])

df_user_info = pd.merge(l.df_superfit_user,l.user_objectives, on = "id", how = "inner")
def remove_prefix(column_name):
    if column_name.startswith('superfit_'):
        return column_name[len('superfit_'):]
    else:
        return column_name

df_user_info = df_user_info.rename(columns=remove_prefix)

#
df_user_info = df_user_info.iloc[user_index].to_dict()

print(df_user_info)