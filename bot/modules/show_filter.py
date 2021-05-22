import re


def show_filter(choices, shows, quality):
    new = set()
    for choice in choices:
        match = r'\b' + choice
        for ep in shows:
            if re.search(match, ep.lower()) and quality in ep:
                new.add(ep)
    return new