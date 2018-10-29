import json
import sys
from urllib import parse
import click

import git
import keyring
import getpass
import requests
from requests.auth import HTTPBasicAuth
from requests import codes

import utils


BITBUCKET = 'bitbucket.org'
GITHUB = 'github.com'
BITBUCKET_API_URL = 'https://api.bitbucket.org/2.0'


def get_username(repo):
    return repo.config_reader("global").get_value("user", "name")

def get_password(domain, username):
    password = keyring.get_password(domain, username)
    if password is None:
        keyring.set_password(domain, username, getpass.getpass())
    password = keyring.get_password(domain, username)
    return password

class CommentPuller():
    def __init__(self, repo):
        self.repo = repo
        self.parsed_url = parse.urlparse(repo.remotes.origin.url)
        self.username = get_username(repo)
        if BITBUCKET in self.parsed_url.netloc:
            password = get_password(BITBUCKET, self.username)
            self.auth = HTTPBasicAuth(self.username, password)
        else:
            print("WIP")
            exit(1)

    def get_comments(self):
        repo_slug = self.parsed_url.path.split('.')[0]
        print(BITBUCKET_API_URL + '/repositories' + repo_slug + '/pullrequests')
        pullrequests = requests.get(BITBUCKET_API_URL 
            + '/repositories'
            + repo_slug
            + '/pullrequests', 
            auth=self.auth)
        pullrequests.raise_for_status()

        for pr in pullrequests.json()['values']:
            if self.username != pr["author"]["username"] or self.repo.active_branch.name != pr["source"]["branch"]["name"]:
                continue
            print("Pull Request : " + pr["title"])
            print(pr["state"])
            print(pr["description"])
            comments = requests.get(pr["links"]["comments"]["href"], 
                auth=self.auth)
            comments.raise_for_status()
            for comment in comments.json()["values"]:
            	# TODO: handle self comments
                comment_full = requests.get(comment["links"]["self"]["href"],
                auth=self.auth)
                comment_full.raise_for_status()
                comment_body = comment_full.json()
				username = comment_body["user"]["username"]
                content_raw = comment_body["content"]["raw"]
                if "inline" in comment_body:
                    print("Inline Comment")
                    filepath = comment_body["inline"]["path"]
                    line_no = comment_body["inline"]["to"]
                    print("In file : " + filepath)
                    print("At : " + line_no)
                    res = input("Want to r(eply), add as t(odo) or a(rchive)?") 
                    # open -a /Applications/Android\ Studio.app filepath
                print(username, " says: ", content_raw)
                res = input("Want to r(eply), add as t(odo) or a(rchive)?")