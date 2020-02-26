def s5psearch(geoj, dateSt, dateEnd, prod):

    import requests
    import json
    from pandas.io.json import json_normalize
    from sentinelsat.sentinel import read_geojson, geojson_to_wkt
    import pandas as pd
    
    #convert geojson to wkt for API query 
    geom = geojson_to_wkt(read_geojson(geoj))

    # set return paramaters
    collection = 'Sentinel5P'
    page = 1
    maxRecords = 2000
    resp = 'json'
    
#    if dateEnd.date() < pd.to_datetime('today').date() - pd.Timedelta(days=14):
#        prodId = '%OFFL%|%RPRO%'
#    else:
#        prodId = ''
        
    if dateSt != dateEnd:
        dateEnd  = dateEnd.date() - pd.Timedelta(days=1)
        

    # create API query dictionary
    input_data = {
        "maxRecords": maxRecords,
    	"page": page,
        "productType" : prod,
        #"productIdentifier": prodId,
    	"startDate": dateSt.strftime('%Y-%m-%dT00:00:00Z'),
    	"completionDate": dateEnd.strftime('%Y-%m-%dT23:59:59Z'),
        "geometry": geom,
        "status": 'all'
    }

    # Build query
    query = f'''http://finder.creodias.eu/resto/api/collections/{collection}/search.{resp}?'''
    
    # Send request
    session = requests.Session()
    response = session.get(query, params=input_data)
    
    response.close()

    r = json.loads(response.text)
    
    res_df = json_normalize(r['features'])
    
    if res_df.empty != True:
        
        res_path = res_df['properties.productIdentifier']
    
        res_path = res_path.str.replace('/eodata', 'y:')
        
        res_path = res_path.astype(str) + '/*.nc'
    
        res_path = res_path.to_list()
        
        return res_path
    
    else:
        return

#