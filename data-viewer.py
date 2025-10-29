#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2025 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Hussein Omar, CSS - EMEA"
__email__ = "husseino@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2021 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

from pprint import pprint as pp
import json


def readJsonFile(fileName):
    try:
        # Use 'r' for read mode and 'utf-8' encoding for compatibility
        with open(fileName, 'r', encoding='utf-8') as jfile:
            # json.load() reads the file object and converts JSON content to a Python dict
            return json.load(jfile)

        print(f"Successfully loaded {fileName}.")
    except FileNotFoundError:
        print(f"Error: The file '{fileName}' was not found.")
    except json.JSONDecodeError:
        print(
            f"Error: Could not decode JSON from '{fileName}'. The file may be malformed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


finalData = readJsonFile('qos-mapping.json')


def removeDuplicates(input_list):
    seen = set()
    final_list = []
    for i in input_list:
        hashed_i = tuple(sorted(i.items()))
        if hashed_i not in seen:
            seen.add(hashed_i)
            final_list.append(i)
    return final_list


def searchByQosMapName(data):
    print('')
    print('========= Search by QoS Map Name =========')
    qosMap = input(' - Please enter the QoS Map Name: ')
    finalresult = {'used-in-localized-policy': [], 'used-in-device-template': [],
                   'number-of-affected-devices': 0, 'affected-devices': []}
    devices = []
    for item in data:
        if qosMap in item['policy']['qosmaps']:
            finalresult['number-of-affected-devices'] += len(item['devices'])
            for dev in item['devices']:
                devices.append(dev)
            finalresult['used-in-localized-policy'].append(
                item['policy']['name'])
            finalresult['used-in-device-template'].append(item['name'])
    uniqueDevs = removeDuplicates(devices)
    finalresult['affected-devices'] = uniqueDevs
    if finalresult['used-in-localized-policy'] == []:
        print('===========================================')
        print(f'xxx> Qos Map {qosMap} is not found !!! ')
        return None
        print('===========================================')
    else:
        return finalresult
        print('===========================================')


def searchByLocalizedPolicyName(data):
    print('')
    print('========= Search by Localized Policy Name =========')
    lpolicyname = input(' - Please enter Localizaed Policy Name: ')
    finalresult = {'qos-maps-used': [], 'used-in-device-template': [],
                   'number-of-affected-devices': 0, 'affected-devices': []}
    qosMaps = []
    for item in data:
        if lpolicyname == item['policy']['name']:
            finalresult['number-of-affected-devices'] += len(item['devices'])
            finalresult['affected-devices'].append(item['devices'])
            for d in item['policy']['qosmaps']:
                qosMaps.append(d)
            finalresult['used-in-device-template'].append(item['name'])
    uniqueQosMaps = set(qosMaps)
    finalresult['qos-maps-used'] = list(uniqueQosMaps)
    if finalresult['qos-maps-used'] == []:
        print('===========================================')
        print(f'xxx> Localized Policy {lpolicyname} is not found !!! ')
        return None
        print('===========================================')
    else:
        return finalresult
        print('===========================================')


def searchByDeviceTemplateName(data):
    print('')
    print('========= Search by QoS Map Name =========')
    devtemplateName = input(' - Please enter Device Template Name: ')
    finalresult = {'used-in-localized-policy': [], 'qos-maps-used': [],
                   'number-of-affected-devices': 0, 'affected-devices': []}
    for item in data:
        if devtemplateName == item['name']:
            finalresult['number-of-affected-devices'] += len(item['devices'])
            finalresult['affected-devices'].append(item['devices'])
            finalresult['used-in-localized-policy'].append(
                item['policy']['name'])
            finalresult['qos-maps-used'].append(
                [d for d in item['policy']['qosmaps']])
    if finalresult['used-in-localized-policy'] == []:
        print('===========================================')
        print(f'xxx> Device Template {devtemplateName} is not found !!! ')
        return None
        print('===========================================')
    else:
        return finalresult
        print('===========================================')


def chooseMethod():
    print(
        '''
        ===================================
        1. Search by QoS Map Name
        2. Search by Localized Policy Name
        3. Search by Device Template Name
        4. Print Full Data Tree as Json
        5. Exit
        ===================================
        '''
    )


def exitConfirm():
    exitYes = 0
    code = input('Are you sure you want to EXIT? Yes/No: ')
    if code.lower() == 'yes':
        exitYes = 1
    elif code.lower() == 'no':
        exitYes = 0
    elif code.lower == 'y':
        exitYes = 1
    elif code.lower == 'n':
        exitYes = 0
    else:
        print('Invalid input')
    return exitYes


exitYes = 0
while exitYes == 0:
    chooseMethod()
    method = input('Please choose a method: ')
    if method == '1':
        finalresult = searchByQosMapName(finalData)
        pp(finalresult)
    elif method == '2':
        finalresult = searchByLocalizedPolicyName(finalData)
        pp(finalresult)
    elif method == '3':
        finalresult = searchByDeviceTemplateName(finalData)
        pp(finalresult)
    elif method == '4':
        print(json.dumps(finalData, indent=4))
    elif method == '5':
        exitYes = exitConfirm()
    else:
        print('Invalid input')
        chooseMethod()
