from django.shortcuts import render, redirect
from .forms import InputForm, LoginForm, SignUpForm, ContactForm, EdinetName
from . import forms
from .models import ZangeModel
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic import DetailView,TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
import requests
import json
from bs4 import BeautifulSoup
import os,zipfile,io
from lxml import etree
from bs4 import BeautifulSoup
import requests
import os
import zipfile
from datetime import datetime, timedelta 
import numpy as np
import pandas as pd
from pandas import DataFrame
from edinet_xbrl.edinet_xbrl_parser import EdinetXbrlParser
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import glob
import csv

 

class ZangeList(ListView):
  model = ZangeModel
  template_name = 'ZANGEapp/index.html'


class Login(LoginView):
  form_class = LoginForm
  template_name = "ZANGEapp/login.html"

class Logout(LogoutView):
  template_name = "ZANGEapp/base.html"

def signup(request):
  if request.method == 'POST':
    form= SignUpForm(request.POST)
    print(form)
    if form.is_valid():
      form.save()
      #フォームから'email'を読み取る
      email = form.cleaned_data.get('email')
      #フォームから'password1'を読み取る
      password = form.cleaned_data.get('password1')
      # 読み取った情報をログインに使用する情報として new_user に格納
      new_user = authenticate(email=email, password=password)
      if new_user is not None:
      # new_user の情報からログイン処理を行う
        login(request, new_user)
        # ログイン後のリダイレクト処理
        return redirect('index')
    else:
      form = SignUpForm()
      return render(request, 'ZANGEapp/signup.html', {'form': form})
  # POST で送信がなかった場合の処理
  else:
    form = SignUpForm()
    return render(request, 'ZANGEapp/signup.html', {'form': form})

@login_required  
def post_form(request):
  if request.method == 'POST':
    form = InputForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      object_list = ZangeModel.objects.order_by("-id")
      return render(request,"ZANGEapp/index.html",{'object_list':object_list})
  else:
    form = InputForm()
    return render(request,'ZANGEapp/post.html',{"form":form})  

def detail(request,pk):
  if request.method == 'POST':
    d_id = request.POST
    d_item = ZangeModel.objects.filter(id=d_id['d_id'])
    d_item.delete()
    items = ZangeModel.objects.all()
    #相対パスでindex.htmlのrequestに戻す(※detail/<int:pk>/から戻らなかったため)
    return redirect('../../')
  else:
    item = ZangeModel.objects.get(pk=pk)
    return render(request,'ZANGEapp/detail.html',{'object':item})

def about(request):
    return render(request,'ZANGEapp/about.html')

def link(request):
    return render(request,'ZANGEapp/link.html')

class ContactFormView(FormView):
    template_name = 'ZANGEapp/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_result')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

class ContactResultView(TemplateView):
    template_name = 'ZANGEapp/contact_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = "お問い合わせは正常に送信されました。"
        return context


#EDINETから指定のEDINETコードでP/Lの売上と営業利益を取得

list_api = "https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date={target}&type=2"
file_api = "https://disclosure.edinet-fsa.go.jp/api/v1/documents/{document_id}?type=1"

def edinet_search(request):
    form = EdinetName()
    return render(request, 'ZANGEapp/search.html',{'form':form})


def call_edinet_api(request):
    #企業検索値の取得
    form = forms.EdinetName(request.GET or None)
    if form.is_valid():
            name= request.GET.get("name")
    else:
      name = '入っていないよ'
    #コードリストの読み込み
    df = pd.read_csv('../ZANGEproject/EdinetcodeDlInfo_utf8.csv')
    df = df[df['提出者名'] == name]
    code = df['ＥＤＩＮＥＴコード'].values
    code = pd.Series(code)
    code = code[0]
    print(name)
    print(code)
    print(os.getcwd())
    for result in get_results("2018-06-19"):
        if result["edinetCode"] == "E01777" and "有価証券" in result["docDescription"]:
            document_id = result["docID"]
            print(document_id)
            url = file_api.format(document_id=document_id)
            r = requests.get(url)

            zip = zipfile.ZipFile(io.BytesIO(r.content))
            zip.extractall()

            file = os.getcwd() + "/XBRL/PublicDoc/jpcrp030000-asr-001_E01777-000_2018-03-31_01_2018-06-19.xbrl"
            data1 = get_information_about_net_sales(file)
            soup1 = BeautifulSoup(data1.text,'lxml')
            #練習
            for script in soup1(["script", "style"]):
              script.decompose()
            text1=soup1.get_text()
            lines1= [line.strip() for line in text1.splitlines()]
            lines1=[]
            for line in text1.splitlines():
              lines1.append(line.strip())
              text1="\n".join(line for line in lines1 if line)
            
            data2 = get_information_about_operating_income(file)
            soup2 = BeautifulSoup(data2.text,'lxml')
            #練習
            for script in soup2(["script", "style"]):
              script.decompose()
            text2=soup2.get_text()
            lines2= [line.strip() for line in text2.splitlines()]
            lines2=[]
            for line in text2.splitlines():
              lines2.append(line.strip())
              text2="\n".join(line for line in lines2 if line)

    return render(request, 'ZANGEapp/stack.html', {'sales':text1, 'profit':text2, 'name':name, 'code':code })

