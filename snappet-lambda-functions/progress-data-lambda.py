import json
import urllib.parse
import boto3
import os
from datetime import date, timedelta, datetime

print('Loading function')

s3 = boto3.client('s3')

BUCKET = os.getenv('S3_BUCKET')

def lambda_handler(event, context):
    key = 'work.json'
    try:
        print(BUCKET)
        response = s3.get_object(Bucket=BUCKET, Key=key)
        response_body = json.load(response['Body'])
        query_date = event['queryStringParameters']['date']
        today = date.today()
        query_date_obj = datetime.strptime(query_date, '%Y-%m-%d').date()
        query_dates = []
        weekly_progress = {}
        print(query_date_obj)
        for i in range(7):
            day = query_date_obj - timedelta(days=i)
            iso = day.isoformat()
            query_dates.append(iso)
            weekly_progress[iso] = []
            print(f"{i} days ago: {iso}")
        print('Getting progress data for: ' + str(query_dates))
                    
        
        for d in response_body:
            submit_date = d['SubmitDateTime']
            
            if submit_date.startswith(tuple(query_dates)):
                week_date = submit_date.split('T')[0]
                progress_data = weekly_progress[week_date]
                progress_data.append(d['Progress'])
                weekly_progress[week_date] = progress_data
                
        labels = []
        series = []
        
        for week_date in weekly_progress:
            progress_data = weekly_progress[week_date]
            formatted_week_date = datetime.strptime(week_date, '%Y-%m-%d').strftime('%d-%b')
            avg_progress = 0
            if len(progress_data) != 0:
                avg_progress = sum(progress_data) * 100 / len(progress_data)
            labels.append(formatted_week_date)
            series.append(avg_progress)
        
        avg_weekly_progress = {
            'labels': labels,
            'series': series
        }     
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': 'http://localhost:4200,http://maithilee-snappet-challenge.s3-website.eu-north-1.amazonaws.com',
                'Access-Control-Allow-Methods': 'GET'
            },
            'body': json.dumps(avg_weekly_progress)
        }
    except Exception as e:
        print('Exception getting progress data: ', e)
        raise e
