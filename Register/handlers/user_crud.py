
from Register.db.sqlalchemy_db import async_session
from Register.db.sqlalchemy_db import Users
from sqlalchemy.future import select
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from Register.keyboards.menus import get_user_menu, get_admin_menu, get_edit_profile_menu, get_back_menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router1 = Router()

async def add_user(
        session: async_session,
        chat_id: int,
        first_name: str,
        last_name: str,
        username: str,
        phone: str,
        email: str,
        address: str
):
    new_user = Users(
        chat_id=chat_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        phone=phone,
        email=email,
        address=address
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user



async def get_user_by_chat_id(session: async_session, chat_id: int):
      result = await session.execute(select(Users).where(Users.chat_id == chat_id))
      user = result.scalars().first()
      return user

async def update_user(session: async_session, user: Users, **kwargs):
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def delete_user(session: async_session, user: Users, chat_id: int = None):
      if chat_id:
            user = await get_user_by_chat_id(session, chat_id)
      if user:
            await session.delete(user)
            await session.commit()
            return True
      return False

async def get_all_users(session: async_session):
    result = await session.execute(select(Users))
    return result.scalars().all()

async def search_users_by_name(session: async_session, ID):
    ID=int(ID)
    result = await session.execute(
        select(Users).where(Users.id == ID)
    )
    return result.scalars().all()


@router1.callback_query(F.data == "my_profile")
async def show_profile(callback: CallbackQuery):
    async with async_session() as session:
        chat_id = callback.from_user.id
        result= await session.execute(select(Users).where(Users.chat_id == chat_id))
        user = result.scalar_one_or_none()
        if user:
            text = (f"👤 <b>Sizning profilingiz</b>:\n\n"
                    f"🆔 ID: <code>{user.chat_id}</code>\n"
                    f"👨‍🦰 Ism: {user.first_name}\n"
                    f"👨‍🦰 Familiya: {user.last_name}\n"
                    f"👤 Username: @{user.username or 'yo‘q'}\n"
                    f"📞 Telefon: {user.phone or 'yo‘q'}\n"
                    f"📧 Email: {user.email or 'yo‘q'}\n"
                    f"🏠 Manzil: {user.address or 'yo‘q'}"
                    )
        else:
            text= "❌ Profil topilmadi."

        await callback.message.edit_text(text=text, reply_markup=get_back_menu(), parse_mode="HTML")



@router1.callback_query(F.data == "edit_profile")
async def edit_profile_start(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=get_edit_profile_menu())


@router1.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=get_user_menu())



@router1.callback_query(F.data == "delete_profile")
async def delete_profile_handler(callback: CallbackQuery):
    async with async_session() as session:
        chat_id = callback.from_user.id
        user = await get_user_by_chat_id(session, chat_id)
        if user:
            await delete_user(session, user)
            await callback.message.edit_text("Sizning profilingiz muvaffaqiyatli o'chirildi.")
        else:
            await callback.message.edit_text("Siz ro'yxatdan o'tmagansiz. Profilni o'chirish mumkin emas.")
        await callback.answer()








