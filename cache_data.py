import requests
import json

def setup_caching(cache_dict, cache_name):
    CACHE_DICTION = cache_dict
    CACHE_FNAME = cache_name

def params_unique_combination(url, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        if k != 'key' or 'apiKey':
            res.append("{}-{}".format(k, params[k]))
    return url + "_".join(res)

def make_request_using_cache(url, CACHE_DICTION, CACHE_FNAME, params=None):
    global header

    if params is not None:
        unique_ident = params_unique_combination(url,params)
    else:
        unique_ident = url

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        #print("Making a request for new data...")
        # Make the request and cache the new data
        if params is not None:
            resp = requests.get(url, params)
            CACHE_DICTION[unique_ident] = json.loads(resp.text)
        else:
            resp = requests.get(url)
            CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]
