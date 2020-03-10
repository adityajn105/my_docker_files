import os
from notebook.auth import passwd
import json

sha = passwd(os.getenv('PASSWORD'))
configuration = { "NotebookApp" : { "password": f"{sha}" } }
if not os.path.exists('/root/.jupyter'): os.mkdir('/root/.jupyter')
with open("/root/.jupyter/jupyter_notebook_config.json",'w') as fp:
    fp.write(json.dumps(configuration))
