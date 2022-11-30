import requests
from bs4 import BeautifulSoup
import logging
from aiogram import Bot, Dispatcher, executor
import asyncio
import json

API_TOKEN="part1:part2"
# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def scheduled(sleep_time):
    txt = ""
    val_new = 0
    val_old = 0
    num = 0
    while True:
        await asyncio.sleep(sleep_time)
        a = requests.get("https://banks.az/servisler/valyuta-mezenneleri")
        soup = BeautifulSoup(a.content,"html.parser")
        res = soup.find('script', attrs={"id":"__NEXT_DATA__"})
        data = json.loads(res.next)
        try:
            for i in range (0,16):
                if data["props"]["initialReduxState"]["courses"]["courses"][i]["name"]=="VTB":
                    num = i
                    break
        except:
            pass
        txt += data["props"]["initialReduxState"]["courses"]["courses"][num]["name"]+":\n"
        txt +="Курс: "+str(float(data["props"]["initialReduxState"]["courses"]["courses"][num]["courses"]["1"]['list']["RUB"]["current"]["course"])*10000)+"\n"
        txt +=data["props"]["initialReduxState"]["courses"]["courses"][num]["courses"]["1"]['list']["RUB"]["current"]["data"]+" "+data["props"]["initialReduxState"]["courses"]["courses"][num]["courses"]["1"]['list']["RUB"]["current"]["time"]
        val_new = float(data["props"]["initialReduxState"]["courses"]["courses"][num]["courses"]["1"]['list']["RUB"]["current"]["course"])
        if val_new ==val_old:
            txt = ""
            pass
        else:
            val_old = val_new
            await bot.send_message(chat_id= 0,text=str(txt))
            txt = ""

@dp.message_handler(commands=['get'])
async def send_welcome(a):
    await bot.send_message(chat_id=0, text="Привет! Теперь тебе будет приходить курс рубля , когда будут изменения.")
    
        

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(600))
    while True:
        try:    
            executor.start_polling(dp, skip_updates=True)
        except:
            pass
