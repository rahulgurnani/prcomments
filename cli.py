import os
import sys
import click

import git

from puller import CommentPuller


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--path', default='.', help='Path to your repository')
def main(path):
    """A tool to address your pull request comments"""
    repo = git.Repo(path)
    puller = CommentPuller(repo)
    puller.get_comments()

if __name__ == '__main__':
    main()
