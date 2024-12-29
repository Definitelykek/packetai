import asyncio

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from openai import AsyncOpenAI
import os

from select import select
from sqlalchemy.util import await_only

from database.requests import save_request
import database.requests as rq
from .keyboards import get_models_kb


class ChatState(StatesGroup):
    waiting_for_response = State()


client = AsyncOpenAI(api_key=os.getenv("api_key"), base_url=os.getenv("base_url"))
router = Router()


@router.callback_query(F.data.startswith("model_"))
async def change_model(call: CallbackQuery):
    selected_model = call.data.split("_")[1]
    tg_id = call.from_user.id
    res = await rq.update_model(tg_id, selected_model)
    if "успешно" in res:
        kb = await get_models_kb(tg_id)
        await  call.message.edit_text(text="Выберите модель нейросети", reply_markup=kb)
    await  call.answer(res)


@router.message(Command("model"))
async def model_cmd(message: Message):
    await message.answer("Выберите модели нейросетей:", reply_markup=await get_models_kb(message.from_user.id))


@router.message(F.text)
async def gpt_text(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == ChatState.waiting_for_response:
        await message.answer("Подождите, бот отвечает на предыдущий запрос")
        return
    await state.set_state(ChatState.waiting_for_response)
    # await bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(3)
    text = message.text
    # model = "o1-preview"
    try:
        tg_id = message.from_user.id
        model = await rq.get_model_by_user(tg_id)
        compaltion = await client.chat.completions.create(
            messages=[{"role": "user", "content": text}],
            model=model

        )
        result = compaltion.choices[0].message.content

    except:
        await message.answer("Что-то пошло не так. Попробуйте снова.")
        await state.clear()
        return
    await save_request(tg_id=message.from_user.id, text=text, answer=result)
    await asyncio.sleep(1)
    await message.answer(result)
    await state.clear()
