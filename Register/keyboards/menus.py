from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_user_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Profilim", callback_data="my_profile"),
            InlineKeyboardButton(text="✏️ Tahrirlash", callback_data="edit_profile")
        ],
        [
            InlineKeyboardButton(text="🗑 O'chirish", callback_data="delete_profile")
        ]
    ])


def get_admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Foydalanuvchi qo‘shish", callback_data="admin_create"),
        InlineKeyboardButton(text="📋 Foydalanuvchilar ro'yxati", callback_data="admin_list")],
        [InlineKeyboardButton(text="✏️ Foydalanuvchini yangilash", callback_data="admin_update"),
        InlineKeyboardButton(text="❌ Foydalanuvchini o‘chirish", callback_data="admin_delete")],
        [InlineKeyboardButton(text="🔍 Foydalanuvchi qidirish", callback_data="admin_search")],

    ])

def get_edit_profile_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👨‍🦰 Ism", callback_data="edit_first_name"),
            InlineKeyboardButton(text="👨‍🦰 Familiya", callback_data="edit_last_name")
        ],
        [
            InlineKeyboardButton(text="📧 Email", callback_data="edit_email"),
            InlineKeyboardButton(text="🏠 Manzil", callback_data="edit_address")
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")
        ]
    ])


def get_back_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
    ])


def admin_edit_profile():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👨‍🦰 Ism", callback_data="a_edit_first_name"),
            InlineKeyboardButton(text="👨‍🦰 Familiya", callback_data="a_edit_last_name"),
            InlineKeyboardButton(text="📞 Telefon", callback_data="a_edit_phone")
        ],
        [
            InlineKeyboardButton(text="📧 Email", callback_data="a_edit_email"),
            InlineKeyboardButton(text="🏠 Manzil", callback_data="a_edit_address"),
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="a_back_to_menu")
        ],
    ])

