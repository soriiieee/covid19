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

import warnings
warnings.simplefilter("ignore")
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly import express as px
import plotly



def tmp():
  plt.scatter(np.arange(10), np.arange(10))
  plt.title("北海道")
  plt.savefig("./tmp.png", bbox_inches="tight")

def sub1(pref):
  tbl = pd.read_csv("../dat/population/05k01-2.csv")
  # return tbl.loc[tbl["pref"].isin(pref), "all"].values[0]
  return tbl.loc[tbl["pref"] == pref, "all"].values[0]

def calc_death(x):
  d = int(x[0])
  c = int(x[1])
  if c > 0:
    return d * 100 / c
  else:
    return 0

def main():
  # FILENAME = "../dat/nhk_news_covid19_domestic_daily_data.csv"
  FILENAME2 = "../dat/nhk_news_covid19_prefectures_daily_data.csv"
  df = pd.read_csv(FILENAME2)
  # _pref = df["都道府県名"]
  _code = sorted(df["都道府県コード"].unique().tolist())

  for code in _code:
    # code=33
    tmp = df[df["都道府県コード"] == code]
    tmp = tmp.dropna()
    tmp["都道府県名"] = tmp["都道府県名"].apply(lambda x: x.strip()) #trim " "2021.01.14
    # print(tmp.head())
    # sys.exit()
    pref = tmp["都道府県名"].values[0]
    # print(tmp.head())
    pop = sub1(pref)  #人口
    # print(pop)
    # sys.exit()
    tmp["cases_per_pop"] = tmp["各地の感染者数_累計"] * 100 / pop
    tmp["death_per_cases"] = tmp[["各地の死者数_累計","各地の感染者数_累計"]].apply(lambda x: calc_death(x),axis=1)
    # print("end", code, tmp.head())
    tmp = tmp.rename(columns={"日付": "time"})
    tmp["time"] = tmp["time"].apply(lambda x: date(
      int(x.split("/")[0]),
      int(x.split("/")[1]),
      int(x.split("/")[2])))

    tmp = tmp.rename(columns={
      "各地の感染者数_1日ごとの発表数": "cases_daily",
      "各地の感染者数_累計": "cases_sum",
      "各地の死者数_1日ごとの発表数": "death_daily",
      "各地の死者数_累計": "death_all"
      })
    # sys.exit()
    tmp.to_csv(f"../dat/pref/{code}.csv", index=False)
    print("end", code,pref)
    # sys.exit()
  return

def set_ylim(col):
  if col == "cases_per_pop":
    return [0, 0.6]

def plot47(col):
  f, ax = plt.subplots(7, 7, figsize=(52, 42))
  ax = ax.flatten()
  for i in range(1,47+1):
    df = pd.read_csv(f"../dat/pref/{i}.csv")
    df["time"] = pd.to_datetime(df["time"])
    ax[i - 1].plot(df["time"].values, df[col].values)
    pref = df["都道府県名"].values[0]
    ymin, ymax = set_ylim(col)
    ax[i - 1].set_ylim(ymin, ymax)
    ax[i - 1].set_title(pref, pad=-30)
    print("end",i)
  
  f.suptitle(col)
  f.savefig(f"../out/png/pref47_{col}.png", bbox_inches="tight")
  return


def mk_pref_sort(col):
  _df=[]
  for i in range(1, 47 + 1):
    df = pd.read_csv(f"../dat/pref/{i}.csv")
    _df.append(df.iloc[-1,:])
  
  tmp = pd.concat(_df, axis=1).T
  tmp = tmp.sort_values(col, ascending=False)
  tmp = tmp.reset_index(drop=True)
  tmp.to_csv("../out/csv/pref_sort.csv", index=False)
  return tmp


