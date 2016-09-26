#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib2
import json
import sys
import subprocess

api_key = os.environ['vscale_secret']

## config
rplan = "small"
make_from = "debian_8_64_001_master"
keys = [189]
location = "spb0"
autostart=True
## config-end

def plans():
    plans = urllib2.Request('https://api.vscale.io/v1/rplans')
    plans.add_header('X-Token', api_key)
    a_plans = urllib2.urlopen(plans)
    json_plans = a_plans.read()
    for i in (json.loads(json_plans)): print i['id'],"    	","RAM:",i['memory'], "CPU:",i['cpus'], "HDD:",i['disk']

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

def del_srv(arg1):
    server_id = str(arg1)
    delete = urllib2.Request('https://api.vscale.io/v1/scalets/' + server_id)
    delete.add_header('X-Token', api_key)
    delete.get_method = lambda: 'DELETE'
    a_delete = urllib2.urlopen(delete)
    print "OK"

def active():
    active = urllib2.Request('https://api.vscale.io/v1/scalets')
    active.add_header('X-Token', api_key)
    a_active = urllib2.urlopen(active)
    json_active = a_active.read()
    for i in (json.loads(json_active)): print "ID: ",i['ctid'],"Status: ",i['status'], "Name: ",i['name'],"img: ",i['made_from'],"IP: ",i['public_address']['address']

def balance():
    balance = urllib2.Request('https://api.vscale.io/v1/billing/balance')
    balance.add_header('X-Token', api_key)
    a_balance = urllib2.urlopen(balance)
    json_balance = a_balance.read()
    bill = (json.loads(json_balance))
    print "Статус:",bill['status'],"Денег:",bill['balance']/100,"Бонусов:",bill['bonus']/100,"	","Всего:",bill['summ']/100

def create_server(arg1):
    name = str(arg1)
    location = "spb0"
    data = {'make_from': make_from,'rplan': rplan,'name': name,'keys': keys,'location': location,'do_start':bool(autostart)}
    data = json.dumps(data)
    a = urllib2.Request('https://api.vscale.io/v1/scalets', data)
    a.add_header('X-Token', api_key)
    a.add_header("Content-Type" , "application/json;charset=UTF-8")
    a.get_method = lambda: 'POST'
    try:
        a_crt = urllib2.urlopen(a)
    except urllib2.HTTPError, e:
        code = e.code
        if code != 200:
            print "ERROR", code
    else:
        js_a = a_crt.read()
        b_create = (json.loads(js_a))
        created_id = str(b_create['ctid'])
        srvreq = urllib2.Request('https://api.vscale.io/v1/scalets/' + created_id)
        srvreq.add_header('X-Token', api_key)
        reqstat = urllib2.urlopen(srvreq)
        json_srv = reqstat.read()
        abc = json.loads(json_srv)
        print "ID:" , abc['ctid'], "    IP:", abc['public_address']['address'], "   ISO:", abc['made_from']

def info(arg1):
    created_id = str(arg1)
    srvreq = urllib2.Request('https://api.vscale.io/v1/scalets/' + created_id)
    srvreq.add_header('X-Token', api_key)
    reqstat = urllib2.urlopen(srvreq)
    json_srv = reqstat.read()
    abc = json.loads(json_srv)

    print "ID:" , abc['ctid'], "    IP:", abc['public_address']['address'], "   ISO:", abc['made_from']

def ssh():
    subprocess.call('ssh -i ~/.ssh/id_rsa_vsacle', shell=True)

def process_command(command):
    if len(sys.argv) < 2:
        print_help()
        return
    command = sys.argv[1].lower()
    if command == 'del':
        if (len(sys.argv) == 3):
            del_srv(sys.argv[2])
        else:
            print "Укажите id для удаления"
    elif command == 'iso':
        if (len(sys.argv) == 3):
            plans_iso(sys.argv[2])
        else:
            print_help()
    elif command == 'info':
        if (len(sys.argv) == 3):
            info(sys.argv[2])
        else:
            print_help()
    elif command == 'create':
        if (len(sys.argv) == 3):
           create_server(sys.argv[2])
        else:
           print_help()
    elif command == 'plans':
        plans()
#    elif command == 'create':
#        create_server()
    elif command == 'scalets':
        active()
    elif command == 'balance':
        balance()
    elif command == 'create':
        create_server()
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
    print("vscl avalible command")
    print("vscl balance         # show current balance")
    print("vscl plans           # show avalible plans")
    print("vscl iso small / medium / large  # show iso for plan")
    print("vscl scalets         # display active instanse")
    print("vscl del id      # delete instance by id")


def print_command_help(command):
    COMMANDS = \
{ "balance": \
	"Show current balance", \
  "plans iso": \
	"Show available plans" \
}

if __name__ == '__main__':
    process_command(sys.argv)
