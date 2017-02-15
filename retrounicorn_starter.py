import os
import urllib
try:
    urllib.urlretrieve ("https://raw.githubusercontent.com/achojoao/retrounicorn/master/retrounicorn.py", "retrounicorn.py")
except:
    pass
os.system("python retrounicorn.py")