def set_layout_plotly(fig,params):
  fig.update_xaxes(title= params["x_label"]) # X軸タイトルを指定
  fig.update_yaxes(title= params["y_label"]) # Y軸タイトルを指定
  fig.update_yaxes(range= (params["y_lim"][0],params["y_lim"][1]))  # X軸の最大最小値を指定
  fig.update_layout(title=params["title"])  # グラフタイトルを設定
  
  fig.update_xaxes(rangeslider={"visible":True}) # X軸に range slider を表示（下図参照）
  # fig.update_yaxes(scaleanchor="x", scaleratio=1) # Y軸のスケールをX軸と同じに（plt.axis("equal")）
  fig.update_layout(title=params["title"]) # グラフタイトルを設定
  fig.update_layout(font={"family":"Meiryo", "size":20}) # フォントファミリとフォントサイズを指定
  fig.update_layout(showlegend=True) # 凡例を強制的に表示（デフォルトでは複数系列あると表示）
  # fig.update_layout(xaxis_type="linear", yaxis_type="log") # X軸はリニアスケール、Y軸はログスケールに
  # fig.update_layout(width=800, height=600)  # 図の高さを幅を指定
  fig.update_xaxes(rangeslider={"visible":True}) # X軸に range slider を表示（下図参照）
  fig.update_layout(template="plotly_white")  # 白背景のテーマに変更
  return fig

def plot1(col,ymin,ymax,isPlotly=True):
  #都道府県ごとを上位順にランキングするようなtmpfileを作成する
  tmp = mk_pref_sort(col)
  #tmpfile上位順からファイル読み込みをして描写
  _code = tmp["都道府県コード"].values.tolist()

  if isPlotly:
    """
    plotly : https://qiita.com/inoory/items/12028af62018bf367722
    """
    fig = go.Figure()
    for rank,i in enumerate(_code):
      df = pd.read_csv(f"../dat/pref/{i}.csv")
      df["time"] = pd.to_datetime(df["time"])
      val = np.round(tmp.loc[tmp["都道府県コード"]==i, col].values[0],3)
      pref = df["都道府県名"].values[0]
      # ax.plot(df["time"].values, df[col].values, label=f"{pref}({val})")
      rank=rank+1
      name = f"{rank}:{pref}({val})"
      fig.add_trace(go.Scatter(x=df["time"], y=df[col].values, name=name))
      #params
    params = {
        "x_label": "Date[yyyy-mm-dd]",
        "y_label": "percentage[%]",
        "y_lim": [ymin,ymax],
        "title": f"{col} in Japan per Pref.."
    }
    fig = set_layout_plotly(fig, params)
    plotly.offline.plot(fig, filename=f'../out/html/ts_new_{col}.html')
      # fig.add_trace(go.Scatter(x=xs, y=randoms, name="random"))
    return
  else:
    f, ax = plt.subplots(figsize=(30, 20))
    for i in _code:
      df = pd.read_csv(f"../dat/pref/{i}.csv")
      df["time"] = pd.to_datetime(df["time"])
      val = np.round(tmp.loc[tmp["都道府県コード"]==i, col].values[0],3)
      pref = df["都道府県名"].values[0]
      ax.plot(df["time"].values, df[col].values, label=f"{pref}({val})")
      # pref = df["都道府県名"].values[0]
    ymin, ymax = set_ylim(col)
    ax.set_ylim(ymin, ymax)
    ax.legend()
    ax.set_title(pref, pad=-30)
    f.suptitle(col)
    f.savefig(f"../out/png/pref1_{col}.png", bbox_inches="tight")
  return

if __name__ == "__main__":
  """
  厚生労働省
  https://www.mhlw.go.jp/stf/covid-19/open-data.html
  のサイトから本日最新版のデータを各種ダウンロードして、./source以下に入れ込み
  """
  if 0:
    """
    都道府県別のcsvファイルの作成(最新をダウンロードしたら)
    """
    subprocess.run("rm -f ../dat/pref/*.csv", shell=True)
    main()
  if 1:
    """
    都道府県別のcsvファイルの作成
    """
    # subprocess.run("rm -f ../dat/pref/*.csv", shell=True)
    col,ymin, ymax ="cases_per_pop", 0,0.6
    col,ymin, ymax ="death_per_cases",0,50
    # plot47(col)
    plot1(col,ymin, ymax)
    # sys.exit()
  sys.exit()