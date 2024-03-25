#!/usr/bin/env python
import os
import httpx
import json
import re

#Define Variables
auth_token = "APITOKEN"
url_base = "https://paperless.local"
custom_field_nr = "8"


def paperless_send(doc):
    #Define API URL
    url_api_doc = url_base + "/api/documents/"
    #Define Token
    auth_header = ({
    "Authorization":"Token "+ auth_token,
    "Content-Type":"application/json" 
    })

    #Debug Auth Header
    print(auth_header)

    api_url = url_api_doc + doc + "/"
    #Debug API URL
    print(api_url)
        # Send POST request with FORM data using the data parameter
    response = httpx.get(api_url, headers=auth_header)

    result = response.json()

    #Debug Doc ID
    print(result["id"])

    json_lookahead = re.search("(?<=Kundennummer)(.*)",result["content"])
    post_custom_kdnr = json_lookahead.group(0)
    post_custom_kdnr = re.sub("[^a-zA-Z0-9]","",post_custom_kdnr)


    custom_kdnr = ({
        "custom_fields": [
            {
                "value": post_custom_kdnr,
                "field": custom_field_nr
            }
        ]
    })
    httpx.patch(api_url, headers=auth_header, json=custom_kdnr)

doc = os.environ.get('DOCUMENT_ID')
paperless_send(doc)
