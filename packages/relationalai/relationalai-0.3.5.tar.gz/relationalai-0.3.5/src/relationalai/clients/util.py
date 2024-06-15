import urllib
import re

from relationalai.errors import RAIException

# replace the values of the URL parameters that start with X-Amz- with XXX
def scrub_url(url):
    parsed = urllib.parse.urlparse(url)
    parsed_qs = urllib.parse.parse_qs(parsed.query)
    for key in parsed_qs:
        if key.startswith("X-Amz-"):
            parsed_qs[key] = "XXX"
    new_qs = urllib.parse.urlencode(parsed_qs, doseq=True)
    return urllib.parse.urlunparse(parsed._replace(query=new_qs))

def find_urls(string):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = re.findall(url_pattern, string)
    return urls

def scrub_urls(string, urls):
    for url in urls:
        # replace with scrubbed version
        string = string.replace(url, scrub_url(url))
    return string

def scrub_exception(exception):
    exception_str = str(exception)
    urls = find_urls(exception_str)
    if urls:
        return RAIException(scrub_urls(exception_str, urls))
    return exception

def escape_for_f_string(code: str) -> str:
    return (
        code
        .replace("\\", "\\\\")
        .replace("{", "{{")
        .replace("}", "}}")
        .replace("\n", "\\n")
        .replace('"', '\\"')
        .replace("'", "\\'")
    )

def escape_for_sproc(code: str) -> str:
    return code.replace("$$", "\$\$")