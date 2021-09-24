import os
import requests
from flask import Flask, request
import time
import re
import random, string
import telebot
from telebot import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from random import sample
from config import Config
import normaltext
import buttons

TOKEN = Config.BOT_TOKEN
bot = telebot.TeleBot(token=TOKEN)#,parse_mode="HTML")
server = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credential.json", scope)
client = gspread.authorize(creds)
ak = client.open(Config.sheetname)
sheet1 = ak.worksheet(Config.sheetA)
sheet2 = ak.worksheet(Config.sheetB)

class User:
    def __init__(self, header):
        self.header = header
        self.pic = pic

cancellist = ["🚫 Cancel","/start"]

@bot.inline_handler(lambda query: True)
def query_text(query):
  ak = query.query
  if f"{ak}" == "":
    try:
      print(ak)
      r = types.InlineQueryResultArticle('1', 'Click Here tho Share', types.InputTextMessageContent(normaltext.sharetext,parse_mode="HTML"))
      bot.answer_inline_query(query.id, [r])
    except Exception as e:
      print(e)
  else:
    print("Query Not Defined")

@bot.message_handler(commands=['start'])
def wlcm(m):
  id = m.chat.id
  cells = sheet2.findall(f"{id}")
  if len(cells) > 0:
    print("Updating")
  else:
    h = sheet2.get('A1000').first()
    h1 = int(h) + 1
    max = "=MAX(A1:A19)"
    sheet2.update_cell(int(h1),1 ,f"{h1}")
    sheet2.update_cell(int(h1),2 ,id)
    sheet2.update_cell(int(h1),3 ,"0")
  usrlnk = f"<a href='tg://user?id={m.chat.id}'>{m.from_user.first_name}</a>"
  bot.send_message(m.chat.id,text=normaltext.welcome.format(usrlnk),reply_markup = buttons.Wlcmbtn.key,parse_mode="HTML")

@bot.message_handler(commands=['admin'])
def admincmd(m):
  Id = m.chat.id
  if int(Id) in Config.admins:
    bot.send_message(m.chat.id,text=normaltext.adminpnl,parse_mode="HTML")#,reply_markup=key)
  else:
    bot.delete_message(m.chat.id,m.message_id)
    ak = bot.send_message(m.chat.id,text=normaltext.nonadminpnl,parse_mode="HTML")
    time.sleep(5)
    bot.delete_message(m.chat.id,ak.message_id)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
  if call.data == "hlp":
    bot.edit_message_text(chat_id = call.message.chat.id,text=f"{normaltext.HelpText}",message_id=call.message.id,reply_markup=buttons.HlpBtn.key,parse_mode="HTML")
  if call.data == "backtohome":
    usrlnk = f"<a href='tg://user?id={call.message.chat.id}'>{call.from_user.first_name}</a>"
    bot.edit_message_text(chat_id = call.message.chat.id,text=f"<b>{normaltext.welcome.format(usrlnk)}</b>",message_id=call.message.id,reply_markup=buttons.Wlcmbtn.key,parse_mode="HTML")
  if call.data == "strtDevEdt":
    bot.edit_message_text(chat_id = call.message.chat.id,text=f"<b>{normaltext.dvlprText.format(normaltext.botUsername,call.message.from_user.first_name)}</b>",message_id=call.message.id,reply_markup=buttons.DevBtn.key,parse_mode="HTML")
  if call.data == "chnladd":
    ak = bot.send_message(chat_id = call.message.chat.id,text=normaltext.ReisterStepA,reply_markup=buttons.CancelKey.keyboard,parse_mode="HTML")
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.id)
    bot.register_next_step_handler(ak, channeladd1)
  if call.data == "mychnl":
    try:
      userid = call.message.chat.id
      ak = client.open(Config.sheetname)
      sheetyyy = ak.worksheet(f"{userid}")
      ttlvhnl = sheetyyy.get('A11').first()
      mid = call.message.message_id
      values_list1 = sheetyyy.col_values(2)
      values_list2 = sheetyyy.col_values(3)
      values_list3 = sheetyyy.col_values(4)
      keyboard = types.InlineKeyboardMarkup()
      for i1,i2,i3 in zip(values_list1,values_list2,values_list3):
        man_detail3 = i1.strip()
        man_detail1 = i2.strip()
        #This interchange bcz i take the channel id as indentifier
        man_detail2 = i3.strip()
        callback_btn1 = types.InlineKeyboardButton(text=man_detail1, callback_data="['key', '" + man_detail3 + "']")
        callback_btn2 = types.InlineKeyboardButton(text=man_detail2, callback_data="['remove', '" + man_detail3 + "']")
        keyboard.add(callback_btn1,callback_btn2)
      keyboard.add(buttons.btnhome)
      mid = call.message.message_id
      bot.edit_message_text(chat_id = f"{userid}",text = "<b>Your registered channels are here✅</b>",message_id=call.message.id,reply_markup = keyboard,parse_mode="HTML")
    except Exception as e:
      print(e)
      bot.edit_message_text(chat_id = call.message.chat.id,text = normaltext.NotanyChnl,message_id=call.message.id,reply_markup = buttons.Ntanychnl.key,parse_mode="HTML")

