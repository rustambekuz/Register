import re

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, update
from aiogram.fsm.state import StatesGroup, State

from Register.db.sqlalchemy_db import async_session, Users, get_address_from_coords
from Register.handlers.config import ADMIN_ID
from Register.handlers.user_crud import add_user
from Register.keyboards.menus import (get_user_menu, get_admin_menu,
                                      get_edit_profile_menu,
                                      phone_keyboard, location_keyboard)


router2 = Router()

class EditProfileFSM(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    email = State()
    address = State()


class RegisterUserFSM(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    email = State()
    address = State()

from Register.db.sqlalchemy_db import update_user_field_by_chat_id
#edit_first_name
@router2.callback_query(F.data == "edit_first_name")
async def edit_first_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✏️ Yangi ismingizni kiriting:")
    await state.set_state(EditProfileFSM.first_name)

@router2.message(EditProfileFSM.first_name)
async def process_first_name(message: Message, state: FSMContext):
    if not re.match(r"^[A-Za-zА-Яа-яʻғқўҳ\s]{2,30}$", message.text):
        await message.answer("❌ Ism noto‘g‘ri formatda.")
        return
    await update_user_field_by_chat_id(message.chat.id, "first_name", message.text)
    await message.answer("✅ Ism yangilandi.")
    await state.clear()

#edit_last_name

@router2.callback_query(F.data == "edit_last_name")
async def edit_last_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✏️ Yangi familiyangizni kiriting:")
    await state.set_state(EditProfileFSM.last_name)
    await callback.answer(cache_time=60)

@router2.message(EditProfileFSM.last_name)
async def process_last_name(message: Message, state: FSMContext):
    if not re.match(r"^[A-Za-zА-Яа-яʻғқўҳ\s]{2,30}$", message.text):
        await message.answer("❌ Familiya noto‘g‘ri formatda.")
        return
    await update_user_field_by_chat_id(message.chat.id, "last_name", message.text)
    await message.answer("✅ Familiya yangilandi.")
    await state.clear()

#edit_phone
@router2.callback_query(F.data == "edit_phone")
async def edit_phone(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("📞 Yangi telefon raqamni kiriting: (+998...)")
    await state.set_state(EditProfileFSM.phone)

@router2.message(EditProfileFSM.phone)
async def process_phone(message: Message, state: FSMContext):
    if not re.match(r"^\+998\d{9}$", message.text):
        await message.answer("❌ Telefon raqami noto‘g‘ri formatda.")
        return
    await update_user_field_by_chat_id(message.chat.id, "phone", message.text)
    await message.answer("✅ Telefon raqami yangilandi.")
    await state.clear()

#edit_email
@router2.callback_query(F.data == "edit_email")
async def edit_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("📧 Yangi email manzilini kiriting:")
    await state.set_state(EditProfileFSM.email)

@router2.message(EditProfileFSM.email)
async def process_email(message: Message, state: FSMContext):
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", message.text):
        await message.answer("❌ Email noto‘g‘ri formatda.")
        return
    await update_user_field_by_chat_id(message.chat.id, "email", message.text)
    await message.answer("✅ Email yangilandi.")
    await state.clear()

#edit_address
@router2.callback_query(F.data == "edit_address")
async def edit_address(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🏠 Yangi manzilingizni kiriting:")
    await state.set_state(EditProfileFSM.address)

@router2.message(EditProfileFSM.address)
async def process_address(message: Message, state: FSMContext):
    await update_user_field_by_chat_id(message.chat.id, "address", message.text)
    await message.answer("✅ Manzil yangilandi.")
    await state.clear()


# Register users

@router2.message(RegisterUserFSM.first_name)
async def get_first_name(message: types.Message, state: FSMContext):
    if not re.match(r"^[A-Za-zА-Яа-яʻғқўҳ\s]{2,30}$", message.text):
        return await message.answer("❌ Ism noto‘g‘ri formatda. Iltimos, qaytdan kiritng")
    await state.update_data(first_name=message.text)
    await message.answer("Familiyangizni kiriting:")
    await state.set_state(RegisterUserFSM.last_name)


@router2.message(RegisterUserFSM.last_name)
async def get_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Telefon raqamingizni ulashing:", reply_markup=phone_keyboard)
    await state.set_state(RegisterUserFSM.phone)


@router2.message(RegisterUserFSM.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if not message.contact or not message.contact.phone_number:
        return await message.answer("❌ Telefon raqamini tugma orqali yuboring.", reply_markup=phone_keyboard)

    phone_number = message.contact.phone_number

    if not re.match(r"^\+?998\d{9}$", phone_number):
        return await message.answer("❌ Telefon raqam noto‘g‘ri formatda. Iltimos, qaytadan yuboring.")

    if not phone_number.startswith("+"):
        phone_number = f"+{phone_number}"

    await state.update_data(phone=phone_number)
    await message.answer("📧 Email manzilingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegisterUserFSM.email)


@router2.message(RegisterUserFSM.email)
async def get_email(message: types.Message, state: FSMContext):
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", message.text):
        return await message.answer("❌ Email noto‘g‘ri formatda. Iltimos, qaytdan kiritng")
    await state.update_data(email=message.text)
    await message.answer("📍 Lokatsiyangizni yuboring quyidagi tugma orqali 👇", reply_markup=location_keyboard)
    await state.set_state(RegisterUserFSM.address)

@router2.message(RegisterUserFSM.address)
async def get_address(message: types.Message, state: FSMContext):
    if not message.location:
        return await message.answer("❌ Iltimos, manzilni 📍 Location tugmasi orqali yuboring.", reply_markup=location_keyboard)

    latitude = message.location.latitude
    longitude = message.location.longitude

    address = await get_address_from_coords(latitude, longitude)
    if not address:
        return await message.answer("❌ Manzilni aniqlab bo‘lmadi. Iltimos, qaytadan yuboring.")

    await state.update_data(address=address)

    data = await state.get_data()
    async with async_session() as session:
        await add_user(
            session=session,
            chat_id=message.from_user.id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=message.from_user.username,
            phone=data.get('phone'),
            email=data.get('email'),
            address=data.get('address')
        )

    await message.answer("✅ Ro‘yxatdan muvaffaqiyatli o‘tdingiz!", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


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
        @router2.callback_query(F.data == "edit_profile")
        async def user_update_start(callback: CallbackQuery, state: FSMContext):
            await callback.message.answer("Tahrirlamoqchi bo'lgan malumotingizni tanlang:", reply_markup=get_edit_profile_menu())

    else:
        await message.answer("👋 Salom! Ro‘yxatdan o‘tish uchun ismingizni kiriting:")
        await state.set_state(RegisterUserFSM.first_name)


@router2.message(Command("help"))
async def help_handler(message: Message):
    help_text = ("Iltimos, quyidagi malumotlarni ko'rish uchun /start buyrug'ini bosing!")
    await message.answer(help_text)







