from v2ex import v2ex

api = v2ex.ApiCli(token="201c2e74-6d12-4025-84d1-359cef8d62b9", debug=True)

#for i in api.notifications()["result"]:
 #   print(i)
print(api.notifications_delete(noid=17458108))