def channeladd1(m):
  if f"{m.text}" in cancellist:
    qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
    bot.delete_message(chat_id=m.chat.id,message_id=qk.id)
    bot.send_message(m.chat.id,text="<b>🤷Operation Cancelled. /start Again</b>",reply_markup=buttons.OrtnCancel.key,parse_mode="HTML")
  else:
    try:
      Ttype = m.forward_from_chat.type
      chnlid =  m.forward_from_chat.id
      adminid = m.chat.id
      celluy = sheet2.find(f"{adminid}")
      cellurowy = celluy.row
      cellidy = "D" + f"{cellurowy}"
      sheet2.update(cellidy,chnlid)
      try:
        a=bot.send_message(chat_id=chnlid,text="This is test message",parse_mode="HTML")
        msgid = a.id
        bot.delete_message(chnlid,msgid)
        qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
        bot.delete_message(chat_id=m.chat.id,message_id=qk.id)
        cellsp = sheet1.findall(f"{chnlid}")
        if len(cellsp) > 0:
          bot.send_message(m.chat.id,text =normaltext.ChnlAlrdyInDTbse,reply_markup=buttons.Ntanychnl.key,parse_mode="HTML")
        else:
          subcount= bot.get_chat_members_count(chat_id=chnlid)
          Min = normaltext.MaxLimitUser
          if int(subcount) >= int(Min):
            chnlname = m.forward_from_chat.title
            chnlusername = m.forward_from_chat.username
            ak = client.open(Config.sheetname)
            try:
              sheetxx = ak.worksheet(f"{adminid}")
            except:
              worksheet = ak.add_worksheet(title=f"{adminid}", rows="11", cols="5")
              sheetxx = ak.worksheet(f"{adminid}")
              max = "=MAX(A1:A10)"
              sheetxx.update_cell(11,1, max)
            h = sheetxx.get('A11').first()
            h1 = int(h) + 1
            sheetxx.update_cell(int(h1),1 ,f"{h1}")
            sheetxx.update_cell(int(h1),2 ,f"{chnlid}")
            sheetxx.update_cell(int(h1),3 ,f"{chnlname}")
            sheetxx.update_cell(int(h1),4 ,"⛔")
            sheetxx.update_cell(int(h1),5 ,f"akh{h1}")
            j = sheet1.get('A1000').first()
            j1 = int(j) + 1
            sheet1.update_cell(int(j1),1 ,f"{j1}")
            sheet1.update_cell(int(j1),2 ,f"{chnlid}")
            sheet1.update_cell(int(j1),3 ,f"{chnlname}")
            sheet1.update_cell(int(j1),4 ,f"@{chnlusername}")
            sheet1.update_cell(int(j1),5 ,"")
            sheet1.update_cell(int(j1),6 ,f"{subcount}")
            sheet1.update_cell(int(j1),7 ,f"{adminid}")
            m = bot.send_message(m.chat.id,text = "<b>Send private link of your channel</b>",reply_markup=buttons.CancelKey.keyboard,parse_mode="HTML")
            bot.register_next_step_handler(m,addlink)
          else:
            ak = bot.send_message(m.chat.id,text=normaltext.NotEnfSub.format(subcount),reply_markup=buttons.Ntanychnl.key,parse_mode="HTML")
      except:
        ak = bot.send_message(m.chat.id,text="<b>Error:</b> <code>Please authrise me with the rights of Post & Delete and Forward The Post Again. Please Try Again</code>",parse_mode="HTML")
        bot.register_next_step_handler(ak, channeladd1)
    except:
      ak = bot.send_message(m.chat.id,text="<b>This message is not forwarded from channel. Please Try Again</b>",parse_mode="HTML")
      bot.register_next_step_handler(ak, channeladd1)

def addlink(m):
  lnk = m.text
  admnid = m.chat.id
  cellu = sheet2.find(f"{admnid}")
  cellurow = cellu.row
  cellid = "D" + f"{cellurow}"
  chnldid = sheet2.get(cellid).first()
  cellucc = sheet1.find(chnldid)
  cellurowcc = cellucc.row
  if f"{lnk}" in cancellist:
    ak = client.open(Config.sheetname)
    sheetyyy = ak.worksheet(f"{admnid}")
    celluccuser = sheetyyy.find(chnldid)
    cellurowuser = celluccuser.row
    cell_list = sheetyyy.range(f"A{cellurowuser}:E{cellurowuser}")
    for cell in cell_list:
      cell.value = ''
      sheetyyy.update_cells(cell_list)
    qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
    bot.delete_message(chat_id=m.chat.id,message_id=qk.id)
    bot.send_message(m.chat.id,text="<b>🤷Operation Cancelled. /start Again</b>",reply_markup=buttons.OrtnCancel.key,parse_mode="HTML")
    cell_list1 = sheet1.range(f"A{cellurowcc}:H{cellurowcc}")
    for cell in cell_list1:
      cell.value = ''
      sheet1.update_cells(cell_list1)
  else:
    myre = '^(http|https|t.me)://'
    if re.search(myre,lnk):
      cellidc = "E" + f"{cellurowcc}"
      chnlnamex = "C" + f"{cellurowcc}"
      chnlname1 = sheet1.get(chnlnamex).first()
      sheet1.update(cellidc,lnk)
      bot.send_message(m.chat.id,text=normaltext.ChnlAdSucess.format(lnk,chnlname1),disable_web_page_preview=True,reply_markup=buttons.Sucessaddchnl.key,parse_mode="HTML")
    else:
      ak = bot.send_message(m.chat.id,text="<b>channel link is not valid,Please Send Me Link Again</b>",parse_mode="HTML")
      bot.register_next_step_handler(ak, addlink)
  ak = client.open(Config.sheetname)
  sheetyyy1 = ak.worksheet(f"{admnid}")
  h = sheetyyy1.get('A11').first()
  if int(h) == 0:
    ak.del_worksheet(sheetyyy1)
  else:
    print("..")

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
 
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://' + Config.app + '.herokuapp.com/' + f"{TOKEN}")
    return "!", 200
 
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
