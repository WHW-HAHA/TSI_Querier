from TSI_Querier import test
from TSI_Querier.DataQuerier import TsiDataQuerier

# fill in environment parameters
if __name__ == '__main__':    
    environment_variables = {'environment_fqdn': 'eaecab34-790f-4736-a7ad-6e26fb0c3f4e.env.timeseries.azure.com',
                             'client_secret': '-YnQjBK_5XV~mjZgyoDl6U4j..9h0hPmD3',
                             'client_id':'2f7a266d-a98e-468d-bf33-8336f820812e' ,
                             'tenant_id':'15f996bf-aad1-451c-8d17-9b95d025eafc' }

    querier = TsiDataQuerier(environment_variables=environment_variables)
    print(querier.get_authorization_token())
    
    # fill in query parameters
    query_variables = {'time_series_id':['OSX66::32/1/VP/rg-01/p--/321VPFT010950.PV',],
                       'start_time':'2020-05-05 00:00:00',
                       'end_time':'2020-05-05 02:00:00',
                       'filter':{"tsx": "($event.value.Double != null)"},
                       'search_string':'Area32Transportlijn1VerpompenVPrg01',
                       'hierarchyName':'WBL Asset Hierarchies -  5 layers'}

    # run test function
    test.tsi_querier_test(environment_variables = environment_variables,
                          query_variables = query_variables)