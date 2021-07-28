import json
import requests
import time

# from .ModelPublisher import TsiModelPublisher

class TsiDataQuerier():
    '''
    This class contains the function to query data from TSI
    '''
    def __init__(self,
                 environment_fqdn,
                 client_secret,
                 client_id,
                 tenant_id,):
        self.storType_list = ['warmstore', 'coldstore']
        self.environment_fqdn = environment_fqdn
        self.client_secret = client_secret
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.api_version = '2020-07-31'
        self.tsi_resource = 'https://api.timeseries.azure.com/'

    def get_authorization_token(self):
        '''
        Send POST request via REST API to get the Azure Access Token
        '''
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {'grant_type': "client_credentials",
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'resource': self.tsi_resource}

        res = requests.request("POST",
                                url=url,
                                headers=headers,
                                data=body)
        self.authorization_token = f"Bearer {res.json()['access_token']}"
        return res

    def query_availability(self, storeType: 'coldstore'):
        '''
        Send GET request via REST API to query the availability/search span of time series
        '''
        if storeType.lower() not in self.storType_list:
            return 'Input storetype is unknown, should be either ColdStore or WarmStore'
        else:
            url = f"https://{self.environment_fqdn}/availability?"
            headers = {'Authorization': self.authorization_token,
                       'Content-Type': 'application/json',
                       'storeType': storeType}
            params = {'api-version': self.api_version}
            res = requests.get(url = url,
                             headers = headers,
                             params =params)
        return res

    def query_event_schema(self, storeType = 'coldstore', searchSpan = {'from': None, 'to': None} ):
        '''
        Send POST request via REST API to get event schema
        '''
        if storeType.lower() not in self.storType_list:
            return 'Input storetype is unknown, should be either ColdStore or WarmStore'
        else:
            url = f"https://{self.environment_fqdn}/eventSchema?"
            headers = {'Authorization': self.authorization_token,
                       'Content-Type': 'application/json',
                       'storeType': storeType}
            params = {'api-version': self.api_version}
            if searchSpan['from'] and searchSpan['to']:
                start_time_stamp = searchSpan['from']
                end_time_stamp = searchSpan['to']
                if start_time_stamp <= end_time_stamp:
                    start_time_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.strptime(start_time_stamp, "%Y-%m-%d %H:%M:%S"))
                    end_time_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.strptime(end_time_stamp, "%Y-%m-%d %H:%M:%S"))
                else:
                    return 'End time stamp should behind the start time stamp'
            else:
                return 'The start time and end time of search span should be given.'

            body = { 'searchSpan':{'from': start_time_stamp,
                                   'to': end_time_stamp}}
            res = requests.post(url = url,
                                headers = headers,
                                params =params,
                                data = json.dumps(body))
        return res

    def query_event_by_id(self,
                          storeType = 'coldstore',
                          timeSeriesId = [],
                          searchSpan = {'from': None, 'to': None},
                          filter = {},):
        '''
        Send POST request via REST API to get the timestamp and associated values of projected properties for asset with certain ID
        '''

        # set the project properties
        projectedProperties = [{'name': 'value', 'type': 'Double'}, {'name': 'body', 'type': 'String'}]

        # verify the store type
        if storeType.lower() not in self.storType_list:
            return 'Input store type is unknown, should be either ColdStore or WarmStore.'
        else:
            url = f"https://{self.environment_fqdn}/timeseries/query?"
            headers = {'Authorization': self.authorization_token,
                       'Content-Type': 'application/json'}        
            params = {'api-version': self.api_version,
                      'storeType': storeType}

        # verify the search span and convert the formats of start and end time
            if searchSpan['from'] and searchSpan['to']:
                start_time_stamp = searchSpan['from']
                end_time_stamp = searchSpan['to']
                if start_time_stamp <= end_time_stamp:
                    start_time_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.strptime(start_time_stamp, "%Y-%m-%d %H:%M:%S"))
                    end_time_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.strptime(end_time_stamp, "%Y-%m-%d %H:%M:%S"))
                else:
                    return 'The end time should behind the start time'
            else:
                return 'The start time and end time of search span should be given.'

            body = { "getEvents":{ "timeSeriesId" : timeSeriesId,
                                   "searchSpan": {"from": start_time_stamp, # the format of the time should be verified
                                                  "to": end_time_stamp},
                                   "filter": filter,
                                   "projectedProperties": projectedProperties
                                    }}


            res = requests.post(url = url,
                                headers = headers,
                                params =params,
                                data = json.dumps(body))
            if res.status_code == 200:
                out_json = json.dumps({timeSeriesId[0]: res.json()})
                print(f'Successfully query instance: {timeSeriesId[0]} \n')
            else:
                return res.status_code
        return out_json


    def query_event_by_hierarchy(self, storeType = 'coldstore',
                                       search_string = '',
                                       hierarchyName = '',
                                       recursive = 'true',
                                       hilight = 'true',
                                       continuationToken = '',
                                       searchSpan = {'from': None, 'to': None},
                                       filter = {}
                                      ):
        '''
        Send POST request via REST API to get the timestamp and associated values of projected properties for asset with certain hierarchy by looking for a search string
        '''

        # Set the projected property
        projectedProperties = [{'name': 'value', 'type': 'Double'}, {'name': 'body', 'type': 'String'}]

        # Get the list of instance by instance search method
        res = self.query_instance_search(search_string=search_string,
                                         hierarchyName=hierarchyName,
                                         recursive=recursive,
                                         hilight=hilight,
                                         continuationToken=continuationToken)

        instances_content = res.json()['instances']['hits']
        # show the instances in hierarchy mode
        timeSeriesID_list = []
        try:
            for instance in instances_content:
                timeSeriesID_list.append(instance['timeSeriesId'][0])
            try:
                continuationToken = res['instances']['continuationToken']
                while continuationToken:
                    res = self.query_instance_search(search_string=search_string,
                                                        hierarchyName=hierarchyName,
                                                        recursive='true',
                                                        hilight='true',
                                                        continuationToken=continuationToken)
                    instance_content = res['instances']['hits']
                    for instance in instance_content:
                        timeSeriesID_list.append(instance['timeSeriesId'][0])
                    try:
                        continuationToken = res['instances']['continuationToken']
                    except:
                        continuationToken = None
            except:
                print('ContinuationToken is not needed')
        except IndexError:
            return f'No instance is available with search string {search_string}'

        if storeType.lower() not in self.storType_list:
            return 'Input storetype is unknown, should be either ColdStore or WarmStore'
        else:
            url = f"https://{self.environment_fqdn}/timeseries/query?"
            headers = {'Authorization': self.authorization_token,
                       'Content-Type': 'application/json'}
            params = {'api-version': self.api_version,
                      'storeType': storeType}

            # verify the search span and convert the formats of start and end time
            if searchSpan['from'] and searchSpan['to']:
                start_time_stamp = searchSpan['from']
                end_time_stamp = searchSpan['to']
                if start_time_stamp <= end_time_stamp:
                    start_time_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.strptime(start_time_stamp, "%Y-%m-%d %H:%M:%S"))
                    end_time_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.strptime(end_time_stamp, "%Y-%m-%d %H:%M:%S"))
                else:
                    return 'The end time should behind the start time'

            # print results, collect and return output in json
            out_dict = {}
            for instance_id in timeSeriesID_list:
                body = { "getEvents":{ "timeSeriesId" : [instance_id],
                                       "searchSpan": {"from": start_time_stamp, # the format of the time should be verified
                                                      "to": end_time_stamp},
                                       "filter": filter,
                                       "projectedProperties": projectedProperties
                                        }}
                res = requests.post(url = url,
                                    headers = headers,
                                    params =params,
                                    data = json.dumps(body))
                out_dict[instance_id] = res.json()
                print(f'instance_id:{instance_id}\t', res.json(), '\n')
            json_out = json.dumps(out_dict)
            print('Successfully query all instances \n')
        return json_out

    def query_instance(self, continuationToken = ''):
        """
        Query all the available instances from TSI.
        If the amount of instances is over 100(maximum 100 per page), the continuationToken is needed to retrieve the next page
        """
        url = f"https://{self.environment_fqdn}/timeseries/instances?"
        params = {'api-version': self.api_version}
        if not continuationToken:
            headers = {'Authorization': self.authorization_token,
                       'Content-Type': 'application/json'}
        else:
            headers = {'Authorization': self.authorization_token,
                       'Content-Type': 'application/json',
                       'x-ms-continuation': continuationToken}

        res = requests.get(url = url,
                           params = params,
                           headers = headers)
        return res

    def query_instance_search(self,
                              search_string = '',
                              hierarchyName = '',
                              recursive = 'true',
                              hilight = 'true',
                              continuationToken = ''):
        """
        Query time series instances based on instance attributes
        If the amount of instances is over 100(maximum 100 per page), the continuationToken is needed to retrieve the next page
        """
        print(f'Query instance by searching keyword: {search_string}')
        url = f"https://{self.environment_fqdn}/timeseries/instances/search?"
        if not continuationToken:
            headers = {'Authorization': self.authorization_token,
                       'Content-Type': 'application/json'}
        else:
            headers = {'Authorization': self.authorization_token,
                       'Content-Type': 'application/json',
                       'x-ms-continuation': continuationToken}
        params = {'api-version': self.api_version}
        data = {"searchString": search_string,
                "path":[hierarchyName],
                "instances": {
                    "recursive": recursive,
                    "sort": {
                        "by": "DisplayName"
                    },
                    "highlights": hilight,
                    "pageSize": 100}
                }
        res = requests.post(url = url,
                            headers = headers,
                            params=params,
                            data=json.dumps(data))
        return res

    def query_hierarchy(self):
        """
        Query hierarchy from TSI
        """
        url = f"https://{self.environment_fqdn}/timeseries/hierarchies?"
        headers = {'Authorization': self.authorization_token,
                   'Content-Type': 'application/json'}

        params = {'api-version': self.api_version}
        res = requests.get(url=url,
                            headers=headers,
                            params=params)
        return res

    def query_type(self):
        """
        Query Types from TSI
        """
        url = f"https://{self.environment_fqdn}/timeseries/types?"
        headers = {'Authorization': self.authorization_token,
                   'Content-Type': 'application/json'}
        params = {'api-version': self.api_version}
        res = requests.get(url=url,
                            headers=headers,
                            params=params)

        return res