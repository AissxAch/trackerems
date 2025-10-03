from info import *
from reply import *
from botcmd import *

# def get_working_proxy():
#     """Get a random working proxy from the list"""
#     proxies = fetch_proxies()
#     if not proxies:
#         return None
    
#     # Test proxies and get working ones
#     working_proxies = check_proxies(proxies)
#     if working_proxies:
#         # Sort by latency and pick the fastest
#         working_proxies.sort(key=lambda x: x['latency'])
#         return working_proxies[0]['proxy']
#     return None
# p=get_working_proxy()
# print("proxies is ready")
# print("Bot is ready")
@bot.message_handler(commands=['start'])
def cmd(m):
        myCmd(m)
@bot.message_handler(func=lambda m: True)
def rm(m):
        reply_mg(m)


bot.infinity_polling()