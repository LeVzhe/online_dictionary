"""
User agent for application.
"""

import re

from django.http import HttpRequest


def get_user_agent(*, request: HttpRequest) -> str:
    """
    Context processor for Django that provides operating system
    information base on HTTP user agent. A user agent looks like (line
    break added): "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6)
    Gecko/2009020409 Iceweasel/3.0.6 (Debian-3.0.6-1)"
    """
    # Mozilla/5.0
    regex = r"(?P<application_name>\w+)/(?P<application_version>[\d\.]+)"
    regex += r" \("
    # X11
    regex += r"(?P<compatibility_flag>\w+)"
    regex += r"; "
    # U
    regex += r"(?P<version_token>[\w .]+)"
    regex += r"; "
    # Linux i686
    regex += r"(?P<platform_token>[\w .]+)"
    # anything else
    regex += r"; .*"

    user_agent = request.META.get("HTTP_USER_AGENT", "")
    result = re.match(regex, user_agent)
    if result:
        result_dict = result.groupdict()
        full_platform = result_dict["platform_token"]
        platform_values = full_platform.split(" ")
        if platform_values[0] in ("Windows", "Linux", "Mac"):
            platform = platform_values[0]
        elif platform_values[1] in ("Mac",):
            # Mac is given as "PPC Mac" or "Intel Mac"
            platform = platform_values[1]
        else:
            platform = None
    else:
        full_platform = None
        platform = None

    return f"{user_agent}, {full_platform}, {platform}"
