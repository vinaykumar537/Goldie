from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as user_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_required
import pandas as pd
import json
from pprint import pprint
import nltk
import re
from nltk.util import ngrams
import pandas as pd
import os
from datetime import date,datetime,timedelta
import speech_recognition as sr

# Create your views here.

# To view Login page 
def home(request):
    return render(request,'login.html')

""" Login Method:
Input: Uername & Password """
def login(request):
    if request.method == 'POST':
        username = request.POST['uname'] # Extracting username from login form
        password = request.POST['pwd'] # Extracting password from login form
        user = authenticate(username=username, password=password) # validating the user
        if user is not None:
           user_login(request, user) # Make user login, if validation got success
           return redirect('firstpage')
        else:
           return redirect('home') 
    else:
        return render(request, 'login.html')

""" Logout Method:
Input : requested user """
def logout(request):
   logout_required(request) # alias name for logout to avaoid recurssion
   return redirect('home')


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

def fd_month(md):
    if md[:3] == 'jan':
        return md[-4:]+'-'+str('01')+'-'+str('01')
    if md[:3] == 'feb':
        return md[-4:]+'-'+str('02')+'-'+str('01')
    if md[:3] == 'mar':
        return md[-4:]+'-'+str('03')+'-'+str('01')
    if md[:3] == 'apr':
        return md[-4:]+'-'+str('04')+'-'+str('01')
    if md[:3] == 'may':
        return md[-4:]+'-'+str('05')+'-'+str('01')
    if md[:3] == 'jun':
        return md[-4:]+'-'+str('06')+'-'+str('01')
    if md[:3] == 'jul':
        return md[-4:]+'-'+str('07')+'-'+str('01')
    if md[:3] == 'aug':
        return md[-4:]+'-'+str('08')+'-'+str('01')
    if md[:3] == 'sep':
        return md[-4:]+'-'+str('09')+'-'+str('01')
    if md[:3] == 'oct':
        return md[-4:]+'-'+str('10')+'-'+str('01')
    if md[:3] == 'nov':
        return md[-4:]+'-'+str('11')+'-'+str('01')
    if md[:3] == 'dec':
        return md[-4:]+'-'+str('12')+'-'+str('01')

def ld_month(md):
    if md[:3] == 'jan':
        return md[-4:]+'-'+str('01')+'-'+str('31')
    if md[:3] == 'feb':
        if (int(md[-4:]) % 4 == 0):
            return md[-4:]+'-'+str('02')+'-'+str('29')
        else:
            return md[-4:]+'-'+str('02')+'-'+str('28')
    if md[:3] == 'mar':
        return md[-4:]+'-'+str('03')+'-'+str('31')
    if md[:3] == 'apr':
        return md[-4:]+'-'+str('04')+'-'+str('30')
    if md[:3] == 'may':
        return md[-4:]+'-'+str('05')+'-'+str('31')
    if md[:3] == 'jun':
        return md[-4:]+'-'+str('06')+'-'+str('30')
    if md[:3] == 'jul':
        return md[-4:]+'-'+str('07')+'-'+str('31')
    if md[:3] == 'aug':
        return md[-4:]+'-'+str('08')+'-'+str('31')
    if md[:3] == 'sep':
        return md[-4:]+'-'+str('09')+'-'+str('30')
    if md[:3] == 'oct':
        return md[-4:]+'-'+str('10')+'-'+str('31')
    if md[:3] == 'nov':
        return md[-4:]+'-'+str('11')+'-'+str('30')
    if md[:3] == 'dec':
        return md[-4:]+'-'+str('12')+'-'+str('31')

def fd_qtr(qd):
    if qd[:2] == 'q1':
        return qd[-4:]+'-'+str('01')+'-'+str('01')
    if qd[:2] == 'q2':
        return qd[-4:]+'-'+str('04')+'-'+str('01')
    if qd[:2] == 'q3':
        return qd[-4:]+'-'+str('07')+'-'+str('01')
    if qd[:2] == 'q4':
        return qd[-4:]+'-'+str('10')+'-'+str('01')

def ld_qtr(qd):
    if qd[:2] == 'q1':
        return qd[-4:]+'-'+str('03')+'-'+str('31')
    if qd[:2] == 'q2':
        return qd[-4:]+'-'+str('06')+'-'+str('30')
    if qd[:2] == 'q3':
        return qd[-4:]+'-'+str('09')+'-'+str('30')
    if qd[:2] == 'q4':
        return qd[-4:]+'-'+str('12')+'-'+str('31')

