import os,sys,re
import numpy as np
import pandas as pd
from datetime import date, datetime
import matplotlib.pyplot as plt
import subprocess
import xlrd
# import matplotlib as mpl
# mpl.rcParams['font.family'] = 'AppleGothic'
from matplotlib import rcParams
rcParams["font.family"] = "sans-serif"
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

def main(flg1,flg2):
  DAT="../dat/population"
  # subprocess.run(f"cp {DAT}/05k01-2.xlsx {DAT}/05k01-2.csv", shell=True)
  # subprocess.run(f"cp {DAT}/05k01-3.xlsx {DAT}/05k01-3.csv",shell=True)
  # subprocess.run(f"nkf -w --overwrite {DAT}/*.xlsx",shell=True)
  # sys.exit()
  if flg1:
    """
    05k01-2.xlsx" : 男女別人口
    """
    FILENAME = f"{DAT}/05k01-2.xlsx"
    df = pd.read_excel(FILENAME,header=None, skiprows=12)
    df = df.dropna(subset=[2])
    df = df.dropna(axis=1)
    df = df[[2, 5, 6, 9, 10]]
    df.columns = ["pref","male_all","female_all","male_jp","female_jp"]
    # print(df.iloc[:,2])
    for col in df.columns[1:]:
      df[col] = df[col] * 1000
    
    df["all"] = df["male_all"]+df["female_all"]
    df["jp"] = df["male_jp"]+df["female_jp"]
    df.to_csv(f"{DAT}/05k01-2.csv", index=False)
  
  if flg2:
    """
    # 05k01-3.xlsx" : 男女別人口
    """
    FILENAME = f"{DAT}/05k01-3.xlsx"
    df = pd.read_excel(FILENAME, header=None, skiprows=12)
    df = df.dropna(subset=[2])
    df = df.dropna(axis=1)
    df = df.drop([1], axis=1)
    
    names = ["pref",
    "teen15_all", "main1564_all", "elder65_all", "elder75_all",
    "teen15_male", "main1564_male", "elder65_male", "elder75_male",
    "teen15_female", "main1564_female", "elder65_female", "elder75_female"
    ]
    df.columns = names
    df["pref"] = df["pref"].apply(lambda x: re.sub(" ","",x))
    df.to_csv(f"{DAT}/05k01-3.csv", index=False)
  return


if __name__ == "__main__":
  main(0,1)
