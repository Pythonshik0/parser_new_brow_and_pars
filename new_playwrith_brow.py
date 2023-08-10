import asyncio
import random
import datetime
import json
import asyncio
import time
import logging
import asyncpg
from playwright.async_api import async_playwright
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
import random
from asyncio.exceptions import TimeoutError

class NewBrow():
    browser = None
    create_new_brow = False
    city = None
    count_req = 0
    proxe = []

    async def get_brow(self):
        if self.browser:
            return self.browser
        else:
            raise Exception("Browser don't work")

    async def obnulen(self):
        if self.browser:
            await self.browser.close()
        self.proxy = None
        self.page = None

    async def get_page(self, city):
        if self.count_req == 800:
            await self.obnulen()
            self.count_req = 0
        self.count_req += 1

        if city != self.city:
            await self.obnulen()
            self.city = city
        if self.page:
            return self.page
        else:
            if self.create_new_brow == True:
                while self.create_new_brow == True:
                    await asyncio.sleep(1)
                return self.page

            else:
                self.create_new_brow = True
                await self.create_browser(city)
                self.create_new_brow = False
                return self.page

    async def create_browser(self, city):
        while True:
            try:
                self.p = await async_playwright().start()
                url = ""
                self.my_proxy = random.choice(self.proxe)
                proxyes = self.my_proxy.replace("@", ":").split(":")
                proxy = {"server": f"{proxyes[2]}", "port": f"{proxyes[3]}"}
                new_proxy = {'server': "http://" + proxy['server'] + ":" + proxy['port'], "username": "",
                             "password": ""}
                print(new_proxy)
                self.browser = await self.p.chromium.launch(proxy=new_proxy, headless=False)
                self.context = await self.browser.new_context(
                    user_agent="")
                self.page = await self.context.new_page()
                with open("cookie_city.json", "r") as f:
                    cities = json.loads(f.read())
                    cookie = [
                        {"name": 'sec-ch-ua-platform', "value": '"Linux"', "path": "/", "domain": ""},
                        cities[city['region']][city['city']]]
                await self.browser.new_context()
                await self.context.add_cookies(cookie)
                await self.page.goto(url, timeout=60000)
                await self.page.wait_for_selector(".pointer.help-city__btn.btn.btn-large.btn-primary_one_fce")
                await self.page.click(".pointer.help-city__btn.btn.btn-large.btn-primary_one_fce")
                print('Нажал на кнопку')
                break
            except Exception as err:
                print(err)
                await self.browser.close()