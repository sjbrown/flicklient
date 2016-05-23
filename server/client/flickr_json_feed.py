import json

def raw_to_json_payload(raw_flickr_text):
    """
    The flickr "JSON" feed wraps the text in jsonFlickrFeed(...)
    so, strip it off
    """
    return raw_flickr_text[15:-1]

def defanged(flickr_json):
    chars = []
    for c in flickr_json:
        try:
            c.encode('ascii')
            chars.append(c)
        except:
            pass
    return ''.join(chars)

def json_to_dict(flickr_json):
    try:
        return json.loads(flickr_json)
    except ValueError:
        return json.loads(defanged(flickr_json))


def response_to_photo_dicts(response):
    """
    response is a response from the 'requests' module after an HTTP GET

    This can raise exceptions (including KeyError) if the input was not
    digestable.
    """
    if not response.ok:
        raise Exception('You gave me a not-OK response. Can not parse.')
    j = raw_to_json_payload(response.text)
    d = json_to_dict(j)
    
    # The dict contains some metadata about itself, what we really want
    # is the stuff under the "items" key
    return d['items']
