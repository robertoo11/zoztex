import re
import json
import shutil
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Tuple, Any
from zoztex.exceptions import QuotexAuthError
from zoztex.utils.playwright_install import install
from playwright.async_api import Playwright, async_playwright
from playwright_stealth import stealth_async

class Browser(object):
    email = None
    password = None

    base_url = "qxbroker.com"
    https_base_url = f"https://{base_url}"

    def __init__(self, api):
        self.api = api

    async def run(self, playwright: Playwright) -> Tuple[Any, str]:
        browser = await playwright.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        await page.goto(f"{self.https_base_url}/pt/sign-in")
        if page.url != f"{self.https_base_url}/pt/trade":
            await page.get_by_role("textbox", name="E-mail").click()
            await page.get_by_role("textbox", name="E-mail").fill(self.email)
            await page.get_by_role("textbox", name="Senha").click()
            await page.get_by_role("textbox", name="Senha").fill(self.password)
            await page.get_by_role("button", name="Entrar").click()
            async with page.expect_navigation():
                await page.wait_for_timeout(5000)
                soup = BeautifulSoup(await page.content(), "html.parser")
                if "Insira o código PIN que acabamos de enviar para o seu e-mail" in soup.get_text():
                    code = input("Enter the PIN code we just sent to your email: ")
                    """await page.evaluate(
                        f'() => {{ document.querySelector("input[name=\\"code\\"]").value = {int(code)}; }}')"""
                    try:
                        await page.get_by_placeholder("Digite o código de 6 dígitos...").click()
                        await page.get_by_placeholder("Digite o código de 6 dígitos...").fill(code)
                        await page.get_by_role("button", name="Entrar").click()
                    except:
                        await page.get_by_placeholder("Digite o código de 6 dígitos...").click()
                        await page.get_by_placeholder("Digite o código de 6 dígitos...").fill(code)
                        await page.get_by_role("button", name="Entrar").click()
        await page.wait_for_timeout(5000)
        cookies = await context.cookies()
        self.api.cookies = cookies
        source = await page.content()
        soup = BeautifulSoup(source, "html.parser")
        user_agent = await page.evaluate("() => navigator.userAgent;")
        self.api.user_agent = user_agent
        try:
            script = soup.find_all("script", {"type": "text/javascript"})[1].get_text()
        except Exception as exc:
            raise QuotexAuthError("incorrect username or password") from exc
        match = re.sub("window.settings = ", "", script.strip().replace(";", ""))

        ssid = json.loads(match).get("token")
        output_file = Path(".session.json")
        output_file.parent.mkdir(exist_ok=True, parents=True)
        cookiejar = requests.utils.cookiejar_from_dict({c["name"]: c["value"] for c in cookies})
        cookie_string = "; ".join([f"{c.name}={c.value}" for c in cookiejar])
        output_file.write_text(json.dumps({"cookies": cookie_string, "ssid": ssid, "user_agent": user_agent}, indent=4))
        await context.close()
        await browser.close()

        return ssid, cookie_string

    async def get_cookies_and_ssid(self) -> Tuple[Any, str]:
        async with async_playwright() as playwright:
            browser = playwright.firefox
            if not shutil.which(browser.name):
                install(browser, with_deps=True)
            return await self.run(playwright)