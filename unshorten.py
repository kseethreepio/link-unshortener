import argparse
import http.client
import re

def fetch_header(url_host, url_path):
    try:
        svc_connection = http.client.HTTPConnection(url_host)
        svc_connection.request("HEAD", "/" + url_path)

        return svc_connection.getresponse()

    except:
        print("ERROR: Couldn't load the URL. Please try again, or try a different URL.")
        pass


def get_link_destination(response_header):
    if response_header.status == 301:
        print("\n***Shortened URL***\n\n" + response_header.getheader("Location"))
    else:
        print("ERROR: Doesn't appear to be a shortened URL. Please try another URL.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Shortened URL to be resolved")
    args = parser.parse_args()
    url_parts = (re.sub("https?://", "", args.url)).split("/")

    try:
        if len(url_parts) == 2:
            shortened_url_response = fetch_header(url_parts[0], url_parts[1])
            get_link_destination(shortened_url_response)
        else:
            print("ERROR: Doesn't appear to be a shortened URL. Please try another URL.")

    except IndexError:
        print("ERROR: Doesn't appear to be a valid URL. Please try another URL.")

