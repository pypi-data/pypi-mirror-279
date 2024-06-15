import logging
from urllib.parse import urlsplit

from har2locust.plugin import entriesprocessor_with_args


@entriesprocessor_with_args  # use with-args version because it is executed last
def default_headers(entries: list[dict], _args):
    # calculate headers shared by all requests (same name and value)
    default_headers = None
    for e in entries:
        headers = e["request"]["headers"]
        if default_headers is None:
            default_headers = headers[:]
        else:
            for dh in default_headers[:]:
                if dh["name"] == "accept-language":
                    # accept-language is likely to be common among most requests so we never remove it from default headers
                    # (instead it will be overridden in the specific requests where it differs)
                    continue
                for h in headers:
                    if dh["name"] == h["name"]:
                        if dh["value"] != h["value"]:
                            logging.debug(
                                f"removed default header {dh['name']} with value {dh['value']} from default headers because it has different value in {e['request']['url']}"
                            )
                            default_headers.remove(dh)  # header has different value
                        break
                else:
                    logging.debug(
                        f"removed default header {dh['name']} with value {dh['value']} from default headers because it was not present in {e['request']['url']}"
                    )
                    default_headers.remove(dh)  # header not present
    if default_headers is None:
        default_headers = []

    default_headers.sort(key=lambda item: item["name"])

    urlparts = urlsplit(entries[0]["request"]["url"])
    host = f"{urlparts.scheme}://{urlparts.netloc}"
    for e in entries:
        e["request"]["url"] = e["request"]["url"].removeprefix(host)
        headers = e["request"]["headers"]
        for h in headers[:]:
            for dh in default_headers:
                if h["name"] == dh["name"] and h["value"] == dh["value"]:
                    headers.remove(dh)
        headers[:] = sorted(headers, key=lambda item: item["name"])

    return {"host": host, "default_headers": default_headers}