def datepicker(userText):
    # Calculating reference dates
    st_dt = ''
    end_dt = ''
    today = date.today()
    curr_month_start = date.today().replace(day=1)
    next_month = date.today().replace(day=28) + timedelta(days=4)
    curr_month_end = next_month - timedelta(days=next_month.day)
    prev_month_start = (date.today().replace(day=1)-timedelta(days=1)).replace(day=1)
    prev_month_end = date.today().replace(day=1)-timedelta(days=1)
    curr_qtr_start = (pd.to_datetime(date.today()) - pd.offsets.QuarterBegin(startingMonth=1)).date()
    curr_qtr_end = (pd.to_datetime(date.today()) + pd.offsets.QuarterEnd()).date()
    prev_qtr_end = (pd.to_datetime(date.today()) - pd.offsets.QuarterEnd()).date()
    prev_qtr_start = (pd.to_datetime(prev_qtr_end) - pd.offsets.QuarterBegin(startingMonth=1)).date()
    curr_year_start = date(date.today().year, 1, 1)
    curr_year_end = date(date.today().year, 12, 31)
    prev_year_start = date(date.today().year-1, 1, 1)
    prev_year_end = date(date.today().year, 1, 1)-timedelta(days=1)


    curr_month = today.strftime("%b")+str(today.year)
    prev_month = prev_month_start.strftime("%b")+str(prev_month_start.year)
    curr_qtr = 'Q'+str(pd.Timestamp(today).quarter)+str(today.year)
    prev_qtr = 'Q'+str(pd.Timestamp(prev_qtr_end).quarter)+str(prev_qtr_end.year)
    curr_year = str(today.year)
    prev_year = str(today.year-1)

    date_names = pd.DataFrame(columns=['Name','date_name'])
    dn1 = pd.DataFrame({'Name': ['current month'],'date_name':[curr_month]})
    date_names = date_names.append(dn1)
    dn2 = pd.DataFrame({'Name': ['previous month'],'date_name':[prev_month]})
    date_names = date_names.append(dn2)
    dn3 = pd.DataFrame({'Name': ['current quarter'],'date_name':[curr_qtr]})
    date_names = date_names.append(dn3)
    dn4 = pd.DataFrame({'Name': ['previous quarter'],'date_name':[prev_qtr]})
    date_names = date_names.append(dn4)
    dn5 = pd.DataFrame({'Name': ['current year'],'date_name':[curr_year]})
    date_names = date_names.append(dn5)
    dn6 = pd.DataFrame({'Name': ['previous year'],'date_name':[prev_year]})
    date_names = date_names.append(dn6)
    date_names = date_names.reset_index(drop=True)
    date_names = date_names.apply(lambda x: x.astype(str).str.lower())



    date_mapping =pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\date_names_mapping.csv')
    for x in range(len(date_mapping.date_names)):
        if date_mapping.date_names[x] in userText:
            userText = userText.replace(date_mapping.date_names[x],date_mapping.other_names[x])

    for x in range(len(date_names.Name)):
        if date_names.Name[x] in userText:
            userText = userText.replace(date_names.Name[x],date_names.date_name[x])


    if 'of' in userText:
        userText = userText.replace('of','')
    if ' ' in userText:
        userText = userText.replace(' ','')
    
    mn_rep = re.findall('(((19|20)+\d{2})+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))', userText)
    if len(mn_rep)==2:
        userText = userText.replace(mn_rep[0][0],mn_rep[0][0][-3:]+mn_rep[0][0][:4])
        userText = userText.replace(mn_rep[1][0],mn_rep[1][0][-3:]+mn_rep[1][0][:4])
    if len(mn_rep)==1:
        userText = userText.replace(mn_rep[0][0],mn_rep[0][0][-3:]+mn_rep[0][0][:4])

    mn_match = re.findall('((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)+(19|20)+\d{2})', userText)
    if len(mn_match)==2:
        st_dt = fd_month(mn_match[0][0])
        end_dt = ld_month(mn_match[1][0])
    if len(mn_match)==1:
        if userText.split(mn_match[0][0])[0][-4:] == 'from':
            st_dt = fd_month(mn_match[0][0])
            end_dt = today
        else:
            st_dt = fd_month(mn_match[0][0])
            end_dt = ld_month(mn_match[0][0])
    qtr_rep = re.findall('(((19|20)+\d{2})+(q1|q2|q3|q4))', userText)

    if len(qtr_rep)==2:
        userText = userText.replace(qtr_rep[0][0],qtr_rep[0][0][-2:]+qtr_rep[0][0][:4])
        userText = userText.replace(qtr_rep[1][0],qtr_rep[1][0][-2:]+qtr_rep[1][0][:4])
    if len(qtr_rep)==1:
        userText = userText.replace(qtr_rep[0][0],qtr_rep[0][0][-2:]+qtr_rep[0][0][:4])

    qtr_match = re.findall('((q1|q2|q3|q4)+(19|20)+\d{2})', userText)
    if len(qtr_match)==2:
        st_dt = fd_qtr(qtr_match[0][0])
        end_dt = ld_qtr(qtr_match[1][0])
    if len(qtr_match)==1:
        if userText.split(qtr_match[0][0])[0][-4:] == 'from':
            st_dt = fd_qtr(qtr_match[0][0])
            end_dt = today
        else:
            st_dt = fd_qtr(qtr_match[0][0])
            end_dt = ld_qtr(qtr_match[0][0])
    if len(qtr_match)+len(mn_match) == 0:
        yr_mtch = re.findall(r'((19|20)\d{2})', userText)
        if len(yr_mtch)==2:
            st_dt = yr_mtch[0][0]+'-'+str('01')+'-'+str('01')
            end_dt = yr_mtch[1][0]+'-'+str('01')+'-'+str('01')
        if len(yr_mtch)==1:
            if userText.split(yr_mtch[0][0])[0][-4:] == 'from':
                st_dt = yr_mtch[0][0]+'-'+str('01')+'-'+str('01')
                end_dt = today
            else:
                st_dt = yr_mtch[0][0]+'-'+str('01')+'-'+str('01')
                end_dt = yr_mtch[0][0]+'-'+str('12')+'-'+str('31')
    return [st_dt, end_dt]


#sub chart keywords
def subChartKeywordFinder(userText):
    userText = userText.lower()
    userText = re.sub(r'[^a-zA-Z0-9\s]', ' ', userText)
    tokens = nltk.word_tokenize(userText)
    bi_grams = list(ngrams(tokens, 2))
    bi_tokens = [ ''.join(grams) for grams in bi_grams]
    tri_grams = list(ngrams(tokens, 3))
    tri_tokens = [ ''.join(grams) for grams in tri_grams]
    tokens = tokens + bi_tokens +tri_tokens
    tkn_list = pd.DataFrame(tokens,columns = ['tokens'])
    sub_chart_keywords = pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\sub_chart_keywords.csv')
    sub_keywords = pd.DataFrame(sub_chart_keywords.Sub_Chart_Keywords.unique(),columns = ['Keywords'])
    sub_chart_df = pd.merge(tkn_list, sub_keywords, left_on='tokens', right_on='Keywords')
    sub_chart_keyword = ''
    if len(sub_chart_df)>0:
        sub_chart_keyword = sub_chart_df.Keywords[0]
    return sub_chart_keyword


def sub_chart_name(prev_chart,sub_key):
    sub_ck = pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\sub_chart_keywords.csv')
    sub_ck = sub_ck[(sub_ck.Main_Chart == prev_chart) & (sub_ck.Sub_Chart_Keywords == sub_key)]
    sub_ck = sub_ck.reset_index(drop=True)
    return sub_ck.Sub_Chart[0]

""" Home page:
Input : HTTP Request """
@login_required
def firstpage(request):

    #Growth of $1000-Since Inception
    df = pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\Growth_1000_inception.csv')
    chart_data1 = growthInception1000(df)
    data = {'chart_data': chart_data1}
   
    #Portfolio Snapshot
    df = pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\page1_table.csv')
    chart_data2 = portfolioSnapshot(df)

    #Monthly Performance
    df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\page1_ytd.csv')
    ytd=df.YTD.values.tolist()
    year=df.YEAR.values.tolist()
    context={'data':data,'data2':chart_data2,'ytd':ytd,'year':year}

    return render(request, 'page1.html',context)


def growthInception1000(df):
    df['year'] = pd.DatetimeIndex(df['Trade_Dt']).year
    df['month'] = pd.DatetimeIndex(df['Trade_Dt']).month
    df['day'] = pd.DatetimeIndex(df['Trade_Dt']).day
    df['month']=df.month.map("{:02}".format)
    df['day']=df.day.map("{:02}".format)
    df['Trade_Dt'] = df['year'].apply(str) +'-'+ df['month'].apply(str)+'-'+ df['day'].apply(str)
    df=df.groupby(['Trade_Dt','year','month','day'],as_index = False).agg('sum')
    df=df.groupby(["Trade_Dt"]).apply(lambda x: x.sort_values(["Trade_Dt"], ascending = True)).reset_index(drop=True)
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    return chart_data

def portfolioSnapshot(df):
    df['year'] = pd.DatetimeIndex(df['Trade_Dt']).year
    df['month'] = pd.DatetimeIndex(df['Trade_Dt']).month
    df['day'] = pd.DatetimeIndex(df['Trade_Dt']).day
    df['month']=df.month.map("{:02}".format)
    df['day']=df.day.map("{:02}".format)
    df['Trade_Dt'] = df['day'].apply(str) +'/'+ df['month'].apply(str)+'/'+ df['year'].apply(str)
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    return chart_data

    

