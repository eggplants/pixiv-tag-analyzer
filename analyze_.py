import collections
import json
from getpass import getpass

from pixivpy3 import AppPixivAPI, PixivAPI

# AA
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
client_info = json.load(open("client.json", "r"))

# login with account info json file
try:
    api = PixivAPI()
    login_info = api.auth(client_info["pixiv_id"], client_info["password"])
    aapi = AppPixivAPI()
    aapi.login(client_info["pixiv_id"], client_info["password"])
except Exception:
    print("[!]Auth from file failed!")

    # login with stdin input
    try:
        print("[+]ID is mail address, userid, account name.")
        stdin_login = (input("[+]ID: "), getpass("[+]Password: "))
        login_info = api.login(stdin_login[0], stdin_login[1])
        aapi = AppPixivAPI()
        aapi.login(stdin_login[0], stdin_login[1])
    except Exception:
        print("[!]Auth from stdin failed!")
        exit()

# input target id
print("[+]Authorization successful!")
print("[+]Target_id?(ex.かにかま->53993): ")
print("[+]If you want to analyze own account, press Enter key.")
target_id = input()
if target_id == "":
    target_id = login_info.response.user.id

# let's analyze!
user_info = aapi.user_detail(target_id)
names = "name: "+user_info.user.name+", account: "+user_info.user.account
tags = []
next = ""
c = [0, 0]

# retrieve bookmark tag


def retrieve_bookmarks_tag(api, tags, next, target_id):
    while True:
        if next == "":
            j = api.user_bookmarks_illust(target_id)
        else:
            j = api.user_bookmarks_illust(**next)

        for _ in [i["tags"] for i in j["illusts"]]:
            for __ in _:
                tags.append(__["name"])
        c[0] += len(j["illusts"])
        if len(j["illusts"]) != 30:
            break
        next = api.parse_qs(j["next_url"])

# retrieve work tag


def retrieve_works_tag(api, tags, next, target_id):
    while True:
        if next == "":
            j = api.user_illusts(target_id)
        else:
            j = api.user_illusts(**next)

        for _ in [i["tags"] for i in j["illusts"]]:
            for __ in _:
                tags.append(__["name"])
        c[1] += len(j["illusts"])
        if len(j["illusts"]) != 30:
            break
        next = api.parse_qs(j["next_url"])


print("[+]Started to analyze user %s(%s)!" % (target_id, names))
print("[+]Now getting tags of this user's bookmarks...")
retrieve_bookmarks_tag(aapi, tags, next, target_id)
print("[+]Now getting tags of this user's work...")
retrieve_works_tag(aapi, tags, next, target_id)
print("bookmark: %d, work: %d found." % (c[0], c[1]))

# show ranking
clist = collections.Counter(tags)
print("[+]How many ranks do u wanna show?(ALL:%dtags):" % (len(clist)))
try:
    rank_num = int(input())
except Exception:
    rank_num = 10
rank = 1
s_c = sorted(clist.most_common(), key=lambda x: x[1], reverse=True)
for t in s_c[0:rank_num]:
    parcentage = t[1]/len(clist)*100
    print("#%03d\t%s\n(%d, %.02f%s)" % (rank, t[0], t[1], parcentage, "%"))
    rank += 1
