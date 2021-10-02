import collections
from datetime import datetime
from json import dumps
from random import random
from time import sleep
from typing import Any, Dict, List, Tuple

from gppt import LoginInfo, PixivAuth


class PixivTagAnalyzer:
    class LoginFailedError(Exception):
        pass

    class UnexpectedError(Exception):
        pass

    class APIConnectionTemporaryRefused(Exception):
        pass

    def __init__(self) -> None:
        self.ts = self.get_timestamp()
        self.aapi, self.login_info = PixivAuth().auth()

    def get_login_info(self) -> LoginInfo:
        return self.login_info

    @staticmethod
    def get_timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")

    @staticmethod
    def rand_wait(base: float = 0.1, rand: float = 1.0) -> None:
        sleep(base + rand * random())

    def analyze(
        self, target_id: str
    ) -> Tuple[List[Tuple[str, int]], List[str], List[str]]:
        self.target_id = target_id
        bookmark_tags, works_tags = self.__collect_tag_data()
        clist = collections.Counter(bookmark_tags + works_tags)
        sorted_clist = sorted(clist.most_common(), key=lambda x: x[1], reverse=True)
        return sorted_clist, bookmark_tags, works_tags

    def get_target_info(self, target_id: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        user_info = self.aapi.user_detail(target_id)
        print(
            dumps(user_info, indent=4),
            file=open("data/{}-{}-userinfo.json".format(target_id, self.ts), "w"),
        )
        self.rand_wait(0.5)
        names = {"name": user_info.user.name, "account": user_info.user.account}
        return user_info, names

    def __collect_tag_data(self) -> Tuple[List[str], List[str]]:
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

    def __get_bookmarks_tag(self) -> List[str]:
        tags = []
        next = None
        res_len = 30
        f = open("data/{}_{}-bookmarks.jsonl".format(self.target_id, self.ts), "a+")
        while res_len == 30:
            if next is None:
                res = self.aapi.user_bookmarks_illust(self.target_id)
            else:
                res = self.aapi.user_bookmarks_illust(**next)

            self.rand_wait(0.5)

            print(dumps(res, indent=4), file=f)

            for tags_ in [i["tags"] for i in res["illusts"]]:
                tag_names = [tag_["name"] for tag_ in tags_]
                tags.extend(tag_names)
            res_len = len(res["illusts"])
            next = self.aapi.parse_qs(res["next_url"])
            self.rand_wait(0.5)
        else:
            f.close()
            return tags

    def __get_works_tag(self) -> List[str]:
        tags = []
        next = None
        res_len = 30
        f = open("data/{}_{}-works.jsonl".format(self.target_id, self.ts), "a+")
        while res_len == 30:
            if next is None:
                res = self.aapi.user_illusts(self.target_id)
            else:
                res = self.aapi.user_illusts(**next)

            print(dumps(res, indent=4), file=f)

            self.rand_wait(0.6)

            for tags_ in [i["tags"] for i in res["illusts"]]:
                tag_name = [tag_["name"] for tag_ in tags_]
                tags.extend(tag_name)
            res_len = len(res["illusts"])
            next = self.aapi.parse_qs(res["next_url"])
            self.rand_wait(0.6)
        else:
            f.close()
            return tags
