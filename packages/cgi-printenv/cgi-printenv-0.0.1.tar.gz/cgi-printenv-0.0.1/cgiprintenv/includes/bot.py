#!/usr/bin/env python

"""
 * cgi-printenv
 * cgi-printenv Bug scanner for WebPentesters and Bugbounty Hunters
 *
 * @Developed By Cappricio Securities <https://cappriciosec.com>
 */
"""
import requests
from cgiprintenv.utils import const
from cgiprintenv.utils import configure


def sendmessage(vul):

    data = {"Tname": "cgi-printenv", "chatid": configure.get_chatid(), "data": vul,
            "Blog": const.Data.blog, "bugname": const.Data.bugname, "Priority": "Medium"}

    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.put(const.Data.api, json=data, headers=headers)
    except:
        print("Bot Error")
