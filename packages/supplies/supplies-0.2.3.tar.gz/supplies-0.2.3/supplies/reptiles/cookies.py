class RequestingError(Exception):
    def __init__(self, meassge="cookie获取时出现错误. \n \
                              English translation: There was an error when the cookie was obtained."):
        self.message = meassge

    def __str__(self):
        return self.message
    
class _ModVersionEror(Exception):
    def __init__(self): pass

    def __str__(self):
        return "requests 依赖包 urllib3 版本错误, 创建文件通过 from supplies import updateToken 调用 updataToken(SysyemVersion)进行更新 \n \
            English translation: Requests dependency package urllib3 version error. Create a file by calling updateToken (SysiemVersion) from suppliers import updateToken to update."
    
# # # # # # # # # # # # # # # # # # # # # 

def rgetcookies(url, method="post", parmas=None ,verify=True):
    try: import requests, urllib3
    except (Exception, ): raise _ModVersionEror()

    import requests
    from requests.utils import dict_from_cookiejar
    from supplies.reptiles import useragents

    r = None

    if method == "post":
        r = requests.get(url, headers=useragents.chrome(), parmas=parmas, verify=verify)
    if method == "get":
        r = requests.get(url=url, headers=useragents.chrome(), parmas=parmas, verify=verify)

    r.encoding = "utf-8"

    try:
        r.raise_for_status()
        return dict_from_cookiejar(r.cookies)
    except (Exception, ):
        raise RequestingError()
