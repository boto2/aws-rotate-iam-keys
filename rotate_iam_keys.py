#!/usr/bin/env python
# encoding: utf-8

import boto3
import argparse
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.credential import AmazonWebServicesCredentials


USERS_TO_EXCLUDE = ['jenkins', 'automation', 'cs-ansible', 'cs-testuser']
AWS_USER_TO_UPDATE = 'test1'


def get_all_users(iam):
    all_users = []
    for user_list in iam.list_users().get('Users'):
        all_users.append(user_list['UserName'])
    return all_users


def delete_keys(users, iam, jenkins_conn, jenkins_credentials_description, aws_user_to_update):
    for user in users:
        if user not in USERS_TO_EXCLUDE:
            rotate_keys_for_user(user_name=user, iam=iam, jenkins_conn=jenkins_conn, jenkins_credentials_description=jenkins_credentials_description, aws_user_to_update=aws_user_to_update)
        else:
	    print "Skipping user {}".format(user)


def rotate_keys_for_user(user_name, iam, jenkins_conn, jenkins_credentials_description, aws_user_to_update):
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
                key_id = access_key.get('AccessKeyId')
                secret_key = access_key.get('SecretAccessKey')
                creds = j.credentials
                aws_creds = {
                    'description': jenkins_credentials_description,
                    'accessKey': key_id,
                    'secretKey': secret_key
                }
                print "Updating Jenkins credentials {} with the AWS user name {} and with the key ID {}".format(jenkins_credentials_description, user_name, key_id)
                creds[jenkins_credentials_description] = AmazonWebServicesCredentials(aws_creds)

    except Exception as e:
        print "There was an error"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--profile-name',
                        default=None,
                        help='The aws profile name')
    parser.add_argument('-u', '--jenkins-user',
                        default=None,
                        required=True,
                        help='The jenkins user name')
    parser.add_argument('-t', '--jenkins-password',
                        default=None,
                        required=True,
                        help='The jenkins password')
    parser.add_argument('-c', '--credentials-description',
                        default=None,
                        required=True,
                        help='The jenkins credentials description')
    parser.add_argument('--aws-user-to-update',
                        required=True,
                        help='The aws user to update')
    aws_profile_name = parser.parse_args().profile_name
    jenkins_user = parser.parse_args().jenkins_user
    jenkins_password = parser.parse_args().jenkins_password
    jenkins_credentials_description = parser.parse_args().credentials_description
    aws_user_to_update = parser.parse_args().aws_user_to_update

    session = boto3.Session(profile_name=aws_profile_name)
    iam_client = session.client('iam')
    j = Jenkins(baseurl='http://52.12.172.116:8080', username=jenkins_user, password=jenkins_password)
    all_users = get_all_users(iam=iam_client)
    delete_keys(users=all_users, iam=iam_client, jenkins_conn=j, jenkins_credentials_description=jenkins_credentials_description, aws_user_to_update=aws_user_to_update)
