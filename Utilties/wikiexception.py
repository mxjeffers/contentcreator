exception_list = {"new york": "New_York_(state)",
                  "georgia": "Georgia_(U.S._state)"
                  }


def find_exception(keyword):
    if keyword.lower() in exception_list:
        keyword = exception_list[keyword]
    return keyword
