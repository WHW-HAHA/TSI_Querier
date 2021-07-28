# from WBL_BDP_TSI_Querier.DataQuerier import TsiDataQuerier
from TSI_Querier.DataQuerier import TsiDataQuerier

if __name__ == '__main__':
    # Service and app credentials
    environment_fqdn = ''
    client_secret = ''
    client_id = ''
    tenant_id = ''

    # Query parameters
    storage_type = 'coldstore'
    time_series_id = ['OSX66::32/1/VP/rg-01/p--/321VPFT010950.PV',]
    start_time = '2020-05-05 00:00:00'
    end_time = '2020-05-05 02:00:00'
    filter = {"tsx": "($event.value.Double != null)"}
    search_string = "Area32Transportlijn1VerpompenVPrg01"
    hierarchyName = 'WBL Asset Hierarchies -  5 layers'

    querier = TsiDataQuerier(environment_fqdn = environment_fqdn,
                             client_secret = client_secret,
                             client_id = client_id,
                             tenant_id = tenant_id)

    res = querier.get_authorization_token()

    res_type = querier.query_type()
    print(f'Status code query Types  : {res_type.status_code}\n')

    res_hierarchy = querier.query_hierarchy()
    print(f'Hierarchies: {res_hierarchy.status_code} \n')

    res_instance = querier.query_instance()
    print(f'Instances: {res_instance.status_code} \n')

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