import os,sys,re
import numpy as np
import pandas as pd
from datetime import date, datetime
import matplotlib.pyplot as plt
import subprocess
# import matplotlib as mpl
# mpl.rcParams['font.family'] = 'AppleGothic'
from matplotlib import rcParams
rcParams["font.family"] = "sans-serif"
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

def main():
  """
  都道府県別の感染者割合
  """
  FILENAME = "../dat/population/05k01-2.xlsx"
  # df = pd.read_csv(FILENAME)
  df = pd.read_excel(FILENAME, sheet_name=1)
  print(df.head())
  sys.exit()
  if 0:
    for col in ["all", "male", "female"]:
      df[col] = df[col].apply(lambda x: re.sub(",", "", str(x)))
  df.to_csv("./dat2/pref_infs.csv", index=False)
  return


if __name__ == "__main__":
  main()
