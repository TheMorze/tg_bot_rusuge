# Основной файл с ботом

import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import user_handlers, stresses_handlers, \
                     prototypes_handlers, \
                     other_handlers, settings_handlers, \
                     statistics_handlers
                     
from database.database import Database

from config_data.menu import set_main_menu
from aiogram.fsm.storage.redis import RedisStorage, Redis

# Инициализация логгера
logger = logging.getLogger(__name__)

# Функция конфигурации и запуска бота
async def main() -> None:
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s ' \
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    
    logger.info('Starting bot')
    
    config: Config = load_config()
    
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    redis = Redis(host='localhost')
    dp = Dispatcher(redis=redis)
    
    Database.create_tables()
    
    dp.include_router(user_handlers.router)
    dp.include_router(settings_handlers.router)
    dp.include_router(statistics_handlers.router)
    dp.include_router(stresses_handlers.router)
    dp.include_router(prototypes_handlers.router)
    dp.include_router(other_handlers.router)
    
    # Запускаем функцию настройки меню с командами
    await set_main_menu(bot)
    
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    
    asyncio.run(main())