#!/usr/bin/env python
# encoding: utf-8

import boto3
import argparse

USERS_TO_EXCLUDE = ['jenkins', 'automation']


def get_all_users(iam):
    all_users = []
    for user_list in iam.list_users().get('Users'):
        all_users.append(user_list['UserName'])
    return all_users


def delete_keys(users, iam):
    for user in users:
        if user not in USERS_TO_EXCLUDE:
            rotate_keys_for_user(user_name=user, iam=iam)
        else:
	    print "Skipping user {}".format(user)


def rotate_keys_for_user(user_name, iam):
    all_keys = iam.list_access_keys(UserName=user_name).get("AccessKeyMetadata")
    if all_keys is not None:
        for key in all_keys:
            key_id = key.get("AccessKeyId")
            print "Deleting key {} for user {}".format(key_id, user_name)
            iam.delete_access_key(UserName=user_name, AccessKeyId=key_id)
        print "Creating a new key for user {}".format(user_name)
        iam.create_access_key(UserName=user_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--profile-name',
                        default=None,
                        help='The aws profile name')
    aws_profile_name = parser.parse_args().profile_name
    session = boto3.Session(profile_name=aws_profile_name)
    iam_client = session.client('iam')

    all_users = get_all_users(iam=iam_client)
    delete_keys(users=all_users, iam=iam_client)
