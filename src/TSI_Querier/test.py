# from WBL_BDP_TSI_Querier.DataQuerier import TsiDataQuerier
from .DataQuerier import TsiDataQuerier

def tsi_querier_test(environment_variables = {},
                     query_variables = {}):
    # Service and app credentials 
    if environment_variables:
        try:
            environment_fqdn = environment_variables['environment_fqdn']
            client_secret = environment_variables['client_secret']
            client_id = environment_variables['client_id']
            tenant_id = environment_variables['tenant_id']
        except:
            print('Environment parameters are not complete provided.')
        
    # Query parameters
    if query_variables:
        try:
            storage_type = query_variables['storage_type']
            time_series_id = query_variables['time_series_id']
            start_time = query_variables['start_time']
            end_time = query_variables['end_time']
            filter = query_variables['filter']
            search_string = query_variables['search_string']
            hierarchyName = query_variables['hierarchyName']
        except:
            print('Query parameters are not complete provided, try to test with default parameters\n')

            query_variables = {'storage_type': 'coldstore',
                                'time_series_id': ['OSX66::32/1/VP/rg-01/p--/321VPFT010950.PV', ],
                                'start_time': '2020-05-05 00:00:00',
                                'end_time': '2020-05-05 02:00:00',
                                'filter': {"tsx": "($event.value.Double != null)"},
                                'search_string': 'Area32Transportlijn1VerpompenVPrg01',
                                'hierarchyName': 'WBL Asset Hierarchies -  5 layers'}

            storage_type = query_variables['storage_type']
            time_series_id = query_variables['time_series_id']
            start_time = query_variables['start_time']
            end_time = query_variables['end_time']
            filter = query_variables['filter']
            search_string = query_variables['search_string']
            hierarchyName = query_variables['hierarchyName']

    else:
        print('Query parameters are not complete provided, try to test with default parameters\n')
        query_variables = {'storage_type':'coldstore',
                            'time_series_id':['OSX66::32/1/VP/rg-01/p--/321VPFT010950.PV',],
                            'start_time':'2020-05-05 00:00:00',
                            'end_time':'2020-05-05 02:00:00',
                            'filter':{"tsx": "($event.value.Double != null)"},
                            'search_string':'Area32Transportlijn1VerpompenVPrg01',
                            'hierarchyName':'WBL Asset Hierarchies -  5 layers'}
        
        storage_type = query_variables['storage_type']
        time_series_id = query_variables['time_series_id']
        start_time = query_variables['start_time']
        end_time = query_variables['end_time']
        filter = query_variables['filter']
        search_string = query_variables['search_string']
        hierarchyName = query_variables['hierarchyName']

    querier = TsiDataQuerier(environment_variables=environment_variables)

    res_add_token = querier.get_authorization_token()
    print(f'Status code ADD token: {res_add_token.status_code}\n')

    res_type = querier.query_type()
    print(f'Status code query Types  : {res_type.status_code}\n')

    res_hierarchy = querier.query_hierarchy()
    print(f'Status code Hierarchies: {res_hierarchy.status_code} \n')

    res_instance = querier.query_instance()
    print(f'Status code Instances: {res_instance.status_code} \n ----- \n')

    out = querier.query_event_by_hierarchy(storeType=storage_type,
                                           search_string=search_string,
                                           hierarchyName=hierarchyName,
                                           searchSpan={'from': start_time,
                                                       'to': end_time},
                                           filter=filter)

    print(f'Results query event by hierarchy: {out}\n')

    out = querier.query_event_by_id(storeType=storage_type,
                                    timeSeriesId= time_series_id,
                                    searchSpan={'from': start_time,
                                                'to': end_time},
                                    filter=filter)

    print(f'Results query event by id: {out}\n')