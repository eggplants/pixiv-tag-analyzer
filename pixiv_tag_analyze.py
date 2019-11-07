import os
import json
#import subprocess
import collections
from getpass import getpass
from pixivpy3 import *

#AA
print('''
#######################################
#######################################
##                                   ##
## mmmmm    "             "          ##
## #   "# mmm    m   m  mmm    m   m ##
## #mmm#"   #     #m#     #    "m m" ##
## #        #     m#m     #     #m#  ##
## #      mm#mm  m" "m  mm#mm    #   ##
##                                   ##
##                                   ##
#######################################
#######################################
''')

# Auth
f = open("client.json", "r")
client_info = json.load(f)
f.close()
api = PixivAPI()
api.hosts = "https://app-api.pixiv.net"

# login with account info json file
try:
	login_info=api.login(client_info["pixiv_id"], client_info["password"])
	aapi=AppPixivAPI()
	aapi.login(client_info["pixiv_id"], client_info["password"])
except:
	print("[!]Auth from file failed!")

	#login with stdin input
	try:
		print("[+]id is mail address,userid, account name")
		stdin_login=(input("[+]id: "),getpass("[+]password: "))
		api.login(stdin_login[0],stdin_login[1])
		aapi=AppPixivAPI()
		aapi.login(stdin_login[0],stdin_login[1])
	except:
		print("[!]Auth from stdin failed!")
		exit()

#input target id
print("[+]Authorization successful!")
print("[+]Target_id?(かにかま->53993): ")
print("[+]If you want to analyze own account, press Enter key.")
target_id=input()
if target_id=="":
	target_id=login_info.response.user.id

#let's analyze!
user_info = aapi.user_detail(target_id)
names="name: "+user_info.user.name+", account: "+user_info.user.account
tags=[]
next=""
c=[0,0]

# retrieve bookmark tag
def retrieve_bookmarks_tag(api,tags,next,target_id):
	while True:
		if next=="":
			j=api.user_bookmarks_illust(target_id)
		else:
			j=api.user_bookmarks_illust(**next)

		for _ in [i["tags"] for i in j["illusts"]]:
			for __ in _:tags.append(__["name"])
		c[0]+=len(j["illusts"])
		if len(j["illusts"])!=30:break
		next=api.parse_qs(j["next_url"])

# retrieve work tag
def retrieve_works_tag(api,tags,next,target_id):
	while True:
		if next=="":
			j=api.user_illusts(target_id)
		else:
			j=api.user_illusts(**next)

		for _ in [i["tags"] for i in j["illusts"]]:
			for __ in _:tags.append(__["name"])
		c[1]+=len(j["illusts"])
		if len(j["illusts"])!=30:break
		next=api.parse_qs(j["next_url"])

print("[+]Started to analyze %s(%s)"%(target_id,names))
print("[+]Now getting tags of this user's bookmarks...")
retrieve_bookmarks_tag(aapi,tags,next,target_id)
print("[+]Now getting tags of this user's work...")
retrieve_works_tag(aapi,tags,next,target_id)
print("bookmark: %d, work: %d found."%(c[0],c[1]))

# show ranking
clist=collections.Counter(tags)
print("[+]How many ranks do u wanna show?(ALL:%dtags):"%(len(clist)))
try:
	rank_num=int(input())
except:
	rank_num=10
rank=1
for t in sorted(clist.most_common(),key=lambda x: x[1],reverse=True)[0:rank_num]:
	parcentage=t[1]/len(clist)*100
	print("#%04d:%s:%d:%.02f"%(rank,t[0],t[1],parcentage))
	rank+=1

# debug json
#j=aapi.user_bookmarks_illust(**next)
#with open('out.json','w') as f:
#	json.dump(j, f, ensure_ascii=False)
#
#cmd='python -m json.tool out.json'
#with open('out_b.json','w') as f:
#	subprocess.call(cmd.split(),stdout=f)
