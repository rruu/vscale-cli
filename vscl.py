#! /usr/bin/env python
# -*- coding: utf-8 -*-
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
    elif command == 'iso':
        if (len(sys.argv) == 3):
            plans_iso(sys.argv[2])
        else:
            print_help()
    elif command == 'small':
        plans_iso('small')
    elif command == 'medium':
        plans_iso('medium')
    elif command == 'large':
        plans_iso('large')
    elif command == 'huge':
        plans_iso('huge')
    elif command == 'monster':
        plans_iso('monster')
    elif command == 'balance':
        balance()
    elif command == 'plans':
        plans()
    else:
		print_help()

def plans_iso(n):
    url = urllib2.Request('https://api.vscale.io/v1/rplans')
    url.add_header('X-Token', api_key)
    a_iso = urllib2.urlopen(url)
    json_iso = a_iso.read()
    if n == 'small':
        for i in (json.loads(json_iso)[0]['templates']): print i
    elif n == 'medium':
        for i in (json.loads(json_iso)[1]['templates']): print i
    elif n == 'large':
        for i in (json.loads(json_iso)[2]['templates']): print i
    elif n == 'huge':
        for i in (json.loads(json_iso)[3]['templates']): print i
    elif n == 'monster':
        for i in (json.loads(json_iso)[4]['templates']): print i
    else:
        print_help()

def print_help():

    print("Usage:\n")
    print("vscl balance            # Show current balance\n")

def print_command_help(command):
    COMMANDS = \
{ "balance": \
	"Show current balance", \
  "plans iso": \
	"Show available plans" \
}

if __name__ == '__main__':
    process_command(sys.argv)
