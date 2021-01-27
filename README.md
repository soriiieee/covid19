# covi19


# DEMO
 
# Feature
毎日、更新予定*自動化は未定（）
推移や、空間分布等を表示する
 
# Requirement
"hoge"を動かすのに必要なライブラリなどを列挙する
* Python 3.8.5
* plotly 4.14.2
* pandas 1.2.0
* matplotlib 3.3.2
* xlrd-2.0.1 
* openpyxl-3.0.5 
 
# Installation

## 1 ディレクトリ構成を揃える
home - py : csvのデータ整形や計算ファイルの格納
     - dat :inputデータ/テーブルファイル等
     - out : outputデータ/作成した記録
        - csv
        - png
## 2 inputデータの入手
### 1 covid関連 
厚生労働省[https://www.mhlw.go.jp/stf/covid-19/open-data.html]
のサイトから本日最新版のデータを各種ダウンロードして、./dat/source/へ
### 2 統計データ
統計局[https://www.stat.go.jp/data/jinsui/2019np/index.html]
第２表と第３表 ./dat/population/へ

### 3 covid19 - 都道府県
[https://www3.nhk.or.jp/news/special/coronavirus/hospital/]

### 4 covid19 - world
ジョンホプキンス大学
[https://github.com/CSSEGISandData/COVID-19]


# 実行方法
## データセット作成
python pre_japan_population.py 




# Author
* yuichi sorimachi
* jwa
* E-mail : sorimachi.y.ab@gmail.com


  
