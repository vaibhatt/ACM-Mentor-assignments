import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

def make_pivot(df):
  mat = df.pivot_table(index = "Title",columns = "csvuserId",values="rating")
  mat = mat.fillna(0)
  return mat

def unique(list):
  unique = []
  for name in list:
    if name not in unique:
      unique.append(name)
  return unique
  
df = pd.read_csv(r"E:\ACM Mentor\week 4\data\ml-latest\df.csv")

pivot_table = make_pivot(df)
movie_matrix = csr_matrix(pivot_table) #creates csr matrix

model = NearestNeighbors(algorithm = "brute")
model.fit(movie_matrix)

def recommend(movie_name,num_recommendations):
  
  n = np.where(pivot_table.index==movie_name)[0][0]
  _,suggestion = model.kneighbors(pivot_table.iloc[n,:].values.reshape(1,-1),n_neighbors=num_recommendations+1)
  suggestion_list = list(suggestion[0][1:num_recommendations+1])
  '''
  print(f"{num_recommendations} movie recommendations for movie '{movie_name}' are:")
  n=1
  for i in suggestion_list:
    print(f"{n}. {pivot_table.index[i]}")
    n+=1
  '''
  recommend_df = pd.DataFrame(columns=["Title","Year"])
  recommend_df.loc[:,"Title"] = pivot_table.index[suggestion_list]
  recommend_df.loc[:,"Year"] = df[["Title","release_year"]].drop_duplicates().set_index("Title").loc[recommend_df.Title.values,"release_year"].values
  return recommend_df


