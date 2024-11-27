import asyncio
from random import randint

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from lib import api
import random

admin = [1001455143]  # Список ID администраторов
sova = [6174830065]

command_list = ['/start', '/stop', '/stats', '/casino']

stats = {'/casino': {0:0}}
for i in range(0, 37):
    stats['/casino'][i] = 0

bot = Bot(token=api)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! У вас есть доступ к этому боту.")

@dp.message(Command("stop"))
async def stop(message: Message):
    if message.from_user.id in admin:
        await message.answer("Бот остановлен. До свидания!")
        await bot.session.close()  # Закрываем сессию бота
        await dp.stop_polling()  # Останавливаем опрос
        raise SystemExit  # Завершаем программу
    else:
        await message.answer("Нельзя, я кусаюсь")  # Сообщение, если не админ
@dp.message(Command("stat"))
async def stat(message: Message, command: CommandObject):
    if message.from_user.id in admin:
        if command.args == None:
            await message.answer("Не написал для какой функции")
            return

        args = command.args.split()
        if args[0] not in list(stats.keys()):
            if args[0] in command_list:
                await message.answer("Статистики для этой команды не существует")
            else:
                await message.answer("Команда не найдена")
        else:
            await message.answer("См. консоль")
            print(stats[args[0]])

    else:
        await message.answer("Нельзя, я кусаюсь")  # Сообщение, если не админ


@dp.message(Command("casino"))
async def casino(message: Message, command: CommandObject):
    if command.args == None:
        await message.answer("Напишите ставку:\n красный для ставки на красное\n черный для ставки на черное\n зеленый для ставки на 0\n свое число для ставки на сове число")
        return

    args = command.args.split()
    rand = randint(0, 36)
    color = lambda x:'зеленый' if x == 0 else ('красный' if x % 2 == 0 else 'черный')
    print(message.text, message.from_user.id, rand)
    stats['/casino'][rand] += 1
    if len(args) == 0:
        await message.answer("Напишите ставку:\n красный для ставки на красное\n черный для ставки на черное\n зеленый для ставки на 0\n свое число для ставки на сове число")
        return
    if args[0].isdigit():
        if int(args[0]) >=37 or int(args[0]) <0:
            await message.answer("Некорректная ставка")
            return
        if int(args[0]) == rand:
            await message.answer(f"Ставка сыграла. Вы получили нифига, ибо админ еще не научил делать реальные ставки\nЧисло было {rand} - {color(rand)}")
        else:
                await  message.answer(f"Вы просрали ставку. Радуйтеся, ведь админ еще не научил делать ставки\nЧисло было {rand} - {color(rand)}")
    else:
        if args[0].lower() == "красный":
            if rand % 2 == 0 and rand != 0:
                await message.answer(f"Ставка сыграла. Вы получили нифига, ибо админ еще не научил делать реальные ставки\nЧисло было {rand} - {color(rand)}")
            else:
                await  message.answer(f"Вы просрали ставку. Радуйтеся, ведь админ еще не научил делать ставки\nЧисло было {rand} - {color(rand)}")
        elif args[0].lower() == "черный" or args[0].lower() == "чёрный":
            if rand % 2 == 1:
                await message.answer(f"Ставка сыграла. Вы получили нифига, ибо админ еще не научил делать реальные ставки\nЧисло было {rand} - {color(rand)}")
            else:
                await  message.answer(f"Вы просрали ставку. Радуйтеся, ведь админ еще не научил делать ставки\nЧисло было {rand} - {color(rand)}")
        elif args[0].lower() == "зеленый" or args[0].lower() == 'зелёный':
            if rand == 0:
                await message.answer(f"Ставка сыграла. Вы получили нифига, ибо админ еще не научил делать реальные ставки\nЧисло было {rand} - {color(rand)}")
            else:
                await  message.answer(f"Вы просрали ставку. Радуйтеся, ведь админ еще не научил делать ставки\nЧисло было {rand} - {color(rand)}")
        else:
            await message.answer("Некорректная ставка")
            return

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
