"""Module for Quotex http login resource."""

from zoztex.http.navigator import Navigator


class Logout(Navigator):
    """Class for Quotex login resource."""

    base_url = "qxbroker.com"
    https_base_url = f"https://{base_url}"

    def _post(self, data=None, headers=None):
        """
        wdyt?
        """
        return self.send_request(method="POST", url=f"{self.https_base_url}/logout", data=data, headers=headers)

    def __call__(self):
        return self._post()
