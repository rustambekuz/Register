from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from Register.keyboards.menus import get_user_menu, get_admin_menu
from Register.handlers.config import ADMIN_ID
from Register.handlers.admin import RegisterState
from Register.db.sqlalchemy_db import async_session, Users
from sqlalchemy import select
from Register.handlers.user_crud import add_user


router2 = Router()

@router2.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    if user_id ==ADMIN_ID:
        text = f"👋 Salom, Admin <b>{full_name}!</b>\nQuyidagi menyulardan birini tanlang:"
        reply_markup = get_admin_menu()
        await message.answer(text, reply_markup=reply_markup)
        return

    async with async_session() as session:
        result= await session.execute(select(Users).where(Users.chat_id == user_id))
        user = result.scalar()
    if user:
        text = f"👋 Salom, <b>{full_name}!</b>\nQuyidagi menyulardan birini tanlang:"
        reply_markup = get_user_menu()
        await message.answer(text, reply_markup=reply_markup)

    else:
        await message.answer("👋 Salom! Ro‘yxatdan o‘tish uchun ismingizni kiriting:")
        await state.set_state(RegisterState.first_name)
        @router2.message(RegisterState.first_name)
        async def get_first_name(message: Message, state: FSMContext):
            await state.update_data(first_name=message.text)
            await message.answer("Familiyangizni kiriting:")
            await state.set_state(RegisterState.last_name)


        @router2.message(RegisterState.last_name)
        async def get_last_name(message: Message, state: FSMContext):
            await state.update_data(last_name=message.text)
            await message.answer("Telefon raqamingiz:")
            await state.set_state(RegisterState.phone)


        @router2.message(RegisterState.phone)
        async def get_phone(message: Message, state: FSMContext):
            await state.update_data(phone=message.text)
            await message.answer("emailingizni kiriting:")
            await state.set_state(RegisterState.email)


        @router2.message(RegisterState.email)
        async def get_email(message: Message, state: FSMContext):
            await state.update_data(email=message.text)
            await message.answer("addresingizni kiriting:")
            await state.set_state(RegisterState.address)

        @router2.message(RegisterState.address)
        async def get_address(message: Message, state: FSMContext):
            await state.update_data(address=message.text)
            data = await state.get_data()
            async with async_session() as session:

                await  add_user(
                    session=session,
                    chat_id=message.from_user.id,
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    username=message.from_user.username,
                    phone=data.get('phone'),
                    email=data.get('email'),
                    address=data.get('address')
                )

                await message.answer("✅ Ro‘yxatdan muvaffaqiyatli o‘tdingiz!")
                await state.clear()







