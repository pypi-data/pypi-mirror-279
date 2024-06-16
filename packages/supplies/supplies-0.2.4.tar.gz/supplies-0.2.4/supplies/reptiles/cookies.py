from .. import execeptions

def rgetcookies(url, method="post", parmas=None ,verify=True):
    try: import requests, urllib3
    except (Exception, ): raise execeptions.ModVersionException()
    else:

        import requests.exceptions
        from requests.utils import dict_from_cookiejar
        from supplies.reptiles import useragents
        if method == "post":
            r = requests.post(url=url, headers=useragents.chrome(), parmas=parmas, verify=verify)
            r.encoding = "utf-8"
        if method == "get":
            r = requests.get(url=url, headers=useragents.chrome(), parmas=parmas, verify=verify)
            r.encoding = "utf-8"

        try:
            r.raise_for_status()
            return dict_from_cookiejar(r.cookies)
        except (Exception, ):
            raise execeptions.RequestingException()
