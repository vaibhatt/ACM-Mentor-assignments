import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix

ratings_df = pd.read_csv(r"E:\ACM Mentor\week 4\data\ml-latest\ratings.csv")
movies_df = pd.read_csv(r"E:\ACM Mentor\week 4\data\ml-latest\movies.csv")

def lower_case(movies_df):
  movies_df.loc[:,"title"] = pd.DataFrame([name.lower() for name in movies_df["title"].values])
  return movies_df

def process_df(movies_df,ratings_df,thresh = 10000):
  df = movies_df.merge(ratings_df,on="movieId")
  df = df.merge(pd.DataFrame(df.groupby('title')["rating"].mean()).rename(columns = {"rating":"mean_rating"}),on = "title")
  df = df.merge(pd.DataFrame(df.groupby("title")["csvuserId"].count()).rename(columns = {"csvuserId":"rate_count"}),on = "title")
  df["release_year"] = pd.DataFrame([name[-5:-1] for name in df.title.values])
  df["Title"] = pd.DataFrame([name[:-7] for name in df.title.values])
  df.drop(columns = ["title"],inplace = True)
  df.rename(index={"Title":"title"},inplace = True)
  df_ratesorted = df[df.rate_count > thresh]
  return df_ratesorted

df = process_df(movies_df,ratings_df)

if __name__=="__main__":
  df.to_csv(r"df.csv")
