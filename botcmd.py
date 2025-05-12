from info import *
from telebot import types

def myCmd(m):
    if m.text == '/start':
        welcome_msg = (
            f"مرحبًا، {m.from_user.first_name}!\n"
            "هذا البوت مخصص لتتبع الطرود البريدية الخاصة بشركة EMS الجزائر.\n"
            "أرسل رقم التتبع لمعرفة حالة شحنتك.\n"
            "للإبلاغ عن أي مشكلة، راسلنا على @AissxAch"
        )
        bot.send_message(m.chat.id, welcome_msg)