@login_required
def secondpage(request):
    # df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\net_exposure_stock.csv')
    # df=df.loc[df['Date'] == '2017-01-04']
    # chart_data1 = df.to_dict(orient='records')
    # chart_data1 = json.dumps(chart_data1, indent=2)
    # df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\net_exposure_sector.csv')
    # df=df.loc[df['Date'] == '2017-01-04']
    # chart_data2 = df.to_dict(orient='records')
    # chart_data2 = json.dumps(chart_data2, indent=2)
    # df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\net_exposure_country.csv')
    # df=df.loc[df['Date'] == '2017-01-04']
    # chart_data3 = df.to_dict(orient='records')
    # chart_data3 = json.dumps(chart_data3, indent=2)
    # context =  {'data1':chart_data1, 'data2':chart_data2, 'data3': chart_data3}
    #return render(request, 'page2.html', context)
    return render(request, 'page2.html')

@login_required
def thirdpage(request):
    df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\page3_fama_french.csv')
    context = famaFrench(df)
    multi_dates = multiFactorDates()
    if 'multi_factor_dates' not in context.keys():
        context['multi_factor_dates'] = multi_dates
    return render(request, 'page3.html',context)


def famaFrench(df):
    df1=df[['Trade_Dt']] 
    list1=[]
    for i in range (0,len(df1)-1):
        list1.append(df1.loc[[i]])
    Row_list1=[]
    for index, rows in df1.iterrows(): 
        my_list =rows.Trade_Dt 
        Row_list1.append(my_list)
    df2=df[['Market']] 
    list2=[]
    for i in range (0,len(df2)-1):
        list2.append(df2.loc[[i]])
    Row_list2=[]
    for index, rows in df2.iterrows(): 
        my_list =rows.Market 
        Row_list2.append(my_list) 
    df3=df[['Growth']] 
    list3=[]
    for i in range (0,len(df3)-1):
        list3.append(df3.loc[[i]])
    Row_list3=[]
    for index, rows in df3.iterrows(): 
        my_list =rows.Growth 
        Row_list3.append(my_list) 
    df4=df[['Momentum']] 
    list4=[]
    for i in range (0,len(df4)-1):
        list4.append(df4.loc[[i]])
    Row_list4=[]
    for index, rows in df4.iterrows(): 
        my_list =rows.Momentum 
        Row_list4.append(my_list) 
    df5=df[['Quality']] 
    list5=[]
    for i in range (0,len(df5)-1):
        list5.append(df5.loc[[i]])
    Row_list5=[]
    for index, rows in df5.iterrows(): 
        my_list =rows.Quality 
        Row_list5.append(my_list)
    df6=df[['Size']] 
    list6=[]
    for i in range (0,len(df6)-1):
        list6.append(df6.loc[[i]])
    Row_list6=[]
    for index, rows in df6.iterrows(): 
        my_list =rows.Size 
        Row_list6.append(my_list)
    df7=df[['Fund']]  
    list7=[]
    for i in range (0,len(df7)-1):
        list7.append(df7.loc[[i]])
    Row_list7=[]
    for index, rows in df7.iterrows(): 
        my_list =rows.Fund
        Row_list7.append(my_list)

    df8=df[['Alpha']]  
    list8=[]
    for i in range (0,len(df8)-1):
        list8.append(df8.loc[[i]])
    Row_list8=[]
    for index, rows in df8.iterrows(): 
        my_list =rows.Alpha
        Row_list8.append(my_list) 
    df9=df[['Capex']]  
    list9=[]
    for i in range (0,len(df9)-1):
        list9.append(df9.loc[[i]])
    Row_list9=[]
    for index, rows in df9.iterrows(): 
        my_list =rows.Capex
        Row_list9.append(my_list)   
    list1=Row_list1
    list2=Row_list2
    list3=Row_list3
    list4=Row_list4
    list5=Row_list5
    list6=Row_list6
    list7=Row_list7
    list8=Row_list8
    list9=Row_list9
    context={'list1':list1,'list2':list2,'list3':list3,'list4':list4,'list5':list5,'list6':list6,'list7':list7,'list8':list8,'list9':list9}
    return context


def multiFactorDates():
    multi_factor_df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\page3_multi_factor.csv')
    multi_factor_dates=multi_factor_df.Trade_Dt.unique().tolist()
    chart_data = multi_factor_df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    return [multi_factor_dates,chart_data]

@login_required
def fourthpage(request):
    df1=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\pie_drilldown_sector.csv')
    df1=df1.sort_values('Gross_Exposure_Percentage')
    trade_dt=list(df1['trade_dt'])
    trade_dt = list(dict.fromkeys(trade_dt))
    sectors_list_total=[]
    for each in trade_dt:
        c=0
        each_date= df1[df1['trade_dt']==each]
        sec_list=list(each_date['sector'])
        pnl_list=list(each_date['Gross_Exposure_Percentage'])
        sectors_list_each=[]
        for i in range(0,len(sec_list)):
           dict1={'date':each,'name':sec_list[i],'y':pnl_list[i],'drilldown':sec_list[i]}   
           sectors_list_each.append(dict1)
           c=c+1
        sectors_list_total.append(sectors_list_each)
    ticker_csv=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\pie_drilldown_region.csv')
    ticker_list_total=[]
    for i in range(0,len(trade_dt)):
        ticker_list1=[]
        ticker_each=ticker_csv[ticker_csv['trade_dt']==trade_dt[i]]
        for j in range(0,len(sectors_list_total[i])):
           sector_match=ticker_each[ticker_each['sector']==sectors_list_total[i][j]['name']]
           ticker_list=list(sector_match['region'])
           pnl_list=list(sector_match['Percentage'])
           ticker_pnl=[]
           for k in range(0,len(ticker_list)):
                   temp_list=[]
                   temp_list.append(ticker_list[k])
                   temp_list.append(float(pnl_list[k]))
                   ticker_pnl.append(temp_list)
           dict2={'date':trade_dt[i],'name':sectors_list_total[i][j]['name'],'id':sectors_list_total[i][j]['name'],"data":ticker_pnl}
           ticker_list1.append(dict2)
        ticker_list_total.append(ticker_list1)

    df1=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\bar_drilldown_sector.csv')
    trade_dt=list(df1['Trade_Dt'])
    trade_dt = list(dict.fromkeys(trade_dt))
    sectors_names=[]
    sectors_list_total2=[]
    for each in trade_dt:
        each_date= df1[df1['Trade_Dt']==each]
        sec_list=list(each_date['Sector'])
        sectors_names.append(sec_list)
        pnl_list=list(each_date['PNL'])
        sectors_list_each=[]
        for i in range(0,len(sec_list)):
            dict1={'name':sec_list[i],'y':pnl_list[i],"drilldown":sec_list[i],'date':each,}
            sectors_list_each.append(dict1)
        sectors_list_total2.append(sectors_list_each)

    ticker_csv=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\bar_drilldown_ticker.csv')
    ticker_list_total2=[]
    for i in range(0,len(trade_dt)):
        ticker_list1=[]
        ticker_each=ticker_csv[ticker_csv['Trade_Dt']==trade_dt[i]]
        for j in range(0,len(sectors_list_total2[i])):
            sector_match=ticker_each[ticker_each['Sector']==sectors_list_total2[i][j]['name']]
            ticker_list=list(sector_match['Client_Symbol'])
            pnl_list=list(sector_match['PNL'])
            ticker_pnl=[]
            for k in range(0,len(ticker_list)):
                    temp_list=[]
                    temp_list.append(ticker_list[k])
                    temp_list.append(pnl_list[k])
                    ticker_pnl.append(temp_list)
            dict2={'name':sectors_list_total2[i][j]['name'],"id":sectors_list_total2[i][j]['name'],"data":ticker_pnl,'date':trade_dt[i]}
            ticker_list1.append(dict2)
        ticker_list_total2.append(ticker_list1)
    context={"sector":sectors_list_total,'region':ticker_list_total,"date":trade_dt,"sector2":sectors_list_total2,"ticker":ticker_list_total2,"sec_names":sectors_names}
    return render(request,'page4.html',context)
    
