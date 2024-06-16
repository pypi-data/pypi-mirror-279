class RequestingException(Exception):
    def __init__(self, meassge="cookie获取时出现错误. \n \
                              English translation: There was an error when the cookie was obtained."):
        self.message = meassge

    def __str__(self): return self.message
    
class ModVersionException(Exception):
    def __init__(self): pass

    def __str__(self):
        return "requests 依赖包 urllib3 版本错误, 创建文件通过 from supplies import updateToken 调用 updataToken(SysyemVersion)进行更新 \n \
            English translation: Requests dependency package urllib3 version error. Create a file by calling updateToken (SysiemVersion) from suppliers import updateToken to update."
