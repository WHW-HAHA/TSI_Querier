import json
import requests
import time
import logging
import sys

class TsiDataQuerier():
    '''
    This class contains the functions to query data from Azure TSI
    '''
    def __init__(self, environment_variables = {}):
        self.storType_list = ['warmstore', 'coldstore']
        self.environment_fqdn = environment_variables['environment_fqdn']
        self.client_secret = environment_variables['client_secret']
        self.client_id = environment_variables['client_id']
        self.tenant_id = environment_variables['tenant_id']
        self.api_version = '2020-07-31'
        self.tsi_resource = 'https://api.timeseries.azure.com/'

    def create_logger(self, stream_level = 'INFO', file_level = 'INFO'):
        # configure logger
        level_dict = {'INFO':logging.INFO,
                      'WARNING': logging.WARNING,
                      'CRITICAL': logging.CRITICAL}

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.INFO)

        # stream handler
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level = level_dict[stream_level])
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # file handler
        file_handler = logging.FileHandler(filename='output.log')
        file_handler.setLevel(level = level_dict[file_level])
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

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
        self.logger.info(f'Status code ADD token: {res.status_code}')
        return res

    def query_availability(self, storeType: 'coldstore'):
        '''
        Send GET request via REST API to query the availability/search span of time series
        '''
        if storeType.lower() not in self.storType_list:
            self.logger.fatal('Input storetype is unknown, should be either coldstore or warmstore')
        else:
            url = f"https://{self.environment_fqdn}/availability?"
            headers = {'Authorization': self.authorization_token,
                       'Content-Type': 'application/json',
                       'storeType': storeType}
            params = {'api-version': self.api_version}
            res = requests.get(url = url,
                             headers = headers,
                             params =params)
            self.logger.info(f'Status code query availability: {res.status_code}')
            return res

    def query_event_schema(self, storeType = 'coldstore', searchSpan = {'from': None, 'to': None} ):
        '''
        Send POST request via REST API to get event schema
        '''
        if storeType.lower() not in self.storType_list:
            self.logger.fatal('Input storetype is unknown, should be either coldstore or warmstore')
            return 'Input store type is unknown, should be either coldstore or warmstore.'
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
                    self.logger.fatal('End time stamp should behind the start time stamp')
            else:
                self.logger.fatal('The start time and end time of search span should be given.')

            body = { 'searchSpan':{'from': start_time_stamp,
                                   'to': end_time_stamp}}
            res = requests.post(url = url,
                                headers = headers,
                                params =params,
                                data = json.dumps(body))
            self.logger.info(f'Status code query event schema: {res.status_code}')
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
            self.logger.fatal('Input store type is unknown, should be either coldstore or warmstore.')
            return 'Input store type is unknown, should be either coldstore or warmstore.'
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
                    self.logger.fatal('The end time should behind the start time')
            else:
                self.logger.fatal('The start time and end time of search span should be given.')

            body = { "getEvents":{ "timeSeriesId" : timeSeriesId,
                                   "searchSpan": {"from": start_time_stamp, # the format of the time should be verified
                                                  "to": end_time_stamp},
                                   "filter": filter,
                                   "projectedProperties": projectedProperties
                                    }}

            res = requests.post(url = url,
                                headers = headers,
                                params = params,
                                data = json.dumps(body))
            if res.status_code == 200:
                out_json = json.dumps({timeSeriesId[0]: res.json()})
                self.logger.info(f'Instance_id: {timeSeriesId[0]}, status_code: {res.status_code}')
            else:
                self.logger.info(f'Instance_id: {timeSeriesId[0]}, status_code: {res.status_code}')
                return res.status_code
        return out_json

    def query_event_by_hierarchy(self, storeType = 'coldstore',
                                       search_string = '',
                                       hierarchyName = '',
                                       recursive = 'true',
                                       highlight = 'true',
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
                                         highlight=highlight,
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
                                                     highlight='true',
                                                     continuationToken=continuationToken)
                    instance_content = res['instances']['hits']
                    for instance in instance_content:
                        timeSeriesID_list.append(instance['timeSeriesId'][0])
                    try:
                        continuationToken = res['instances']['continuationToken']
                    except:
                        continuationToken = None
            except:
                self.logger.info('ContinuationToken is not needed, the amount of outcome instance is less than 100.')
        except IndexError:
            self.logger.warning(f'No instance is available with search string {search_string}')
            # return 'No instance is available with search string {search_string}'

        if storeType.lower() not in self.storType_list:
            self.logger.fatal('Input storetype is unknown, should be either coldstore or warmstore.')
            return 'Input store type is unknown, should be either coldstore or warmstore.'
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
                    self.logger.fatal('The end time should behind the start time.')

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
                self.logger.info(f'Instance_id: {instance_id}, status_code:{res.status_code}')
            json_out = json.dumps(out_dict)
        return json_out

    def query_all_instances(self):
        res = self.query_instance()
        res_json = res.json()
        instance_list = res_json['instances']
        self.logger.info(f'Status code query all instance: {res.status_code}')
        i = 1
        self.logger.info(f'Page {i}')
        try:
            continuationToken = res_json['continuationToken']
            while continuationToken:
                i += 1
                res = self.query_instance(continuationToken=continuationToken)
                self.logger.info(f'page {i}')
                res_json = res.json()
                instance_list += res_json['instances']
                continuationToken = res_json['continuationToken']
        except:
            self.logger.info(f'{len(instance_list)} intances in {i} pages')
            return json.dumps({'instances': instance_list})
        return json.dumps({'instances': instance_list})

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
                              highlight = 'true',
                              continuationToken = ''):
        """
        Query time series instances based on instance attributes
        If the amount of instances is over 100(maximum 100 per page), the continuationToken is needed to retrieve the next page
        """
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
                    "highlights": highlight,
                    "pageSize": 100}
                }
        res = requests.post(url = url,
                            headers = headers,
                            params=params,
                            data=json.dumps(data))
        self.logger.info(f'searching_keyword: {search_string}, status_code: {res.status_code}')
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
        self.logger.info(f'Status code query hierarchy: {res.status_code}')
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
        self.logger.info(f'Status code query type: {res.status_code}')
        return res