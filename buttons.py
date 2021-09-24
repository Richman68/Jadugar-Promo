
from telebot import types

btnaddcnnl = types.InlineKeyboardButton(text=" ➕ ADD CHANNEL ", callback_data="chnladd")
btnmychnl = types.InlineKeyboardButton(text=" 🗂️ MY CHANNELS ", callback_data="mychnl")
btnbotstatus= types.InlineKeyboardButton(text=" 📊 Bot Status ", callback_data="btstts")
btnhelp = types.InlineKeyboardButton(text=" 🆘 Help  ", callback_data="hlp")
btnshrebot = types.InlineKeyboardButton(text="🔄 Share Bot  ", switch_inline_query="")
btnabtdev = types.InlineKeyboardButton("About Dev ❤️", callback_data="strtDevEdt")
btnhome = types.InlineKeyboardButton(" 🔙 ", callback_data="backtohome")
btncncl = types.KeyboardButton('🚫 Cancel')

class Wlcmbtn:
  key = types.InlineKeyboardMarkup()
  key.add(btnaddcnnl,btnmychnl)
  key.add(btnhelp,btnabtdev)
  key.add(btnshrebot)

class HlpBtn:
  key = types.InlineKeyboardMarkup()
  key.add(btnaddcnnl,btnmychnl)
  key.add(btnhome,btnabtdev)
  key.add(btnshrebot)

class DevBtn:
  key = types.InlineKeyboardMarkup()
  key.add(btnaddcnnl,btnmychnl)
  key.add(btnhelp,btnhome)
  key.add(btnshrebot)
class Sucessaddchnl:
  key = types.InlineKeyboardMarkup()
  key.add(btnaddcnnl,btnmychnl)
  
class OrtnCancel:
  key = types.InlineKeyboardMarkup()
  key.add(btnhome)

class CancelKey:
  keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
  keyboard.add(btncncl)

class RmvKeyBrd:
  key = types.ReplyKeyboardRemove()
  
class Ntanychnl:
  key = types.InlineKeyboardMarkup()
  key.add(btnaddcnnl,btnhome)
  
  
