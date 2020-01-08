#bajar credenciales de api console (CUENTA DE SERVICIO). Dar acceso de editor al mail de la cuenta de servicio a GA.
#completar view ID
#crear los reportes que queramos

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import csv, time
import datetime
import pandas as pd
import json

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

SAMPLING_LEVEL = 'LARGE'
PAGE_SIZE = '10000'
PAGE_TOKEN = '10000'
NEXT_PAGE = '10000'

def GA_to_DF(KEY_FILE_LOCATION,VIEW_ID,cant_dias,repo):

    
    START_DATE = (datetime.date.today() - datetime.timedelta(days = cant_dias)).isoformat()
    END_DATE = (datetime.date.today() - datetime.timedelta(days = 1)).isoformat()
    repo['reportRequests'][0]['dateRanges'][0]['endDate']=END_DATE
    repo['reportRequests'][0]['dateRanges'][0]['startDate']=START_DATE
    
        #se conecta a analytics
    def initialize_analyticsreporting(KEY_FILE_LOCATION):
      """Initializes an Analytics Reporting API V4 service object.

      Returns:
        An authorized Analytics Reporting API V4 service object.
      """
      credentials = ServiceAccountCredentials.from_json_keyfile_name(
          KEY_FILE_LOCATION, SCOPES)

      # Build the service object.
      analytics = build('analyticsreporting', 'v4', credentials=credentials)

      return analytics

    #baja el reporte
    def get_report(analytics, report_config):
      """Queries the Analytics Reporting API V4.

      Args:
        analytics: An authorized Analytics Reporting API V4 service object.
      Returns:
        The Analytics Reporting API V4 response.
      """
      return analytics.reports().batchGet(body = report_config).execute()


    #convierte el reporte a un mejor formato para poder guardarlo en un df
    def arrangedict(response):  
      okarray = []
      for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
          dimensions = row.get('dimensions', [])
          metrics = row.get('metrics', [])[0].get('values',[])
          rowdict = {}
          for header, dimension in zip(dimensionHeaders, dimensions):
                rowdict[header] = dimension
          for header, metric in zip(metricHeaders, metrics):
                rowdict[header['name']] = metric
          okarray.append(rowdict)
      return okarray

    
    #convierte el reporte a df
    def convert_to_df(array):
        jsonfinal = json.dumps(array)
        df = pd.read_json(jsonfinal)
        return df

    analytics = initialize_analyticsreporting(KEY_FILE_LOCATION=KEY_FILE_LOCATION)
    data = get_report(analytics, repo)
    df = convert_to_df(arrangedict(data))
    return df