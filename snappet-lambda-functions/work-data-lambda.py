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
        progress_list = []
        subject_list = []
        learning_list = []
        exercises = []
        students = []
        
        for d in filtered_list:
            progress_list.append(d['Progress'])
            if not d['Subject'] in subject_list:
                subject_list.append(d['Subject'])
            if not d['LearningObjective'] in learning_list:
                learning_list.append(d['LearningObjective'])
            if not d['ExerciseId'] in exercises:
                exercises.append(d['ExerciseId'])
            if not d['UserId'] in students:
                students.append(d['UserId'])
        
        avg_progress = sum(progress_list) / len(progress_list)
        
        filtered_list = sorted(filtered_list, key=lambda k: k['UserId'])
    
        response = {
            'avgProgress': avg_progress,
            'submittedAssessments': filtered_list.__len__(),
            'submittedExercises': exercises.__len__(),
            'studentsAssessed': students.__len__(),
            'subjects': subject_list,
            'learningObjectives': learning_list,
            'progressData': filtered_list
        }
    
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': 'http://localhost:4200,http://maithilee-snappet-challenge.s3-website.eu-north-1.amazonaws.com',
                'Access-Control-Allow-Methods': 'GET'
            },
            'body': json.dumps(response)
        }
    except Exception as e:
        print('Exception getting work data: ', e)
        raise e