@login_required
def fifthpage(request):
    df = pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\VaR_PNL_monitoring.csv')
    df1=df[['Positive_Var90D','Negative_Var90D']] 
    list1=[]
    list3=[]
    for i in range (0,len(df1)-1):
        list1.append([df1.loc[[i]]])
    df2=df[['PNL']] 
    df3=df[['Trade_Dt']] 
    list2=[]
    for i in range (0,len(df2)-1):
        list2.append([df2.loc[[i]]])
    Row_list =[] 
    for index, rows in df1.iterrows(): 
        my_list =[rows.Positive_Var90D,rows.Negative_Var90D] 
        Row_list.append(my_list) 
    Row_list2 =[] 
    for i in range (0,len(df3)-1):
        list3.append([df3.loc[[i]]])
    Row_list3 =[] 
    for index, rows in df3.iterrows(): 
        my_list =rows.Trade_Dt
        Row_list3.append(my_list) 
    for index, rows in df2.iterrows(): 
        my_list =rows.PNL
        Row_list2.append(my_list) 
    list1=Row_list
    list2=Row_list2
    list3=Row_list3
    df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\var_attribution_reduction.csv')
    df1=df[['trade_dt']] 
    list4=[]
    for i in range (0,len(df1)-1):
        list4.append(df1.loc[[i]])
    Row_list4=[]
    for index, rows in df1.iterrows(): 
        my_list =rows.trade_dt 
        Row_list4.append(my_list) 
    df2=df[['India']] 
    list5=[]
    for i in range (0,len(df2)-1):
        list5.append(df2.loc[[i]])
    Row_list5=[]
    for index, rows in df2.iterrows(): 
        my_list =rows.India 
        Row_list5.append(my_list) 
    df3=df[['Brazil']] 
    list6=[]
    for i in range (0,len(df3)-1):
        list6.append(df3.loc[[i]])
    Row_list6=[]
    for index, rows in df3.iterrows(): 
        my_list =rows.Brazil 
        Row_list6.append(my_list) 
    df4=df[['China']] 
    list7=[]
    for i in range (0,len(df4)-1):
        list7.append(df4.loc[[i]])
    Row_list7=[]
    for index, rows in df4.iterrows(): 
        my_list =rows.China 
        Row_list7.append(my_list)
    df5=df[['Mexico']] 
    list8=[]
    for i in range (0,len(df5)-1):
        list8.append(df5.loc[[i]])
    Row_list8=[]
    for index, rows in df5.iterrows(): 
        my_list =rows.Mexico 
        Row_list8.append(my_list) 
    df6=df[['Taiwan']] 
    list9=[]
    for i in range (0,len(df6)-1):
        list9.append(df6.loc[[i]])
    Row_list9=[]
    for index, rows in df6.iterrows(): 
        my_list =rows.Taiwan 
        Row_list9.append(my_list) 
    df7=df[['Philippines']] 
    list10=[]
    for i in range (0,len(df7)-1):
        list10.append(df7.loc[[i]])
    Row_list10=[]
    for index, rows in df7.iterrows(): 
        my_list =rows.Philippines 
        Row_list10.append(my_list) 
    list4=Row_list4
    list5=Row_list5
    list6=Row_list6
    list7=Row_list7
    list8=Row_list8
    list9=Row_list9
    list10=Row_list10
    context={'data':list1,'data2':list2,'data3':list3,'list4':list4,'list5':list5,'list6':list6,'list7':list7,'list8':list8,'list9':list9,'list10':list10}
    return render(request, 'page5.html',context)

@login_required
def sixthpage(request):
    df = pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\page6_T12M_upside_downside.csv')
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    context={'data4':chart_data}
    
    return render(request, 'page6.html',context)

def portfolioMeasurments():
    df = pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page1_table.csv')
    df['year'] = pd.DatetimeIndex(df['Trade_Dt']).year
    df['month'] = pd.DatetimeIndex(df['Trade_Dt']).month
    df['day'] = pd.DatetimeIndex(df['Trade_Dt']).day
    df['month']=df.month.map("{:02}".format)
    df['day']=df.day.map("{:02}".format)
    df['Trade_Dt'] = df['day'].apply(str) +'/'+ df['month'].apply(str)+'/'+ df['year'].apply(str)
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    return chart_data

