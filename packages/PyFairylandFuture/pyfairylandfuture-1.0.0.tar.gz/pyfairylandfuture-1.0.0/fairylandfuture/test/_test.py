# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-06-01 下午11:59:09 UTC+8
"""


def load_logo():
    with open("../conf/logo", "r", encoding="UTF-8") as logo_file:
        logo_text = logo_file.read()
    return logo_text


if __name__ == "__main__":
    print(load_logo())
