from celery import shared_task
import boto3

@shared_task
def create_keys_using_localstack(email):
    session = boto3.Session(
        aws_access_key_id="test", 
        aws_secret_access_key="test",
    )
    
    iam_client = session.client('iam', endpoint_url='http://localhost:4566')

    iam_client.create_user(UserName=email)
    access_key_response = iam_client.create_access_key(UserName=email)
    
    access_key = access_key_response['AccessKey']['AccessKeyId']
    secret_key = access_key_response['AccessKey']['SecretAccessKey']
    
    return {
        "AccessKeyId": access_key,
        "SecretAccessKey": secret_key
    }
