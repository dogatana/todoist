import json
import re
import io
import sys
from collections import namedtuple
from itertools import groupby

Bookmark = namedtuple("Bookmark", "title url project")


def main():
    projects = read_json("projects.json")
    tasks = read_json("tasks.json")

    bookmarks = []
    for task in tasks.values():
        content = task["content"]
        title, url = search_title_url(content)
        if title == "":
            continue
        bookmarks.append(Bookmark(title, url, projects[str(task["project_id"])]))

    breakpoint()
    func = lambda b: b.project
    for k, grp in groupby(sorted(bookmarks, key=func), key=func):
        print(k, len(list(grp)))
    


def read_json(file):
    with open(file, encoding="utf-8") as fp:
        return json.load(fp)


def search_title_url(content):
    if "https://" not in content:
        return "", None

    m = re.match(r"\[(.*?)\]\((.*)\)", content)
    if m:
        return m.group(1).strip(), m.group(2).strip()

    m = re.match(r"(http[^ ]+)(.*)$", content)
    if m:
        return m.group(2).strip(), m.group(1).strip()

    m = re.match(r"(.*?)\((http[^ ]+)", content)
    if m:
        return m.group(1).strip(), m.group(2).strip()

    m = re.match("(.*?)(http[^ )）]+)", content)
    if m:
        return m.group(1).strip(), m.group(2).strip()

    return "", None


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
