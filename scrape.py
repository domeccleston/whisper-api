import re
import sys
import urllib.request

import modal

stub = modal.Stub(name="link-scraper")

playwright_image = modal.Image.debian_slim(python_version="3.10").run_commands(
    "apt-get update",
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    "pip install playwright==1.30.0",
    "playwright install-deps chromium",
    "playwright install chromium",
)

@stub.function(image=playwright_image)
async def get_links(cur_url: str):
  from playwright.async_api import async_playwright

  async with async_playwright() as p:
      browser = await p.chromium.launch()
      page = await browser.new_page()
      await page.goto(cur_url)
      links = await page.eval_on_selector_all("a[href]", "elements => elements.map(element => element.href)")
      await browser.close()
  
  print("links", links)
  return links

@stub.local_entrypoint()
def main():
  urls = ["https://modal.com", "https://vercel.com", "https://github.com"]
  for links in get_links.map(urls):
     for link in links:
        print(link)
