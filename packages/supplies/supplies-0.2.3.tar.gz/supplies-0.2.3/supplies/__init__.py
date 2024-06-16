from .reptiles import useragents
from .reptiles.cookies import rgetcookies

def updataToken(SystemVersion: str = "Windows7") -> None:
    import subprocess as sub

    if SystemVersion == "Windows7":
        print("正在安装 urllib3 == 1.7.1 \n Collecting urllib3 == 1.7.1")
        sub.run("pip uninstall urllib3==1.7.1")
        print("Done")
