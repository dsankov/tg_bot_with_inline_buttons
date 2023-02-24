from aiogram.dispatcher import Dispatcher
from aiogram import types
from icecream import ic
from button_bot.callback_datas import cell_CallbackData
from button_bot.keyboards.reversi_board import get_game_board

def register_callback_handlers(dp: Dispatcher):

    dp.register_callback_query_handler(
        process_cell_pressed, 
        cell_CallbackData.filter()
        )




# @dp.callback_query_handler(cell_CallbackData.filter())
async def process_cell_pressed(callback_query: types.CallbackQuery, callback_data: dict):

    y = callback_data['y']
    x = callback_data['x']
    ic(callback_data)
    # game_board[int(y)][int(x)] = 1
    
    await callback_query.message.edit_text(
        text=f"pressed cell: {y}, {x}",
        reply_markup=get_game_board()
        )

    await callback_query.answer()


# @dp.errors_handler(exception=MessageNotModified)
async def board_not_modified_handler(update, error):
    return True

