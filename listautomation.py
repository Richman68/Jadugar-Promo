import time
from telebot import types


catApostTimeExmaple = '''<b>Schedule sending</b>
When you want the post to be sent?

Send me your Timings in given format <code>YYYY-MM-DD HH:MM:SS</code> In IST STANDARD Time and Use 24 Hrs Format.

Examples: <b>2021-10-12 22:30:00</b>'''

catBpostTimeExmaple = '''B <b>Schedule sending</b>
When you want the post to be sent?

Send me your Timings in given format <code>DD/MM/YYYY HH:MM:SS</code> In IST STANDARD Time and Use 24 Hrs Format.
Examples: <b>06/09/16 22:30:00</b>'''

catCpostTimeExmaple = '''<b>Schedule sending For Everyday</b>
When you want the post to be sent?

Send me your Timings in given format <code>HH:MM:SS</code> In IST STANDARD Time and Use 24 Hrs Format.
Examples: <b>22:30:00</b>

<b>Note:-</b> <i> For multiple timings use new line</i>'''

class Lidtautocatg:
  key = types.InlineKeyboardMarkup()
  #key.add(btnaddcnnl,btnmychnl)

cat1Y = types.InlineKeyboardButton("✅ On DD/MM/YYYY At HH:MM:SS",callback_data="['autolist', '" + "cat1" + "']")
cat1N = types.InlineKeyboardButton("On DD/MM/YYYY At HH:MM:SS",callback_data="['autolist', '" + "cat1" + "']")
cat2Y = types.InlineKeyboardButton("✅ Every DAYNAME At HH:MM:SS X Times",callback_data="['autolist', '" + "cat2" + "']")
cat2N = types.InlineKeyboardButton("Every DAYNAME At HH:MM:SS X Times",callback_data="['autolist', '" + "cat2" + "']")
cat3Y = types.InlineKeyboardButton("✅ Everyday X Time From HH:MM:SS At Interval of HH:MM:SS Time",callback_data="['autolist', '" + "cat3" + "']")
cat3N = types.InlineKeyboardButton("Everyday X Time From HH:MM:SS At Interval of HH:MM:SS Time",callback_data="['autolist', '" + "cat3" + "']")
backtolistadmi = types.InlineKeyboardButton("🔙",callback_data="listopt")
BacktoListautopost = types.InlineKeyboardButton(text=" 🔙 ", callback_data="lstautomation")


def autopostingtimings(markup,valueFromCallBack,currenttimer):
  Resettimng = types.InlineKeyboardButton("🚨 Reset Timings",callback_data="['resettimngpost', '" + valueFromCallBack + "']")
  UpdateTimings = types.InlineKeyboardButton(text=" 🔄 Update Timings ", callback_data="['updatetimings', '" + valueFromCallBack + "']")
  if f"{currenttimer}" == "Not Set Yet":
    markup.add(UpdateTimings)
  else:
    #markup.add(UpdateTimings,Resettimng)
    markup.add(Resettimng)
  markup.add(BacktoListautopost)
  return markup
  
def autopostingbutton(markup,AutoPostingcatf):
  row = []
  if f"{AutoPostingcatf}"  == "cat1":
    row.append(cat1Y)
  else:
    row.append(cat1N)
  if f"{AutoPostingcatf}"  == "cat2":
    row.append(cat2Y)
  else:
    row.append(cat2N)
  if f"{AutoPostingcatf}"  == "cat3":
    row.append(cat3Y)
  else:
    row.append(cat3N)
  markup.add(*row)
  markup.add(backtolistadmi)
  return markup