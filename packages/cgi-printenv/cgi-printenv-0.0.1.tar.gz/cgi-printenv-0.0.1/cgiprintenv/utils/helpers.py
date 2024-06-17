#!/usr/bin/env python

"""
 * cgi-printenv
 * cgi-printenv Bug scanner for WebPentesters and Bugbounty Hunters
 *
 * @Developed By Cappricio Securities <https://cappriciosec.com>
 */

"""
import getpass
username = getpass.getuser()


def display_help():
    help_banner = f"""

👋 Hey \033[96m{username}
   \033[92m                                                       v1.0
              _                  _       __
  _________ _(_)     ____  _____(_)___  / /____  ____ _   __
 / ___/ __ `/ /_____/ __ \/ ___/ / __ \/ __/ _ \/ __ \ | / /
/ /__/ /_/ / /_____/ /_/ / /  / / / / / /_/  __/ / / / |/ /
\___/\__, /_/     / .___/_/  /_/_/ /_/\__/\___/_/ /_/|___/
    /____/       /_/

                              \033[0mDeveloped By \x1b[31;1m\033[4mhttps://cappriciosec.com\033[0m


\x1b[31;1mcgi-printenv : Bug scanner for WebPentesters and Bugbounty Hunters

\x1b[31;1m$ \033[92mcgi-printenv\033[0m [option]

Usage: \033[92mcgi-printenv\033[0m [options]

Options:
  -u, --url     URL to scan                                cgi-printenv -u https://target.com
  -i, --input   <filename> Read input from txt             cgi-printenv -i target.txt
  -o, --output  <filename> Write output in txt file        cgi-printenv -i target.txt -o output.txt
  -c, --chatid  Creating Telegram Notification             cgi-printenv --chatid yourid
  -b, --blog    To Read about cgi-printenv Bug             cgi-printenv -b
  -h, --help    Help Menu
    """
    print(help_banner)


def banner():
    help_banner = f"""
    \033[94m
👋 Hey \033[96m{username}
      \033[92m                                               v1.0
              _                  _       __
  _________ _(_)     ____  _____(_)___  / /____  ____ _   __
 / ___/ __ `/ /_____/ __ \/ ___/ / __ \/ __/ _ \/ __ \ | / /
/ /__/ /_/ / /_____/ /_/ / /  / / / / / /_/  __/ / / / |/ /
\___/\__, /_/     / .___/_/  /_/_/ /_/\__/\___/_/ /_/|___/
    /____/       /_/

                              \033[0mDeveloped By \x1b[31;1m\033[4mhttps://cappriciosec.com\033[0m


\x1b[31;1mcgi-printenv : Bug scanner for WebPentesters and Bugbounty Hunters

\033[0m"""
    print(help_banner)
