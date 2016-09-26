#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib2
import json
import sys
import subprocess

## Вариант кофнигурации #############################################################

api_key = os.environ['vscale_secret'] # брать из окружения системы (export)
#api_key = 'xxxxxxx' # указать перманентно

rplan = "small"                         # указать тарифный план
make_from = "debian_8_64_001_master"    # указать образ
ssh_keys_id = [189]                     # id ssh публичного ключа в vsacle
sshkey = "~/.ssh/id_rsa_vscale"         # путь до приватного ключа
location = "spb0"                       # локация серверов
autostart=True                          # включать виртуалку сразу после создания

####################################################################################

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
    name_for_del = str(arg1)
    active = urllib2.Request('https://api.vscale.io/v1/scalets')
    active.add_header('X-Token', api_key)
    a_active = urllib2.urlopen(active)
    json_active = a_active.read()
    if (json.loads(json_active))[0]['name'] == name_for_del:
        ctid = (json.loads(json_active))[0]['ctid']
        ctid = str(ctid)
        delete = urllib2.Request('https://api.vscale.io/v1/scalets/' + ctid)
        delete.add_header('X-Token', api_key)
        delete.get_method = lambda: 'DELETE'
        a_delete = urllib2.urlopen(delete)
        print "Сервер:", name_for_del, "id:", ctid, "удален"
    else:
        print "Сервер с именем:", name_for_del, "не найден"

def active():
    active = urllib2.Request('https://api.vscale.io/v1/scalets')
    active.add_header('X-Token', api_key)
    a_active = urllib2.urlopen(active)
    json_active = a_active.read()
    if not json.loads(json_active):
        print "Список серверов пуст"
    else:
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
    data = {'make_from': make_from,'rplan': rplan,'name': name,'keys': ssh_keys_id,'location': location,'do_start':bool(autostart)}
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

def ssh(arg1):
    name_for_ip = str(arg1)
    active = urllib2.Request('https://api.vscale.io/v1/scalets')
    active.add_header('X-Token', api_key)
    a_active = urllib2.urlopen(active)
    json_active = a_active.read()
    if (json.loads(json_active))[0]['name'] == name_for_ip:
        ipaddr = (json.loads(json_active))[0]['public_address']['address']
        ssh = subprocess.call(["ssh " + "root@"+ipaddr + " -i " + sshkey], shell=True)
    else:
        print "Сервер", name_for_ip, "не найден"

def process_command(command):
    if len(sys.argv) < 2:
        print_help()
        return
    command = sys.argv[1].lower()
    if command == 'del':
        if (len(sys.argv) == 3):
            del_srv(sys.argv[2])
        else:
            print "Укажите _имя сервера_ для удаления"
    elif command == 'ssh':
        if (len(sys.argv) == 3):
            ssh(sys.argv[2])
        else:
            print "Укажите _имя сервера_ для подключения"
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
            print "Укажите _имя сервера_ для создания"
    elif command == 'plans':
        plans()
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

    print("vscl доступные команды:\n")
    print("vscl balance                     # показать текущий баланс")
    print("vscl plans                       # показать доступные планы")
    print("vscl iso small                   # показать образы доступны для плана small")
    print("vscl scalets                     # показать созданые сервера")
    print("vscl del name                    # удалить сервер с именем name")
    print("vscl create name                 # создать сервер с именем name")
    print("vscl ssh name                    # подключиться к сервер name по ssh")


if __name__ == '__main__':
    process_command(sys.argv)