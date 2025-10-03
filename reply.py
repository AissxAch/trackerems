from time import sleep
from info import *
from search import *


def reply_mg(m):
    result = track_ems_package(m.text.strip())
    if "events" in result:
        bot.send_message(m.chat.id, f"\nتم العثور على {result.get('count', 0)} حدث تتبع لرقم {result['tracking_number']}:")
        for i, event in enumerate(result["events"], 1):
            message = (
                f"الحدث {i}:\n"
                f"📅 التاريخ: {event['date']}\n"
                f"📍 الموقع: {event['location']}\n"
                f"🔄 الحالة: {event['status']}"
            )
            bot.send_message(m.chat.id, message)
    else:
        error_msg = (
            "⚠️ خطأ:\n"
            f"{result.get('error', 'خطأ غير معروف')}\n"
            f"التفاصيل: {result.get('response', 'لا توجد تفاصيل إضافية')}"
        )
        bot.send_message(m.chat.id, error_msg)