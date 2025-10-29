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

# Imports
from vAPI import main as vapi
from pprint import pprint as pp
import json

# Find if dict exists in a list of dicts


def id_based_dict(id_name, data_list):
    return {d[id_name]: d for d in data_list}


# Get Device Templates with Attached devices

def getDeviceTemplates(session):
    print('==> Fetching Device Templates ...')
    mountURL = '/dataservice/template/device'
    data = session.getDataResponse(mountURL)
    deviceTemplates = []
    for template in data:
        try:
            if template['factoryDefault'] == False and template['devicesAttached'] >= 1:
                deviceTemplates.append(template)
        except:
            pass

    return deviceTemplates

# Get which device templates that have localized policy


def getDeviceTemplateWithPolicy(templateId):
    print(
        f'==> Fetching Device Templates with localized policy for {templateId}...')
    mountURL = f'/dataservice/template/device/object/{templateId}'
    data2 = session.getFullResponse(mountURL)
    return data2['policyId']

# Get attached devices to a device template


def getAttachedDevices(templateId):
    print(f'==> Fetching attached devices details for {templateId}...')
    mountURL = f'/dataservice/template/device/config/attached/{templateId}'
    return session.getDataResponse(mountURL)

# Get Localized policy details


def getLocalizedPolicy(session):
    print('==> Fetching Localized policy ...')
    mountURL = f'/dataservice/template/policy/vedge'
    return session.getDataResponse(mountURL)

# Get Qos Map Details


def getQosMap(session):
    print('==> Fetching Qos Map details...')
    mountURL = f'/dataservice/template/policy/definition/qosmap'
    return session.getDataResponse(mountURL)

# Normalizing Data


def normalizeQoSMap(data):
    print('==> Normalizing Qos Map details...')
    qosMaps = []
    for qmap in data:
        qqmap = {}
        qqmap['name'] = qmap['name']
        qqmap['id'] = qmap['definitionId']
        qqmap['references'] = [ref['id'] for ref in qmap['references']]
        qosMaps.append(qqmap)
    return qosMaps


def normalizeLocalizedPolicy(data):
    print('==> Normalizing Localized policy details...')
    localizedPolicies = []
    for policy in data:
        lpolicy = {}
        lpolicy['name'] = policy['policyName']
        lpolicy['id'] = policy['policyId']
        lpolicy['devices'] = policy['devicesAttached']
        lpolicy['deviceTemplates'] = policy['mastersAttached']
        lpolicy['qosmaps'] = []
        for i in json.loads(policy['policyDefinition'])['assembly']:
            if i['type'] == 'qosMap':
                qMap = {}
                qMap['qmapId'] = i['definitionId']
                lpolicy['qosmaps'].append(qMap)
        localizedPolicies.append(lpolicy)
    return localizedPolicies


def normalizeDeviceTemplates(data):
    print('==> Normalizing Device Templates details...')
    deviceTemplates = []
    for template in data:
        # Is this template using policy
        policyId = getDeviceTemplateWithPolicy(template['templateId'])
        if policyId != '':
            dtemplate = {}
            dtemplate['name'] = template['templateName']
            dtemplate['id'] = template['templateId']
            dtemplate['numDevices'] = template['devicesAttached']
            dtemplate['policy'] = {}
            dtemplate['policy']['policyId'] = policyId
            dtemplate['devices'] = []
            for dev in getAttachedDevices(template['templateId']):
                device = {}
                device['name'] = dev['host-name']
                device['ip'] = dev['deviceIP']
                device['siteId'] = dev['site-id']
                device['serial'] = dev['uuid']
                dtemplate['devices'].append(device)
            deviceTemplates.append(dtemplate)
    return deviceTemplates

# Curating Data for Final Data


def curatingQosMapsIntoPolicies(qosMaps, localizedPolicies):
    print('==> Curating Qos Maps into policies...')
    qosMapsData = id_based_dict('id', qosMaps)
    for policy in localizedPolicies:
        for qmap in policy['qosmaps']:
            if qmap['qmapId'] in qosMapsData:
                qmap['name'] = qosMapsData[qmap['qmapId']]['name']
    return localizedPolicies


def curatingFinalData(deviceTemplates, curatedLocalizedPolicies):
    print('==> Curating Final Data...')
    localizedPoliciesData = id_based_dict('id', curatedLocalizedPolicies)
    for template in deviceTemplates:
        if template['policy']['policyId'] in localizedPoliciesData:
            template['policy']['name'] = localizedPoliciesData[template['policy']
                                                               ['policyId']]['name']
            template['policy']['qosmaps'] = [qmap['name']
                                             for qmap in localizedPoliciesData[template['policy']['policyId']]['qosmaps']]
    return deviceTemplates


session = vapi()
qosMaps = normalizeQoSMap(getQosMap(session))
localizedPolicies = normalizeLocalizedPolicy(getLocalizedPolicy(session))
deviceTemplates = normalizeDeviceTemplates(getDeviceTemplates(session))
curatedLocalizedPolicies = curatingQosMapsIntoPolicies(
    qosMaps, localizedPolicies)
finalData = curatingFinalData(deviceTemplates, curatedLocalizedPolicies)


def saveDictToJson(data, outputFile, path):
    print('')
    print(f'==> Saving data to {path}/{outputFile} ...')
    with open(f'{path}/{outputFile}', "w") as outfile:
        json.dump(data, outfile)


saveDictToJson(finalData, 'qos-mapping.json', '.')
