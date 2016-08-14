#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# add api key to env
# exmaple
# $ export vscale_secret=EASKD392039420394KSKA
import os
import urllib2
import json
#import decimal
import sys

api_key = os.environ['vscale_secret']


def balance():
    balance = urllib2.Request('https://api.vscale.io/v1/billing/balance')
    balance.add_header('X-Token', api_key)
    a_balance = urllib2.urlopen(balance)
    json_balance = a_balance.read()
    billing = (json.loads(json_balance)['summ'])
    print "Баланс:",(json.loads(json_balance)['summ'] /100)

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
    elif command == 'viewwindow':
        if (len(sys.argv)==3):
            viewwindow(sys.argv[2])
        else:
            print_help()


def print_help():

    print("Usage:\n")
    print("vscl balance            # Show current balance\n")
#       vscl servers            # Show active servers
#        vscl create NAMEOFSRV   # Create server named
#    Options:
#        -h --help      Display this usage information

def print_command_help(command):
    COMMANDS = \
{ "balance": \
	"All argument show summary", \
  "servers": \
	"Images argument show summary OS" \
}
    if command in COMMANDS:
        print (COMMANDS[command])
    else:
        print ("Unknown command!")
        print_help()

if __name__ == '__main__':
    process_command(sys.argv)
