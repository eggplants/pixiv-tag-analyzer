#!/usr/bin/env python3

from os import makedirs
from typing import Optional

from .PixivTagAnalyzer import PixivTagAnalyzer

BANNER = """
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
"""


def main() -> None:
    print(BANNER)

    p = PixivTagAnalyzer()

    # create data dir
    makedirs("data", exist_ok=True)

    # specify target id
    print("[+]OK!")
    print("[+]Target_id?(ex.かにかま->53993): ")
    print("[+]If you want to analyze own account, press Enter key.: ", end="")
    target_id = input()
    target_id = (
        target_id if target_id != "" else p.get_login_info()["response"]["user"]["id"]
    )
    _, names = p.get_target_info(target_id)

    # start to analyze
    print("[+]Started to analyze user %s(%s)!" % (target_id, names))
    print("[+]Now getting tags of this user's bookmarks & works...")
    sorted_clist, bookmark_tags, works_tags = p.analyze(target_id)
    print(
        "[+]Fetched data: bookmark: %d, work: %d"
        % (len(bookmark_tags), len(works_tags))
    )

    # specify number of tags to show
    len_clist = len(sorted_clist)
    print("[+]How many ranks do you wanna show?(ALL:%dtags): " % len_clist, end="")
    rank_num: Optional[int] = None
    while type(rank_num) is not int:
        try:
            rank_num = int(input())
        except ValueError:
            print("[!]Invalid input.: ", end="")

    # print top n
    result_lines = []
    for rank, t in enumerate(sorted_clist):
        parcentage = t[1] / len_clist * 100
        result_lines.append(
            f"#%0{len(str(len_clist))}d\t%s\n(%d tags, %.02f%s)"
            % (rank + 1, t[0], t[1], parcentage, "%")
        )
    else:
        print(
            "\n".join(result_lines),
            file=open("data/{}_{}_ranking.txt".format(target_id, p.ts), "w"),
        )
        print(
            "[[Tag ranking for {}({}, {})]]".format(
                names["name"], target_id, names["account"]
            )
        )
        print("\n".join(result_lines[0:rank_num]))


if __name__ == "__main__":
    main()
