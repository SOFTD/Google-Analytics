#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import csv
from datetime import date, timedelta
from collections import OrderedDict
import glob
import pandas as pd

yesterday = date.today() - timedelta(1)


# API token proporcionada por appsflyer
api_token='AQUI TU API token'
fromdate=yesterday.strftime('%Y-%m-%d')
todate=yesterday.strftime('%Y-%m-%d')
params={'api_token':api_token,'from':fromdate,'to':todate}

#Datos de tu apps en cada appsstore

iOS = 'EL ID DE TU APP EN IOS'
Android = 'EL ID DE TU APP EN ANDROID'

# Conexiones con la API

url_appevents_Android='https://hq.appsflyer.com/export/'+Android+'/in_app_events_report/v5'
url_installs_Android='https://hq.appsflyer.com/export/'+Android+'/installs_report/v5'
url_appevents_iOS='https://hq.appsflyer.com/export/'+iOS+'/in_app_events_report/v5'
url_installs_iOS='https://hq.appsflyer.com/export/'+iOS+'/installs_report/v5'

