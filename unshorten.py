import argparse
import http.client
import re


ERR_CANT_LOAD_URL = "ERROR: Couldn't load the URL. Please try again, or try a different URL."
ERR_NOT_SHORT_URL = "ERROR: Doesn't appear to be a shortened URL. Please try another URL."


def fetch_header(url_host, url_path):
    try:
        svc_connection = http.client.HTTPConnection(url_host)
        svc_connection.request("HEAD", "/" + url_path)

        return svc_connection.getresponse()

    except:
        print(ERR_CANT_LOAD_URL)
        return False


def get_link_destination(response_header):
    try:
        if response_header.status == 301:
            print("\n***Shortened URL***\n\n" + response_header.getheader("Location"))
            return True
        else:
            print(ERR_NOT_SHORT_URL)
            return False

    except AttributeError:
        print(ERR_CANT_LOAD_URL)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Shortened URL to be resolved")
    args = parser.parse_args()
    url_parts = (re.sub("https?://", "", args.url)).split("/")

    if len(url_parts) == 2:
        shortened_url_response = fetch_header(url_parts[0], url_parts[1])
        if shortened_url_response:
            get_link_destination(shortened_url_response)

    else:
        print(ERR_NOT_SHORT_URL)

