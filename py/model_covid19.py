# https://api.rakuten.net/api-sports/api/api-football?endpoint=apiendpoint_33b2c650-e8fb-4ac6-aa3c-715d2bb5032f
# reference
# edit 2020.11.26
# edit 2021.01.10 
import numpy as np
import sys, os, re, glob
import re
# sys.path.append('/Users/soriiieee/.local/lib/python3.7/site-packages')
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

from datetime import datetime, timedelta

import requests
import json
import time

headers = {
  # "x-rapidapi-host": open("../env/api_host.env").read(),
  "x-rapidapi-host": "covid-19-data.p.rapidapi.com",
  "x-rapidapi-key": open("../env/api_key.env").read()
}

querystring = {"format":"json"}
# sys.exit()

def load_json(json_path):
  with open(json_path, "r") as json_file:
    data = json.load(json_file)
  return data

def save_json(data,json_path):
  with open(json_path, "w") as f:
    json.dump(data,f)
  return data

class Covid19:
  def __init__(self):
    # self.nation = nation
    print("make COVID Analysis...")
  
  def get_info(self,json_path,isSave=True):
    # self.nation = nation
    if not os.path.exists(json_path):
      url = "https://covid-19-data.p.rapidapi.com/help/countries"
      res = requests.request("GET", url, headers=headers, params=querystring)
      data = res.json()
      if isSave:
        data = save_json(data, json_path)
    else:
      data = load_json(json_path)
    return data
  
  def get_nation_data(self,querystring, json_path, isSave=True):
    if not os.path.exists(json_path):
      print("[No Local] get_nation_data..at->",querystring["date"])
      url = "https://covid-19-data.p.rapidapi.com/report/country/code"
      res = requests.request("GET", url, headers=headers, params=querystring)
      data = res.json()
      if isSave:
        save_json(data, json_path)
    else:
      print("[Already] get_nation_data..at->",querystring["date"])
    return


if __name__ == "__main__":
  print("starts...")
  cv19 = Covid19()
  #-- country list... ----
  json_path = "../dat/country.json"
  df_path = "../dat/country.csv"
  # data = cv19.get_info(json_path,isSave=True)
  # data = load_json(json_path)
  # df = pd.DataFrame(data)
  # df.to_csv(df_path, index=False)
  # print()

  #-- JP ---
  code = "JP"
  today = datetime.now().strftime("%Y%m%d%H%M")
  _t = pd.date_range(start="202011010000", end=today, freq="D")
  _t = [t.strftime("%Y-%m-%d") for t in _t]
  for t in _t[:]:
    querystring = {"format": "json", "date-format": "YYYY-MM-DD", "date": t, "code": code}
    json_path = f"../dat/{code}/{t}.json"
    cv19.get_nation_data(querystring,json_path,isSave=True)
    time.sleep(1.0)
    # sys.exit()

  sys.exit()
  # url = "https://covid-19-data.p.rapidapi.com/report/country/code"
  # querystring = {"format":"json","date-format":"YYYY-MM-DD","date":"2020-04-01","code":"it"}
  # json_path = "../dat/JP"
  # get_nation_data("JP",date_time,json_path,,isSave=True)

  # print(covid)

  sys.exit()  


