# ============================================
# Bulk Mod Downloader
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 2/2/23
# License: MIT
# ============================================

import argparse
import collections
import os
import requests
import sys
import time

from contextlib import contextmanager
from mediafiredl import MediafireDL as MF

collections.Callable = collections.abc.Callable

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
            
def parse_args():
    parser = argparse.ArgumentParser(
        description='Technic Parser')
    parser.add_argument('-s', '--slug', type=str, required=True, metavar="slug", help='ID for mod.')
    parser.add_argument('-r', '--repo', type=str, default="CurseForge", metavar="repo", help="Choose repo for downloading mods from.")
    parser.add_argument('-p', '--path', type=str, default=os.getcwd(), metavar="path", help="Path to place downloads. Defaults to current directory.")
    args = parser.parse_args()
    go_to_path(args, parser)
    return args


def go_to_path(args, parser):
    try:
        os.chdir(args.path)
    except:
        print(f"ERROR: Cannot go to path {args.path}!")
        parser.print_help()
        sys.exit(1)

def download_manifest(repo, slug):
    if repo == "MCArchive":
        url = "https://mcarchive.net/api/v1/mods/by_slug/" + slug
        headers = {
        'User-Agent': 'BulkModDownloader/1.0.0'
        }
    elif repo == "CurseForge":
        url = "https://api.curse.tools/v1/cf/mods/" + slug + "/files"
        headers = {
        }
    elif repo == "Modrinth":
        url = "https://api.modrinth.com/v2/project/" + slug + "/version"
        headers = {
        'User-Agent': 'BulkModDownloader/1.0.0'
        }
    else:
        print(f"ERROR: Cannot find proper repo! Hypothetically this should never be hit!")
        sys.exit(1)
    

    responce = requests.get(url, headers=headers)
    json = responce.json()
    if repo == "MCArchive":
        for modList in json["mod_versions"]:
            for modLink in modList["files"]:
                try:
                    mod_content = requests.get(modLink["archive_url"]).content
                    with open(modLink['name'], 'wb') as f:
                        f.write(mod_content)
                        print('Downloaded: {}!'.format(modLink['name']))
                except:
                    try:
                        mod_content = requests.get(modLink["direct_url"]).content
                        with open(modLink['name'], 'wb') as f:
                            f.write(mod_content)
                            print('Downloaded: {}!'.format(modLink['name']))
                    except:
                        try:
                            with suppress_stdout():
                                MF.Download(modLink["redirect_url"], os.getcwd())
                            print('Downloaded: {}!'.format(modLink['name']))
                        except:
                            pass

    elif repo == "CurseForge":
        for modLink in json["data"]:
            mod_content = requests.get(modLink["downloadUrl"]).content
            with open(modLink['fileName'], 'wb') as f:
                f.write(mod_content)
                print('Downloaded: {}!'.format(modLink['fileName']))

    elif repo == "Modrinth":
        print("================= WARNING ===================")
        print("Modrinth has a bug with downloading from its API")
        print("When the program crashes it has succesfully scraped")
        print("")
        time.sleep(2)
        for number in range(0,999999): # hack to get alsround modrinth API bug
            for modLink in json[number]["files"]:
                mod_content = requests.get(modLink["url"]).content
                with open(modLink['filename'], 'wb') as f:
                    f.write(mod_content)
                    print('Downloaded: {}!'.format(modLink['filename']))

if __name__ == "__main__":
    download_manifest( parse_args().repo, parse_args().slug)