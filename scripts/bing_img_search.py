import os
import requests, argparse, cv2
from requests import exceptions

#helper method to check for correct input
def check_positive(val):
    int_val = int(val)
    if int_val <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid number" % val)
    return int_val

'''
keep in mind this program is reliant on the bing api, so please keep in mind
that the results you will get are going to vary dependant on bing's algorithm

'''
if __name__ == "__main__":
        ap = argparse.ArgumentParser()
        ap.add_argument("-q", "--query", required=True, help="search query to search Bing IMage API for")
        ap.add_argument("-o", "--output", required=True, help="path to output directory of images")
        ap.add_argument("-m", "--max", nargs="?", default = 10, type = check_positive, help="maximum number of images to grab")
        ap.add_argument("-n", "--number", required=True, type = check_positive, help="number of images to grab")

        #parse the command line arguments
        args = vars(ap.parse_args())
        #read in azure credentials, must be file azure_api_key.txt
        with open("azure_api_key.txt", "r") as f:
            key_val = f.read().replace('\n','')
        API_KEY = key_val
        MAX_RESULTS = args["max"]
        GROUP_SIZE = args["number"]

        #url to do the searching
        URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

        #types of exceptions we are expecting with requests
        EXCEPTIONS = set([IOError, FileNotFoundError, exceptions.RequestException, exceptions.HTTPError, exceptions.ConnectionError, exceptions.Timeout])

        #term we are going to search for
        term = args["query"]
        headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
        #offset initially is going to be zero
        params = {"q": term, "offset": 0, "count": min(GROUP_SIZE, MAX_RESULTS)}

        #making the search
        print("searching Bing API for '{}'".format(term))
        search = requests.get(URL, headers=headers, params=params)
        search.raise_for_status()


        results = search.json()
        #pick the minimum factor of either the number we found or the passed max
        estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
        print ("est: {}, MAX_RESULTS: {}".format(results["totalEstimatedMatches"], MAX_RESULTS))
        print("{} total results for '{}'".format(estNumResults,term))


        total = 0

        for offset in range(0, estNumResults, GROUP_SIZE):

            print("Making request for group {}-{} of {}...\n".format(offset, offset + GROUP_SIZE, estNumResults))
            params["offset"] = offset
            search = requests.get(URL, headers=headers, params=params)
            search.raise_for_status()
            results = search.json()
            print("Saving images for group {}-{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))

            for v in results["value"]:
                try:
                    print("Grabbing: {}".format(v["contentUrl"]))
                    r = requests.get(v["contentUrl"], timeout = 30)
                    ext = v["contentUrl"][v["contentUrl"].rfind("."):]
                    p = os.path.sep.join([args["output"], "{}{}".format(str(total).zfill(8),ext)])
                    #write image data
                    f = open(p, "wb")
                    f.write(r.content)
                    f.close()

                #handle exceptions
                except Exception as e:
                    if type(e) in EXCEPTIONS:
                        print("got an error: {}".format(v["contentUrl"]))
                        continue
                #check if file is good, otherwise just remove it
                image = cv2.imread(p)
                if image is None:
                    print("Sorry something is wrong with this file, can't read it")
                    os.remove(p)
                    continue
                #increment the counter
                total += 1
