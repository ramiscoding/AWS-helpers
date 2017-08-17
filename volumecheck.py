#!/usr/bin/env python

import argparse
import boto3
import pprint
import ast



def get_volume_status(args):
  """ Method to get the status of volume id passed. """
  corrected_profile_name = str.lower(args.profile.encode('ascii','ignore'))
  session = boto3.session.Session(profile_name=corrected_profile_name)
  ec2_client = session.client('ec2')
  my_id = args.volume.strip()
  response = ec2_client.describe_volumes(
    VolumeIds=[my_id]
)
  print "Volume Id : %s" % my_id
  print "Status : %s" % response['Volumes'][0]['State']
  if response['Volumes'][0]['Attachments']:
    print "Instance Id : %s" % response['Volumes'][0]['Attachments'][0]['InstanceId']
  if 'Tags' in response['Volumes'][0]:
    for tag in response['Volumes'][0]['Tags']:
      if str.lower(tag['Key']) in 'name':
        print "Name : %s" % tag['Value']
  exit()
  

def get_volume_status_from_file(args):
  """ Method to get the volume status of all volume ids in the file. """
  corrected_profile_name = str.lower(args.profile.encode('ascii','ignore'))
  session = boto3.session.Session(profile_name=corrected_profile_name)
  ec2_client = session.client('ec2')
  my_volumes = []
  file = open(args.vfile, 'r')
  for line in file:
    my_volumes.append(line)
  for vol in my_volumes:
    my_id = vol.strip()
    response = ec2_client.describe_volumes(
      VolumeIds=[my_id]
  )
    print "Volume Id : %s" % my_id
    print "Status : %s" % response['Volumes'][0]['State']
    if response['Volumes'][0]['Attachments']:
      print "Instance Id : %s" % response['Volumes'][0]['Attachments'][0]['InstanceId']
    if 'Tags' in response['Volumes'][0]:
      for tag in response['Volumes'][0]['Tags']:
        if str.lower(tag['Key']) in 'name':
          print "Name : %s" % tag['Value']
    print ""
  exit()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check volume status")
    parser.add_argument('--id',action='store',dest='volume',required=False,help='The volume id')
    parser.add_argument('--vfile',action='store',dest='vfile',required=False,help='The filename which has the list of volume ids to scan')
    parser.add_argument('--profile',action='store',dest='profile',required=True,help='The profile name of AWS account')
    parser.set_defaults(func = get_volume_status, func1 = get_volume_status_from_file)
    args = parser.parse_args()
    if args.volume:
      args.func(args)
    elif args.vfile:
      args.func1(args)
    else:
      print "Please provide valid arguments [Either --id or --vfile is required]"
      exit()
