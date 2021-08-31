#!/usr/bin/env python3

import collections
import json
from datetime import datetime
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

    class UnexpectedError(Exception):
        pass

    class APIConnectionTemporaryRefused(Exception):
        pass

    def __init__(self, pixiv_id, pixiv_pass):
        self.ts = self.get_timestamp()
        self.pixiv_id, self.pixiv_pass = pixiv_id, pixiv_pass
        try:
            self.__login()
        except ValueError:
            raise self.LoginFailedError("Check your auth info. Maybe wrong.")
        except Exception as e:
            raise self.UnexpectedError("{}: {}".format(type(e), e))

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
        bookmark_tags, works_tags = self.__collect_tag_data()
        clist = collections.Counter(self.bookmark_tags + self.works_tags)
        sorted_clist = sorted(
            clist.most_common(), key=lambda x: x[1], reverse=True)
        return sorted_clist, bookmark_tags, works_tags

    def get_target_info(self, target_id):
        user_info = self.aapi.user_detail(target_id)
        self.rand_wait(0.5)
        names = {"name": user_info.user.name,
                 "account": user_info.user.account}
        return names

    def __collect_tag_data(self):
        try:
            bookmark_tags = self.__get_bookmarks_tag()
            works_tags = self.__get_works_tag()
        except KeyError as e:
            if e.args[0] == "illusts":
                raise self.APIConnectionTemporaryRefused("Wait for a while")
            else:
                raise e
        except Exception as e:
            raise self.UnexpectedError("{}: {}".format(type(e), e))
        else:
            return bookmark_tags, works_tags

    def __get_bookmarks_tag(self):
        tags = []
        next = None
        res_len = 30
        f = open(
            "{}_{}-bookmarks.jsonl".format(self.target_id, self.ts), "a+")
        while res_len == 30:
            if next is None:
                res = self.aapi.user_bookmarks_illust(self.target_id)
            else:
                res = self.aapi.user_bookmarks_illust(**next)

            self.rand_wait(0.5)

            print(res, file=f)  # debug

            for tags_ in [i["tags"] for i in res["illusts"]]:
                tag_names = [tag_["name"] for tag_ in tags_]
                tags.extend(tag_names)
            res_len = len(res["illusts"])
            next = self.aapi.parse_qs(res["next_url"])
            self.rand_wait(0.5)
        else:
            f.close()
            return tags

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")

    def __get_works_tag(self):
        tags = []
        next = None
        res_len = 30
        f = open(
            "{}_{}-works.jsonl".format(self.target_id, self.ts), "a+")
        while res_len == 30:
            if next is None:
                res = self.aapi.user_illusts(self.target_id)
            else:
                res = self.aapi.user_illusts(**next)

            print(res, file=f)

            self.rand_wait(0.5)

            for tags_ in [i["tags"] for i in res["illusts"]]:
                tag_name = [tag_["name"] for tag_ in tags_]
                tags.extend(tag_name)
            next = self.aapi.parse_qs(res["next_url"])
            self.rand_wait(0.5)
        else:
            f.close()
            return tags

    @staticmethod
    def rand_wait(base=0.1, rand=1.0):
        sleep(base + rand*random())


def main():
    print(BANNER)

    # init and login
    print('[+]login...')
    client_info = json.load(open("client.json", "r"))
    p = PixivTagAnalyzer(client_info["pixiv_id"], client_info["password"])

    # specify target id
    print("[+]OK!")
    print("[+]Target_id?(ex.かにかま->53993): ")
    print("[+]If you want to analyze own account, press Enter key.")
    target_id = input()
    target_id = (target_id if target_id == ""
                 else p.login_info.response.user.id)
    names = p.get_target_info(target_id)

    # start to analyze
    print("[+]Started to analyze user %s(%s)!" % (target_id, names))
    print("[+]Now getting tags of this user's bookmarks & works...")
    sorted_clist, bookmark_tags, works_tags = p.analyze(target_id)
    print("bookmark: %d, work: %d found." %
          (len(bookmark_tags), len(works_tags)))

    # specify number of tags to show
    len_clist = len(sorted_clist)
    print("[+]How many ranks do u wanna show?(ALL:%dtags):" % len_clist)
    rank_num = None
    while type(rank_num) is int:
        try:
            rank_num = int(input())
        except ValueError:
            print("[!]Invalid input.")

    # print top n
    for rank, t in enumerate(sorted_clist[0:rank_num]):
        parcentage = t[1]/len_clist*100
        print("#%03d\t%s\n(%d, %.02f%s)" % (rank, t[0], t[1], parcentage, "%"))


if __name__ == '__main__':
    main()
