from WBL_BDP_TSI_Querier.tsi import TsiDataQuerier


if __name__ == '__main__':
    # Query parameters
    storage_type = 'coldstore'
    time_series_id = ['OSX66::32/1/VP/rg-01/p--/321VPFT010950.PV', ]
    start_time = ''
    end_time = ''
    start_time = '2020-05-05 00:00:00'
    end_time = '2020-05-05 02:00:00'
    filter = {"tsx": "($event.value.Double != null)"}
    search_string = "rg-05"
    hierarchyName = 'WBL Asset Hierarchies -  5 layers'
    available_projected_properties = [{'name': 'asset_id', 'type': 'String'}, {'name': 'value', 'type': 'Double'}, {'name': 'body', 'type': 'String'}]

    querier = TsiDataQuerier()

    res = querier.get_authorization_token()

    res_type = querier.query_type()
    print(f'Types: {res_type.status_code}')

    res_hierarchy = querier.query_hierarchy()
    print(f'Hierarchies: {res_hierarchy.status_code}')

    res_instance = querier.query_instance()
    print(f'Instances: {res_instance.status_code}')


    out = querier.query_event_by_hierarchy(storeType=storage_type,
                                           search_string=search_string, # Necessary
                                           hierarchyName=hierarchyName, # Necessary
                                           searchSpan={'from': start_time,
                                                       'to': end_time},
                                           filter=filter) # Necessary

    out = querier.query_event_by_id(storeType=storage_type,
                                    timeSeriesId= time_series_id,
                                    searchSpan={'from': start_time,
                                               'to': end_time},
                                    filter=filter) # Necessary


