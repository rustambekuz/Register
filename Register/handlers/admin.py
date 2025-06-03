from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.types import Message
from sqlalchemy import select, update
from Register.db.sqlalchemy_db import Users
from aiogram import types
import re

from Register.handlers.user_crud import get_all_users, add_user, search_users_by_name
from Register.keyboards.menus import admin_edit_profile, get_admin_menu, get_user_menu

admin_router = Router()


class RegisterState(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    email = State()
    address = State()


class AdminSearchUserFSM(StatesGroup):
    search_name = State()


class AdminUpdateUserFSM(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()


class AdminDeleteUserFSM(StatesGroup):
      delete_user_id = State()


# Register new user
@admin_router.callback_query(F.data == "admin_create")
async def admin_create_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegisterState.first_name)
    await callback.message.answer("Ismini kiriting:")
    await callback.answer(cache_time=60)



@admin_router.message(RegisterState.first_name)
async def register_first_name(message: types.Message, state: FSMContext):
    if not re.match(r"^[A-Za-zА-Яа-яʻғқўҳ\s]{2,30}$", message.text):
        return await message.answer("❌ Ism noto‘g‘ri formatda. Iltimos, qaytdan kiritng")
    await state.update_data(first_name=message.text)
    await state.set_state(RegisterState.last_name)
    await message.answer("Familiyasini kiriting:")



@admin_router.message(RegisterState.last_name)
async def register_last_name(message: types.Message, state: FSMContext):
    if not re.match(r"^[A-Za-zА-Яа-яʻғқўҳ\s]{2,30}$", message.text):
        return await message.answer("❌ Familiya noto‘g‘ri formatda. Iltimos, faqat harflardan iborat familiya kiriting.")
    await state.update_data(last_name=message.text)
    await state.set_state(RegisterState.phone)
    await message.answer("Telefon raqamini kiriting (masalan, +998901234567):")


@admin_router.message(RegisterState.phone)
async def register_phone(message: types.Message, state: FSMContext):
    if not re.match(r"^\+998\d{9}$", message.text):
        return await message.answer("❌ Telefon raqami noto‘g‘ri. Formati: +998901234567")
    await state.update_data(phone=message.text)
    await state.set_state(RegisterState.email)
    await message.answer("Email manzilini kiriting:")


@admin_router.message(RegisterState.email)
async def register_email(message: types.Message, state: FSMContext):
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", message.text):
        return await message.answer("❌ Email noto‘g‘ri formatda. Masalan: test@mail.com")
    await state.update_data(email=message.text)
    await state.set_state(RegisterState.address)
    await message.answer("Yashash manzilini kiriting:")

from Register.db.sqlalchemy_db import async_session


@admin_router.message(RegisterState.address)
async def process_address(message: Message, state: FSMContext):
    if not re.match(r"^.{5,100}$", message.text):
        return await message.answer("❌ Manzil xato formatda, Iltimos qaytadan kiriting.")
    await state.update_data(address=message.text)
    data = await state.get_data()

    async with async_session() as session:
        await add_user(
            session=session,
            chat_id=None,
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=message.from_user.username,
            phone=data.get('phone'),
            email=data.get('email'),
            address=data.get('address'),
        )

    await message.answer("✅ Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi!")
    await state.clear()


#foydalanuvchi qidirish
@admin_router.callback_query(F.data == "admin_search")
async def admin_search_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🔍 Foydalanuvchi qidirish uchun ID kiriting:")
    await state.set_state(AdminSearchUserFSM.search_name)
    await callback.answer(cache_time=60)


@admin_router.message(AdminSearchUserFSM.search_name)
async def process_search_name(message: Message, state: FSMContext):
    search_name = message.text
    async with async_session() as session:
        users = await search_users_by_name(session, search_name)
        if users:
            users_text = "\n".join([f"ID:{user.id}.  {user.first_name} {user.last_name}" for user in users])
        else:
            users_text = "Foydalanuvchilar topilmadi."
        await message.answer(f"🔍 Qidiruv natijalari:\n{users_text}")
    await state.clear()


# barcha foydalanuvchilar ro'yxati
@admin_router.callback_query(F.data == "admin_list")
async def admin_list_handler(callback: CallbackQuery):
    async with async_session() as session:
        users = await get_all_users(session)
        if users:
            users_text = "\n".join([f"ID:{user.id}\n{user.first_name} {user.last_name}" for user in users])
        else:
            users_text = "Foydalanuvchilar topilmadi."
        await callback.message.answer(f"📋 Barcha foydalanuvchilar ro‘yxati:\n{users_text}")
    await callback.answer(cache_time=60)


# admin user update
@admin_router.callback_query(F.data == "admin_update")
async def admin_update_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🆔 Tahrirlamoqchi bo‘lgan foydalanuvchining ID sini yuboring:")
    await state.set_state(AdminUpdateUserFSM.step1)
    await callback.answer(cache_time=60)



@admin_router.message(AdminUpdateUserFSM.step1)
async def admin_receive_user_id(message: Message, state: FSMContext):
    async with async_session() as session:
        user_id = message.text

        if not user_id.isdigit():
            await message.answer("❗️ Iltimos, faqat raqamli ID kiriting.")
            return

        result = await session.execute(select(Users).where(Users.id == int(user_id)))
        user = result.scalar()

        if not user:
            await message.answer("😕 Bunday ID ga ega foydalanuvchi topilmadi.")
            return

        await state.update_data(user_id=int(user_id))

        await message.answer("✏️ Qaysi malumotni tahrirlaysiz tanlang?", reply_markup=admin_edit_profile())
        await state.set_state(AdminUpdateUserFSM.step2)

@admin_router.callback_query(AdminUpdateUserFSM.step2)
async def admin_field_choice(callback: CallbackQuery, state: FSMContext):
    field_map = {
        "a_edit_first_name": "first_name",
        "a_edit_last_name": "last_name",
        "a_edit_phone": "phone",
        "a_edit_email": "email",
        "a_edit_address": "address"
    }

    field_key = callback.data

    if field_key == "a_back_to_menu":
        await callback.message.edit_text("Asosiy admin menyu:", reply_markup=get_admin_menu())
        await state.clear()
        return

    field = field_map.get(field_key)
    if field is None:
        await callback.answer("⚠️ Noto‘g‘ri tanlov.")
        return

    await state.update_data(field=field)
    await callback.message.answer(f"✍️ Yangi qiymatni yuboring ({field.replace('_', ' ').capitalize()}):")
    await state.set_state(AdminUpdateUserFSM.step3)
    await callback.answer(cache_time=60)



@admin_router.message(AdminUpdateUserFSM.step3)
async def admin_update_field(message: Message, state: FSMContext):
    async with async_session() as session:
        data = await state.get_data()
        user_id = data["user_id"]
        field = data["field"]
        new_value = message.text

        await session.execute(update(Users).where(Users.id == user_id).values({field: new_value}))
        await session.commit()

        await message.answer(f"✅ {field.replace('_', ' ').capitalize()} yangilandi.")
        await message.answer("✏️ Yana nimani tahrirlaysiz?", reply_markup=admin_edit_profile())
        await state.set_state(AdminUpdateUserFSM.step2)


@admin_router.callback_query(F.data == "admin_delete")
async def admin_delete_user(callback: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        await callback.message.answer("🆔 O‘chirmoqchi bo‘lgan foydalanuvchining ID sini yuboring:")
        await state.set_state(AdminDeleteUserFSM.delete_user_id)
        await callback.answer(cache_time=60)

@admin_router.message(AdminDeleteUserFSM.delete_user_id)
async def admin_delete_user_id(message: Message, state: FSMContext):
    async with async_session() as session:
        user_id = message.text.strip()

        if not user_id.isdigit():
            await message.answer("❗️ Iltimos, faqat raqamli ID kiriting.")
            return

        result = await session.execute(select(Users).where(Users.id == int(user_id)))
        user = result.scalar_one_or_none()

        if not user:
            await message.answer("😕 Bunday ID ga ega foydalanuvchi topilmadi.")
            return

        await session.delete(user)
        await session.commit()

        await message.answer(f"✅ Foydalanuvchi (ID: {user_id}) muvaffaqiyatli o‘chirildi.")
        await state.clear()






