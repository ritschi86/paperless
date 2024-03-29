#!/usr/bin/env python
import os
import httpx
import json
import re

#Define Variables
auth_token = "xxxxxxxxxxx"
url_base = "https://paperless.local"
custom_field_nr = "8"

search_pattern = ["Kundennummer",
                  "Kunden-Nr",
                  "Kd.Nr",
                  "Mitglieds-Nr",
                  "Unser Zeichen"
                ]


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
    response = httpx.get(api_url, headers=auth_header)
    result = response.json()

    #Debug Doc ID
    print(result["id"])

    def adding_cf():
        custom_fields = result["custom_fields"]
        add_custom_field = {"value":post_custom_kdnr, "field":custom_field_nr}
        custom_fields.append(add_custom_field)
        print(custom_fields)

        post_custom_fields = ({
                    "custom_fields": custom_fields
                })
        httpx.patch(api_url, headers=auth_header, json=post_custom_fields)
    for search_word in search_pattern:
        try:
            print(f"Suchwort: {search_word}")
            json_lookahead = re.search(f"(?<={search_word})(.*)",result["content"])
            post_custom_kdnr = json_lookahead.group(0)
            post_custom_kdnr = re.sub("[^a-zA-Z0-9]","",post_custom_kdnr)
            # modify the custom fields
            adding_cf()
        except:
            print(f"Keinen Treffer für {search_word}")
    

doc = os.environ.get('DOCUMENT_ID')
paperless_send(doc)