class SearchError(Exception):
    def __init__(self, query):
        self.error_message = f"Couldn't complete search for '{query}'."
        super().__init__(self.error_message)


class IdError(Exception):
    def __init__(self, url):
        self.error_message = f"Couldn't extract id from '{url}'."
        super().__init__(self.error_message)


class ExtractError(Exception):
    def __init__(self, url, reason, extract_type):
        self.error_message = f"Couldn't extract {extract_type} for '{url}': {reason}."
        super().__init__(self.error_message)


class DownloadError(Exception):
    def __init__(self, url, reason):
        self.error_message = f"Couldn't download '{url}': {reason}."
        super().__init__(self.error_message)


class ForbiddenError(Exception):
    def __init__(self, url):
        self.error_message = f"Couldn't download '{url}': HTTP <403> Forbidden - You might have reached a ratelimit, " \
                             f"try again later or try use_login=False."
        super().__init__(self.error_message)


class NoQueryError(Exception):
    def __init__(self):
        self.error_message = f"No query provided."
        super().__init__(self.error_message)

