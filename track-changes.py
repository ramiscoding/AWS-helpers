#!/usr/bin/env python

import argparse
import boto3
import pprint
import ast

def get_logs_for_resource(args):
  """ Method to get the event logs for the resource.

      This method provides you with the username, eventname, eventid
      and the time of event.
  """
  corrected_profile_name = str.lower(args.profile.encode('ascii','ignore'))
  session = boto3.session.Session(profile_name=corrected_profile_name)
  ct_client = session.client('cloudtrail')
  response = ct_client.lookup_events(
    LookupAttributes=[
        {
            'AttributeKey': 'ResourceName',
            'AttributeValue': args.res
        }
    ])
  output = response.copy()
  print "Username : %s" % response['Events'][0]['Username']
  print "Eventname : %s" % response['Events'][0]['EventName']
  print "Event ID : %s" % response['Events'][0]['EventId']
  print "Event Time : %s" % response['Events'][0]['EventTime']
  for resource in response['Events'][0]['Resources']:
    if args.res in resource['ResourceName']:
      print "Resource type : %s" % resource['ResourceType']
  exit()
  

def get_event_details(args):
  """ Method to get the exact change detail for the event id. """
  corrected_profile_name = str.lower(args.profile.encode('ascii','ignore'))
  session = boto3.session.Session(profile_name=corrected_profile_name)
  config_client = session.client('config')
  response = config_client.get_resource_config_history(
    resourceType=args.resourcetype,
    resourceId=args.res,
)
  for config in response['configurationItems']:
    if args.event in config['relatedEvents'][0]:
      print "Resource name : %s" % config['resourceName']
      print "Status : %s" % config['configurationItemStatus']
      print "Relationships : "
      pprint.pprint(config['relationships'])
      print "Configuration change : "
      pprint.pprint(ast.literal_eval(config['configuration']))
      exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Track changes to AWS resources.")
    parser.add_argument('--resource',action='store',dest='res',required=True,help='The AWS resource name')
    parser.add_argument('--profile',action='store',dest='profile',required=True,help='AWS Profile name')
    parser.add_argument('--event',action='store',dest='event',required=False,help='Event ID to get the exact changes')
    parser.add_argument('--type',action='store',dest='resourcetype',required=False,help='Type of AWS resource')
    parser.set_defaults(func = get_logs_for_resource, func1 = get_event_details)
    args = parser.parse_args()
    if args.event:
      if not args.resourcetype:
        print "Please provide the --type argument"
        exit()
    if args.res and args.event :
      args.func1(args)
    elif args.res:
      args.func(args)
    else:
      print "Please provide valid arguments"
      exit()