def plotFamaFrench(df):
    df1=df[['Trade_Dt']] 
    list1=[]
    for i in range (0,len(df1)-1):
        list1.append(df1.loc[[i]])
    Row_list1=[]
    for index, rows in df1.iterrows(): 
    # Create list for the current row 
        my_list =rows.Trade_Dt 
        Row_list1.append(my_list)
    df2=df[['Market']] 
    list2=[]
    for i in range (0,len(df2)-1):
        list2.append(df2.loc[[i]])
    Row_list2=[]
    for index, rows in df2.iterrows(): 
    # Create list for the current row 
        my_list =rows.Market 
        Row_list2.append(my_list) 
    df3=df[['Growth']] 
    list3=[]
    for i in range (0,len(df3)-1):
        list3.append(df3.loc[[i]])
    Row_list3=[]
    for index, rows in df3.iterrows(): 
    # Create list for the current row 
        my_list =rows.Growth 
        Row_list3.append(my_list) 
    df4=df[['Momentum']] 
    list4=[]
    for i in range (0,len(df4)-1):
        list4.append(df4.loc[[i]])
    Row_list4=[]
    for index, rows in df4.iterrows(): 
    # Create list for the current row 
        my_list =rows.Momentum 
        Row_list4.append(my_list) 
    df5=df[['Quality']] 
    list5=[]
    for i in range (0,len(df5)-1):
        list5.append(df5.loc[[i]])
    Row_list5=[]
    for index, rows in df5.iterrows(): 
    # Create list for the current row 
        my_list =rows.Quality 
        Row_list5.append(my_list)
    df6=df[['Size']] 
    list6=[]
    for i in range (0,len(df6)-1):
        list6.append(df6.loc[[i]])
    Row_list6=[]
    for index, rows in df6.iterrows(): 
    # Create list for the current row 
        my_list =rows.Size 
        Row_list6.append(my_list)
    df7=df[['Fund']]  
    list7=[]
    for i in range (0,len(df7)-1):
        list7.append(df7.loc[[i]])
    Row_list7=[]
    for index, rows in df7.iterrows(): 
    # Create list for the current row 
        my_list =rows.Fund
        Row_list7.append(my_list)

    df8=df[['Alpha']]  
    list8=[]
    for i in range (0,len(df8)-1):
        list8.append(df8.loc[[i]])
    Row_list8=[]
    for index, rows in df8.iterrows(): 
    # Create list for the current row 
        my_list =rows.Alpha
        Row_list8.append(my_list) 

    df9=df[['Capex']]  
    list9=[]
    for i in range (0,len(df9)-1):
        list9.append(df9.loc[[i]])
    Row_list9=[]
    for index, rows in df9.iterrows(): 
    # Create list for the current row 
        my_list =rows.Capex
        Row_list9.append(my_list)   
    list1=Row_list1
    list2=Row_list2
    list3=Row_list3
    list4=Row_list4
    list5=Row_list5
    list6=Row_list6
    list7=Row_list7
    list8=Row_list8
    list9=Row_list9
    
    # multi_factor_df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\page3_multi_factor.csv')
    # multi_factor_dates=multi_factor_df.Trade_Dt.unique().tolist()

    context={'list1':list1,'list2':list2,'list3':list3,'list4':list4,'list5':list5,'list6':list6,'list7':list7,'list8':list8,'list9':list9}
    # context={'list1':list1,'list2':list2,'list3':list3,'list4':list4,'list5':list5,'list6':list6,'list7':list7}
    return context


def varnpl(df):
    df1=df[['Positive_Var90D','Negative_Var90D']] 
    list1=[]
    list3=[]
    for i in range (0,len(df1)-1):
        list1.append([df1.loc[[i]]])
    df2=df[['PNL']] 
    df3=df[['Trade_Dt']] 
    list2=[]
    for i in range (0,len(df2)-1):
        list2.append([df2.loc[[i]]])
    Row_list =[] 
    for index, rows in df1.iterrows(): 
        my_list =[rows.Positive_Var90D,rows.Negative_Var90D] 
        Row_list.append(my_list) 
    Row_list2 =[] 
    for i in range (0,len(df3)-1):
        list3.append([df3.loc[[i]]])
    Row_list3 =[] 
    for index, rows in df3.iterrows(): 
        my_list =rows.Trade_Dt
        Row_list3.append(my_list) 
    for index, rows in df2.iterrows(): 
        my_list =rows.PNL
        Row_list2.append(my_list) 
    list1=Row_list
    list2=Row_list2
    list3=Row_list3
    context={'data11':list1,'data12':list2,'data13':list3}
    return context


