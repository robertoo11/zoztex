from zoztex.http.qxbroker import Browser


class Login(Browser):
    """Class for Quotex login resource."""

    url = ""
    ssid = None
    cookies = None
    base_url = "qxbroker.com"
    https_base_url = f"https://{base_url}"

    async def __call__(self, email, password):
        """
      D4rk3sst, no explanations
        """

        self.email = email
        self.password = password

        self.ssid, self.cookies = await self.get_cookies_and_ssid()
        return self.ssid, self.cookies
