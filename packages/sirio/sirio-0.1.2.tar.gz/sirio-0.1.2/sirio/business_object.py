import requests
from enum import Enum

class TypeValue(Enum):
    string = 1
    date = 2
    numeric = 3


class ObjBusiness:
    jsonComplete = {}
    businessObject = {}
    businessKey =  ""
    subject = ""
    description = ""
    urlGetBO = ""
    urlComplete = ""
    def __init__(self, businessKey: str, urlGetBO: str, urlComplete: str):
        self.jsonComplete = {"businessKey": businessKey}
        self.objects = []
        self.data = {}
        self.urlGetBO = urlGetBO
        self.urlComplete = urlComplete
        response = requests.get(urlGetBO.replace('{businessKey}', businessKey))
        if response.status_code == 200:
            self.businessObject = response.json()
            self.description = self.businessObject['description']
            self.subject = self.businessObject['subject']
        else:
            self = None

    def getValue(self, bind:str, id:str):
        valReturn = None
        try:
            if self.businessObject['data'] != None and self.businessObject['data'][bind] != None and self.businessObject['data'][bind][id] != None:
                valReturn = self.businessObject['data'][bind][id]['value']['value']
        except Exception as ex:
            print("Eccezione su getValue [{}][{}] - {}".format(bind, id, ex))
        return valReturn
    
    def setValue(self, bind: str, id: str, value, typeValue=TypeValue.string):
        if 'data' not in self.jsonComplete:
            self.jsonComplete['data'] = {}
        if bind not in self.jsonComplete['data']:
            self.jsonComplete['data'][bind] = {}
        if id not in self.jsonComplete['data'][bind]:
            self.jsonComplete['data'][bind][id] =  {"dataType": typeValue.name,  "description": "string",   "value": {"value": value }, "extendedValue": [] }
        elif self.jsonComplete['data'][bind][id]['value']['value'] != value:
            self.jsonComplete['data'][bind][id]['value']['value'] = value

        if 'data' not in self.businessObject:
            self.businessObject['data'] = {}
        if bind not in self.businessObject['data']:
            self.businessObject['data'][bind] = {}
        if id not in self.businessObject['data'][bind]:
            self.businessObject['data'][bind][id] = {"dataType": typeValue.name,  "description": "string",   "value": {"value": value }, "extendedValue": [] }
        elif self.businessObject['data'][bind][id]['value']['value'] != value:
            self.businessObject['data'][bind][id]['value']['value'] = value
    
    def getObject(self, key: str):
        object = None
        try:
            objList = self.businessObject['objects']
            if objList is not None:
                objects = list(objList)
                if objects is not None:
                    for obj in objects:
                        if obj['key'] == key:
                            object = obj
                            break
        except Exception as ex:
            print("Eccezione su getObject - {}".format(ex))
        return object
    
    def setObject(self, object):
        if 'objects' not in self.jsonComplete:
            self.jsonComplete['objects'] = []
        self.jsonComplete['objects'].append(object)

    def complete(self, domain, taskId, priority=None, owner=None):
        responseComplete = requests.post(self.urlComplete.replace('{domain}', domain).replace('{taskId}', taskId), json=self.jsonComplete)
        return responseComplete