@login_required
def chatbot(request):
    userText = request.POST.get('input')
    title=''
    if userText is not None:
        userText = userText.lower()
        userText = re.sub(r'[^a-zA-Z0-9\s]', ' ', userText)
        tokens = nltk.word_tokenize(userText)
        bi_grams = list(ngrams(tokens, 2))
        bi_tokens = [ ''.join(grams) for grams in bi_grams]
        tri_grams = list(ngrams(tokens, 3))
        tri_tokens = [ ''.join(grams) for grams in tri_grams]
        tokens = tokens + bi_tokens +tri_tokens
        # reading chart title keywords and extracting name of required chart
        chart_titles = pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\chart_titles.csv')
        tkn_list = pd.DataFrame(tokens,columns = ['tokens'])
        req_chart = pd.merge(tkn_list, chart_titles, left_on='tokens', right_on='Keywords')
        flag = req_chart.empty
        if flag is False:
           req_chart_name = req_chart.Chart_Name[0]
           request.session['title'] = req_chart_name
        # else:
        #     request.session['title'] = 'nochart'
    else:
        request.session['title'] = ''

    if request.method == 'POST':
        try:
            chart_data = []
            print(request.session['title'])
            sub_key = subChartKeywordFinder(userText)
            if sub_key is not '':
                title = sub_chart_name(request.session['title'], sub_key)
            if  request.session['title'] == "Portfolio Measurements":
                chart_data = portfolioMeasurments()
                return render(request, 'chat.html', {'data2': chart_data})    

            elif title == 'Multi Factor Model':
                multi_dates = multiFactorDates()
                return render(request, 'chat.html', {'multi_dates': multi_dates[0], 'multi_chart': multi_dates[1]})
            
            elif request.session['title'] == 'Benchmark vs Fund Returns':
                df1 = pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\page6_T12M_upside_downside.csv')
                df2 = pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\page6_Fund_benchmark_return.csv')
                chart_data1 = df1.to_dict(orient='records')
                chart_data1 = json.dumps(chart_data1, indent=2)
                chart_data2 = df2.to_dict(orient='records')
                chart_data2 = json.dumps(chart_data2, indent=2)
                context={'bench':chart_data1,'benchreturn':chart_data2}
                return render(request, 'chat.html', context) 

            elif request.session['title'] == 'Volatility Evolution':
                df = pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\page6_T12M_upside_downside.csv')
                chart_data = df.to_dict(orient='records')
                chart_data = json.dumps(chart_data, indent=2)
                context={'volatility':chart_data}
                return render(request, 'chat.html', context)
            elif request.session['title'] == 'Frequency Distribution - Since Inception':
                df = pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\frequency_dist_inception.csv')
                chart_data = df.to_dict(orient='records')
                chart_data = json.dumps(chart_data, indent=2)
                context={'freqinception':chart_data}
                return render(request, 'chat.html', context)

            elif request.session['title'] == 'Gross Exposure Drilldown By Sector':
                    df1=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\pie_drilldown_sector.csv')
                    df1=df1.sort_values('Gross_Exposure_Percentage')
                    trade_dt=list(df1['trade_dt'])
                    trade_dt = list(dict.fromkeys(trade_dt))
                    sectors_list_total=[]
                    for each in trade_dt:
                        c=0
                        each_date= df1[df1['trade_dt']==each]
                        sec_list=list(each_date['sector'])
                        pnl_list=list(each_date['Gross_Exposure_Percentage'])
                        sectors_list_each=[]
                        for i in range(0,len(sec_list)):
                            dict1={'date':each,'name':sec_list[i],'y':pnl_list[i],'drilldown':sec_list[i]}   
                            sectors_list_each.append(dict1)
                            c=c+1
                        sectors_list_total.append(sectors_list_each)
                    ticker_csv=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\pie_drilldown_region.csv')
                    ticker_list_total=[]
                    for i in range(0,len(trade_dt)):
                        ticker_list1=[]
                        ticker_each=ticker_csv[ticker_csv['trade_dt']==trade_dt[i]]
                        for j in range(0,len(sectors_list_total[i])):
                            sector_match=ticker_each[ticker_each['sector']==sectors_list_total[i][j]['name']]
                            ticker_list=list(sector_match['region'])
                            pnl_list=list(sector_match['Percentage'])
                            ticker_pnl=[]
                            for k in range(0,len(ticker_list)):
                                temp_list=[]
                                temp_list.append(ticker_list[k])
                                temp_list.append(float(pnl_list[k]))
                                ticker_pnl.append(temp_list)
                        dict2={'date':trade_dt[i],'name':sectors_list_total[i][j]['name'],'id':sectors_list_total[i][j]['name'],"data":ticker_pnl}
                        ticker_list1.append(dict2)
                    ticker_list_total.append(ticker_list1)
                    context={"sector":sectors_list_total,'region':ticker_list_total}
                    return render(request, 'chat.html',context)
            elif request.session['title'] == "PNL Drilldown By Sector":
                df1=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\bar_drilldown_sector.csv')
                trade_dt=list(df1['Trade_Dt'])
                trade_dt = list(dict.fromkeys(trade_dt))
                sectors_names=[]
                sectors_list_total2=[]
                for each in trade_dt:
                    each_date= df1[df1['Trade_Dt']==each]
                    sec_list=list(each_date['Sector'])
                    sectors_names.append(sec_list)
                    pnl_list=list(each_date['PNL'])
                    sectors_list_each=[]
                    for i in range(0,len(sec_list)):
                        dict1={'name':sec_list[i],'y':pnl_list[i],"drilldown":sec_list[i],'date':each,}
                        sectors_list_each.append(dict1)
                    sectors_list_total2.append(sectors_list_each)

                ticker_csv=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\bar_drilldown_ticker.csv')
                ticker_list_total2=[]
                for i in range(0,len(trade_dt)):
                    ticker_list1=[]
                    ticker_each=ticker_csv[ticker_csv['Trade_Dt']==trade_dt[i]]
                    for j in range(0,len(sectors_list_total2[i])):
                        sector_match=ticker_each[ticker_each['Sector']==sectors_list_total2[i][j]['name']]
                        ticker_list=list(sector_match['Client_Symbol'])
                        pnl_list=list(sector_match['PNL'])
                        ticker_pnl=[]
                        for k in range(0,len(ticker_list)):
                                temp_list=[]
                                temp_list.append(ticker_list[k])
                                temp_list.append(pnl_list[k])
                                ticker_pnl.append(temp_list)
                        dict2={'name':sectors_list_total2[i][j]['name'],"id":sectors_list_total2[i][j]['name'],"data":ticker_pnl,'date':trade_dt[i]}
                        ticker_list1.append(dict2)
                    ticker_list_total2.append(ticker_list1)
                context = {"date":trade_dt,"sector2":sectors_list_total2,"ticker":ticker_list_total2,"sec_names":sectors_names}
                return render(request, 'chat.html',context)
            elif request.session['title'] == "Frequency Distribution - Trailing 2 Years":
                df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\frequency_dist_T2years.csv')
                chart_data1 = df.to_dict(orient='records')
                chart_data1 = json.dumps(chart_data1, indent=2)
                return render(request, 'chat.html',{'freqdist': chart_data1})
            elif request.session['title'] == "FAMA FRENCH MODEL":
                df=pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page3_fama_french.csv')
                if userText is not None:
                    dates = datepicker(userText)
                    if dates[0] is not '':
                        start_date = pd.to_datetime(dates[0], format='%Y-%m-%d')
                        end_date = pd.to_datetime(dates[1], format='%Y-%m-%d')
                        df['Trade_Dt'] = pd.to_datetime(df['Trade_Dt'])
                        mask = (df['Trade_Dt'] > start_date) & (df['Trade_Dt'] <= end_date)
                        df['Trade_Dt'] = pd.to_datetime(df['Trade_Dt'] ).dt.strftime('%d-%m-%y')
                        df = df[mask]
                        df = df.reset_index()
                    context = plotFamaFrench(df)
                    return render(request, 'chat.html',context)

            elif title == 'Portfolio Measurements':
                df = pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page1_table.csv')
                # df=df.loc[df['Trade_Dt'] == '1/19/2017']
                chart_data2 = portfolioSnapshot(df)
                return render(request, 'chat.html',{'port1': chart_data2})

            elif title == 'Monthly Performance':
                df=pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page1_ytd.csv')
                ytd=df.YTD.values.tolist()
                year=df.YEAR.values.tolist()
                context={'ytd':ytd,'year':year}
                return render(request, 'chat.html', context)

            elif request.session['title'] == "Growth of $1000-Since Inception":
                df = pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\chart1.csv')
                df['year'] = pd.DatetimeIndex(df['Trade_Dt']).year            
                df['month'] = pd.DatetimeIndex(df['Trade_Dt']).month
                df['day'] = pd.DatetimeIndex(df['Trade_Dt']).day
                df['month']=df.month.map("{:02}".format)
                df['day']=df.day.map("{:02}".format)
                df['Trade_Dt'] = df['year'].apply(str) +'-'+ df['month'].apply(str)+'-'+ df['day'].apply(str)
                df=df.groupby(['Trade_Dt','year','month','day'],as_index = False).agg('sum')
                df=df.groupby(["Trade_Dt"]).apply(lambda x: x.sort_values(["Trade_Dt"], ascending = True)).reset_index(drop=True)
                if userText is not None:
                    dates = datepicker(userText)
                    if dates[0] is not '':
                        start_date = pd.to_datetime(dates[0], format='%Y-%m-%d')
                        end_date = pd.to_datetime(dates[1], format='%Y-%m-%d')
                        df['Trade_Dt'] = pd.to_datetime(df['Trade_Dt'])
                        mask = (df['Trade_Dt'] > start_date) & (df['Trade_Dt'] <= end_date)
                        df['Trade_Dt'] = pd.to_datetime(df['Trade_Dt'] ).dt.strftime('%Y-%m-%d')
                        df = df[mask]
                    chart_data = df.to_dict(orient='records')
                    chart_data = json.dumps(chart_data, indent=2)
                    return render(request, 'chat.html',{'chart_data': chart_data})

            elif title == 'Net Exposure by Stock':
                df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\net_exposure_stock.csv')
                # df=df.loc[df['Date'] == '2017-01-04']
                chart_data1 = df.to_dict(orient='records')
                chart_data1 = json.dumps(chart_data1, indent=2)
                return render(request, 'chat.html',{'chart1': chart_data1})

            elif title == 'Net Exposure by Country':
                df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\net_exposure_country.csv')
                # df=df.loc[df['Date'] == '2017-01-04']
                chart_data3 = df.to_dict(orient='records')
                chart_data3 = json.dumps(chart_data3, indent=2)
                return render(request, 'chat.html',{'chart2': chart_data3})

            elif title == 'Net Exposure by Sector':
                df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\net_exposure_sector.csv')
                # df=df.loc[df['Date'] == '2017-01-04']
                chart_data2 = df.to_dict(orient='records')
                chart_data2 = json.dumps(chart_data2, indent=2)
                return render(request, 'chat.html',{'chart3': chart_data2})

            elif request.session['title'] == 'Net Exposure':
                df = pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\three.csv')
                if userText is not None:
                    dates = datepicker(userText)
                    if dates[0] is not '':
                        start_date = pd.to_datetime(dates[0], format='%Y-%m-%d')
                        end_date = pd.to_datetime(dates[1], format='%Y-%m-%d')
                        df['Date'] = pd.to_datetime(df['Date'])
                        mask = (df['Date'] > start_date) & (df['Date'] <= end_date)
                        df['Date'] = pd.to_datetime(df['Date'] ).dt.strftime('%d-%b-%y')
                        df = df[mask]
                    chart_data = df.to_dict(orient='records')
                    chart_data = json.dumps(chart_data, indent=2)
                    return render(request, 'chat.html',{'chart_data1': chart_data})

            elif title == 'VaR by Stock':
                df=pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page5_table1.csv')
                # df=df.loc[df['trade_dt'] == '1/2/2017']
                # df=df.iloc[:5]
                chart_data2 = df.to_dict(orient='records')
                chart_data2 = json.dumps(chart_data2, indent=2)
                return render(request, 'chat.html',{'chart4': chart_data2})

            elif title == 'VaR by Country':
                df=pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page5_table2.csv')
                # df=df.loc[df['trade_dt'] == '1/2/2017']
                # df=df.iloc[:5]
                chart_data2 = df.to_dict(orient='records')
                chart_data2 = json.dumps(chart_data2, indent=2)
                return render(request, 'chat.html',{'chart5': chart_data2})

            elif title == 'VaR by Sector':
                df=pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page5_table3.csv')
                # df=df.loc[df['trade_dt'] == '1/2/2017']
                # df=df.iloc[:5]
                chart_data2 = df.to_dict(orient='records')
                chart_data2 = json.dumps(chart_data2, indent=2)
                return render(request, 'chat.html',{'chart6': chart_data2})

            elif request.session['title'] == 'VaRnPNL':
                df = pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\VaR_PNL_monitoring.csv')
                if userText is not None:
                    dates = datepicker(userText)
                    if dates[0] is not '':
                        start_date = pd.to_datetime(dates[0], format='%Y-%m-%d')
                        end_date = pd.to_datetime(dates[1], format='%Y-%m-%d')
                        df['Trade_Dt'] = pd.to_datetime(df['Trade_Dt'])
                        mask = (df['Trade_Dt'] > start_date) & (df['Trade_Dt'] <= end_date)
                        df['Trade_Dt'] = pd.to_datetime(df['Trade_Dt'] ).dt.strftime('%d-%b-%y')
                        df = df[mask]
                        df = df.reset_index()   
                    context = varnpl(df)
                    return render(request, 'chat.html',context)
            
            elif request.session['title'] == 'nochart':
                msg = "To get started, Simply ask chart name. Ex: fama french or net exposure or fund returns"
                return render(request, 'chat.html',{'error': msg})
            elif request.session['title'] == 'Hello':
                msg = "Hello, I am Goldie. To get started, Simply ask me a question!"
                return render(request, 'chat.html',{'error': msg})
            elif request.session['title'] == 'Hi':
                msg = "Hi, I am Goldie. To get started, Simply ask me a question!"
                return render(request, 'chat.html',{'error': msg})
            elif request.session['title'] == 'Bye':
                msg = "Bye, Thank you"
                return render(request, 'chat.html',{'error': msg})
            elif request.session['title'] == 'Ok':
                msg = "Okay, Thank you. If you want any chart, I'll help you."
                return render(request, 'chat.html',{'error': msg})
            elif request.session['title'] == 'noquery':
                msg = "To get started, Simply ask me a question!"
                return render(request, 'chat.html',{'error': msg})
            else:
                msg = "I didn't understand, please try something else Ex: fama french or net exposure or fund returns"
                return render(request, 'chat.html',{'error': msg})
        except IndexError:
            msg = "I didn't find any related chart, please try something else"
            return render(request, 'chat.html',{'error': msg})
    else:
        return render(request, 'chat.html')

