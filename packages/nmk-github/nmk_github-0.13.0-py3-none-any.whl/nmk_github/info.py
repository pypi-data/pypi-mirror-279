"""
Miscellaneous project information resolvers
"""

import re
import urllib.parse
from typing import Tuple

from nmk.model.resolver import NmkStrConfigResolver
from nmk.utils import run_with_logs

_REMOTE_PATTERN = re.compile("origin[\\t ]+(?:(?:git@)|(?:https://))github.com[:/]([^/]+)/([^.]+)(?:.git)?[\\t ]+\\(fetch\\)")


# Abstract class with common URL parsing logic
class _GithubRemoteParser(NmkStrConfigResolver):
    def get_remote(self) -> Tuple[str, str]:
        cp = run_with_logs(["git", "remote", "-v"])
        for line in cp.stdout.split("\n"):
            m = _REMOTE_PATTERN.match(line)
            if m is not None:
                return (m.group(1), m.group(2))
        raise AssertionError("Failed to parse git fetch remote URL")


class GithubUserResolver(_GithubRemoteParser):
    """
    Github user resolving logic
    """

    def get_value(self, name: str) -> str:
        """
        Gets Github user from git remote URL

        :param name: config item name
        :returns: parsed user name
        """
        user, _ = self.get_remote()
        return user


class GithubRepoResolver(_GithubRemoteParser):
    """
    Github repo resolving logic
    """

    def get_value(self, name: str) -> str:
        """
        Gets Github repo from git remote URL

        :param name: config item name
        :returns: parsed repo name
        """
        _, repo = self.get_remote()
        return repo


class GithubIssuesLabelResolver(NmkStrConfigResolver):
    """
    Github issues query optional label resolver
    """

    def get_value(self, name: str, label: str) -> str:
        """
        If **githubIssuesLabel** is set, provides additional query parameter for it

        :param name: config item name
        :param label: provided label, if any
        :returns: issues query additional parameter for provided label
        """

        # Check for optional label
        return "+" + urllib.parse.quote(f"label:{label}") if len(label) else ""
