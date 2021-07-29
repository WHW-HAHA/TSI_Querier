## TSI_QUERIER - A querier to query data from Azure Time Series Insight  

### Assumptions:
* Assuming Python(>=3.6) is installed in your system
* The following environment fqdn and credentials are known by users
  * environment fqdn of the TSI instance
  * client secret of the service principle
  * client id of the service principle 
  * tenant id of the service principle

### Functions:
All the functions in the module are designed based on REST API which are documented in TSI official documentation https://docs.microsoft.com/en-us/rest/api/time-series-insights/reference-data-access-overview
* get_authorization_token(): Send POST request via REST API to get the Azure Access Token
  * Return:
    * json type response

* query_availability(): Send GET request via REST API to query the availability/search span of time series
  * Return:
    * json type response
  
* query_type(): Query available hierarchies from TSI
  * Return:
    * json type response
  
* query_type(): Query available types from TSI
  * Return:
    * json type response
  
* query_event_schema(storeType, searchSpan): Send POST request via REST API to get event schema.
  * Parameters:
    * storeType:
      * type: string
      * value: 'coldstore' or 'warmstore', not case sensitive
      * nullable: true
    * searchSpan:
      * type: dictionary 
      * value: searchSpan = {'from': 'yyyy-mm-dd hh-mm-ss' , 'to': 'yyyy-mm-dd hh-mm-ss'}
      * nullable: false
  * Return:
    * json type response

* query_instance(continuationToken): Query all the available instances from TSI. If the amount of instances is over 100(maximum 100 per page), the continuationToken is needed to retrieve the next page
  * Parameter:
    * continuationToken
      * type: string
      * nullable: true
  * Return:
    * json type response

* query_instance_search(search_string, hierarchyName, recursive, highlights, continuationToken):  Query time series instances based on instance attributes. If the amount of instances is over 100(maximum 100 per page), the continuationToken is needed to retrieve the next page
  * Parameters:
    * search_string
      * type: string
      * nullable: true
    * hierarchyName：
      * type: string
      * nullable: false
    * recursive:
      * type: string
      * value: 'true' or 'false'
      * nullable: true
    * continuationToken
      * type: string
      * nullable: true
  * Return:
    * json type response

* query_event_by_id(storeType, timeSeriesId, searchSpan, filter): Send POST request via REST API to get the timestamp and associated values of projected properties for asset with certain ID
  * Parameters:
    * storeType:
      * type: string
      * value: 'coldstore' or 'warmstore', not case sensitive
      * nullable: true
    * timeSeriesId:
      * type: string
      * nullable: false
    * searchSpan:
      * type: dictionary 
      * value: searchSpan = {'from': 'yyyy-mm-dd hh-mm-ss' , 'to': 'yyyy-mm-dd hh-mm-ss'}
      * nullable: false
    * filter:
      * type: string
      * nullable: true
  * Return:
    * json type response    
* query_event_by_hierarchy(search_string, hierarchyName, recursive, highlight, continuationToken): Send POST request via REST API to get the timestamp and associated values of projected properties for asset with certain hierarchy by looking for a search string
  * Parameters:
    * search_string
      * type: string
      * nullable: true
    * hierarchyName：
      * type: string
      * nullable: false
    * recursive:
      * type: string
      * value: 'true' or 'false'
      * nullable: true
    * highlight:
      * type: string
      * value: 'true' or 'false'
      * nullable: true
    * continuationToken
      * type: string
      * nullable: true
  * Return:
    * json type response
    
### Variable explainations
Environment fqdn and credentials
* environment_fqdn = environment fqdn
* client_secret = client secret
* client_id = client id
* tenant_id = tenant id

Query parameters
The details of the explainations and use cases of are available in official documentation https://docs.microsoft.com/en-us/rest/api/time-series-insights/reference-data-access-overview
* time_series_id = the time series id of the instance
  
Start time and end time in 'yyyy-mm-dd hh-mm-ss' format e.g.,
* start_time = '2020-05-05 00:00:00'
* end_time = '2020-05-05 02:00:00'

The filter that is used to filter the resulted values e.g., 
* filter = {"tsx": "($event.value.Double != null)"}
  
The keyword to identify the instance, e.g,   
* search_string = "Area32Transportlijn1VerpompenVPrg01"
  
The hierarchy name of the which the instance is nested in
* hierarchyName = 'WBL Asset Hierarchies -  5 layers'

Run the testing scripts in IDE or console, the test.py will execute following functions in order
* TsiDataQuerier.get_authorization_token()
* TsiDataQuerier.query_type()
* TsiDataQuerier.query_hierarchy()
* TsiDataQuerier.query_instance()
* TsiDataQuerier.query_event_by_hierarchy()
* TsiDataQuerier.query_event_by_id()

### Test and use
#### Test:
To test the module, replace the empty string with correct strings and execute the following code example

```Python
from TSI_Querier import test

# fill in environment parameters
if __name__ == '__main__':    
    environment_variables = {'environment_fqdn': '',
                             'client_secret': '',
                             'client_id':'' ,
                             'tenant_id':'' }
    
    # fill in query parameters
    query_variables = {'time_series_id':[''],
                       'start_time':'',
                       'end_time':'',
                       'filter':{"tsx": "($event.value.Double != null)"},
                       'search_string':'',
                       'hierarchyName':''}

    # run test function
    test.tsi_querier_test(environment_variables = environment_variables,
                          query_variables = query_variables)
```
#### Use
Instantiate the class to use the above mentioned functions
```Python
from TSI_Querier.DataQuerier import TsiDataQuerier

# fill in environment variables
environment_variables = {'environment_fqdn': '',
                         'client_secret': '',
                         'client_id':'' ,
                         'tenant_id':'' }
# instantiate the querier
querier = TsiDataQuerier(environment_variables=environment_variables)
# run query functions e.g,
response = querier.get_authorization_token()
```
