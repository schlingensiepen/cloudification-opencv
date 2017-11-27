import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests, time, json
import threading, argparse


###############################################
#### Update or verify the following values. ###
###############################################
# Replace the subscription_key string value with your valid subscription key.
subscription_key = '__TODO__'

uri_base = 'westcentralus.api.cognitive.microsoft.com'

def process_file(filename):
    print ("process_file ", filename)
    headers = {
        # Request headers.
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }
    
    params = urllib.parse.urlencode({
        # Request parameters. The language setting "unk" means automatically detect the language.
        
        'detectOrientation ': 'true',
    })
    
    # The URL of a JPEG image containing text.
    body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png'}"
    
    try:
        req_body = open(filename, 'rb').read()
        # Execute the REST API call and get the response.
        conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')		
        conn.request("POST", "/vision/v1.0/ocr?%s" % params, body=req_body, headers=headers)
        #conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read().decode('utf8')
    
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()
    
    except Exception as e:
        print('Error:')
        print(e)
    
####################################

def process_file_async(filename):
    print ("process_file_async ", filename)
    thread = threading.Thread(target=process_file, args=[filename])
    thread.start()

def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", 
       help="path to the file to ocr")
    args = None
    try:
        args = vars(ap.parse_args())
    except:
        ap.print_help()
        quit()

    timed = False
    if args.get("file", None) is None:
        ap.print_help()
        quit()

    process_file_async (args["file"])

if __name__ == "__main__": main()