def voicebot(request):
    # get audio from the microphone
    try:
        r = sr.Recognizer()
        title =''
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            userText= r.recognize_google(audio)
            if userText is not None:
                userText = userText.lower()
                userText = re.sub(r'[^a-zA-Z0-9\s]', ' ', userText)
                tokens = nltk.word_tokenize(userText)
                bi_grams = list(ngrams(tokens, 2))
                bi_tokens = [ ''.join(grams) for grams in bi_grams]
                tri_grams = list(ngrams(tokens, 3))
                tri_tokens = [ ''.join(grams) for grams in tri_grams]
                tokens = tokens + bi_tokens +tri_tokens
                # reading chart title keywords and extracting name of required chart
                chart_titles = pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\chart_titles.csv')
                tkn_list = pd.DataFrame(tokens,columns = ['tokens'])
                req_chart = pd.merge(tkn_list, chart_titles, left_on='tokens', right_on='Keywords')
                flag = req_chart.empty
                if flag is False:
                    req_chart_name = req_chart.Chart_Name[0]
                    request.session['title'] = req_chart_name
            else:
                request.session['title'] = ''
            try:
                sub_key = subChartKeywordFinder(userText)
                if sub_key is not '':
                    title = sub_chart_name(request.session['title'], sub_key)

                if  request.session['title'] == "Portfolio Measurements":
                    chart_data = portfolioMeasurments()
                    return render(request, 'chat.html', {'data2': chart_data})    

                elif title == 'Multi Factor Model':
                    multi_dates = multiFactorDates()
                    return render(request, 'chat.html', {'multi_dates': multi_dates[0], 'multi_chart': multi_dates[1]}) 

                elif request.session['title'] == "FAMA FRENCH MODEL":
                    df=pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page3_fama_french.csv')
                    if userText is not None:
                        dates = datepicker(userText)
                        print("Fama French Dates:")
                        print(dates)
                        if dates[0] is not '':
                            start_date = pd.to_datetime(dates[0], format='%Y-%m-%d')
                            end_date = pd.to_datetime(dates[1], format='%Y-%m-%d')
                            df['Trade_Dt'] = pd.to_datetime(df['Trade_Dt'])
                            mask = (df['Trade_Dt'] > start_date) & (df['Trade_Dt'] <= end_date)
                            df['Trade_Dt'] = pd.to_datetime(df['Trade_Dt'] ).dt.strftime('%d-%m-%y')
                            df = df[mask]
                            df = df.reset_index()
                        context = plotFamaFrench(df)
                        return render(request, 'chat.html',context)

                elif title == 'Portfolio Measurements':
                    df = pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page1_table.csv')
                    chart_data2 = portfolioSnapshot(df)
                    return render(request, 'chat.html',{'port1': chart_data2})

                elif title == 'Monthly Performance':
                    df=pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page1_ytd.csv')
                    ytd=df.YTD.values.tolist()
                    year=df.YEAR.values.tolist()
                    context={'ytd':ytd,'year':year}
                    return render(request, 'chat.html', context)

                elif request.session['title'] == "Growth of $1000-Since Inception":
                    df = pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\chart1.csv')
                    df['year'] = pd.DatetimeIndex(df['Trade_Dt']).year            
                    df['month'] = pd.DatetimeIndex(df['Trade_Dt']).month
                    df['day'] = pd.DatetimeIndex(df['Trade_Dt']).day
                    df['month']=df.month.map("{:02}".format)
                    df['day']=df.day.map("{:02}".format)
                    df['Trade_Dt'] = df['year'].apply(str) +'-'+ df['month'].apply(str)+'-'+ df['day'].apply(str)
                    df=df.groupby(['Trade_Dt','year','month','day'],as_index = False).agg('sum')
                    df=df.groupby(["Trade_Dt"]).apply(lambda x: x.sort_values(["Trade_Dt"], ascending = True)).reset_index(drop=True)
                    if userText is not None:
                        dates = datepicker(userText)
                        print("Cumulative Dates")
                        print(dates)
                        if dates[0] is not '':
                            start_date = pd.to_datetime(dates[0], format='%Y-%m-%d')
                            end_date = pd.to_datetime(dates[1], format='%Y-%m-%d')
                            df['Trade_Dt'] = pd.to_datetime(df['Trade_Dt'])
                            mask = (df['Trade_Dt'] > start_date) & (df['Trade_Dt'] <= end_date)
                            df['Trade_Dt'] = pd.to_datetime(df['Trade_Dt'] ).dt.strftime('%Y-%m-%d')
                            df = df[mask]
                        chart_data = df.to_dict(orient='records')
                        chart_data = json.dumps(chart_data, indent=2)
                        return render(request, 'chat.html',{'chart_data': chart_data})

                elif title == 'Net Exposure by Stock':
                    df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\net_exposure_stock.csv')
                    chart_data1 = df.to_dict(orient='records')
                    chart_data1 = json.dumps(chart_data1, indent=2)
                    return render(request, 'chat.html',{'chart1': chart_data1})

                elif title == 'Net Exposure by Country':
                    df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\net_exposure_country.csv')
                    chart_data3 = df.to_dict(orient='records')
                    chart_data3 = json.dumps(chart_data3, indent=2)
                    return render(request, 'chat.html',{'chart2': chart_data3})

                elif title == 'Net Exposure by Sector':
                    df=pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\net_exposure_sector.csv')
                    chart_data2 = df.to_dict(orient='records')
                    chart_data2 = json.dumps(chart_data2, indent=2)
                    return render(request, 'chat.html',{'chart3': chart_data2})

                elif request.session['title'] == 'Net Exposure':
                    df = pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\three.csv')
                    if userText is not None:
                        dates = datepicker(userText)
                        print("Net Exposure Dates")
                        print(dates)
                        if dates[0] is not '':
                            start_date = pd.to_datetime(dates[0], format='%Y-%m-%d')
                            end_date = pd.to_datetime(dates[1], format='%Y-%m-%d')
                            df['Date'] = pd.to_datetime(df['Date'])
                            mask = (df['Date'] > start_date) & (df['Date'] <= end_date)
                            df['Date'] = pd.to_datetime(df['Date'] ).dt.strftime('%d-%b-%y')
                            df = df[mask]
                        chart_data = df.to_dict(orient='records')
                        chart_data = json.dumps(chart_data, indent=2)
                        return render(request, 'chat.html',{'chart_data1': chart_data})

                elif title == 'VaR by Stock':
                    df=pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page5_table1.csv')
                    chart_data2 = df.to_dict(orient='records')
                    chart_data2 = json.dumps(chart_data2, indent=2)
                    return render(request, 'chat.html',{'chart4': chart_data2})

                elif title == 'VaR by Country':
                    df=pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page5_table2.csv')
                    chart_data2 = df.to_dict(orient='records')
                    chart_data2 = json.dumps(chart_data2, indent=2)
                    return render(request, 'chat.html',{'chart5': chart_data2})

                elif title == 'VaR by Sector':
                    df=pd.read_csv(r'C:\Users\vinaykumar.ch\Desktop\Kiski_New\Kiski\Graphs\static\csv\page5_table3.csv')
                    chart_data2 = df.to_dict(orient='records')
                    chart_data2 = json.dumps(chart_data2, indent=2)
                    return render(request, 'chat.html',{'chart6': chart_data2})

                elif request.session['title'] == 'VaRnPNL':
                    df = pd.read_csv(r'I:\Kiski_Project\Kiski\Graphs\static\csv\VaR_PNL_monitoring.csv')
                    if userText is not None:
                        dates = datepicker(userText)
                        print("Risk Dates")
                        print(dates)
                        if dates[0] is not '':
                            start_date = pd.to_datetime(dates[0], format='%Y-%m-%d')
                            end_date = pd.to_datetime(dates[1], format='%Y-%m-%d')
                            df['Trade_Dt'] = pd.to_datetime(df['Trade_Dt'])
                            mask = (df['Trade_Dt'] > start_date) & (df['Trade_Dt'] <= end_date)
                            df['Trade_Dt'] = pd.to_datetime(df['Trade_Dt'] ).dt.strftime('%d-%b-%y')
                            df = df[mask]
                            df = df.reset_index()   
                        context = varnpl(df)
                        return render(request, 'chat.html',context)
                
                elif request.session['title'] == 'nochart':
                    msg = "To get started, Simply ask chart name. Ex: fama french or net exposure or fund returns"
                    return render(request, 'chat.html',{'error': msg})
                elif request.session['title'] == 'Hello':
                    msg = "Hello, I am Goldie. To get started, Simply ask me a question!"
                    return render(request, 'chat.html',{'error': msg})
                elif request.session['title'] == 'Hi':
                    msg = "Hi, I am Goldie. To get started, Simply ask me a question!"
                    return render(request, 'chat.html',{'error': msg})
                elif request.session['title'] == 'Bye':
                    msg = "Bye, Thank you"
                    return render(request, 'chat.html',{'error': msg})
                elif request.session['title'] == 'Ok':
                    msg = "Okay, Thank you. If you want any chart, I'll help you."
                    return render(request, 'chat.html',{'error': msg})
                elif request.session['title'] == 'noquery':
                    msg = "To get started, Simply ask me a question!"
                    return render(request, 'chat.html',{'error': msg})
                else:
                    msg = "I didn't understand, please try something else Ex: fama french or net exposure or fund returns"
                    return render(request, 'chat.html',{'error': msg})
            except IndexError:
                msg = "I didn't find any related chart, please try something else"
                return render(request, 'chat.html',{'error': msg})
        except sr.UnknownValueError:
            msg = "I could not understand your voice, please try again once!"
        except sr.RequestError as e:
            msg = "Could not request results; {0}".format(e)
            return render(request, 'chat.html',{'error': msg})
    except:
        msg = "Please connet to microphone."
        return render(request, 'chat.html',{'error1': msg})