from TSI_Querier.src.TSI_Querier import test
from TSI_Querier.src.TSI_Querier.DataQuerier import TsiDataQuerier

# fill in environment parameters
if __name__ == '__main__':    
    environment_variables = {'environment_fqdn':'891b666f-5619-467a-b554-c4acb36e8c60.env.timeseries.azure.com',
                             'client_secret':'-YnQjBK_5XV~mjZgyoDl6U4j..9h0hPmD3',
                             'client_id':'2f7a266d-a98e-468d-bf33-8336f820812e' ,
                             'tenant_id':'15f996bf-aad1-451c-8d17-9b95d025eafc' }

    querier = TsiDataQuerier(environment_variables=environment_variables)
    print(querier.get_authorization_token())
    
    # fill in query parameters
    query_variables = {'storage_type': 'coldstore',
                       'time_series_id':['OSX66::32/1/VP/rg-07/p--/321VPp--07001.RbkOut',],
                       'start_time':'2021-03-28 00:00:00',
                       'end_time':'2021-03-28 01:00:00',
                       'filter':{"tsx": "($event.value.Double != null)"},
                       'search_string':'Area32Transportlijn1VerpompenVPrg07',
                       'hierarchyName':'WBL Asset Hierarchies -  5 layers'}

    # run test function
    test.tsi_querier_test(environment_variables = environment_variables,
                          query_variables = query_variables)