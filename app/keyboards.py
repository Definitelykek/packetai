from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database.requests as rq

async def get_models_kb(tg_id):
    models_dict = {
        "GPT-4o mini": "gpt-4o-mini",
        "GPT-4o": "gpt-4o",
        "o1 mini": "o1-mini",
        "o1-preview": "o1-preview"
        }
    model = await rq.get_model_by_user(tg_id)
    kb = InlineKeyboardBuilder()
    for k,v in models_dict.items():
        if v == model:
            k+= " ✅"
        kb.add(InlineKeyboardButton(text=k, callback_data=f"model_{v}"))
    kb.adjust(2)
    return kb.as_markup()

# kb = InlineKeyboardMarkup(
#     inline_keyboard=[
#     [InlineKeyboardButton(text="GPT-4o mini", callback_data="model_gpt-4o-mini"), InlineKeyboardButton(text="GPT-4o", callback_data="model_gpt-4o")],
#     [InlineKeyboardButton(text="o1 mini", callback_data="model_o1-mini"), InlineKeyboardButton(text="o1-preview", callback_data="model_o1-preview")]
#     ]
# )