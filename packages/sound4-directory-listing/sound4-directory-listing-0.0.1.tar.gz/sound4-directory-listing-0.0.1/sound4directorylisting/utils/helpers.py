#!/usr/bin/env python

"""
 * sound4-directory-listing
 * sound4-directory-listing Bug scanner for WebPentesters and Bugbounty Hunters
 *
 * @Developed By Cappricio Securities <https://cappriciosec.com>
 */

"""
import getpass
username = getpass.getuser()


def display_help():
    help_banner = f"""

👋 Hey \033[96m{username}
   \033[92m                                                                          v1.0
                               ____ __            ___                __                         __           __
   _________  __  ______  ____/ / // /       ____/ (_)_______  _____/ /_____  _______  __      / /__  ____ _/ /_______
  / ___/ __ \/ / / / __ \/ __  / // /_______/ __  / / ___/ _ \/ ___/ __/ __ \/ ___/ / / /_____/ / _ \/ __ `/ //_/ ___/
 (__  ) /_/ / /_/ / / / / /_/ /__  __/_____/ /_/ / / /  /  __/ /__/ /_/ /_/ / /  / /_/ /_____/ /  __/ /_/ / ,< (__  )
/____/\____/\__,_/_/ /_/\__,_/  /_/        \__,_/_/_/   \___/\___/\__/\____/_/   \__, /     /_/\___/\__,_/_/|_/____/
                                                                                /____/

                              \033[0mDeveloped By \x1b[31;1m\033[4mhttps://cappriciosec.com\033[0m


\x1b[31;1msound4-directory-listing : Bug scanner for WebPentesters and Bugbounty Hunters

\x1b[31;1m$ \033[92msound4-directory-listing\033[0m [option]

Usage: \033[92msound4-directory-listing\033[0m [options]

Options:
  -u, --url     URL to scan                                sound4-directory-listing -u https://target.com
  -i, --input   <filename> Read input from txt             sound4-directory-listing -i target.txt
  -o, --output  <filename> Write output in txt file        sound4-directory-listing -i target.txt -o output.txt
  -c, --chatid  Creating Telegram Notification             sound4-directory-listing --chatid yourid
  -b, --blog    To Read about sound4-directory-listing Bug sound4-directory-listing -b
  -h, --help    Help Menu
    """
    print(help_banner)


def banner():
    help_banner = f"""
    \033[94m
👋 Hey \033[96m{username}
      \033[92m                                                                      v1.0
                               ____ __            ___                __                         __           __
   _________  __  ______  ____/ / // /       ____/ (_)_______  _____/ /_____  _______  __      / /__  ____ _/ /_______
  / ___/ __ \/ / / / __ \/ __  / // /_______/ __  / / ___/ _ \/ ___/ __/ __ \/ ___/ / / /_____/ / _ \/ __ `/ //_/ ___/
 (__  ) /_/ / /_/ / / / / /_/ /__  __/_____/ /_/ / / /  /  __/ /__/ /_/ /_/ / /  / /_/ /_____/ /  __/ /_/ / ,< (__  )
/____/\____/\__,_/_/ /_/\__,_/  /_/        \__,_/_/_/   \___/\___/\__/\____/_/   \__, /     /_/\___/\__,_/_/|_/____/
                                                                                /____/

                              \033[0mDeveloped By \x1b[31;1m\033[4mhttps://cappriciosec.com\033[0m


\x1b[31;1msound4-directory-listing : Bug scanner for WebPentesters and Bugbounty Hunters

\033[0m"""
    print(help_banner)
