import json
import urllib.parse
import boto3
import os

print('Loading function')

s3 = boto3.client('s3')

BUCKET = os.getenv('S3_BUCKET')

def lambda_handler(event, context):
    key = 'work.json'
    try:
        response = s3.get_object(Bucket=BUCKET, Key=key)
        response_body = json.load(response['Body'])
        date = event['queryStringParameters']['date']
        print('Fetching data for: ' + date)
        filtered_list = [
            dictionary for dictionary in response_body
            if dictionary['SubmitDateTime'].startswith(date)
        ]
        subject_progress = {}
        
        for d in filtered_list:
            subject = d['Subject']
            progress = d['Progress']
            subject_progress
            if not subject in subject_progress:
                subject_progress[subject] = [progress]
            else:
                progress_data = subject_progress[subject]
                progress_data.append(d['Progress'])
                subject_progress[subject] = progress_data
        
        labels = []
        series = []
        for subject in subject_progress:
            progress_data = subject_progress[subject]
            total_progress = sum(progress_data)
            labels.append(subject)
            series.append(total_progress)
        
        response_data = {
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
            'body': json.dumps(response_data)
        }
    except Exception as e:
        print('Exception getting subject progress data: ', e)
        raise e
