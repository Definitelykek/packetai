from .models import Request, async_session, User
from sqlalchemy import update, select


async def save_request(tg_id: int, text: str, answer: str):
    async with async_session() as session:
        req = Request(tg_id=tg_id, text=text, answer=answer)
        session.add(req)
        await session.commit()

async def get_model_by_user(tg_id: int):
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            if not user:
                    user = User(tg_id=tg_id)
                    session.add(user)
                    await session.flush()
                    await session.commit()
        except Exception as e:
            await session.rollback()
            return f"Что-то пошло не так: {e}"
        else:
            return user.model


async def update_model(tg_id: int, model: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        try:
            if user:
                user.model = model
                await session.commit()

            else:
                user = User(tg_id=tg_id, model=model)
                session.add(user)
                await session.flush()
                await session.commit()
        except Exception as e:
            await session.rollback()
            return f"Что-то пошло не так: {e}"
        else:
            return f"Модель успешно обновлена на {model}"
