param ($doc_id)

$auth_token = "xxxxxx"
$content_type = "application/json"
$base_url = "https://dms.richert.family"
$api_documents = $base_url+"/api/documents/"

#Define Auth Header
$auth_headers = @{
    Authorization="Token $auth_token"   
}
#build api doc
$api_doc = $api_documents+$doc_id+"/"
#get content of document
$content = (Invoke-RestMethod -Uri $api_doc -Headers $auth_headers -ContentType $content_type).content

#Extract Content Kundennummer
$pattern = "(?<=Kundennummer)(.*)"
$result = [regex]::Matches($content, $pattern).Value -replace ("[^a-zA-Z0-9]","")

if ($result -ne $null) {

    $post_data = @{
        custom_fields      = @(
            @{"value"="$result"
            "field"="8" #Kundennummer Feld MUSS ANGEPASST WERDEN
            }
        )
    } | ConvertTo-Json

        $post = Invoke-RestMethod -Uri $api_doc -Headers $auth_headers -ContentType $content_type -Body $post_data -Method Patch

}
