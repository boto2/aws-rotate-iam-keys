#!/usr/bin/env python
# encoding: utf-8

import boto3
import argparse
import json
import os, sys
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.credential import AmazonWebServicesCredentials


AWS_USER_TO_UPDATE = ""
AWS_JENKINS_USER_PARAMETER_STORE = "/Servers/Infra/Jenkins/UserName"
AWS_JENKINS_PASSWORD_PARAMETER_STORE = "/Servers/Infra/Jenkins/Password"
S3_BUCKET_NAME = "personal-storage-mike"

def get_parameter_store_value(parameter_key, session):
    ssm_client = session.client('ssm')
    res = ssm_client.get_parameter(Name=parameter_key, WithDecryption=False)
    return res.get('Parameter').get('Value')

def get_all_users(iam):
    all_users = []
    for user_list in iam.list_users().get("Users"):
        all_users.append(user_list["UserName"])
    return all_users


def delete_keys(users, iam, jenkins_conn, jenkins_credentials_description, aws_user_to_update, s3_client):
    for user in users:
        if user == aws_user_to_update:
            rotate_keys_for_user(user_name=user, iam=iam, jenkins_conn=jenkins_conn, jenkins_credentials_description=jenkins_credentials_description, aws_user_to_update=aws_user_to_update, s3_client=s3_client)
        else:
            print "Skipping user {}".format(user)        


def rotate_keys_for_user(user_name, iam, jenkins_conn, jenkins_credentials_description, aws_user_to_update, s3_client):
    try:
        all_keys = iam.list_access_keys(UserName=user_name).get("AccessKeyMetadata")
        if all_keys is not None:
            for key in all_keys:
                key_id = key.get("AccessKeyId")
                print "Deleting key {} for user {}".format(key_id, user_name)
                iam.delete_access_key(UserName=user_name, AccessKeyId=key_id)
            print "Creating a new key for user {}".format(user_name)
            res = iam.create_access_key(UserName=user_name)                                     
            if user_name == aws_user_to_update:
                access_key = res.get("AccessKey")
                key_id = access_key.get("AccessKeyId")
                secret_key = access_key.get("SecretAccessKey")                
                user_dict = {
                    "access_key": str(access_key),
                    "key_id": str(key_id),
                    "secret_key": str(secret_key)
                }
                with open('aws_creds.json', 'a') as f:
                    f.write(json.dumps(user_dict, indent=4))
                    s3_client.list_objects(Bucket=S3_BUCKET_NAME)
                    print "Uploading the user credentials to {}".format(S3_BUCKET_NAME)
                    s3_client.upload_file('aws_creds.json', S3_BUCKET_NAME, 'aws_creds.json')

                creds = j.credentials                               
                aws_creds = {
                    "description": jenkins_credentials_description,
                    "accessKey": key_id,
                    "secretKey": secret_key
                }
                print "Updating Jenkins credentials {} with the AWS user name {} and with the key ID {}".format(jenkins_credentials_description, user_name, key_id)
                creds[jenkins_credentials_description] = AmazonWebServicesCredentials(aws_creds)

    except Exception as e:
        print "There was an error"
        print "{}".format(e)
        raise e


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--profile-name',
                        default=None,
                        help='The aws profile name')
    # parser.add_argument('-u', '--jenkins-user',
    #                     default=None,
    #                     required=True,
    #                     help='The jenkins user name')
    # parser.add_argument('-t', '--jenkins-password',
    #                     default=None,
    #                     required=True,
    #                     help='The jenkins password')
    # parser.add_argument('-c', '--credentials-description',
    #                     default=None,
    #                     required=True,
    #                     help='The jenkins credentials description')
    # parser.add_argument('--aws-user-to-update',
    #                     required=True,
    #                     help='The aws user to update')
    parser.add_argument('--users-file-name',
                        required=True,
                        help='The users file name')

    aws_profile_name = parser.parse_args().profile_name
    # jenkins_user = parser.parse_args().jenkins_user
    # jenkins_password = parser.parse_args().jenkins_password
    # jenkins_credentials_description = parser.parse_args().credentials_description
    # aws_user_to_update = parser.parse_args().aws_user_to_update
    users_file_name = parser.parse_args().users_file_name
    session = boto3.Session(profile_name=aws_profile_name, region_name='us-east-1')
    pathname = os.path.dirname(sys.argv[0])
    script_path = os.path.abspath(pathname)
    users_file_path = os.path.join(script_path, users_file_name)
    print "users_file_path={}".format(users_file_path)
    jenkins_user = get_parameter_store_value(session=session, parameter_key=AWS_JENKINS_USER_PARAMETER_STORE)
    jenkins_password = get_parameter_store_value(session=session, parameter_key=AWS_JENKINS_PASSWORD_PARAMETER_STORE)

    iam_client = session.client('iam')
    s3_client = session.client('s3')
    j = Jenkins(baseurl='http://34.217.108.43:8080', username=jenkins_user, password=jenkins_password)
    all_users = get_all_users(iam=iam_client)
    #delete_keys(users=all_users, iam=iam_client, jenkins_conn=j, jenkins_credentials_description=jenkins_credentials_description, aws_user_to_update=aws_user_to_update, s3_client=s3_client)