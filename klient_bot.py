import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
import asyncio
import json
import os

TOKEN = "8020803338:AAGOesGlRBDLJj8aWCmpdo18WApmRTsxcCY"
ADMIN_ID = 6551375195
USTALAR_FAYL = "ustalar.json"

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

def get_ustalar(xizmat_turi: str) -> list:
    try:
        with open(USTALAR_FAYL, "r", encoding="utf-8") as f:
            all_ustalar = json.load(f)
        mos = [u for u in all_ustalar if u.get("xizmat") == xizmat_turi and u.get("tasdiqlangan") == True]
        return mos[:5]
    except:
        return []

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚿 Santexnik", callback_data="xizmat:Santexnik"),
            InlineKeyboardButton(text="⚡ Elektrik", callback_data="xizmat:Elektrik"),
        ],
        [
            InlineKeyboardButton(text="🔥 Gaz ustasi", callback_data="xizmat:Gaz ustasi"),
            InlineKeyboardButton(text="🪑 Mebel ustasi", callback_data="xizmat:Mebel ustasi"),
        ],
        [
            InlineKeyboardButton(text="🎨 Oboychi", callback_data="xizmat:Oboychi"),
            InlineKeyboardButton(text="📦 Labo / Yuk", callback_data="xizmat:Labo"),
        ],
        [
            InlineKeyboardButton(text="🛵 Yetkazib berish", callback_data="xizmat:Yetkazib berish"),
        ],
    ])
    await message.answer(
        "👋 <b>UBER TERMEZ</b> botiga xush kelibsiz!\n\n"
        "🏙 Termiz shahri uchun usta va xizmatlar platformasi.\n\n"
        "👇 Qanday xizmat kerak?",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswith("xizmat:"))
async def xizmat_tanlandi(callback: types.CallbackQuery):
    xizmat = callback.data.split(":")[1]
    await callback.message.answer(
        f"✅ <b>{xizmat}</b> tanlandi!\n\n⏳ Termiz shahridagi ustalar qidirilmoqda...",
        parse_mode="HTML"
    )
    ustalar = get_ustalar(xizmat)
    if not ustalar:
        await callback.message.answer(
            f"😔 Hozircha <b>{xizmat}</b> bo'yicha usta topilmadi.\n\n"
            "🔄 Tez orada ustalar qo'shiladi!\n📞 Murojaat: @UberTermezAdmin",
            parse_mode="HTML"
        )
        await callback.answer()
        return

    await callback.message.answer(
        f"🔍 <b>Termiz shahridagi {xizmat} ustalar:</b>\n{'━'*28}",
        parse_mode="HTML"
    )
    for u in ustalar:
        matn = (
            f"👷 <b>{u['ism']}</b>\n"
            f"📍 Termiz shahri\n"
            f"⭐ {u['reyting']} ({u['sharhlar']} ta sharh)\n"
            f"💰 Narx: Kelishilgan holda\n"
            f"📞 {u['telefon']}"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Qo'ng'iroq qilish", url=f"tel:{u['telefon']}")]
        ])
        await callback.message.answer(matn, reply_markup=keyboard, parse_mode="HTML")

    await callback.message.answer(
        "☝️ Yuqoridagi ustalardan biriga qo'ng'iroq qiling.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="bosh_menyu")]
        ])
    )
    await callback.answer()

@dp.callback_query(F.data == "bosh_menyu")
async def bosh_menyu(callback: types.CallbackQuery):
    await start(callback.message)
    await callback.answer()

async def main():
    print("✅ UBER TERMEZ Klient boti ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
