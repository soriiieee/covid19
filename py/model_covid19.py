# https://api.rakuten.net/api-sports/api/api-football?endpoint=apiendpoint_33b2c650-e8fb-4ac6-aa3c-715d2bb5032f
# reference

import numpy as np
import sys, os, re, glob
import re
# sys.path.append('/Users/soriiieee/.local/lib/python3.7/site-packages')
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

import requests
import json
import time

url = "https://api-football-v1.p.rapidapi.com/v2/predictions/157462"
url = "https://api-football-v1.p.rapidapi.com/v2/countries"

headers = {
  "x-rapidapi-host": open("../env/api_host.env").read(),
  "x-rapidapi-key": open("../env/api_key.env").read()
}
# sys.exit()

def load_json(json_path):
  with open(json_path, "r") as json_file:
    json_data = json.load(json_file)
  return json_data

def save_json(json_path):
  with open(json_path, "w") as json_file:
    json_data = json.load(json_file)
  return json_data

class Covid19:
  def __init__(self, nation="JP"):
    self.nation = nation
  
  def get_info(self,):
    nation


if __name__ == "__main__":
  print("starts...")



  sys.exit()  


