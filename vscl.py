#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# add api key to env
# exmaple
# $ export vscale_secret=EASKD392039420394KSKA
import os
import urllib2
import json
import sys
import subprocess

api_key = os.environ['vscale_secret']

def plans():
    plans = urllib2.Request('https://api.vscale.io/v1/rplans')
    plans.add_header('X-Token', api_key)
    a_plans = urllib2.urlopen(plans)
    json_plans = a_plans.read()
    for i in (json.loads(json_plans)): print i['id'],"    	","RAM:",i['memory'], "CPU:",i['cpus'], "HDD:",i['disk']

def balance():
    balance = urllib2.Request('https://api.vscale.io/v1/billing/balance')
    balance.add_header('X-Token', api_key)
    a_balance = urllib2.urlopen(balance)
    json_balance = a_balance.read()
    bill = (json.loads(json_balance))
    print "Статус:",bill['status'],"Денег:",bill['balance']/100,"Бонусов:",bill['bonus']/100,"	","Всего:",bill['summ']/100

def ssh():
    subprocess.call('ssh -i ~/.ssh/id_rsa_vsacle', shell=True)

def process_command(command):
    if len(sys.argv) < 2:
        print_help()
        return
    command = sys.argv[1].lower()
    if command == 'help':
        if (len(sys.argv) == 3):
            print_command_help(sys.argv[2])
        else:
            print_help()
    elif command == 'balance':
        balance()
    elif command == 'plans':
        plans()
    else:
		print_help()

def print_help():

    print("Usage:\n")
    print("vscl balance            # Show current balance\n")

def print_command_help(command):
    COMMANDS = \
{ "balance": \
	"Show current balance", \
  "plans": \
	"Show available plans" \
}
    if command in COMMANDS:
        print (COMMANDS[command])
    else:
        print ("Unknown command!")
        print_help()



if __name__ == '__main__':
    process_command(sys.argv)
