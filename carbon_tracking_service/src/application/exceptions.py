class SiteNotFoundException(Exception):

    def __init__(self, site: str):
        super().__init__(f"site {site} not found")
