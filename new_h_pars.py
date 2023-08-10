import asyncio
import json
from browsers import *



class NewVita():
    city = None
    repetition = []
    browser: NewBrow

    def __init__(self, b_brow):
        self.browser = b_brow

    async def get_page_data(self, city, url_, site, task_id):
        error_c = 0
        url = url_['url']
        while True:
            try:
                self.page = await self.browser.get_page(city)
                address = []
                js = f'''() => {{return fetch("{url}").then(response => {{return response.text();}})}}'''
                fit = await asyncio.wait_for(self.page.evaluate(js), timeout=10.0)
                if '<a class="slide' in fit:
                    if '-' in url:
                        url = url.replace('-', '_')
                        js = f'''() => {{return fetch("{url}").then(response => {{return response.text();}})}}'''
                        fit = await asyncio.wait_for(self.page.evaluate(js), timeout=10.0)
                        if '<a class="slide' in fit:
                            break

                    elif '_' in url:
                        url = url.replace('_', '-')
                        js = f'''() => {{return fetch("{url}").then(response => {{return response.text();}})}}'''
                        fit = await asyncio.wait_for(self.page.evaluate(js), timeout=10.0)
                        if '<a class="slide' in fit:
                            break

                e = fit.split(r'"products": [')[1].split(r']')[0]
                res = json.loads(e)
                g_id = res['id']
                if res['price'] != "0":
                    js_city = f'''() => {{return fetch("{g_id}").then(response => {{return response.json();}})}}'''
                    main_address = await self.page.evaluate(js_city)
                    for i in main_address['TODAY_RESULT']['RESULT']:
                        main_name_g = f"{i['name']}, {i['address']}"
                        address.append(main_name_g)

                    name = res['name']
                    price = res['price']
                    print(f"{len(fit)}{url}")
                    daties = []
                    for separate_address in address:
                        daties.append(
                            {
                                'site1': site,
                                'region1': city['region'],
                                'city1': city['city'],
                                'name': name,
                                'apteka': separate_address,
                                'price': price,
                                'count': '-',
                                'dataGodn': '',
                                'task_id': task_id
                            }
                        )

                    error_c = 0

                    return daties
                else:
                    print(f"{url} not price")
                    break

            except Exception as err:
                print(err, error_c)
                if error_c > 10:
                    await self.browser.obnulen()
                    error_c = 0
                error_c += 1
                await asyncio.sleep(1)
