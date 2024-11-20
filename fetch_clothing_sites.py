#تخمط ماكش راجل
#جهاد مطور سورس
#بدون تشفير
import os
import subprocess
import sys

required_packages = [
    "googlesearch-python",
    "requests",
    "beautifulsoup4",
    "asyncio",
    "python-telegram-bot",
    "termcolor"
]

def install_packages():
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except Exception as e:
            print(f"ولك الووو")

install_packages()

from googlesearch import search
import requests
from bs4 import BeautifulSoup
import asyncio
from telegram import Bot
from termcolor import colored


proxies = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}


def fetch_clothing_sites(query, country, max_results=10):
    print(colored(f"🔍 جلب مواقع بيع الملابس لـ {country}...", "green"))
    results = []
    search_query = f"{query} site:.{country} online clothing store"

    count = 0
    for url in search(search_query):
        if count >= max_results:
            break
        try:

            response = requests.get(url, timeout=10, proxies=proxies)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string if soup.title else "No title"
                results.append({"url": url, "title": title})
                print(colored(f"✅ تم العثور على: {url} - {title}", "cyan"))
            count += 1
        except Exception as e:
            print(colored(f"⚠️ خطأ أثناء الوصول إلى {url}: {e}", "red"))
    
    return results


def save_to_txt(sites, filepath):
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            for site in sites:
                file.write(f"{site['title']} - {site['url']}\n")
        print(colored(f"✅ تم حفظ النتائج في {filepath}", "green"))
    except Exception as e:
        print(colored(f"⚠️ خطأ أثناء حفظ النتائج: {e}", "red"))


async def send_to_telegram(bot_token, chat_id, message):
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
        print(colored("📩 تم إرسال الرسالة إلى Telegram بنجاح!", "green"))
    except Exception as e:
        print(colored(f"⚠️ خطأ أثناء إرسال الرسالة إلى Telegram: {e}", "red"))


if __name__ == "__main__":

    bot_token = input(colored("أدخل توكن البوت الخاص بـ Telegram: ", "yellow")).strip()
    chat_id = input(colored("أدخل معرف الدردشة (Chat ID): ", "yellow")).strip()
    country_code = input(colored("🌍 أدخل رمز الدولة (مثل 'uk' أو 'us'): ", "yellow")).strip()
    query = "online clothing store"

    sites = fetch_clothing_sites(query, country_code, max_results=10)

    filepath = "/storage/emulated/0/jihad.txt"
    save_to_txt(sites, filepath)

    if sites:
        message = "<b>🛍️ قائمة مواقع الملابس:</b>\n\n"
        for site in sites:
            message += f"🔗 <a href='{site['url']}'>{site['title']}</a>\n"

        asyncio.run(send_to_telegram(bot_token, chat_id, message))
    else:
        print(colored("⚠️ لم يتم العثور على أي مواقع.", "red"))