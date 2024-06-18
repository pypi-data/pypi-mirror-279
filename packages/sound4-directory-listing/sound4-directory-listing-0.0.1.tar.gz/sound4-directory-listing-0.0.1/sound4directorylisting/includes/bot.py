#!/usr/bin/env python

"""
 * sound4-directory-listing
 * sound4-directory-listing Bug scanner for WebPentesters and Bugbounty Hunters
 *
 * @Developed By Cappricio Securities <https://cappriciosec.com>
 */
"""
import requests
from sound4directorylisting.utils import const
from sound4directorylisting.utils import configure


def sendmessage(vul):

    data = {"Tname": "sound4-directory-listing", "chatid": configure.get_chatid(), "data": vul,
            "Blog": const.Data.blog, "bugname": const.Data.bugname, "Priority": "Medium"}

    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.put(const.Data.api, json=data, headers=headers)
    except:
        print("Bot Error")
