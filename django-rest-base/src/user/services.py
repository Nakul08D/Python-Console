import subprocess

def execute_aws_code(code):
    try:

        result = subprocess.run(
            ['python3', '-c', code],  
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout, result.stderr 
    except subprocess.CalledProcessError as e:
        return "", f"Error executing code: {e.stderr}"
    


# import boto3
# import subprocess

# def execute_aws_code(code, access_key_id, secret_access_key, service='s3'):
#     setup_code = f"""
# import boto3 
# session = boto3.Session(
#     aws_access_key_id='{access_key_id}', 
#     aws_secret_access_key='{secret_access_key}'
# )
# client = session.client('{service}', endpoint_url='http://localhost:4566')
# """
#     final_code = setup_code + code  

#     try:

#         result = subprocess.run(
#             ['python3', '-c', final_code],
#             capture_output=True,
#             text=True,
#             check=True
#         )
#         return result.stdout, result.stderr
#     except subprocess.CalledProcessError as e:
#         return "", f"Error executing code: {e.stderr}"