def get_information_about_net_sales(file):
    root = read_xml_lxml_etree(file)
    namespace = root.nsmap['jppfs_cor']
    tag = 'NetSales'
    attr = 'contextRef'
    value = 'CurrentYearDuration_NonConsolidatedMember'

    xpath = './/{%s}%s[@%s="%s"]' % (namespace, tag, attr, value)
    data = root.find(xpath)

    return data

def get_information_about_operating_income(file):
    root = read_xml_lxml_etree(file)
    namespace = root.nsmap['jppfs_cor']
    tag = 'OperatingIncome'
    attr = 'contextRef'
    value = 'CurrentYearDuration_NonConsolidatedMember'

    xpath = './/{%s}%s[@%s="%s"]' % (namespace, tag, attr, value)
    data = root.find(xpath)

    return data

def read_xml_lxml_etree(file):
    with open(file, 'rb') as f:
        return etree.fromstring(f.read())

def get_results(target):

    url = list_api.format(target=target)
    r = requests.get(url)
    data = json.loads(r.text)
    results = data["results"]
    return results

#seleniumによるEDINETコードリストの取得(リストが古くなったら更新する)

def edinet_code_dl():
    # seleniumでchromeからzipファイルをダウンロード
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option(
        "prefs",
        {"download.default_directory": "./"},
        # 保存先のディレクトリの指定
    )

    # ブラウザ非表示
    chromeOptions.add_argument("--headless")

    url = "https://disclosure.edinet-fsa.go.jp/E01EW/BLMainController.jsp"
    url += "?uji.bean=ee.bean.W1E62071.EEW1E62071Bean&uji.verb"
    url += "=W1E62071InitDisplay&TID=W1E62071&"
    url += "PID=W0EZ0001&SESSIONKEY=&lgKbn=2&dflg=0&iflg=0"

    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=chromeOptions,
    )
    driver.maximize_window()

    # EDINETのEDINETコードリストにアクセス
    driver.get(url)
    driver.execute_script(
        "EEW1E62071EdinetCodeListDownloadAction('lgKbn=2&dflg=0&iflg=0&dispKbn=1');"
    )
    time.sleep(5)
    driver.quit()

def get_edinet_code_list():
    # ダウンロードしたzipファイルのパスを取得
    # ディレクトリのリストを取得する.
    # ワイルドカードを追加
    edinet_code_dl()

    list_of_files = glob.glob("./" + r"/*")

    # 作成日時が最新のファイルパスを取得
    latest_file = max(list_of_files, key=os.path.getctime)

    # zipファイルを同じディレクトリに展開
    zip_f = zipfile.ZipFile(latest_file)
    zip_f.extractall("./")
    zip_f.close()

    # zipファイルを削除
    os.remove(latest_file)

    list_of_files = glob.glob("./" + r"/*")  # ワイルドカードを追加
    csv_filepath = max(list_of_files, key=os.path.getctime)
    cp932_file = open(csv_filepath, "r", encoding="cp932")
    cp932_file_list = [row for row in cp932_file]

    # 一番最初の行である不要なカラムを削除する
    del cp932_file_list[0]

    utf8_file_name = "EdinetcodeDlInfo_utf8.csv"
    utf8_file = open(utf8_file_name, "w", encoding="utf-8")

    for row in cp932_file_list:
      utf8_file.write(row)

    cp932_file.close()
    utf8_file.close()
