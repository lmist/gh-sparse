from github import Auth, Github
from dataclasses import dataclass


class Gh():
    def __init__(self, c):
        self.c = c
        self.auth = Auth.Token(c.github_secret.get_secret_value())
        self.g = Github(auth=self.auth)

    def get_myrepos(self):
        me = self.g.get_user()

        ret = []
        for repo in me.get_repos():
            ret.append(repo)
        return ret


    def get_repo_contents(self):
        usr = self.c.gh.user
        repo_name = self.c.gh.repo

        repo = self.g.get_repo(f"{usr}/{repo_name}")

        contents = repo.get_contents("")
        alist = [cf for cf in contents]
        return alist