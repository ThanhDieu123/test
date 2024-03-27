import telegram


    
my_token = "6189869386:AAHIb6rcUzj43T3NQeo0_znrq2RbbMdUuzQ"
bot = telegram.Bot(token=my_token)
bot.sendPhoto(chat_id="6231784055", photo=open("alert.png", "rb"), caption="Có xâm nhập, nguy hiêm!")
    

 