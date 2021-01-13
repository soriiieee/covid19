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
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro','Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']


def tmp():
  plt.scatter(np.arange(10), np.arange(10))
  plt.title("北海道")
  plt.savefig("./tmp.png", bbox_inches="tight")

def main2():
  """
  感染者数/死者数/回復者の推移
  """
  f1 = "../dat/source/cases_total.csv"
  f2 = "../dat/source/severe_daily.csv"
  f3 = "../dat/source/death_total.csv"
  f4 = "../dat/source/recovery_total.csv"

  f5 = "../dat/source/pcr_positive_daily.csv"
  f6 = "../dat/source/pcr_tested_daily.csv"
  
  # 入院治療を要する者,重症者数,死亡者数,退院、療養解除となった者,PCR 検査陽性者数(単日),PCR 検査実施件数(単日)
  ["goHospital","severe", "death","recover","PCR_positive","PCR_test"]
  # _lbl = ["cases", "deaths", "recovery"]
  _f = [f1, f2, f3, f4, f5, f6]
  # sys.exit()
  
  _df =[]
  for i,f in enumerate(_f):
    #---convert to utf-8
    com = "nkf -w --overwrite {}".format(f)
    subprocess.run(com, shell=True)
    #--- read file convert DF type
    df = pd.read_csv(f)
    # print(df.head())
    # sys.exit()
    # df.columns = ["time", lbl]
    df = df.rename(columns={"日付": "time"})
    # print(df.head())
    # sys.exit() 
    df["time"] = df["time"].apply(lambda x: date(
      int(x.split("/")[0]),
      int(x.split("/")[1]),
      int(x.split("/")[2])))
    df = df.set_index("time")
    # print(df.head(1))
    # continue
    _df.append(df)
  df = pd.concat(_df, axis=1)
  df = df.reset_index()
  df = df.replace(np.nan, 0)
  df.columns = ["time","hospital_all","severe_all", "death_all","recover_all","pcr_positive_daily","pcr_test_daily"]
  # df = df.reset_index()
  df = df.sort_values("time")

  df["week"] = df["time"].apply(lambda x: x.weekday())
  #make calc
  df["pcr_positive_all"] = df["pcr_positive_daily"].cumsum()
  df["pcr_test_all"] = df["pcr_test_daily"].cumsum()

  df["hospital_daily"] = df["hospital_all"].diff().fillna(0)
  df["severe_daily"] = df["severe_all"].diff().fillna(0)
  df["death_daily"] = df["death_all"].diff().fillna(0)
  df["recover_daily"] = df["recover_all"].diff().fillna(0)
  df.to_csv("../out/csv/ts_01.csv", index=False)
  return 

def png1(isMV=0):
  f, ax = plt.subplots(2, 1, figsize=(22, 16))
  _title = ["All_day Cumsum", "Daily"]
  df = pd.read_csv("../out/csv/ts_01.csv")
  df["time"] = pd.to_datetime(df["time"])
  df = df[df["time"] < datetime(2021, 1, 9)]
  cols = [col for col in df.columns if not "pcr_test" in col] #drop test numbers
  # cols = df.columns #contain test numbers
  all_cols = [ col for col in cols if "all" in col ]
  daily_cols = [ col for col in cols if "daily" in col]
  for col in all_cols:
    ax[0].plot(df["time"].values, df[col].values, label=col)
  for col in daily_cols:
    if isMV:
      df[col] = df[col].rolling(isMV).mean()
    ax[1].plot(df["time"].values, df[col].values, label=f"{col}({isMV})")
  
  for i in range(2):
    ax[i].legend(loc="upper left")
    ax[i].set_title(_title[i], pad=-15)
  f.savefig("../out/png/ts1.png", bbox_inches="tight")
  return
  
if __name__ == "__main__":
  """
  厚生労働省
  https://www.mhlw.go.jp/stf/covid-19/open-data.html
  のサイトから本日最新版のデータを各種ダウンロードして、./source以下に入れ込み
  """
  if 1:
    main2()
  # sys.exit()
  png1(isMV=7)
  # tmp()