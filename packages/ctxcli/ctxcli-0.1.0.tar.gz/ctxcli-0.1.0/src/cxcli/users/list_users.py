import json
from cxcli import USER_SERVICE_NAME
from cxcli.cx_caller import CxCaller, Verb



def list_users(cx: CxCaller, params):
    a = cx.call(verb=Verb.GET, service=USER_SERVICE_NAME, path="users?returnAll=true")
    # a = call_cx(token=token,verb=Verb.GET,service="user-management")
    users = a["response"]["Users"]
    print(json.dumps(users,indent='\t'))
    