## TSI_QUERIER - A wrapped querier to query data from Azure Time Series Insight  

### Assumptions:
* Assuming Python is installed on your system
* The following environment fqdn and credentials are known by users
  * environment fqdn of the TSI instance
  * client secret of the service principle
  * client id of the service principle 
  * tenant id of the service principle

### Functions:
All the functions in the module are designed based on REST API which are documented in TSI official documentation https://docs.microsoft.com/en-us/rest/api/time-series-insights/reference-data-access-overview
* get_authorization_token(): Send POST request via REST API to get the Azure Access Token
* query_availability(): Send GET request via REST API to query the availability/search span of time series
* query_event_schema(): Send POST request via REST API to get event schema
* query_instance(): Query all the available instances from TSI. If the amount of instances is over 100(maximum 100 per page), the continuationToken is needed to retrieve the next page
* query_instance_search():  Query time series instances based on instance attributes. If the amount of instances is over 100(maximum 100 per page), the continuationToken is needed to retrieve the next page
* query_event_by_id(): Send POST request via REST API to get the timestamp and associated values of projected properties for asset with certain ID
* query_event_by_hierarchy(): Send POST request via REST API to get the timestamp and associated values of projected properties for asset with certain hierarchy by looking for a search string 

### Test:
To test the module, edit the test.py file, filling in the below variables

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




