# setup.py
from distutils.core import setup
import py2exe

includes = []


options = {"py2exe":
            {   "compressed": 1,
                "optimize": 2,
                "includes": includes,
                "bundle_files": 1
            }
          }

setup(   
    version = "0.1.0",
    description = "run nginx and php",
    name = "wnp",
    options = options,
    zipfile=None,
    windows=[{"script": "wnp.pyw","icon_resources" : [(1, "nginx.ico")]}],  
    data_files=[("./.",["nginx.ico"]),]
)