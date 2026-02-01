from aiogram import F,Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.email_sender import email_sender
import app.keyboards as kb

router = Router()

class QuestionForm(StatesGroup):
    real_name = State()
    letter = State()
    email = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    file_media = 'media/arrow.png'
    
    await message.answer_photo(
        photo=FSInputFile(file_media),
        caption='<b>Снизу появились две кнопки.</b>\n\nВыбери один из подходящих вариантов.',
        parse_mode='HTML',
        reply_markup=kb.main
    )

@router.message(F.text == 'Задать вопрос')
async def handle_question(message: Message):
    file_media = 'media/support.png'

    await message.answer_photo(
        photo=FSInputFile(file_media),
        caption='<b>Здесь вы можете обратиться по любому вопросу.</b>\n\nТакже можете предложить партнерство или сотрудничество.\n\n<i>Чтобы связаться с вами нам понадобиться следующая информация: имя, Ваш вопрос или предложение, почта куда мы отправим ответ.</i>',
        parse_mode='HTML',
        reply_markup=kb.name
    )

@router.message(F.text == 'Поддержать')
async def handle_question(message: Message):
    file_media = 'media/donate.png'

    await message.answer_photo(
        photo=FSInputFile(file_media),
        caption='<b>Чтобы поддержать наш проект отправьте по этому адресу ниже любое количество TON.</b>\n\n<code>UQCldtav8_57fvU8fYUMWaKHJlbr7PgnzSMrbQJUSo3i64DP</code> \n\n<i>Как только мы наберем необходимое количество, будет выпущен токен.</i>\n\nБольшое спасибо, что поддерживаете наш проект!!!',
        parse_mode='HTML'
    )

@router.callback_query(F.data == 'name')
async def name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(QuestionForm.real_name)
    await callback.answer('')
    await callback.message.answer('Введите ваше имя(в случае если имя будет не корректным, письмо будет проигнорировано):')

@router.message(QuestionForm.real_name)
async def writing_a_letter(message: Message, state: FSMContext):
    await state.update_data(real_name=message.text)
    await state.set_state(QuestionForm.letter)
    await message.answer('Введите текст вопроса или предложения.')

@router.message(QuestionForm.letter)
async def input_email(message: Message, state: FSMContext):
    await state.update_data(letter=message.text)
    await state.set_state(QuestionForm.email)
    await message.answer('Введите вашу почту.')

@router.message(QuestionForm.email)
async def sending(message: Message, state: FSMContext):
    user_email = message.text.strip()
    await state.update_data(email=user_email)
    
    data = await state.get_data()
    
    user_real_name = data.get('real_name', 'НЕТ')
    user_letter = data.get('letter', 'НЕТ')
    user_email = data.get('email', 'НЕТ')
    
    # Показываем, что отправляем
    await message.answer("⏳ Отправляем ваше письмо...")
    
    # Отправляем на вашу почту
    success, result_message = await email_sender.send_email(
    name=user_real_name,      
    user_email=user_email,   
    message=user_letter       
    )
    
    if success:
        await message.answer(
            f"✅ <b>Ваше письмо отправлено!</b>\n\n"
            f"<b>Имя:</b> {user_real_name}\n"
            f"<b>Ваша почта:</b> {user_email}\n\n"
            "Мы ответим вам в ближайшее время.",
            parse_mode='HTML'
        )
    else:
        await message.answer(
            f"❌ <b>Ошибка отправки:</b>\n{result_message}\n\n"
            "Попробуйте позже или свяжитесь другим способом.",
            parse_mode='HTML'
        )


    await state.clear()