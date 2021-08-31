#!/usr/bin/env python3

import collections
import json
from random import random
from time import sleep

from gppt import selenium as s
from pixivpy3 import AppPixivAPI, PixivAPI

BANNER = '''
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
'''


class PixivTagAnalyzer:
    class LoginFailedError(Exception):
        pass

    def __init__(self, pixiv_id, pixiv_pass):
        self.pixiv_id, self.pixiv_pass = pixiv_id, pixiv_pass
        try:
            self.__login()
        except Exception as e:
            raise self.LoginFailedError("{}: {}".format(type(e), e))

    def __login(self):
        REFRESH_TOKEN = self.__get_refresh_token(
            self.pixiv_id, self.pixiv_pass)
        self.api = PixivAPI()
        self.login_info = self.api.auth(refresh_token=REFRESH_TOKEN)
        self.rand_wait(0.1)
        self.aapi = AppPixivAPI()
        self.aapi.auth(refresh_token=REFRESH_TOKEN)
        self.rand_wait(0.1)

    @staticmethod
    def __get_refresh_token(pixiv_id, pixiv_pass):
        gpt = s.GetPixivToken(headless=True, user=pixiv_id, pass_=pixiv_pass)
        res = gpt.login()
        return res["refresh_token"]

    def analyze(self, target_id):
        self.target_id = target_id
        self.counters = [0, 0]
        bookmark_tags = self.__get_bookmarks_tag()
        works_tags = self.__get_works_tag()
        clist = collections.Counter(self.bookmark_tags + self.works_tags)
        sorted_clist = sorted(
            clist.most_common(), key=lambda x: x[1], reverse=True)
        return sorted_clist, bookmark_tags, works_tags

    def get_target_info(self, target_id):
        user_info = self.aapi.user_detail(target_id)
        self.randSleep(0.1)
        names = {"name": user_info.user.name,
                 "account": user_info.user.account}
        return names

    def __get_bookmarks_tag(self):
        tags = []
        next = None
        res_len = 30
        while res_len == 30:
            if next is None:
                res = self.aapi.user_bookmarks_illust(self.target_id)
            else:
                res = self.aapi.user_bookmarks_illust(**next)

            self.randSleep(0.1)

            for tags_ in [i["tags"] for i in res["illusts"]]:
                tag_names = [tag_["name"] for tag_ in tags_]
                tags.extend(tag_names)
            res_len = len(res["illusts"])
            self.counters[0] += res_len
            next = self.aapi.parse_qs(res["next_url"])
            self.randSleep(0.3)
        else:
            return tags

    def __get_works_tag(self):
        tags = []
        next = None
        res_len = 30
        while res_len == 30:
            if next is None:
                res = self.aapi.user_illusts(self.target_id)
            else:
                res = self.aapi.user_illusts(**next)

            self.randSleep(0.1)

            for tags_ in [i["tags"] for i in res["illusts"]]:
                tag_name = [tag_["name"] for tag_ in tags_]
                tags.extend(tag_name)
            self.counters[1] += len(res["illusts"])
            next = self.aapi.parse_qs(res["next_url"])
            self.randSleep(0.1)
        else:
            return tags

    def rand_wait(self, base=0.1, rand=0.5):
        sleep(base + rand*random())


def main():
    print('[+]login...')
    client_info = json.load(open("client.json", "r"))
    p = PixivTagAnalyzer(client_info["pixiv_id"], client_info["password"])
    print("[+]OK!")
    print("[+]Target_id?(ex.かにかま->53993): ")
    print("[+]If you want to analyze own account, press Enter key.")
    target_id = input()
    if target_id == "":
        target_id = p.login_info.response.user.id

    names = p.get_target_info(target_id)
    print("[+]Started to analyze user %s(%s)!" % (target_id, names))
    print("[+]Now getting tags of this user's bookmarks & works...")
    sorted_clist, bookmark_tags, works_tags = p.analyze(target_id)
    print("bookmark: %d, work: %d found." %
          (len(bookmark_tags), len(works_tags)))
    len_clist = len(sorted_clist)
    print("[+]How many ranks do u wanna show?(ALL:%dtags):" % len_clist)
    rank_num = None
    while type(rank_num) is int:
        try:
            rank_num = int(input())
        except ValueError:
            print("[!]Invalid input.")

    for rank, t in enumerate(sorted_clist[0:rank_num]):
        parcentage = t[1]/len_clist*100
        print("#%03d\t%s\n(%d, %.02f%s)" % (rank, t[0], t[1], parcentage, "%"))


if __name__ == '__main__':
    main()
