from locust import FastHttpUser, run_single_user, task


class apple_buy_a_mac(FastHttpUser):
    host = "https://secure2.store.apple.com"

    @task
    def t(self):
        with self.client.request(
            "GET",
            "/shop/sign_in?c=aHR0cHM6Ly93d3cuYXBwbGUuY29tL3Nob3AvYmFnfDFhb3NjY2QxZjg4ZGZjYjY4YWRhNWZmMmY5ZTY5YWMzNjE0OTYyMjZlOWMz&o=O01HTjYz&r=SXYD4UDAPXU7P7KXF&s=aHR0cHM6Ly9zZWN1cmUyLnN0b3JlLmFwcGxlLmNvbS9zaG9wL2NoZWNrb3V0L3N0YXJ0P3BsdG49QTZGNDNFMER8MWFvczg4MjgzMjY3MzJkNWEzNjIxMTQxMDE0ZTU4NmZiNTY5MjEzZGEyY2M&t=SXYD4UDAPXU7P7KXF&up=t",
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Cookie": "geo=IT; ccl=Kdn52WwZ2zpMXc5ABjC73A==; check=true; mbox=session#bb7cc510c65f4f4eaba6b8ef81b5547f#1606566556; s_fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A; s_cc=true; s_vi=[CS]v1|2FE11DAC8515EE05-60000A946BBC0874[CE]; dssid2=0deece74-9857-4594-b36e-273d7f7dec11; dssf=1; as_pcts=JL+lxkMf1kjWAQTYt2GskuGVDw8znwk71-I-NVSCf8uZS0oApzy36fX3ooRv-qe7ZdyyZyWpPgHke; as_dc=nc; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; pxro=1; xp_ci=3z18Z3F8zC6gz55bzBPQzTOhDqgGy; as_xs=flc=; as_xsm=1&TsS1k4znjEvnGjBoAe_vvw; s_sq=%5B%5BB%5D%5D",
                "Host": "secure2.store.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://www.apple.com/",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-site",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/shop/buy-mac/macbook-air?proceed=proceed&bfil=2&product=MGN63LL%2FA&step=attach",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/shop/bag",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/shop/buy-mac/macbook-air/space-gray-apple-m1-chip-with-8%E2%80%91core-cpu-and-7%E2%80%91core-gpu-256gb?option.memory__dummy_z124=065-C99M&option.hard_drivesolid_state_drive__dummy_z124=065-C99Q&option.keyboard_and_documentation_z124=065-C9DG&option.sw_final_cut_pro_x_z124=065-C171&option.sw_logic_pro_x_z124=065-C172&add-to-cart=add-to-cart&product=MGN63LL%2FA&step=config&bfil=2&atbtoken=bd24f42caddadc789d311b27afde1f05fc9262f2",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/shop/buy-mac/macbook-air?bfil=2&product=MGN63LL/A&step=attach",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/shop/buy-mac/macbook-air?proceed=proceed&product=MGN63LL%2FA&step=select",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/shop/buy-mac/macbook-air?product=MGN63LL/A&step=config",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/shop/buy-mac/macbook-air/space-gray-apple-m1-chip-with-8%E2%80%91core-cpu-and-7%E2%80%91core-gpu-256gb",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/us/shop/goto/buy_mac/macbook_air",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/us/shop/go/buy_mac/macbook_air",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/shop/buy-mac/macbook-air",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/macbook-air/",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/mac/",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://securemvt.apple.com/m2/apple/mbox/json?mbox=target-global-mbox&mboxSession=bb7cc510c65f4f4eaba6b8ef81b5547f&mboxPC=&mboxPage=28a825d8368e433fb1840aed16581b46&mboxRid=e1e5810447114e1ea0db6ddfae46a383&mboxVersion=1.5.0&mboxCount=1&mboxTime=1606568330064&mboxHost=www.apple.com&mboxURL=https%3A%2F%2Fwww.apple.com%2F&mboxReferrer=&browserHeight=630&browserWidth=1420&browserTimeOffset=60&screenHeight=1080&screenWidth=1920&colorDepth=24&devicePixelRatio=1&screenOrientation=landscape&webGLRenderer=Intel%20HD%20Graphics%205000%20OpenGL%20Engine",
            headers={
                "Referer": "https://www.apple.com/",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/ac/localeswitcher/3/it_IT/content/localeswitcher.json",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/search-services/suggestions/defaultlinks/?src=globalnav&locale=en_US",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/favicon.ico",
            headers={
                "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/ac/localeswitcher/3/it_IT/content/localeswitcher.json",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/search-services/suggestions/defaultlinks/?src=globalnav&locale=en_US",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/us/shop/mcm/product-price?parts=MACBOOKAIR_M1,MBP2020_13_M1,MACMINI_M1,MBP2019_16",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/favicon.ico",
            headers={
                "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/ac/localeswitcher/3/it_IT/content/localeswitcher.json",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/search-services/suggestions/defaultlinks/?src=globalnav&locale=en_US",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/us/shop/mcm/product-price?parts=MACBOOKAIR_M1,MBP2020_13_M1,MBP2019_16",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/us/shop/mcm/tradein-credit?ids=6822",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/favicon.ico",
            headers={
                "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/bag/status?apikey=SJHJUH4YFCTTPD4F4",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/delivery-message?parts.0=MGN63LL%2FA&parts.1=MGND3LL%2FA&parts.2=MGN93LL%2FA&mt=regular&_=1606564751169",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/delivery-message?parts.0=MGN73LL%2FA&parts.1=MGNE3LL%2FA&parts.2=MGNA3LL%2FA&mt=regular&_=1606564751170",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/retail/pickup-message?parts.0=MGN63LL%2FA&parts.1=MGND3LL%2FA&parts.2=MGN93LL%2FA",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/retail/pickup-message?parts.0=MGN73LL%2FA&parts.1=MGNE3LL%2FA&parts.2=MGNA3LL%2FA",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/updateFinanceSummary?node=home/shop_mac/family/macbook_air&parts.0=MGN63LL%2FA&parts.1=MGND3LL%2FA&parts.2=MGN93LL%2FA&parts.3=MGN73LL%2FA&parts.4=MGNE3LL%2FA&parts.5=MGNA3LL%2FA&tia=&bfil=2",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.client.request(
            "POST",
            "https://securemetrics.apple.com/b/ss/applestoreww,appleglobal/1/JS-2.17.0/s55089049129067?AQB=1&ndh=1&pf=1&t=28%2F10%2F2020%2012%3A59%3A13%206%20-60&fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A&ce=UTF-8&pageName=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fselect&g=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-air&r=https%3A%2F%2Fwww.apple.com%2Fmacbook-air%2F&cc=USD&server=as-13.5.0&events=event210%3D1.07%2Cevent246&v3=AOS%3A%20US%20Consumer&c4=D%3Dg&v4=D%3DpageName&c5=macintel&c8=AOS%3A%20Mac&c14=macbook%20air%20-%20overview%20%28us%29&v14=en-us&c19=AOS%3A%20US%20Consumer%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fselect&v19=D%3Dc19&c20=AOS%3A%20US%20Consumer&v35=web%20apply%7Cdenied%7Cpre%3Anot%20safari&c40=10078&v49=D%3Dr&v54=D%3Dg&v94=1.07&v97=s.tl-o&pe=lnk_o&pev2=Step%201&s=1920x1080&c=24&j=1.6&v=N&k=Y&bw=1420&bh=630&lrt=724&AQE=1",
            headers={
                "Content-Type": "text/plain;charset=UTF-8",
                "Referer": "https://www.apple.com/",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/search-services/suggestions/defaultlinks/?src=globalnav&locale=en_US",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.client.request(
            "POST",
            "https://securemetrics.apple.com/b/ss/applestoreww,appleglobal/1/JS-2.17.0/s57395114027206?AQB=1&ndh=1&pf=1&t=28%2F10%2F2020%2012%3A59%3A13%206%20-60&fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A&ce=UTF-8&pageName=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fselect&g=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-air&r=https%3A%2F%2Fwww.apple.com%2Fmacbook-air%2F&cc=USD&server=as-13.5.0&events=event33%2Cevent210%3D1.39%2Cevent246&v3=AOS%3A%20US%20Consumer&c4=D%3Dg&v4=D%3DpageName&c5=macintel&c8=AOS%3A%20Mac&c14=macbook%20air%20-%20overview%20%28us%29&v14=en-us&c19=AOS%3A%20US%20Consumer%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fselect&v19=D%3Dc19&c20=AOS%3A%20US%20Consumer&c37=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fselect%7Ccold%20start&c40=10078&v49=D%3Dr&v54=D%3Dg&v94=1.39&v97=s.tl-o&pe=lnk_o&pev2=Cold&s=1920x1080&c=24&j=1.6&v=N&k=Y&bw=1420&bh=630&lrt=1&AQE=1",
            headers={
                "Content-Type": "text/plain;charset=UTF-8",
                "Referer": "https://www.apple.com/",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/favicon.ico",
            headers={
                "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://store.storeimages.cdn-apple.com/4982/store.apple.com/shop/rs-external/rel/external.js",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Host": "store.storeimages.cdn-apple.com",
                "Origin": "https://www.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://www.apple.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "POST",
            "https://xp.apple.com/report/2/xp_aos_clientperf",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Length": "2450",
                "Cookie": "geo=IT; ccl=Kdn52WwZ2zpMXc5ABjC73A==; check=true; mbox=session#bb7cc510c65f4f4eaba6b8ef81b5547f#1606566556; s_fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A; s_cc=true; s_vi=[CS]v1|2FE11DAC8515EE05-60000A946BBC0874[CE]; dssid2=0deece74-9857-4594-b36e-273d7f7dec11; dssf=1; as_pcts=JL+lxkMf1kjWAQTYt2GskuGVDw8znwk71-I-NVSCf8uZS0oApzy36fX3ooRv-qe7ZdyyZyWpPgHke; as_dc=nc; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; s_sq=%5B%5BB%5D%5D; pxro=1",
                "Host": "xp.apple.com",
                "Origin": "https://www.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://www.apple.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            json={
                "deliveryVersion": "1.0",
                "postTime": 1606564754563,
                "events": [
                    {
                        "app": "com.apple.www.Store",
                        "eventType": "pageview",
                        "postTime": 1606564754562,
                        "host": "www.apple.com",
                        "pageHostname": "www.apple.com",
                        "pagePathname": "/shop/buy-mac/macbook-air",
                        "pageUrl": "https://www.apple.com/shop/buy-mac/macbook-air?<query>",
                        "pageViewId": "adc83313-f3d2-4cb3-9aa0-e24b5bc75806",
                        "sessionStartTS": 1606564751090,
                        "triggeredBy": "load",
                        "name": "https://www.apple.com/shop/buy-mac/macbook-air",
                        "entryType": "navigation",
                        "startTime": 0,
                        "duration": 4234.415000013541,
                        "initiatorType": "navigation",
                        "nextHopProtocol": "h2",
                        "workerStart": 0,
                        "redirectStart": 4.039999999804422,
                        "redirectEnd": 390.1049999985844,
                        "fetchStart": 390.1049999985844,
                        "domainLookupStart": 390.1049999985844,
                        "domainLookupEnd": 390.1049999985844,
                        "connectStart": 390.1049999985844,
                        "connectEnd": 390.1049999985844,
                        "secureConnectionStart": 390.1049999985844,
                        "requestStart": 396.3950000179466,
                        "responseStart": 622.4349999974947,
                        "responseEnd": 744.2250000021886,
                        "transferSize": 40033,
                        "encodedBodySize": 37868,
                        "decodedBodySize": 365519,
                        "serverTiming": [],
                        "workerTiming": [],
                        "unloadEventStart": 635.1700000232086,
                        "unloadEventEnd": 635.1700000232086,
                        "domInteractive": 2291.170000011334,
                        "domContentLoadedEventStart": 2291.3249999983236,
                        "domContentLoadedEventEnd": 3387.9950000264216,
                        "domComplete": 4211.800000019139,
                        "loadEventStart": 4211.820000025909,
                        "loadEventEnd": 4234.415000013541,
                        "type": "navigate",
                        "redirectCount": 2,
                        "NavigationTimingLevel": 2,
                        "networkDownlink": 10,
                        "networkEffectiveType": "4g",
                        "networkRtt": 50,
                        "imageCountOnLoad": 31,
                        "referer": "https://www.apple.com/macbook-air/?<query>",
                        "support": {"subtleCrypto": True},
                        "asDc": "nc",
                        "audit": {
                            "telemetry": {"version": ["2.18.9"]},
                            "echo": {"version": ["2.0.6"]},
                            "recon": {"version": ["undef"]},
                            "jquery": {"version": ["1.11.3"]},
                            "can": {"version": ["2.3.29"]},
                        },
                        "cookies": [
                            "geo",
                            "ccl",
                            "check",
                            "mbox",
                            "s_fid",
                            "s_cc",
                            "s_vi",
                            "as_dc",
                            "as_sfa",
                            "s_sq",
                            "pxro",
                        ],
                        "crypto": {
                            "exists": True,
                            "passed": True,
                            "algorithm": "RSA-OAEP",
                            "encryptTime": 496.5249999950174,
                            "decryptTime": 308.4649999800604,
                        },
                        "pageId": "AOS: home/shop_mac/family/macbook_air/select",
                        "pageShopPath": "/buy-mac/macbook-air",
                        "pixelRatio": 1,
                        "pluginCount": 4,
                        "pxro": "1",
                        "rsNames": ["rs-external", "rs-mac"],
                        "screenHeight": 1080,
                        "screenWidth": 1920,
                        "scripts": 2,
                        "styles": 8,
                        "validPageUrl": True,
                        "windowInnerHeight": 630,
                        "windowInnerWidth": 1420,
                        "windowOrientation": 0,
                        "windowOuterHeight": 1077,
                        "windowOuterWidth": 1420,
                        "environment": "",
                        "sf": "us",
                        "segment": "Consumer",
                        "locale": "en-us",
                    }
                ],
            },
        ) as resp:
            pass
        with self.client.request(
            "POST",
            "https://securemetrics.apple.com/b/ss/applestoreww,appleglobal/1/JS-2.17.0/s56893829888064?AQB=1&ndh=1&pf=1&t=28%2F10%2F2020%2012%3A59%3A19%206%20-60&fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A&ce=UTF-8&pageName=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fselect&g=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-air&r=https%3A%2F%2Fwww.apple.com%2Fmacbook-air%2F&cc=USD&server=as-13.5.0&events=event210%3D7.01%2Cevent246%2Cevent500&v3=AOS%3A%20US%20Consumer&c4=D%3Dg&v4=D%3DpageName&c5=macintel&v6=D%3DpageName%2B%22%7C%7C%7CStep%201%20-%20Select%20Button%7Cselected%22&c8=AOS%3A%20Mac&c14=macbook%20air%20-%20overview%20%28us%29&v14=en-us&c19=AOS%3A%20US%20Consumer%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fselect&v19=D%3Dc19&c20=AOS%3A%20US%20Consumer&c40=10078&v49=D%3Dr&v54=D%3Dg&v94=7.01&v97=s.tl-o&pe=lnk_o&pev2=undefined%7CStep%201%20-%20Select%20Button%7Cselected&c.&a.&activitymap.&page=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fselect&link=select%20apple%20m1%20chip%20with%208core%20cpu%20and%207core%20gpu%20%7C%20no%20href%20%7C%20body&region=body&pageIDType=1&.activitymap&.a&.c&pid=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fselect&pidt=1&oid=proceed&oidt=3&ot=SUBMIT&s=1920x1080&c=24&j=1.6&v=N&k=Y&bw=1420&bh=630&lrt=91&AQE=1",
            headers={
                "Content-Type": "text/plain;charset=UTF-8",
                "Referer": "https://www.apple.com/",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/delivery-message?parts.0=MGN63LL%2FA&option.0=065-C99M%2C065-C99Q%2C065-C9DG%2C065-C171%2C065-C172&mt=regular&_=1606564760188",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.client.request(
            "POST",
            "https://securemetrics.apple.com/b/ss/applestoreww,appleglobal/1/JS-2.17.0/s54378695892321?AQB=1&ndh=1&pf=1&t=28%2F10%2F2020%2012%3A59%3A21%206%20-60&fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A&ce=UTF-8&pageName=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fconfig&g=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-air%2Fspace-gray-apple-m1-chip-with-8%25E2%2580%2591core-cpu-and-7%25E2%2580%2591core-gpu-256gb%23&r=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-air&cc=USD&server=as-13.5.0&events=event210%3D0.96%2Cevent246&v3=AOS%3A%20US%20Consumer&c4=D%3Dg&v4=D%3DpageName&c5=macintel&c8=AOS%3A%20Mac&c14=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fselect&v14=en-us&c19=AOS%3A%20US%20Consumer%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fconfig&v19=D%3Dc19&c20=AOS%3A%20US%20Consumer&v35=web%20apply%7Cdenied%7Cpre%3Anot%20safari&c40=10078&v49=D%3Dr&v54=D%3Dg&v94=0.96&v97=s.tl-o&pe=lnk_o&pev2=Step%201&s=1920x1080&c=24&j=1.6&v=N&k=Y&bw=1420&bh=630&lrt=598&AQE=1",
            headers={
                "Content-Type": "text/plain;charset=UTF-8",
                "Referer": "https://www.apple.com/",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/search-services/suggestions/defaultlinks/?src=globalnav&locale=en_US",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/retail/pickup-message?parts.0=MGN63LL%2FA&option.0=065-C99M%2C065-C99Q%2C065-C9DG%2C065-C171%2C065-C172",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/configUpdate/MGN63LL/A?node=home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fconfig&option.memory__dummy_z124=065-C99M&option.hard_drivesolid_state_drive__dummy_z124=065-C99Q&option.keyboard_and_documentation_z124=065-C9DG&option.sw_final_cut_pro_x_z124=065-C171&option.sw_logic_pro_x_z124=065-C172&product=MGN63LL%2FA&step=config&bfil=2",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.client.request(
            "POST",
            "https://securemetrics.apple.com/b/ss/applestoreww,appleglobal/1/JS-2.17.0/s5719408662668?AQB=1&ndh=1&pf=1&t=28%2F10%2F2020%2012%3A59%3A22%206%20-60&fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A&ce=UTF-8&pageName=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fconfig&g=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-air%2Fspace-gray-apple-m1-chip-with-8%25E2%2580%2591core-cpu-and-7%25E2%2580%2591core-gpu-256gb%23&r=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-air&cc=USD&server=as-13.5.0&events=event33%2Cevent210%3D1.33%2Cevent246&v3=AOS%3A%20US%20Consumer&c4=D%3Dg&v4=D%3DpageName&c5=macintel&c8=AOS%3A%20Mac&c14=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fselect&v14=en-us&c19=AOS%3A%20US%20Consumer%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fconfig&v19=D%3Dc19&c20=AOS%3A%20US%20Consumer&c37=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fconfig%7Ccold%20start&c40=10078&v49=D%3Dr&v54=D%3Dg&v94=1.33&v97=s.tl-o&pe=lnk_o&pev2=Cold&s=1920x1080&c=24&j=1.6&v=N&k=Y&bw=1420&bh=630&lrt=1&AQE=1",
            headers={
                "Content-Type": "text/plain;charset=UTF-8",
                "Referer": "https://www.apple.com/",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/delivery-message?parts.0=MGN63LL%2FA&option.0=065-C99J%2C065-C99M%2C065-C99Q%2C065-C9CL%2C065-C9DG%2C065-C9CK%2C065-C9CH%2C065-C9CJ%2C065-C171%2C065-C172&mt=regular&_=1606564760189",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/retail/pickup-message?parts.0=MGN63LL%2FA&option.0=065-C99J%2C065-C99M%2C065-C99Q%2C065-C9CL%2C065-C9DG%2C065-C9CK%2C065-C9CH%2C065-C9CJ%2C065-C171%2C065-C172",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/favicon.ico",
            headers={
                "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://store.storeimages.cdn-apple.com/4982/store.apple.com/shop/rs-external/rel/external.js",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Host": "store.storeimages.cdn-apple.com",
                "Origin": "https://www.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://www.apple.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "POST",
            "https://xp.apple.com/report/2/xp_aos_clientperf",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Length": "2794",
                "Cookie": "geo=IT; ccl=Kdn52WwZ2zpMXc5ABjC73A==; check=true; mbox=session#bb7cc510c65f4f4eaba6b8ef81b5547f#1606566556; s_fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A; s_cc=true; s_vi=[CS]v1|2FE11DAC8515EE05-60000A946BBC0874[CE]; dssid2=0deece74-9857-4594-b36e-273d7f7dec11; dssf=1; as_pcts=JL+lxkMf1kjWAQTYt2GskuGVDw8znwk71-I-NVSCf8uZS0oApzy36fX3ooRv-qe7ZdyyZyWpPgHke; as_dc=nc; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; pxro=1; xp_ci=3z18Z3F8zC6gz55bzBPQzTOhDqgGy; xp_aci=4z8hxmMMiACdfEG13LyJHUIH; s_sq=%5B%5BB%5D%5D",
                "Host": "xp.apple.com",
                "Origin": "https://www.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://www.apple.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            json={
                "deliveryVersion": "1.0",
                "postTime": 1606564763281,
                "events": [
                    {
                        "app": "com.apple.www.Store",
                        "eventType": "pageview",
                        "postTime": 1606564763279,
                        "host": "www.apple.com",
                        "pageHostname": "www.apple.com",
                        "pagePathname": "/shop/buy-mac/macbook-air/space-gray-apple-m1-chip-with-8%E2%80%91core-cpu-and-7%E2%80%91core-gpu-256gb",
                        "pageUrl": "https://www.apple.com/shop/buy-mac/macbook-air/space-gray-apple-m1-chip-with-8%E2%80%91core-cpu-and-7%E2%80%91core-gpu-256gb?<query>",
                        "pageViewId": "7f68746a-867e-43b6-9f85-780a8d15bbf4",
                        "sessionStartTS": "1606564751090",
                        "triggeredBy": "load",
                        "name": "https://www.apple.com/shop/buy-mac/macbook-air/space-gray-apple-m1-chip-with-8%E2%80%91core-cpu-and-7%E2%80%91core-gpu-256gb#",
                        "entryType": "navigation",
                        "startTime": 0,
                        "duration": 3625.1399999891873,
                        "initiatorType": "navigation",
                        "nextHopProtocol": "h2",
                        "workerStart": 0,
                        "redirectStart": 7.3549999797251076,
                        "redirectEnd": 397.7549999835901,
                        "fetchStart": 397.7549999835901,
                        "domainLookupStart": 397.7549999835901,
                        "domainLookupEnd": 397.7549999835901,
                        "connectStart": 397.7549999835901,
                        "connectEnd": 397.7549999835901,
                        "secureConnectionStart": 397.7549999835901,
                        "requestStart": 403.0999999959022,
                        "responseStart": 570.7099999999627,
                        "responseEnd": 575.23499999661,
                        "transferSize": 47494,
                        "encodedBodySize": 45248,
                        "decodedBodySize": 362315,
                        "serverTiming": [],
                        "workerTiming": [],
                        "unloadEventStart": 582.525000005262,
                        "unloadEventEnd": 582.605000003241,
                        "domInteractive": 1824.1399999824353,
                        "domContentLoadedEventStart": 1824.304999987362,
                        "domContentLoadedEventEnd": 2800.004999997327,
                        "domComplete": 3624.1750000044703,
                        "loadEventStart": 3624.199999991106,
                        "loadEventEnd": 3625.1399999891873,
                        "type": "navigate",
                        "redirectCount": 2,
                        "NavigationTimingLevel": 2,
                        "networkDownlink": 10,
                        "networkEffectiveType": "4g",
                        "networkRtt": 50,
                        "imageCountOnLoad": 25,
                        "referer": "https://www.apple.com/shop/buy-mac/macbook-air?<query>",
                        "support": {"subtleCrypto": True},
                        "asDc": "nc",
                        "audit": {
                            "telemetry": {"version": ["2.18.9"]},
                            "echo": {"version": ["2.0.6"]},
                            "recon": {"version": ["undef"]},
                            "jquery": {"version": ["1.11.3"]},
                            "can": {"version": ["2.3.29"]},
                        },
                        "cookies": [
                            "geo",
                            "ccl",
                            "check",
                            "mbox",
                            "s_fid",
                            "s_cc",
                            "s_vi",
                            "as_dc",
                            "as_sfa",
                            "pxro",
                            "xp_ci",
                            "s_sq",
                            "as_atb",
                        ],
                        "crypto": {
                            "exists": True,
                            "passed": True,
                            "algorithm": "RSA-OAEP",
                            "encryptTime": 379.9099999887403,
                            "decryptTime": 256.7949999938719,
                        },
                        "pageId": "AOS: home/shop_mac/family/macbook_air/config",
                        "pageShopPath": "/buy-mac/macbook-air/space-gray-apple-m1-chip-with-8%E2%80%91core-cpu-and-7%E2%80%91core-gpu-256gb#",
                        "pixelRatio": 1,
                        "pluginCount": 4,
                        "pxro": "1",
                        "rsNames": ["rs-external", "rs-mac"],
                        "screenHeight": 1080,
                        "screenWidth": 1920,
                        "scripts": 2,
                        "styles": 6,
                        "validPageUrl": True,
                        "windowInnerHeight": 630,
                        "windowInnerWidth": 1420,
                        "windowOrientation": 0,
                        "windowOuterHeight": 1077,
                        "windowOuterWidth": 1420,
                        "environment": "",
                        "sf": "us",
                        "segment": "Consumer",
                        "locale": "en-us",
                    }
                ],
            },
        ) as resp:
            pass
        with self.client.request(
            "POST",
            "https://securemetrics.apple.com/b/ss/applestoreww,appleglobal/1/JS-2.17.0/s5737338969557?AQB=1&ndh=1&pf=1&t=28%2F10%2F2020%2012%3A59%3A24%206%20-60&fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A&ce=UTF-8&pageName=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fconfig&g=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-air%2Fspace-gray-apple-m1-chip-with-8%25E2%2580%2591core-cpu-and-7%25E2%2580%2591core-gpu-256gb%23&r=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-air&cc=USD&server=as-13.5.0&events=scAdd%2Cevent210%3D3.37%2Cevent246%2Cevent500&products=macbook_air%3BMGN63%3B1%3B999.00%3B%3B&v3=AOS%3A%20US%20Consumer&c4=D%3Dg&v4=D%3DpageName&c5=macintel&v5=D%3DpageName%2B%22%7C%7CCTO%7CAdd%20to%20Bag%22&c8=AOS%3A%20Mac&c14=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fselect&v14=en-us&c19=AOS%3A%20US%20Consumer%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fconfig&v19=D%3Dc19&c20=AOS%3A%20US%20Consumer&c40=10078&v49=D%3Dr&v54=D%3Dg&v94=3.37&v97=s.tl-o&pe=lnk_o&pev2=CTO&c.&a.&activitymap.&page=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fconfig&link=add%20to%20bag%20%28inner%20text%29%20%7C%20no%20href%20%7C%20body&region=body&pageIDType=1&.activitymap&.a&.c&pid=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fconfig&pidt=1&oid=add-to-cart&oidt=3&ot=SUBMIT&s=1920x1080&c=24&j=1.6&v=N&k=Y&bw=1420&bh=630&lrt=62&AQE=1",
            headers={
                "Content-Type": "text/plain;charset=UTF-8",
                "Referer": "https://www.apple.com/",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/bag/status?apikey=SJHJUH4YFCTTPD4F4",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/buyFlowAttachConfigProductSummary/MGN63LL/A?node=home/shop_mac/family/macbook_air&step=attach&bfil=2&product=MGN63LL%2FA&step=attach&option.sw_logic_pro_x_z124=065-C172&option.keyboard_and_documentation_z124=065-C9DG&option.memory__dummy_z124=065-C99M&complete=true&option.hard_drivesolid_state_drive__dummy_z124=065-C99Q&option.sw_final_cut_pro_x_z124=065-C171&proceed=proceed",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/engrave/json?product=MWP22AM%2FA",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/engrave/json?product=MV7N2AM%2FA",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/engrave/json?product=MRXJ2AM%2FA",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/delivery-message?parts.0=S6124LL%2FA&parts.1=MJ1M2AM%2FA&parts.2=MX0K2AM%2FA&mt=compact&_=1606564765355",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/delivery-message?parts.0=MLA02LL%2FA&parts.1=MUF82AM%2FA&parts.2=MRQM2ZM%2FA&mt=compact&_=1606564765356",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/delivery-message?parts.0=MUFG2AM%2FA&parts.1=MQ4H2AM%2FA&parts.2=MWP22AM%2FA&mt=compact&_=1606564765357",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/delivery-message?parts.0=MV7N2AM%2FA&parts.1=MRXJ2AM%2FA&parts.2=MMEL2AM%2FA&mt=compact&_=1606564765358",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/delivery-message?parts.0=HMUA2VC%2FA&parts.1=HMUB2LL%2FA&parts.2=MK122LL%2FA&mt=compact&_=1606564765359",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/delivery-message?parts.0=HMU22ZM%2FA&parts.1=HPA02ZM%2FA&mt=compact&_=1606564765360",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/retail/pickup-message?parts.0=S6124LL%2FA&parts.1=MJ1M2AM%2FA&parts.2=MX0K2AM%2FA&little=true",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/retail/pickup-message?parts.0=MLA02LL%2FA&parts.1=MUF82AM%2FA&parts.2=MRQM2ZM%2FA&little=true",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/retail/pickup-message?parts.0=MUFG2AM%2FA&parts.1=MQ4H2AM%2FA&parts.2=MWP22AM%2FA&little=true",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/retail/pickup-message?parts.0=MV7N2AM%2FA&parts.1=MRXJ2AM%2FA&parts.2=MMEL2AM%2FA&little=true",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/retail/pickup-message?parts.0=HMUA2VC%2FA&parts.1=HMUB2LL%2FA&parts.2=MK122LL%2FA&little=true",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/retail/pickup-message?parts.0=HMU22ZM%2FA&parts.1=HPA02ZM%2FA&little=true",
            headers={
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/search-services/suggestions/defaultlinks/?src=globalnav&locale=en_US",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.client.request(
            "POST",
            "https://securemetrics.apple.com/b/ss/applestoreww,appleglobal/1/JS-2.17.0/s52456596436101?AQB=1&ndh=1&pf=1&t=28%2F10%2F2020%2012%3A59%3A28%206%20-60&fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A&ce=UTF-8&pageName=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fattach&g=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-air%3Fbfil%3D2%26product%3DMGN63LL%2FA%26step%3Dattach&r=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-air%2Fspace-gray-apple-m1-chip-with-8%25E2%2580%2591core-cpu-and-7%25E2%2580%2591core-gpu-256gb&cc=USD&server=as-13.5.0&events=event33%2Cevent210%3D2.88%2Cevent246&v3=AOS%3A%20US%20Consumer&c4=D%3Dg&v4=D%3DpageName&c5=macintel&c8=AOS%3A%20Mac&c14=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fconfig&v14=en-us&c19=AOS%3A%20US%20Consumer%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fattach&v19=D%3Dc19&c20=AOS%3A%20US%20Consumer&c37=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fattach%7Ccold%20start&c40=10078&v49=D%3Dr&v54=D%3Dg&v94=2.88&v97=s.tl-o&pe=lnk_o&pev2=Cold&s=1920x1080&c=24&j=1.6&v=N&k=Y&bw=1420&bh=630&lrt=2503&AQE=1",
            headers={
                "Content-Type": "text/plain;charset=UTF-8",
                "Referer": "https://www.apple.com/",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/favicon.ico",
            headers={
                "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://store.storeimages.cdn-apple.com/4982/store.apple.com/shop/rs-external/rel/external.js",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Host": "store.storeimages.cdn-apple.com",
                "Origin": "https://www.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://www.apple.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "POST",
            "https://xp.apple.com/report/2/xp_aos_clientperf",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Length": "2643",
                "Cookie": "geo=IT; ccl=Kdn52WwZ2zpMXc5ABjC73A==; check=true; mbox=session#bb7cc510c65f4f4eaba6b8ef81b5547f#1606566556; s_fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A; s_cc=true; s_vi=[CS]v1|2FE11DAC8515EE05-60000A946BBC0874[CE]; dssid2=0deece74-9857-4594-b36e-273d7f7dec11; dssf=1; as_pcts=JL+lxkMf1kjWAQTYt2GskuGVDw8znwk71-I-NVSCf8uZS0oApzy36fX3ooRv-qe7ZdyyZyWpPgHke; as_dc=nc; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; pxro=1; xp_ci=3z18Z3F8zC6gz55bzBPQzTOhDqgGy; xp_aci=4z8hxmMMiACdfEG13LyJHUIH; s_sq=%5B%5BB%5D%5D",
                "Host": "xp.apple.com",
                "Origin": "https://www.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://www.apple.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            json={
                "deliveryVersion": "1.0",
                "postTime": 1606564770068,
                "events": [
                    {
                        "app": "com.apple.www.Store",
                        "eventType": "pageview",
                        "postTime": 1606564770067,
                        "host": "www.apple.com",
                        "pageHostname": "www.apple.com",
                        "pagePathname": "/shop/buy-mac/macbook-air",
                        "pageUrl": "https://www.apple.com/shop/buy-mac/macbook-air?<query>",
                        "pageViewId": "02f7d2f3-2849-4bf9-9092-32df9aceb358",
                        "sessionStartTS": "1606564751090",
                        "triggeredBy": "load",
                        "name": "https://www.apple.com/shop/buy-mac/macbook-air?bfil=2&product=MGN63LL/A&step=attach",
                        "entryType": "navigation",
                        "startTime": 0,
                        "duration": 5203.4050000074785,
                        "initiatorType": "navigation",
                        "nextHopProtocol": "h2",
                        "workerStart": 0,
                        "redirectStart": 10.255000001052395,
                        "redirectEnd": 245.71499999728985,
                        "fetchStart": 245.7200000062585,
                        "domainLookupStart": 245.7200000062585,
                        "domainLookupEnd": 245.7200000062585,
                        "connectStart": 245.7200000062585,
                        "connectEnd": 245.7200000062585,
                        "secureConnectionStart": 245.7200000062585,
                        "requestStart": 252.34499998623505,
                        "responseStart": 427.54999999306165,
                        "responseEnd": 434.36499999370426,
                        "transferSize": 48247,
                        "encodedBodySize": 46722,
                        "decodedBodySize": 432197,
                        "serverTiming": [],
                        "workerTiming": [],
                        "unloadEventStart": 438.9049999881536,
                        "unloadEventEnd": 439.1100000066217,
                        "domInteractive": 1455.1050000009127,
                        "domContentLoadedEventStart": 1455.3650000016205,
                        "domContentLoadedEventEnd": 3566.5399999998044,
                        "domComplete": 5193.9950000087265,
                        "loadEventStart": 5194.040000002133,
                        "loadEventEnd": 5203.4050000074785,
                        "type": "navigate",
                        "redirectCount": 1,
                        "NavigationTimingLevel": 2,
                        "networkDownlink": 10,
                        "networkEffectiveType": "4g",
                        "networkRtt": 50,
                        "imageCountOnLoad": 31,
                        "referer": "https://www.apple.com/shop/buy-mac/macbook-air/space-gray-apple-m1-chip-with-8%E2%80%91core-cpu-and-7%E2%80%91core-gpu-256gb?<query>",
                        "support": {"subtleCrypto": True},
                        "asDc": "nc",
                        "audit": {
                            "telemetry": {"version": ["2.18.9"]},
                            "echo": {"version": ["2.0.6"]},
                            "recon": {"version": ["undef"]},
                            "jquery": {"version": ["1.11.3"]},
                            "can": {"version": ["2.3.29"]},
                        },
                        "cookies": [
                            "geo",
                            "ccl",
                            "check",
                            "mbox",
                            "s_fid",
                            "s_cc",
                            "s_vi",
                            "as_dc",
                            "as_sfa",
                            "pxro",
                            "xp_ci",
                            "s_sq",
                            "as_atb",
                        ],
                        "crypto": {
                            "exists": True,
                            "passed": True,
                            "algorithm": "RSA-OAEP",
                            "encryptTime": 384.72999999066815,
                            "decryptTime": 2593.640000006417,
                        },
                        "pageId": "AOS: home/shop_mac/family/macbook_air/attach",
                        "pageShopPath": "/buy-mac/macbook-air?bfil=2&product=MGN63LL/A&step=attach",
                        "pixelRatio": 1,
                        "pluginCount": 4,
                        "pxro": "1",
                        "rsNames": ["rs-external", "rs-mac"],
                        "screenHeight": 1080,
                        "screenWidth": 1920,
                        "scripts": 2,
                        "styles": 4,
                        "validPageUrl": True,
                        "windowInnerHeight": 630,
                        "windowInnerWidth": 1420,
                        "windowOrientation": 0,
                        "windowOuterHeight": 1077,
                        "windowOuterWidth": 1420,
                        "environment": "",
                        "sf": "us",
                        "segment": "Consumer",
                        "locale": "en-us",
                    }
                ],
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/shop/bag/status?apikey=SJHJUH4YFCTTPD4F4",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.rest(
            "POST",
            "https://www.apple.com/shop/recommendedForYou-full?partsInCart.0=MGN63LL/A&inline=true&recentAddedPart=MGN63LL/A",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "modelversion": "v2",
                "pragma": "no-cache",
                "syntax": "graviton",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-aos-model-page": "cart",
                "x-aos-stk": "9b49e9bc",
                "x-requested-with": "XMLHttpRequest",
            },
        ) as resp:
            pass
        with self.rest(
            "GET",
            "https://www.apple.com/search-services/suggestions/defaultlinks/?src=globalnav&locale=en_US",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://www.apple.com/favicon.ico",
            headers={
                "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://store.storeimages.cdn-apple.com/4982/store.apple.com/shop/rs-external/rel/external.js",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Host": "store.storeimages.cdn-apple.com",
                "Origin": "https://www.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://www.apple.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "POST",
            "https://xp.apple.com/report/2/xp_aos_clientperf",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Length": "2302",
                "Cookie": "geo=IT; ccl=Kdn52WwZ2zpMXc5ABjC73A==; check=true; mbox=session#bb7cc510c65f4f4eaba6b8ef81b5547f#1606566556; s_fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A; s_cc=true; s_vi=[CS]v1|2FE11DAC8515EE05-60000A946BBC0874[CE]; dssid2=0deece74-9857-4594-b36e-273d7f7dec11; dssf=1; as_pcts=JL+lxkMf1kjWAQTYt2GskuGVDw8znwk71-I-NVSCf8uZS0oApzy36fX3ooRv-qe7ZdyyZyWpPgHke; as_dc=nc; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; pxro=1; xp_ci=3z18Z3F8zC6gz55bzBPQzTOhDqgGy; xp_aci=4z8hxmMMiACdfEG13LyJHUIH; as_xs=flc=; as_xsm=1&TsS1k4znjEvnGjBoAe_vvw; s_sq=%5B%5BB%5D%5D",
                "Host": "xp.apple.com",
                "Origin": "https://www.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://www.apple.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            json={
                "deliveryVersion": "1.0",
                "postTime": 1606564773590,
                "events": [
                    {
                        "app": "com.apple.www.Store",
                        "eventType": "pageview",
                        "postTime": 1606564773589,
                        "host": "www.apple.com",
                        "pageHostname": "www.apple.com",
                        "pagePathname": "/shop/bag",
                        "pageUrl": "https://www.apple.com/shop/bag?<query>",
                        "pageViewId": "58ecf02c-72ab-40ec-885e-f52c88f7161d",
                        "sessionStartTS": "1606564751090",
                        "triggeredBy": "load",
                        "name": "https://www.apple.com/shop/bag",
                        "entryType": "navigation",
                        "startTime": 0,
                        "duration": 2808.694999985164,
                        "initiatorType": "navigation",
                        "nextHopProtocol": "h2",
                        "workerStart": 0,
                        "redirectStart": 3.5700000007636845,
                        "redirectEnd": 221.34499999810942,
                        "fetchStart": 221.34499999810942,
                        "domainLookupStart": 221.34499999810942,
                        "domainLookupEnd": 221.34499999810942,
                        "connectStart": 221.34499999810942,
                        "connectEnd": 221.34499999810942,
                        "secureConnectionStart": 221.34499999810942,
                        "requestStart": 230.79999999026768,
                        "responseStart": 577.4699999892619,
                        "responseEnd": 662.0149999798741,
                        "transferSize": 34937,
                        "encodedBodySize": 33186,
                        "decodedBodySize": 159525,
                        "serverTiming": [],
                        "workerTiming": [],
                        "unloadEventStart": 589.5799999998417,
                        "unloadEventEnd": 589.6749999956228,
                        "domInteractive": 1582.0349999994505,
                        "domContentLoadedEventStart": 1582.2000000043772,
                        "domContentLoadedEventEnd": 2115.319999982603,
                        "domComplete": 2783.6349999997765,
                        "loadEventStart": 2783.6700000043493,
                        "loadEventEnd": 2808.694999985164,
                        "type": "navigate",
                        "redirectCount": 1,
                        "NavigationTimingLevel": 2,
                        "networkDownlink": 10,
                        "networkEffectiveType": "4g",
                        "networkRtt": 50,
                        "imageCountOnLoad": 13,
                        "referer": "https://www.apple.com/shop/buy-mac/macbook-air?<query>",
                        "support": {"subtleCrypto": True},
                        "asDc": "nc",
                        "audit": {"telemetry": {"version": ["2.18.9"]}, "echo": {"version": ["2.0.6"]}},
                        "cookies": [
                            "geo",
                            "ccl",
                            "check",
                            "mbox",
                            "s_fid",
                            "s_cc",
                            "s_vi",
                            "as_dc",
                            "as_sfa",
                            "pxro",
                            "xp_ci",
                            "as_atb",
                            "s_sq",
                        ],
                        "crypto": {
                            "exists": True,
                            "passed": True,
                            "algorithm": "RSA-OAEP",
                            "encryptTime": 918.5550000111107,
                            "decryptTime": 424.4699999981094,
                        },
                        "pageId": "AOS: bag",
                        "pageShopPath": "/bag",
                        "pixelRatio": 1,
                        "pluginCount": 4,
                        "pxro": "1",
                        "rsNames": ["rs-external", "rs-checkout"],
                        "screenHeight": 1080,
                        "screenWidth": 1920,
                        "scripts": 2,
                        "styles": 7,
                        "validPageUrl": True,
                        "windowInnerHeight": 630,
                        "windowInnerWidth": 1420,
                        "windowOrientation": 0,
                        "windowOuterHeight": 1077,
                        "windowOuterWidth": 1420,
                        "environment": "",
                        "sf": "us",
                        "seg": "Consumer",
                        "locale": "en-us",
                    }
                ],
            },
        ) as resp:
            pass
        with self.client.request(
            "POST",
            "https://securemetrics.apple.com/b/ss/applestoreww,appleglobal/1/JS-2.17.0/s52405784184661?AQB=1&ndh=1&pf=1&t=28%2F10%2F2020%2012%3A59%3A37%206%20-60&fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A&ce=UTF-8&pageName=AOS%3A%20bag&g=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbag&r=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-mac%2Fmacbook-air%3Fbfil%3D2%26product%3DMGN63LL%2FA%26step%3Dattach&cc=USD&server=as-13.5.0&events=event210%3D6.08%2Cevent246%2Cevent500&v3=AOS%3A%20US%20Consumer&c4=D%3Dg&v4=D%3DpageName&c5=macintel&c8=AOS%3A%20Bag&c14=AOS%3A%20home%2Fshop_mac%2Ffamily%2Fmacbook_air%2Fattach&v14=en-us&c19=AOS%3A%20US%20Consumer%3A%20bag&v19=D%3Dc19&c20=AOS%3A%20US%20Consumer&v39=D%3DpageName%2B%22%7C%7CBag%7CStandardCheckout%22&c40=10078&v49=D%3Dr&v54=D%3Dg&v94=6.08&v97=s.tl-o&pe=lnk_o&pev2=shoppingCart.actions.t.checkout&c.&a.&activitymap.&page=AOS%3A%20bag&link=check%20out%20%28inner%20text%29%20%7C%20no%20href%20%7C%20body&region=body&pageIDType=1&.activitymap&.a&.c&pid=AOS%3A%20bag&pidt=1&oid=Check%20Out&oidt=3&ot=SUBMIT&s=1920x1080&c=24&j=1.6&v=N&k=Y&bw=1420&bh=630&lrt=61&AQE=1",
            headers={
                "Content-Type": "text/plain;charset=UTF-8",
                "Referer": "https://www.apple.com/",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "POST",
            "https://www.apple.com/shop/bagx/checkout_now?_a=checkout&_m=shoppingCart.actions",
            headers={
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "content-type": "application/x-www-form-urlencoded",
                "modelversion": "v2",
                "pragma": "no-cache",
                "syntax": "graviton",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "x-aos-model-page": "cart",
                "x-aos-stk": "9b49e9bc",
                "x-requested-with": "XMLHttpRequest",
            },
            data="shoppingCart.recommendations.recommendedItem.part=&shoppingCart.items.item-3dedbef6-e7e0-423c-a6a2-3afc452d63f7.isIntentToGift=false&shoppingCart.items.item-3dedbef6-e7e0-423c-a6a2-3afc452d63f7.itemQuantity.quantity=1&shoppingCart.summary.promoCode.promoCode=&shoppingCart.actions.fcscounter=&shoppingCart.actions.fcsdata=",
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "GET",
            "/shop/bag/status?apikey=SKCXTKATUYT9JK4HD",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Cookie": "geo=IT; ccl=Kdn52WwZ2zpMXc5ABjC73A==; check=true; mbox=session#bb7cc510c65f4f4eaba6b8ef81b5547f#1606566556; s_fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A; s_cc=true; s_vi=[CS]v1|2FE11DAC8515EE05-60000A946BBC0874[CE]; dssid2=0deece74-9857-4594-b36e-273d7f7dec11; dssf=1; as_pcts=JL+lxkMf1kjWAQTYt2GskuGVDw8znwk71-I-NVSCf8uZS0oApzy36fX3ooRv-qe7ZdyyZyWpPgHke; as_dc=nc; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; pxro=1; xp_ci=3z18Z3F8zC6gz55bzBPQzTOhDqgGy; s_sq=%5B%5BB%5D%5D; as_xs=flc=&idmsl=1; as_xsm=1&93mZGW_YVaxBa9JRiFse-Q",
                "Host": "secure2.store.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://secure2.store.apple.com/shop/sign_in?c=aHR0cHM6Ly93d3cuYXBwbGUuY29tL3Nob3AvYmFnfDFhb3NjY2QxZjg4ZGZjYjY4YWRhNWZmMmY5ZTY5YWMzNjE0OTYyMjZlOWMz&o=O01HTjYz&r=SXYD4UDAPXU7P7KXF&s=aHR0cHM6Ly9zZWN1cmUyLnN0b3JlLmFwcGxlLmNvbS9zaG9wL2NoZWNrb3V0L3N0YXJ0P3BsdG49QTZGNDNFMER8MWFvczg4MjgzMjY3MzJkNWEzNjIxMTQxMDE0ZTU4NmZiNTY5MjEzZGEyY2M&t=SXYD4UDAPXU7P7KXF&up=t",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "/search-services/suggestions/defaultlinks/?src=globalnav&locale=en_US",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Cookie": "geo=IT; ccl=Kdn52WwZ2zpMXc5ABjC73A==; check=true; mbox=session#bb7cc510c65f4f4eaba6b8ef81b5547f#1606566556; s_fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A; s_cc=true; s_vi=[CS]v1|2FE11DAC8515EE05-60000A946BBC0874[CE]; dssid2=0deece74-9857-4594-b36e-273d7f7dec11; dssf=1; as_pcts=JL+lxkMf1kjWAQTYt2GskuGVDw8znwk71-I-NVSCf8uZS0oApzy36fX3ooRv-qe7ZdyyZyWpPgHke; as_dc=nc; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; pxro=1; xp_ci=3z18Z3F8zC6gz55bzBPQzTOhDqgGy; s_sq=%5B%5BB%5D%5D; as_xs=flc=&idmsl=1; as_xsm=1&93mZGW_YVaxBa9JRiFse-Q",
                "Host": "secure2.store.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://secure2.store.apple.com/shop/sign_in?c=aHR0cHM6Ly93d3cuYXBwbGUuY29tL3Nob3AvYmFnfDFhb3NjY2QxZjg4ZGZjYjY4YWRhNWZmMmY5ZTY5YWMzNjE0OTYyMjZlOWMz&o=O01HTjYz&r=SXYD4UDAPXU7P7KXF&s=aHR0cHM6Ly9zZWN1cmUyLnN0b3JlLmFwcGxlLmNvbS9zaG9wL2NoZWNrb3V0L3N0YXJ0P3BsdG49QTZGNDNFMER8MWFvczg4MjgzMjY3MzJkNWEzNjIxMTQxMDE0ZTU4NmZiNTY5MjEzZGEyY2M&t=SXYD4UDAPXU7P7KXF&up=t",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://idmsa.apple.com/appleauth/auth/authorize/signin?frame_id=auth-bbfc2b43-ol01-rowz-a4jz-l79n3zhj&language=en_US&iframeId=auth-bbfc2b43-ol01-rowz-a4jz-l79n3zhj&client_id=a797929d224abb1cc663bb187bbcd02f7172ca3a84df470380522a7c6092118b&redirect_uri=https://secure2.store.apple.com&response_type=code&response_mode=web_message&state=auth-bbfc2b43-ol01-rowz-a4jz-l79n3zhj",
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Cookie": "geo=IT; ccl=Kdn52WwZ2zpMXc5ABjC73A==; check=true; mbox=session#bb7cc510c65f4f4eaba6b8ef81b5547f#1606566556; s_fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A; s_cc=true; s_vi=[CS]v1|2FE11DAC8515EE05-60000A946BBC0874[CE]; dssid2=0deece74-9857-4594-b36e-273d7f7dec11; dssf=1; as_pcts=JL+lxkMf1kjWAQTYt2GskuGVDw8znwk71-I-NVSCf8uZS0oApzy36fX3ooRv-qe7ZdyyZyWpPgHke; as_dc=nc; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; pxro=1; xp_ci=3z18Z3F8zC6gz55bzBPQzTOhDqgGy; s_sq=%5B%5BB%5D%5D; as_xs=flc=&idmsl=1; as_xsm=1&93mZGW_YVaxBa9JRiFse-Q",
                "Host": "idmsa.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://secure2.store.apple.com/",
                "Sec-Fetch-Dest": "iframe",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-site",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "https://store.storeimages.cdn-apple.com/4982/store.apple.com/shop/rs-external/rel/external.js",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Host": "store.storeimages.cdn-apple.com",
                "Origin": "https://secure2.store.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://secure2.store.apple.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.rest(
            "POST",
            "https://xp.apple.com/report/2/xp_aos_clientperf",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Length": "3275",
                "Cookie": "geo=IT; ccl=Kdn52WwZ2zpMXc5ABjC73A==; check=true; mbox=session#bb7cc510c65f4f4eaba6b8ef81b5547f#1606566556; s_fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A; s_cc=true; s_vi=[CS]v1|2FE11DAC8515EE05-60000A946BBC0874[CE]; dssid2=0deece74-9857-4594-b36e-273d7f7dec11; dssf=1; as_pcts=JL+lxkMf1kjWAQTYt2GskuGVDw8znwk71-I-NVSCf8uZS0oApzy36fX3ooRv-qe7ZdyyZyWpPgHke; as_dc=nc; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; pxro=1; xp_ci=3z18Z3F8zC6gz55bzBPQzTOhDqgGy; xp_aci=4z8hxmMMiACdfEG13LyJHUIH; s_sq=%5B%5BB%5D%5D; as_xs=flc=&idmsl=1; as_xsm=1&93mZGW_YVaxBa9JRiFse-Q; dslang=US-EN; site=USA",
                "Host": "xp.apple.com",
                "Origin": "https://secure2.store.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://secure2.store.apple.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            json={
                "deliveryVersion": "1.0",
                "postTime": 1606564780131,
                "events": [
                    {
                        "app": "com.apple.www.Store",
                        "eventType": "error",
                        "postTime": 1606564779670,
                        "host": "secure2.store.apple.com",
                        "pageHostname": "secure2.store.apple.com",
                        "pagePathname": "/shop/sign_in",
                        "pageUrl": "https://secure2.store.apple.com/shop/sign_in?<query>",
                        "pageViewId": "fd3d8c41-3430-4b37-8283-5d5e16272a2f",
                        "sessionStartTS": 1606564779057,
                        "errorMsg": "Script error.",
                        "errorCol": 0,
                        "errorLine": 0,
                    },
                    {
                        "app": "com.apple.www.Store",
                        "eventType": "pageview",
                        "postTime": 1606564780130,
                        "host": "secure2.store.apple.com",
                        "pageHostname": "secure2.store.apple.com",
                        "pagePathname": "/shop/sign_in",
                        "pageUrl": "https://secure2.store.apple.com/shop/sign_in?<query>",
                        "pageViewId": "fd3d8c41-3430-4b37-8283-5d5e16272a2f",
                        "sessionStartTS": 1606564779057,
                        "triggeredBy": "load",
                        "name": "https://secure2.store.apple.com/shop/sign_in?c=aHR0cHM6Ly93d3cuYXBwbGUuY29tL3Nob3AvYmFnfDFhb3NjY2QxZjg4ZGZjYjY4YWRhNWZmMmY5ZTY5YWMzNjE0OTYyMjZlOWMz&o=O01HTjYz&r=SXYD4UDAPXU7P7KXF&s=aHR0cHM6Ly9zZWN1cmUyLnN0b3JlLmFwcGxlLmNvbS9zaG9wL2NoZWNrb3V0L3N0YXJ0P3BsdG49QTZGNDNFMER8MWFvczg4MjgzMjY3MzJkNWEzNjIxMTQxMDE0ZTU4NmZiNTY5MjEzZGEyY2M&t=SXYD4UDAPXU7P7KXF&up=t",
                        "entryType": "navigation",
                        "startTime": 0,
                        "duration": 1461.2450000131503,
                        "initiatorType": "navigation",
                        "nextHopProtocol": "http/1.1",
                        "workerStart": 0,
                        "redirectStart": 0,
                        "redirectEnd": 0,
                        "fetchStart": 7.270000001881272,
                        "domainLookupStart": 144.83999999356456,
                        "domainLookupEnd": 147.02000000397675,
                        "connectStart": 147.02000000397675,
                        "connectEnd": 418.8350000185892,
                        "secureConnectionStart": 275.0649999943562,
                        "requestStart": 418.9349999942351,
                        "responseStart": 570.015000004787,
                        "responseEnd": 574.3850000144448,
                        "transferSize": 11650,
                        "encodedBodySize": 10158,
                        "decodedBodySize": 30767,
                        "serverTiming": [],
                        "workerTiming": [],
                        "unloadEventStart": 0,
                        "unloadEventEnd": 0,
                        "domInteractive": 1145.409999997355,
                        "domContentLoadedEventStart": 1146.0599999991246,
                        "domContentLoadedEventEnd": 1263.4050000051502,
                        "domComplete": 1420.8250000083353,
                        "loadEventStart": 1420.8600000129081,
                        "loadEventEnd": 1461.2450000131503,
                        "type": "navigate",
                        "redirectCount": 0,
                        "NavigationTimingLevel": 2,
                        "networkDownlink": 10,
                        "networkEffectiveType": "4g",
                        "networkRtt": 50,
                        "imageCountOnLoad": 1,
                        "referer": "https://www.apple.com/?<query>",
                        "support": {"subtleCrypto": True},
                        "asDc": "nc",
                        "audit": {"telemetry": {"version": ["2.18.9"]}, "echo": {"version": ["2.0.6"]}},
                        "cookies": [
                            "geo",
                            "ccl",
                            "check",
                            "mbox",
                            "s_fid",
                            "s_cc",
                            "s_vi",
                            "as_dc",
                            "as_sfa",
                            "pxro",
                            "xp_ci",
                            "s_sq",
                        ],
                        "crypto": {
                            "exists": True,
                            "passed": True,
                            "algorithm": "RSA-OAEP",
                            "encryptTime": 203.99500001803972,
                            "decryptTime": 194.69999999273568,
                        },
                        "pageId": "AOS: checkout : sign in",
                        "pageShopPath": "/sign_in?c=aHR0cHM6Ly93d3cuYXBwbGUuY29tL3Nob3AvYmFnfDFhb3NjY2QxZjg4ZGZjYjY4YWRhNWZmMmY5ZTY5YWMzNjE0OTYyMjZlOWMz&o=O01HTjYz&r=SXYD4UDAPXU7P7KXF&s=aHR0cHM6Ly9zZWN1cmUyLnN0b3JlLmFwcGxlLmNvbS9zaG9wL2NoZWNrb3V0L3N0YXJ0P3BsdG49QTZGNDNFMER8MWFvczg4MjgzMjY3MzJkNWEzNjIxMTQxMDE0ZTU4NmZiNTY5MjEzZGEyY2M&t=SXYD4UDAPXU7P7KXF&up=t",
                        "pixelRatio": 1,
                        "pluginCount": 4,
                        "pxro": "1",
                        "rsNames": ["rs-external", "rs-checkout"],
                        "screenHeight": 1080,
                        "screenWidth": 1920,
                        "scripts": 3,
                        "styles": 3,
                        "validPageUrl": True,
                        "windowInnerHeight": 630,
                        "windowInnerWidth": 1420,
                        "windowOrientation": 0,
                        "windowOuterHeight": 1077,
                        "windowOuterWidth": 1420,
                        "environment": "",
                        "sf": "us",
                        "seg": "Consumer",
                        "locale": "en-us",
                    },
                ],
            },
        ) as resp:
            pass
        with self.client.request(
            "POST",
            "https://idmsa.apple.com/appleauth/jslog",
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Length": "280",
                "Content-type": "application/json",
                "Cookie": "geo=IT; ccl=Kdn52WwZ2zpMXc5ABjC73A==; check=true; mbox=session#bb7cc510c65f4f4eaba6b8ef81b5547f#1606566556; s_fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A; s_cc=true; s_vi=[CS]v1|2FE11DAC8515EE05-60000A946BBC0874[CE]; dssid2=0deece74-9857-4594-b36e-273d7f7dec11; dssf=1; as_pcts=JL+lxkMf1kjWAQTYt2GskuGVDw8znwk71-I-NVSCf8uZS0oApzy36fX3ooRv-qe7ZdyyZyWpPgHke; as_dc=nc; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; pxro=1; xp_ci=3z18Z3F8zC6gz55bzBPQzTOhDqgGy; s_sq=%5B%5BB%5D%5D; as_xs=flc=&idmsl=1; as_xsm=1&93mZGW_YVaxBa9JRiFse-Q; aa=991DE1862A229067497F55E997BAE2F5; dslang=US-EN; site=USA",
                "Host": "idmsa.apple.com",
                "Origin": "https://idmsa.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://idmsa.apple.com/appleauth/auth/authorize/signin?frame_id=auth-bbfc2b43-ol01-rowz-a4jz-l79n3zhj&language=en_US&iframeId=auth-bbfc2b43-ol01-rowz-a4jz-l79n3zhj&client_id=a797929d224abb1cc663bb187bbcd02f7172ca3a84df470380522a7c6092118b&redirect_uri=https://secure2.store.apple.com&response_type=code&response_mode=web_message&state=auth-bbfc2b43-ol01-rowz-a4jz-l79n3zhj",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "scnt": "",
                "x-csrf-token": "",
            },
            data='{"type":"INFO","title":"AppleAuthDebug","message":"APPLE ID : Launching AppleAuth application.{\\"data\\":{\\"initApp\\":{\\"startTime\\":1400.0300000188872}},\\"order\\":[\\"initApp\\"]}","iframeId":"auth-bbfc2b43-ol01-rowz-a4jz-l79n3zhj","details":"{\\"pageVisibilityState\\":\\"visible\\"}"}',
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "GET",
            "/favicon.ico",
            headers={
                "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Cookie": "geo=IT; ccl=Kdn52WwZ2zpMXc5ABjC73A==; check=true; mbox=session#bb7cc510c65f4f4eaba6b8ef81b5547f#1606566556; s_fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A; s_cc=true; s_vi=[CS]v1|2FE11DAC8515EE05-60000A946BBC0874[CE]; dssid2=0deece74-9857-4594-b36e-273d7f7dec11; dssf=1; as_pcts=JL+lxkMf1kjWAQTYt2GskuGVDw8znwk71-I-NVSCf8uZS0oApzy36fX3ooRv-qe7ZdyyZyWpPgHke; as_dc=nc; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; pxro=1; xp_ci=3z18Z3F8zC6gz55bzBPQzTOhDqgGy; s_sq=%5B%5BB%5D%5D; as_xs=flc=&idmsl=1; as_xsm=1&93mZGW_YVaxBa9JRiFse-Q; dslang=US-EN; site=USA",
                "Host": "secure2.store.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://secure2.store.apple.com/shop/sign_in?c=aHR0cHM6Ly93d3cuYXBwbGUuY29tL3Nob3AvYmFnfDFhb3NjY2QxZjg4ZGZjYjY4YWRhNWZmMmY5ZTY5YWMzNjE0OTYyMjZlOWMz&o=O01HTjYz&r=SXYD4UDAPXU7P7KXF&s=aHR0cHM6Ly9zZWN1cmUyLnN0b3JlLmFwcGxlLmNvbS9zaG9wL2NoZWNrb3V0L3N0YXJ0P3BsdG49QTZGNDNFMER8MWFvczg4MjgzMjY3MzJkNWEzNjIxMTQxMDE0ZTU4NmZiNTY5MjEzZGEyY2M&t=SXYD4UDAPXU7P7KXF&up=t",
                "Sec-Fetch-Dest": "image",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
            },
            catch_response=True,
        ) as resp:
            pass
        with self.client.request(
            "POST",
            "https://idmsa.apple.com/appleauth/jslog",
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Length": "399",
                "Content-type": "application/json",
                "Cookie": "geo=IT; ccl=Kdn52WwZ2zpMXc5ABjC73A==; check=true; mbox=session#bb7cc510c65f4f4eaba6b8ef81b5547f#1606566556; s_fid=0EE10F1DE7BC5EFE-229AB97ADA08D75A; s_cc=true; s_vi=[CS]v1|2FE11DAC8515EE05-60000A946BBC0874[CE]; dssid2=0deece74-9857-4594-b36e-273d7f7dec11; dssf=1; as_pcts=JL+lxkMf1kjWAQTYt2GskuGVDw8znwk71-I-NVSCf8uZS0oApzy36fX3ooRv-qe7ZdyyZyWpPgHke; as_dc=nc; as_sfa=Mnx1c3x1c3x8ZW5fVVN8Y29uc3VtZXJ8aW50ZXJuZXR8MHwwfDE; pxro=1; xp_ci=3z18Z3F8zC6gz55bzBPQzTOhDqgGy; s_sq=%5B%5BB%5D%5D; as_xs=flc=&idmsl=1; as_xsm=1&93mZGW_YVaxBa9JRiFse-Q; aa=991DE1862A229067497F55E997BAE2F5; dslang=US-EN; site=USA",
                "Host": "idmsa.apple.com",
                "Origin": "https://idmsa.apple.com",
                "Pragma": "no-cache",
                "Referer": "https://idmsa.apple.com/appleauth/auth/authorize/signin?frame_id=auth-bbfc2b43-ol01-rowz-a4jz-l79n3zhj&language=en_US&iframeId=auth-bbfc2b43-ol01-rowz-a4jz-l79n3zhj&client_id=a797929d224abb1cc663bb187bbcd02f7172ca3a84df470380522a7c6092118b&redirect_uri=https://secure2.store.apple.com&response_type=code&response_mode=web_message&state=auth-bbfc2b43-ol01-rowz-a4jz-l79n3zhj",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
                "scnt": "",
                "x-csrf-token": "",
            },
            data='{"type":"INFO","title":"AppleAuthPerf","message":"APPLE ID : TTI {\\"data\\":{\\"initApp\\":{\\"startTime\\":1400.0300000188872},\\"loadAuthComponent\\":{\\"startTime\\":2087.4300000141375},\\"startAppToTTI\\":{\\"duration\\":686.1000000208151}},\\"order\\":[\\"initApp\\",\\"loadAuthComponent\\",\\"startAppToTTI\\"]}","iframeId":"auth-bbfc2b43-ol01-rowz-a4jz-l79n3zhj","details":"{\\"pageVisibilityState\\":\\"visible\\"}"}',
            catch_response=True,
        ) as resp:
            pass


if __name__ == "__main__":
    run_single_user(apple_buy_a_mac)
