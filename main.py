import os
import requests
from flask import Flask, request
import time
import re
import ast
import random, string
import telebot
from telebot import types
from telebot import util
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from random import sample
from config import Config
import normaltext
import buttons
import demoji
import emojis
import markdown


TOKEN = Config.BOT_TOKEN
bot = telebot.TeleBot(token=TOKEN)#,parse_mode="HTML")
server = Flask(__name__)


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credential.json", scope)
client = gspread.authorize(creds)
ak = client.open(Config.sheetname)
sheet1 = ak.worksheet(Config.sheetA)
sheet2 = ak.worksheet(Config.sheetB)
sheet3 = ak.worksheet(Config.sheetC)

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
      r = types.InlineQueryResultArticle('1', 'Click Here tho Share', types.InputTextMessageContent(normaltext.sharetext.format(Config.botUsername),parse_mode="HTML"))
      bot.answer_inline_query(query.id, [r])
    except Exception as e:
      print(e)
  else:
    print("Query Not Defined")

@bot.message_handler(commands=['update_Chnl_Data'])
def updatedata(m):
  bot.delete_message(m.chat.id,m.message_id)
  ak = bot.send_message(m.chat.id,text=normaltext.updateChnlData,parse_mode="HTML")
  time.sleep(5)
  bot.delete_message(m.chat.id,ak.message_id)
  
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
  am = bot.send_message(m.chat.id,text="⏳",reply_markup=buttons.RmvKeyBrd.key)
  bot.delete_message(chat_id=m.chat.id,message_id=am.message_id)

@bot.message_handler(commands=['admin'])
def admincmd(m):
  Id = m.chat.id
  if int(Id) in Config.admins:
    bot.send_message(m.chat.id,text=normaltext.adminpnl,parse_mode="HTML",reply_markup=buttons.AdminMenu.key)
  else:
    bot.delete_message(m.chat.id,m.message_id)
    ak = bot.send_message(m.chat.id,text=normaltext.nonadminpnl,parse_mode="HTML")
    time.sleep(5)
    bot.delete_message(m.chat.id,ak.message_id)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
  if call.data == "hlp":
    bot.edit_message_text(chat_id = call.message.chat.id,text=f"{normaltext.HelpText}",message_id=call.message.message_id,reply_markup=buttons.HlpBtn.key,parse_mode="HTML")
  if call.data == "backtohome":
    usrlnk = f"<a href='tg://user?id={call.message.chat.id}'>{call.from_user.first_name}</a>"
    bot.edit_message_text(chat_id = call.message.chat.id,text=f"<b>{normaltext.welcome.format(usrlnk)}</b>",message_id=call.message.message_id,reply_markup=buttons.Wlcmbtn.key,parse_mode="HTML")
  if call.data == "strtDevEdt":
    bot.edit_message_text(chat_id = call.message.chat.id,text=f"<b>{normaltext.dvlprText.format(Config.botUsername,call.message.from_user.first_name)}</b>",message_id=call.message.message_id,reply_markup=buttons.DevBtn.key,parse_mode="HTML")
  if call.data == "chnladd":
    ak = bot.send_message(chat_id = call.message.chat.id,text=normaltext.ReisterStepA,reply_markup=buttons.CancelKey.keyboard,parse_mode="HTML")
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    bot.register_next_step_handler(ak, channeladd1)
  if call.data == "mychnl":
    try:
      userid = call.message.chat.id
      ak = client.open(Config.sheetname)
      sheetyyy = ak.worksheet(f"{userid}")
      sheetyyy.sort((2, 'des'),range='A1:E10')
      values_list5 = sheetyyy.col_values(2)
      while("" in values_list5):
        values_list5.remove("")
      total_count = len(values_list5)
      #print(total_count)
      for i in range(1,total_count+1):
        sheetyyy.update(f"A{i}",i)
        sheetyyy.update(f"E{i}",f"akh{i}")
      ttlvhnl = sheetyyy.get('A11').first()
      if int(ttlvhnl) >=1:
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
        bot.edit_message_text(chat_id = f"{userid}",text = "<b>Your registered channels are here✅</b>",message_id=call.message.message_id,reply_markup = keyboard,parse_mode="HTML")
      else:
        bot.edit_message_text(chat_id = call.message.chat.id,text = normaltext.NotanyChnl,message_id=call.message.message_id,reply_markup = buttons.Ntanychnl.key,parse_mode="HTML")
    except Exception as e:
      print(e)
      bot.edit_message_text(chat_id = call.message.chat.id,text = normaltext.NotanyChnl,message_id=call.message.message_id,reply_markup = buttons.Ntanychnl.key,parse_mode="HTML")
  if (call.data.startswith("['remove'")):
    valueFromCallBack = ast.literal_eval(call.data)[1]
    ak = client.open(Config.sheetname)
    userid = call.message.chat.id
    sheetyyy = ak.worksheet(f"{userid}")
    cells = sheetyyy.find(valueFromCallBack)
    print(cells)
    rowx = cells.row
    sheetyyy.batch_clear([f"A{rowx}:E{rowx}"])
    cnlcell = sheet1.find(valueFromCallBack)
    row1 = cnlcell.row
    sheet1.batch_clear([f"A{row1}:K{row1}"])
    h = sheetyyy.get('A11').first()
    if int(h) == 0:
      bot.edit_message_text(chat_id = call.message.chat.id,text = normaltext.NotanyChnl,message_id=call.message.message_id,reply_markup = buttons.Ntanychnl.key,parse_mode="HTML")
      ak.del_worksheet(sheetyyy)
    else:
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
      #bot.edit_message_text(chat_id = f"{userid}",text = "<b>Your registered channels are here✅</b>",message_id=call.message.message_id,reply_markup = keyboard,parse_mode="HTML")
      bot.edit_message_reply_markup(userid,mid,reply_markup = keyboard)
  if call.data == "useropt":
    bot.edit_message_text(chat_id = call.message.chat.id,text="<b>⚙️ Users Settings</b>",message_id=call.message.message_id,reply_markup=buttons.Adminuserpnl.key,parse_mode="HTML")
  if call.data == "chnlopt":
    bot.edit_message_text(chat_id = call.message.chat.id,text="<b>⚙️ Channels Settings</b>",message_id=call.message.message_id,reply_markup=buttons.Adminchnlpnl.key,parse_mode="HTML")
  if call.data == "listopt":
    bot.edit_message_text(chat_id = call.message.chat.id,text="<b>💠 List Options</b>",message_id=call.message.message_id,reply_markup=buttons.AdminListpnl.key,parse_mode="HTML")
  if call.data == "backadminhome":
    bot.edit_message_text(chat_id = call.message.chat.id,text=normaltext.adminpnl,message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.AdminMenu.key)
  if call.data == "vrfyusrs":
    values_list3 = sheet2.col_values(2)
    ttlusers = len(values_list3)
    while("" in values_list3):
      values_list3.remove("")
    i=0
    j=0
    ak = ""
    for p in values_list3:
      try:
        bot.send_chat_action(f"{p}", "typing")
        i+=1
      except Exception as e:
        j+=1
        ak+=f"/n{p} {e}"
    try:
      bot.send_message(call.message.chat.id,text=f"{ak}")
    except:
      bot.send_message(call.message.chat.id,text=f"All Users are Active")
    bot.send_message(call.message.chat.id,text=normaltext.usrststext.format(ttlusers,i,j),parse_mode="HTML")
  if call.data == "vrfychnls":
    values_list3 = sheet1.col_values(2)
    ttlusers = len(values_list3)
    while("" in values_list3):
      values_list3.remove("")
    i=0
    j=0
    ak = ""
    for p in values_list3:
      try:
        bot.send_chat_action(f"{p}", "typing")
        i+=1
      except Exception as e:
        j+=1
        ak+=f"/n{p} {e}"
    try:
      bot.send_message(call.message.chat.id,text=f"{ak}")
    except:
      bot.send_message(call.message.chat.id,text=f"All Channels are Active")
    bot.send_message(call.message.chat.id,text=normaltext.Chanlsststext.format(ttlusers,i,j),parse_mode="HTML")
  if call.data == "listtypeset":
    lisType = sheet3.get('B1').first()
    if f"{lisType}" == "clskUlist":
      bot.edit_message_text(chat_id = call.message.chat.id,text=normaltext.setlistType,message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.ClassicUListY.key)
    if f"{lisType}" == "clskNlist":
      bot.edit_message_text(chat_id = call.message.chat.id,text=normaltext.setlistType,message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.ClassicNListY.key)
    if f"{lisType}" == "Stndrdlist":
      bot.edit_message_text(chat_id = call.message.chat.id,text=normaltext.setlistType,message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.StandardListY.key)
    if f"{lisType}" == "Buttonlist":
      bot.edit_message_text(chat_id = call.message.chat.id,text=normaltext.setlistType,message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.ButtonListY.key)
  if call.data == "clskUnamelistN":
    sheet3.update("B1","clskUlist")
    bot.edit_message_text(chat_id = call.message.chat.id,text=normaltext.setlistType,message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.ClassicUListY.key)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True , text=normaltext.listtypesetalert)
  if call.data == "clskCnamelistN":
    sheet3.update("B1","clskNlist")
    bot.edit_message_text(chat_id = call.message.chat.id,text=normaltext.setlistType,message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.ClassicNListY.key)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True , text=normaltext.listtypesetalert)
  if call.data == "StandardlistN":
    sheet3.update("B1","Stndrdlist")
    bot.edit_message_text(chat_id = call.message.chat.id,text=normaltext.setlistType,message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.StandardListY.key)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True , text=normaltext.listtypesetalert)
  if call.data == "ButtonlistN":
    sheet3.update("B1","Buttonlist")
    bot.edit_message_text(chat_id = call.message.chat.id,text=normaltext.setlistType,message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.ButtonListY.key)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True , text=normaltext.listtypesetalert)
  if call.data == "clicknotagn":
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True , text="Wrong Click 😏")
  if call.data=="hdrspncr":
    hdrspcr = sheet3.get('B4').first()
    if f"{hdrspcr}" == "None":
      ak = bot.send_message(call.message.chat.id,text="Send me Header in HTML FORMAT")
      bot.register_next_step_handler(ak,updthdr)
    else:
      keyboard = types.InlineKeyboardMarkup()
      keyboard.add(types.InlineKeyboardButton(text="🔄 Update Header ", callback_data="updthdr"))
      keyboard.add(types.InlineKeyboardButton(text="❌ Close",callback_data = "clsewndw"))
      bot.send_message(call.message.chat.id,text=f"<b>Here is Header</b>\n\n{hdrspcr}",parse_mode="HTML",reply_markup=keyboard,disable_web_page_preview=True)
  if call.data=="updthdr":
    ak = bot.send_message(call.message.chat.id,text="Send me Header in HTML FORMAT")
    bot.register_next_step_handler(ak,updthdr)
  if call.data=="ftrspncr":
    hdrspcr = sheet3.get('B5').first()
    if f"{hdrspcr}" == "None":
      ak = bot.send_message(call.message.chat.id,text="Send me Footer in HTML FORMAT")
      bot.register_next_step_handler(ak,updtftr)
    else:
      keyboard = types.InlineKeyboardMarkup()
      keyboard.add(types.InlineKeyboardButton(text="🔄 Update Footer ", callback_data="updtftr"))
      keyboard.add(types.InlineKeyboardButton(text="❌ Close",callback_data = "clsewndw"))
      bot.send_message(call.message.chat.id,text=f"<b>Here is Footer</b>\n\n{hdrspcr}",parse_mode="HTML",reply_markup=keyboard,disable_web_page_preview=True)
  if call.data=="updtftr":
    ak = bot.send_message(call.message.chat.id,text="Send me Footer in HTML FORMAT")
    bot.register_next_step_handler(ak,updtftr)
  if call.data=="setemoji":
    hdrspcr = sheet3.get('B6').first()
    if f"{hdrspcr}" == "None":
      ak = bot.send_message(call.message.chat.id,text="Send me Emoji")
      bot.register_next_step_handler(ak,updtemoji)
    else:
      keyboard = types.InlineKeyboardMarkup()
      keyboard.add(types.InlineKeyboardButton(text="🔄 Update Emoji ", callback_data="updtemoji"))
      keyboard.add(types.InlineKeyboardButton(text="❌ Close",callback_data = "clsewndw"))
      bot.send_message(call.message.chat.id,text=f"<b>Here is Emoji</b>\n\n{hdrspcr}",parse_mode="HTML",reply_markup=keyboard)
  if call.data=="updtemoji":
    ak = bot.send_message(call.message.chat.id,text="Send me Emoji")
    bot.register_next_step_handler(ak,updtemoji)
  if call.data=="capty":
    sheet3.update("B12","Yes")
    userid = call.message.chat.id
    mid = call.message.message_id
    bot.edit_message_reply_markup(userid,mid,reply_markup = buttons.CaptsN.key)
  if call.data=="captn":
    sheet3.update("B12","No")
    userid = call.message.chat.id
    mid = call.message.message_id
    bot.edit_message_reply_markup(userid,mid,reply_markup = buttons.CaptsY.key)
  if call.data=="setcptn":
    hdrspcr = sheet3.get('B7').first()
    if f"{hdrspcr}" == "None":
      ak = bot.send_message(call.message.chat.id,text="Send me Caption In HTML Format")
      bot.register_next_step_handler(ak,updtcptn)
    else:
      keyboard = types.InlineKeyboardMarkup()
      captYN = sheet3.get('B12').first()
      keyboard = types.InlineKeyboardMarkup()
      if f"{captYN}" == "Yes":
        bot.send_message(call.message.chat.id,text=f"<b>Here is Caption</b>\n\n{hdrspcr}",parse_mode="HTML",reply_markup=buttons.CaptsY.key,disable_web_page_preview=True)
      else:
        bot.send_message(call.message.chat.id,text=f"<b>Here is Caption</b>\n\n{hdrspcr}",parse_mode="HTML",reply_markup=buttons.CaptsN.key,disable_web_page_preview=True)
  if call.data=="updtcptn":
    ak = bot.send_message(call.message.chat.id,text="Send me Caption In HTML Format")
    bot.register_next_step_handler(ak,updtcptn)
  if call.data=="updsubscdtn":
    ak = bot.send_message(call.message.chat.id,text="Send me Number of subscibers Required")
    bot.register_next_step_handler(ak,updtreqsub)
  if call.data=="mnmreqsubs":
    hdrspcr = sheet3.get('B13').first()
    if f"{hdrspcr}" == "None":
      ak = bot.send_message(call.message.chat.id,text="Send me Minimum Required Subscribe In chNnel in numbers")
      bot.register_next_step_handler(ak,updtreqsub)
    else:
      keyboard = types.InlineKeyboardMarkup()
      keyboard.add(types.InlineKeyboardButton(text="🔄 Update  Minimum Subscribers ", callback_data="updsubscdtn"))
      keyboard.add(types.InlineKeyboardButton(text="❌ Close",callback_data = "clsewndw"))
      bot.send_message(call.message.chat.id,text=f"<b>Here is Minimum Sub to add channel</b>\n\n{hdrspcr}",parse_mode="HTML",reply_markup=keyboard)
  if call.data=="chnlinalist":
    hdrspcr = sheet3.get('B10').first()
    if f"{hdrspcr}" == "None":
      ak = bot.send_message(call.message.chat.id,text="Send me No.of Channel in A list.")
      bot.register_next_step_handler(ak,updtchnlinalist)
    else:
      keyboard = types.InlineKeyboardMarkup()
      keyboard.add(types.InlineKeyboardButton(text="🔄 Update Channnels Number ", callback_data="updatechnlinalist"))
      keyboard.add(types.InlineKeyboardButton(text="❌ Close",callback_data = "clsewndw"))
      bot.send_message(call.message.chat.id,text=f"<b> No. of Total Channels In One List Is Now </b>\n\n{hdrspcr}",parse_mode="HTML",reply_markup=keyboard,disable_web_page_preview=True)
  if call.data=="updatechnlinalist":
    ak = bot.send_message(call.message.chat.id,text="Send me No. of Channel you want in one list")
    bot.register_next_step_handler(ak,updtchnlinalist)
  if call.data=="picy":
    #sheet3.update("B11","Yes")
    sheet3.update_cell(11, 2, 'Yes')
    userid = call.message.chat.id
    mid = call.message.message_id
    bot.edit_message_reply_markup(userid,mid,reply_markup = buttons.SponcerpicN.key)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True , text="Pic Will Be Added")
  if call.data=="picn":
    #sheet3.update("B11","No")
    sheet3.update_cell(11, 2, 'No')
    userid = call.message.chat.id
    mid = call.message.message_id
    bot.edit_message_reply_markup(userid,mid,reply_markup = buttons.SponcerpicY.key)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True , text="Pic Removed")
  if call.data=="setpic":
    #hdrspcr = sheet3.cell(int(8),int(2)).value
    try:
      hdrspcr = sheet3.get('B8').first()
      spncrpicst = sheet3.get('B11').first()
      keyboard = types.InlineKeyboardMarkup()
      print(spncrpicst)
      if f"{spncrpicst}" == "Yes":
        bot.send_photo(call.message.chat.id,photo =hdrspcr, caption=f"<b>Here is Sponcer Pic</b>",parse_mode="HTML",reply_markup=buttons.SponcerpicN.key)
      elif f"{spncrpicst}" == "No":
        bot.send_photo(call.message.chat.id,photo =hdrspcr, caption=f"<b>Here is Sponcer Pic</b>",parse_mode="HTML",reply_markup=buttons.SponcerpicY.key)
      else:
        print("Error")
    except:
      print("bk")
      ak = bot.send_message(call.message.chat.id,text="Invalid Format Found...Send me Sponcer pic")
      bot.register_next_step_handler(ak,updtpic)
  if call.data=="updtpic":
    ak = bot.send_message(call.message.chat.id,text="Send me Sponcer pic")
    bot.register_next_step_handler(ak,updtpic)
  if call.data=="frwdlists":
    cid = call.message.chat.id
    mid = call.message.message_id
    bot.edit_message_text(chat_id = call.message.chat.id,text="📋 List Forward Options",message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.FrwdListopt.key)
  if call.data=="dltlists":
    cid = call.message.chat.id
    mid = call.message.message_id
    bot.edit_message_text(chat_id = call.message.chat.id,text="🗑️ List Delete Options",message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.DltListopt.key)
  if call.data=="createlist":
    ListChnl = Config.ListChannel
    lisType = sheet3.get('B1').first()
    EntryInOneList = sheet3.get('B10').first()
    ExtraChannel = sheet3.get('B14').first
    #sheet1.sort((6, 'des'))
    #sheet1.sort((6, 'asc'), range='A1:K999')
    sheet1.sort((6, 'des'),range='A1:K999')
    values_list1 = sheet1.col_values(3)
    values_list2 = sheet1.col_values(4)
    values_list3 = sheet1.col_values(5)
    if f"{lisType}" == "clskUlist":
      header = sheet3.get('B4').first()
      footer = sheet3.get('B5').first()
      emoji = sheet3.get('B6').first()
      contxt = ""
      for i1,i2,i3 in zip(values_list1,values_list2,values_list3):
        Name = i1.strip()
        Uname = i2.strip()
        Link = i3.strip()
        if f"{Uname}" == "None":
          emojis_list_de= re.findall(r'(:[!_\-\w]+:)', Name)
          list_emoji= [emoji.emojize(x) for x in emojis_list_de]
          Name2 = demoji.replace(Name, "")
          Name3 = Name2.replace(" ", "")
          Name5 = Name3.lower()
          #Name5 = "{}{}".format(list_emoji[0],Name4)
          if len(f"{Name5}") >= 16:
            Name1 = Name5[0:16]
            contxt+=f"\n{emoji} <a href='{Link}'>@{Name1}</a>"
          else:
            contxt+=f"\n{emoji} <a href='{Link}'>@{Name5}</a>"
        else:
          contxt+=f"\n{emoji} {Uname}"
      fxdbtn = sheet3.get('B3').first()
      if f"{fxdbtn}" == "Yes":
        fxdbtndata = sheet3.get('B2').first()
        pakshi = f"{fxdbtndata}"
        tag_split = pakshi.splitlines()
        keyboard = types.InlineKeyboardMarkup()
        for each_cn in tag_split:
          new_cn = each_cn.strip()
          splitter = " | "
          if splitter in each_cn:
            manybtn = (new_cn.split("|"))
            row = []
            for i in manybtn:
              c_detail, c_link = (i.split("="))
              channel_detail = c_detail.strip()
              channel_link = c_link.strip()
              row.append(types.InlineKeyboardButton(text=channel_detail, url=channel_link))
            keyboard.row(*row)
          else:
            c_detail, c_link = (new_cn.split("="))
            channel_detail = c_detail.strip()
            channel_link = c_link.strip()
            btn = types.InlineKeyboardButton(text=channel_detail,url = channel_link)
            keyboard.add(btn)
      else:
        print("..")
      lines = contxt.split("\n")
      non_empty_lines = [line for line in lines if line.strip() != ""]
      finallines = ""
      for line in non_empty_lines:
        finallines += line + "\n"
      spliallline = finallines.splitlines()
      nmbrline = len(spliallline)
      Linetosplit = int(EntryInOneList)
      totalpara1 = nmbrline/Linetosplit
      totalpara = round(totalpara1)
      remainder = nmbrline%Linetosplit
      ListPstId = []
      fg = bot.send_message(call.message.chat.id,text="List Creating...")
      for x in range(int(totalpara)):
        dk =""
        dk+=header + "\n"
        if int(x + 1)== int(totalpara):
          if int(remainder*2) >= Linetosplit:
            new_l1=spliallline[-int(remainder):]
            for new_l in new_l1:
              dk+=f"\n{new_l}"
          else:
            new_l1=spliallline[-int(Linetosplit+remainder):]
            for new_l in new_l1:
              dk+=f"\n{new_l}"
        else:
          for y in range(Linetosplit):
            new_l = spliallline[(x*Linetosplit)+y]
            dk+=f"\n{new_l}"
        dk+=f"\n\n{footer}"
        enblwebpageveiw = sheet3.get('B9').first()
        if f"{enblwebpageveiw}" == "Yes":
          if f"{fxdbtn}" == "Yes":
            jk = bot.send_message(chat_id=ListChnl,text=dk,parse_mode="HTML",reply_markup=keyboard)
            msgid = jk.message_id
            ListPstId.append(msgid)
          else:
            jk = bot.send_message(chat_id=ListChnl,text=dk,parse_mode="HTML")
            msgid = jk.message_id
            ListPstId.append(msgid)
        else:
          if f"{fxdbtn}" == "Yes":
            jk = bot.send_message(chat_id=ListChnl,text=dk,parse_mode="HTML",reply_markup=keyboard,disable_web_page_preview=True)
            msgid = jk.message_id
            ListPstId.append(msgid)
          else:
            jk = bot.send_message(chat_id=ListChnl,text=dk,parse_mode="HTML",disable_web_page_preview=True)
            msgid = jk.message_id
            ListPstId.append(msgid)
      linkforlist=""
      cnt=0
      for i in ListPstId:
        cnt+=1
        linkforlist+=f"\n<a href='https://t.me/c/{Config.ListChannel1}/{i}'>List {cnt}</a>"
      bot.edit_message_text(chat_id = call.message.chat.id,text=f"Lists Created ✅{linkforlist}\nNow Updating ListId To DataBase",message_id=fg.message_id,parse_mode="HTML")
      TotalList = len(ListPstId)
      for q in range(TotalList):
        if remainder > 0:
          if int(q+1) == int(TotalList):
            if int(remainder*2) >= Linetosplit:
              for y in range(remainder):
                time.sleep(2)
                sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[-1])
            else:
              for y in range(int(remainder+Linetosplit)):
                time.sleep(2)
                sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[-1])
          else:
            for y in range(Linetosplit):
              time.sleep(2)
              sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[q])
        else:
          for y in range(Linetosplit):
            time.sleep(2)
            sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[q])
      bot.edit_message_text(chat_id = call.message.chat.id,text=f"Lists Created ✅{linkforlist}\nListId Updated ✅\nNow u can forward to channels ...",message_id=fg.message_id,parse_mode="HTML")
    if f"{lisType}" == "clskNlist":
      header = sheet3.get('B4').first()
      footer = sheet3.get('B5').first()
      emoji = sheet3.get('B6').first()
      print(ExtraChannel)
      extrchnl = ""
      output = markdown.markdown(ExtraChannel)
      tag = output.splitlines()
      for h in tag:
        #c_detail, c_link = (i.split("="))
        #channel_detail = c_detail.strip()
        #channel_link = c_link.strip()
        extrchnl+=f"{h}\n"
        #extrchnl+=f"{emoji} <a href='{channel_link}'>{channel_detail}</a>\n"
      print(extrchnl)
      contxt = ""
      for i1,i2,i3 in zip(values_list1,values_list2,values_list3):
        Name = i1.strip()
        Uname = i2.strip()
        Link = i3.strip()
        list_emoji = emojis.get(f'{Name}')
        Name4 = demoji.replace(Name, "")
        #Name4 = Name2.replace(" ", "")
        #Name4 = Name3.lower()
        Name5=""
        try:
          list_emoji1 = list(list_emoji)
          Name5+= "{}{}".format(list_emoji1[0],Name4)
        except:
          list_emoji1 = list(Config.EmojiText)
          print(list_emoji1)
          wordcount = emojis.count(Config.EmojiText)
          n = random.randint(1,int(wordcount-1))
          try:
            Name5+= "{}{}".format(list(list_emoji1)[n],Name4)
          except:
            Name5+= "🔥{}".format(Name4)
        if len(f"{Name5}") >= 16:
          Name1 = Name5[0:16]
          contxt+=f"\n{emoji} <a href='{Link}'>{Name1}</a>"
        else:
          contxt+=f"\n{emoji} <a href='{Link}'>{Name5}</a>"
      fxdbtn = sheet3.get('B3').first()
      if f"{fxdbtn}" == "Yes":
        fxdbtndata = sheet3.get('B2').first()
        pakshi = f"{fxdbtndata}"
        tag_split = pakshi.splitlines()
        keyboard = types.InlineKeyboardMarkup()
        for each_cn in tag_split:
          new_cn = each_cn.strip()
          splitter = " | "
          if splitter in each_cn:
            manybtn = (new_cn.split("|"))
            row = []
            for i in manybtn:
              c_detail, c_link = (i.split("="))
              channel_detail = c_detail.strip()
              channel_link = c_link.strip()
              row.append(types.InlineKeyboardButton(text=channel_detail, url=channel_link))
            keyboard.row(*row)
          else:
            c_detail, c_link = (new_cn.split("="))
            channel_detail = c_detail.strip()
            channel_link = c_link.strip()
            btn = types.InlineKeyboardButton(text=channel_detail,url = channel_link)
            keyboard.add(btn)
      else:
        print("..")
      lines = contxt.split("\n")
      non_empty_lines = [line for line in lines if line.strip() != ""]
      finallines = ""
      #print(non_empty_lines)
      for line in non_empty_lines:
        finallines += line + "\n"
      spliallline = finallines.splitlines()
      nmbrline = len(spliallline)
      Linetosplit = int(EntryInOneList)
      totalpara1 = nmbrline/Linetosplit
      totalpara = round(totalpara1)
      remainder = nmbrline%Linetosplit
      ListPstId = []
      fg = bot.send_message(call.message.chat.id,text="List Creating...")
      for x in range(int(totalpara)):
        dk =""
        dk+=header + "\n"
        if int(x + 1)== int(totalpara):
          if int(remainder*2) >= Linetosplit:
            new_l1=spliallline[-int(remainder):]
            for new_l in new_l1:
              dk+=f"\n{new_l}"
          else:
            new_l1=spliallline[-int(Linetosplit+remainder):]
            for new_l in new_l1:
              dk+=f"\n{new_l}"
        else:
          for y in range(Linetosplit):
            new_l = spliallline[(x*Linetosplit)+y]
            dk+=f"\n{new_l}"
        dk+=f"\n{extrchnl}"
        dk+=f"\n{footer}"
        enblwebpageveiw = sheet3.get('B9').first()
        if f"{enblwebpageveiw}" == "Yes":
          if f"{fxdbtn}" == "Yes":
            jk = bot.send_message(chat_id=ListChnl,text=dk,parse_mode="HTML",reply_markup=keyboard)
            msgid = jk.message_id
            ListPstId.append(msgid)
          else:
            jk = bot.send_message(chat_id=ListChnl,text=dk,parse_mode="HTML")
            msgid = jk.message_id
            ListPstId.append(msgid)
        else:
          if f"{fxdbtn}" == "Yes":
            jk = bot.send_message(chat_id=ListChnl,text=dk,parse_mode="HTML",reply_markup=keyboard,disable_web_page_preview=True)
            msgid = jk.message_id
            ListPstId.append(msgid)
          else:
            jk = bot.send_message(chat_id=ListChnl,text=dk,parse_mode="HTML",disable_web_page_preview=True)
            msgid = jk.message_id
            ListPstId.append(msgid)
      linkforlist=""
      cnt=0
      for i in ListPstId:
        cnt+=1
        linkforlist+=f"\n<a href='https://t.me/c/{Config.ListChannel1}/{i}'>List {cnt}</a>"
      bot.edit_message_text(chat_id = call.message.chat.id,text=f"Lists Created ✅{linkforlist}\nNow Updating ListId To DataBase",message_id=fg.message_id,parse_mode="HTML")
      TotalList = len(ListPstId)
      for q in range(TotalList):
        if remainder > 0:
          if int(q+1) == int(TotalList):
            if int(remainder*2) >= Linetosplit:
              for y in range(remainder):
                time.sleep(2)
                sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[-1])
            else:
              for y in range(int(remainder+Linetosplit)):
                time.sleep(2)
                sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[-1])
          else:
            for y in range(Linetosplit):
              time.sleep(2)
              sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[q])
        else:
          for y in range(Linetosplit):
            time.sleep(2)
            sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[q])
      bot.edit_message_text(chat_id = call.message.chat.id,text=f"Lists Created ✅{linkforlist}\nListId Updated ✅\nNow u can forward to channels ...",message_id=fg.message_id,parse_mode="HTML")
    if f"{lisType}" == "Stndrdlist":
      header = sheet3.get('B4').first()
      footer = sheet3.get('B5').first()
      emoji = sheet3.get('B6').first()
      contxt = ""
      for i1,i2,i3 in zip(values_list1,values_list2,values_list3):
        Name = i1.strip()
        Uname = i2.strip()
        Link = i3.strip()
        if len(f"{Name}") >= 16:
          Name1 = Name[0:16]
          contxt+=f"\n{Name1} = {Link}"
        else:
          contxt+=f"\n{Name} = {Link}"
      fxdbtn = sheet3.get('B3').first()
      if f"{fxdbtn}" == "Yes":
        fxdbtndata = sheet3.get('B2').first()
        pakshi = f"{fxdbtndata}"
        tag_split = pakshi.splitlines()
        keyboard = types.InlineKeyboardMarkup()
        for each_cn in tag_split:
          new_cn = each_cn.strip()
          splitter = " | "
          if splitter in each_cn:
            manybtn = (new_cn.split("|"))
            row = []
            for i in manybtn:
              c_detail, c_link = (i.split("="))
              channel_detail = c_detail.strip()
              channel_link = c_link.strip()
              row.append(types.InlineKeyboardButton(text=channel_detail, url=channel_link))
            keyboard.row(*row)
          else:
            c_detail, c_link = (new_cn.split("="))
            channel_detail = c_detail.strip()
            channel_link = c_link.strip()
            btn = types.InlineKeyboardButton(text=channel_detail,url = channel_link)
            keyboard.add(btn)
      else:
        print("..")
      lines = contxt.split("\n")
      non_empty_lines = [line for line in lines if line.strip() != ""]
      finallines = ""
      for line in non_empty_lines:
        finallines += line + "\n"
      spliallline = finallines.splitlines()
      nmbrline = len(spliallline)
      Linetosplit = int(EntryInOneList)
      totalpara1 = nmbrline/Linetosplit
      totalpara = round(totalpara1)
      remainder = nmbrline%Linetosplit
      ListPstId = []
      fg = bot.send_message(call.message.chat.id,text="List Creating...")
      for x in range(int(totalpara)):
        dk =""
        if int(x + 1)== int(totalpara):
          if int(remainder*2) >= Linetosplit:
            new_l1=spliallline[-int(remainder):]
            for new_l in new_l1:
              dk+=f"\n{new_l}"
          else:
            new_l1=spliallline[-int(Linetosplit+remainder):]
            for new_l in new_l1:
              dk+=f"\n{new_l}"
        else:
          for y in range(Linetosplit):
            new_l = spliallline[(x*Linetosplit)+y]
            dk+=f"\n{new_l}"
        enblwebpageveiw = sheet3.get('B9').first()
        sk = ""
        sk+=header + "\n"
        lines1 = dk.split("\n")
        non_empty_lines1 = [line for line in lines1 if line.strip() != ""]
        ok = ""
        for line in non_empty_lines1:
          ok += line + "\n"
        everyline = ok.splitlines()
        for u in everyline:
          c_detail, c_link = (u.split("="))
          channel_detail = c_detail.strip()
          channel_link = c_link.strip()
          sk+=f"\n{channel_detail}\n<a href='{channel_link}'>{emoji}Join Now{emoji}</a>\n"
        sk+=f"\n{footer}"
        if f"{enblwebpageveiw}" == "Yes":
          if f"{fxdbtn}" == "Yes":
            jk = bot.send_message(chat_id=ListChnl,text=sk,parse_mode="HTML",reply_markup=keyboard)
            msgid = jk.message_id
            ListPstId.append(msgid)
          else:
            jk = bot.send_message(chat_id=ListChnl,text=sk,parse_mode="HTML")
            msgid = jk.message_id
            ListPstId.append(msgid)
        else:
          if f"{fxdbtn}" == "Yes":
            jk = bot.send_message(chat_id=ListChnl,text=sk,parse_mode="HTML",reply_markup=keyboard,disable_web_page_preview=True)
            msgid = jk.message_id
            ListPstId.append(msgid)
          else:
            jk = bot.send_message(chat_id=ListChnl,text=sk,parse_mode="HTML",disable_web_page_preview=True)
            msgid = jk.message_id
            ListPstId.append(msgid)
      linkforlist=""
      cnt=0
      for i in ListPstId:
        cnt+=1
        linkforlist+=f"\n<a href='https://t.me/c/{Config.ListChannel1}/{i}'>List {cnt}</a>"
      bot.edit_message_text(chat_id = call.message.chat.id,text=f"Lists Created ✅{linkforlist}\nNow Updating ListId To DataBase",message_id=fg.message_id,parse_mode="HTML")
      TotalList = len(ListPstId)
      for q in range(TotalList):
        if remainder > 0:
          if int(q+1) == int(TotalList):
            if int(remainder*2) >= Linetosplit:
              for y in range(remainder):
                time.sleep(2)
                sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[-1])
            else:
              for y in range(int(remainder+Linetosplit)):
                time.sleep(2)
                sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[-1])
          else:
            for y in range(Linetosplit):
              time.sleep(2)
              sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[q])
        else:
          for y in range(Linetosplit):
            time.sleep(2)
            sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[q])
      bot.edit_message_text(chat_id = call.message.chat.id,text=f"Lists Created ✅{linkforlist}\nListId Updated ✅\nNow u can forward to channels ...",message_id=fg.message_id,parse_mode="HTML")
    if f"{lisType}" == "Buttonlist":
      header = sheet3.get('B4').first()
      footer = sheet3.get('B5').first()
      emoji = sheet3.get('B6').first()
      contxt = ""
      for i1,i2,i3 in zip(values_list1,values_list2,values_list3):
        Name = i1.strip()
        Uname = i2.strip()
        Link = i3.strip()
        list_emoji = emojis.get(f'{Name}')
        Name4 = demoji.replace(Name, "")
        #Name4 = Name2.replace(" ", "")
        #Name4 = Name3.lower()
        emoji2add=""
        Name5=""
        try:
          list_emoji1 = list(list_emoji)
          emoji2add+="{}".format(list_emoji1[0])
          Name5+= "{}".format(Name4)
        except:
          list_emoji1 = list(Config.EmojiText)
          wordcount = emojis.count(Config.EmojiText)
          n = random.randint(1,int(wordcount))
          print(list(list_emoji1))
          emoji2add+="{}".format(list(list_emoji1)[n])
          Name5+= "{}".format(Name4)
        if len(f"{Name5}") >= 16:
          Name1 = Name5[0:16]
          contxt+=f"\n{emoji2add}{Name1}{emoji2add} = {Link}"
        else:
          contxt+=f"\n{emoji2add}{Name5}{emoji2add} = {Link}"
      lines = contxt.split("\n")
      non_empty_lines = [line for line in lines if line.strip() != ""]
      finallines = ""
      for line in non_empty_lines:
        finallines += line + "\n"
      spliallline = finallines.splitlines()
      nmbrline = len(spliallline)
      Linetosplit = int(EntryInOneList)
      totalpara1 = nmbrline/Linetosplit
      totalpara = round(totalpara1)
      remainder = nmbrline%Linetosplit
      ListPstId = []
      fg = bot.send_message(call.message.chat.id,text="List Creating...")
      for x in range(int(totalpara)):
        fxdbtn = sheet3.get('B3').first()
        keyboard = types.InlineKeyboardMarkup()
        dk =""
        if int(x + 1)== int(totalpara):
          if int(remainder*2) >= Linetosplit:
            new_l1=spliallline[-int(remainder):]
            for new_l in new_l1:
              dk+=f"\n{new_l}"
          else:
            new_l1=spliallline[-int(Linetosplit+remainder):]
            for new_l in new_l1:
              dk+=f"\n{new_l}"
        else:
          for y in range(Linetosplit):
            new_l = spliallline[(x*Linetosplit)+y]
            dk+=f"\n{new_l}"
        enblwebpageveiw = sheet3.get('B9').first()
        lines1 = dk.split("\n")
        non_empty_lines1 = [line for line in lines1 if line.strip() != ""]
        ok = ""
        for line in non_empty_lines1:
          ok += line + "\n"
        everyline = ok.splitlines()
        for u in everyline:
          print(u)
          c_detail, c_link = (u.split("="))
          channel_detail = c_detail.strip()
          channel_link = c_link.strip()
          btn1 = types.InlineKeyboardButton(channel_detail, url=channel_link)
          keyboard.add(btn1)
          #sk+=f"\n{channel_detail}\n<a href='{channel_link}'>{emoji}Join Now{emoji}</a>\n"
        #sk+=f"\n{footer}"
        if f"{fxdbtn}" == "Yes":
          fxdbtndata = sheet3.get('B2').first()
          pakshi = f"{fxdbtndata}"
          tag_split = pakshi.splitlines()
          for each_cn in tag_split:
            new_cn = each_cn.strip()
            splitter = " | "
            if splitter in each_cn:
              manybtn = (new_cn.split("|"))
              row = []
              for i in manybtn:
                c_detail, c_link = (i.split("="))
                channel_detail = c_detail.strip()
                channel_link = c_link.strip()
                row.append(types.InlineKeyboardButton(text=channel_detail, url=channel_link))
              keyboard.row(*row)
            else:
              c_detail, c_link = (new_cn.split("="))
              channel_detail = c_detail.strip()
              channel_link = c_link.strip()
              btn = types.InlineKeyboardButton(text=channel_detail,url = channel_link)
              keyboard.add(btn)
          picyoN = sheet3.get('B11').first()
          if f"{picyoN}" == "Yes":
            picValue = sheet3.get('B8').first()
            CaptyoN = sheet3.get('B12').first()
            if f"{CaptyoN}" == "Yes":
              captValue = sheet3.get('B7').first()
              jk = bot.send_photo(chat_id=ListChnl,photo=picValue,caption=captValue,parse_mode="HTML",reply_markup=keyboard)
              msgid = jk.message_id
              ListPstId.append(msgid)
            else:
              jk = bot.send_photo(chat_id=ListChnl,photo=picValue,reply_markup=keyboard)
              msgid = jk.message_id
              ListPstId.append(msgid)
          else:
            captValue = sheet3.get('B7').first()
            if f"{enblwebpageveiw}" == "Yes":
              jk = bot.send_message(chat_id=ListChnl,text=captValue,parse_mode="HTML",reply_markup=keyboard)
              msgid = jk.message_id
              ListPstId.append(msgid)
            else:
              jk = bot.send_message(chat_id=ListChnl,text=captValue,parse_mode="HTML",reply_markup=keyboard,disable_web_page_preview=True)
              msgid = jk.message_id
              ListPstId.append(msgid)
        else:
          picyoN = sheet3.get('B11').first()
          if f"{picyoN}" == "Yes":
            picValue = sheet3.get('B8').first()
            #CaptyoN = sheet3.get('B12').first()
            if f"{CaptyoN}" == "Yes":
              captValue = sheet3.get('B7').first()
              jk = bot.send_photo(chat_id=ListChnl,photo=picValue,caption=captValue,parse_mode="HTML",reply_markup=keyboard)
              msgid = jk.message_id
              ListPstId.append(msgid)
            else:
              jk = bot.send_photo(chat_id=ListChnl,photo=picValue,reply_markup=keyboard)
              msgid = jk.message_id
              ListPstId.append(msgid)
          else:
            captValue = sheet3.get('B7').first()
            if f"{enblwebpageveiw}" == "Yes":
              jk = bot.send_message(chat_id=ListChnl,text=captValue,parse_mode="HTML",reply_markup=keyboard)
              msgid = jk.message_id
              ListPstId.append(msgid)
            else:
              jk = bot.send_message(chat_id=ListChnl,text=captValue,parse_mode="HTML",disable_web_page_preview=True,reply_markup=keyboard)
              msgid = jk.message_id
              ListPstId.append(msgid)
      linkforlist=""
      cnt=0
      for i in ListPstId:
        cnt+=1
        linkforlist+=f"\n<a href='https://t.me/c/{Config.ListChannel1}/{i}'>List {cnt}</a>"
      bot.edit_message_text(chat_id = call.message.chat.id,text=f"Lists Created ✅{linkforlist}\nNow Updating ListId To DataBase",message_id=fg.message_id,parse_mode="HTML")
      TotalList = len(ListPstId)
      for q in range(TotalList):
        if remainder > 0:
          if int(q+1) == int(TotalList):
            if int(remainder*2) >= Linetosplit:
              for y in range(remainder):
                time.sleep(2)
                sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[-1])
            else:
              for y in range(int(remainder+Linetosplit)):
                time.sleep(2)
                sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[-1])
          else:
            for y in range(Linetosplit):
              time.sleep(2)
              sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[q])
        else:
          for y in range(Linetosplit):
            time.sleep(2)
            sheet1.update(f"H{int((q*Linetosplit)+y+1)}",ListPstId[q])
      bot.edit_message_text(chat_id = call.message.chat.id,text=f"Lists Created ✅{linkforlist}\nListId Updated ✅\nNow u can forward to channels ...",message_id=fg.message_id,parse_mode="HTML")
  if call.data=="setblwbtns":
    fxdbtn = sheet3.get('B3').first()
    if f"{fxdbtn}" == "No":
      bot.edit_message_text(chat_id = call.message.chat.id,text="⭕ Fixed Buttons Options",message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.FxdListN.key)
    if f"{fxdbtn}" == "Yes":
      bot.edit_message_text(chat_id = call.message.chat.id,text="⭕ Fixed Buttons Options",message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.FxdListY.key)
  if call.data=="lstwebprvw":
    fxdbtn = sheet3.get('B9').first()
    if f"{fxdbtn}" == "No":
      bot.edit_message_text(chat_id = call.message.chat.id,text="⭕ List Webpage Preview",message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.EblPrvw.key)
    if f"{fxdbtn}" == "Yes":
      bot.edit_message_text(chat_id = call.message.chat.id,text="⭕ List Webpage Preview",message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.Dblprvw.key)
  if call.data=="enbleprvw":
    sheet3.update("B9","Yes")
    bot.edit_message_text(chat_id = call.message.chat.id,text="⭕ List Webpage Preview",message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.Dblprvw.key)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True , text="Webpage Preview Enabled")
  if call.data=="dsblprvw":
    sheet3.update("B9","No")
    bot.edit_message_text(chat_id = call.message.chat.id,text="⭕ List Webpage Preview",message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.EblPrvw.key)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True , text="Webpage Preview Disabled")
  if call.data=="FxdButtonN":
    sheet3.update("B3","Yes")
    bot.edit_message_text(chat_id = call.message.chat.id,text="⭕ Fixed Buttons Options",message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.FxdListY.key)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True , text="Fixed Buttons Added Below List")
  if call.data=="FxdButtonY":
    sheet3.update("B3","No")
    bot.edit_message_text(chat_id = call.message.chat.id,text="⭕ Fixed Buttons Options",message_id=call.message.message_id,parse_mode="HTML",reply_markup=buttons.FxdListN.key)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True , text="Fixed Buttons Removed From Below List")
  if call.data=="updtbtns":
    ak = bot.send_message(call.message.chat.id,text=normaltext.SetBtnText,parse_mode="HTML",reply_markup=buttons.CancelKey.keyboard)
    bot.register_next_step_handler(ak,setBtntText)
  if call.data=="FxdButtonYPrvw":
    fxdbtndata = sheet3.get('B2').first()
    try:
      pakshi = f"{fxdbtndata}"
      tag_split = pakshi.splitlines()
      keyboard = types.InlineKeyboardMarkup()
      for each_cn in tag_split:
        new_cn = each_cn.strip()
        splitter = " | "
        if splitter in each_cn:
          manybtn = (new_cn.split("|"))
          row = []
          for i in manybtn:
            c_detail, c_link = (i.split("="))
            channel_detail = c_detail.strip()
            channel_link = c_link.strip()
            row.append(types.InlineKeyboardButton(text=channel_detail, url=channel_link))
          keyboard.row(*row)
        else:
          c_detail, c_link = (new_cn.split("="))
          channel_detail = c_detail.strip()
          channel_link = c_link.strip()
          btn = types.InlineKeyboardButton(text=channel_detail,url = channel_link)
          keyboard.add(btn)
      keyboard.add(types.InlineKeyboardButton(text="❌ Close",callback_data = "clsewndw"))
      bot.send_message(call.message.chat.id,text="🍉 This is Below Buttons for List",reply_markup=keyboard)
    except Exception as e:
      sk = bot.send_message(call.message.chat.id,text=f"{e}")
  if call.data=="fakeentery":
    for i in range(5):
      j = sheet1.get('A1000').first()
      j1 = int(j) + 1
      sheet1.update_cell(int(j1),1 ,f"{j1}")
      sheet1.update_cell(int(j1),2 ,f"12345{j1}")
      sheet1.update_cell(int(j1),3 ,f"Test{j1}")
      sheet1.update_cell(int(j1),4 ,f"@Test{j1}")
      sheet1.update_cell(int(j1),5 ,f"https://t.me/Test{j1}")
      sheet1.update_cell(int(j1),6 ,f"678{j1}")
      sheet1.update_cell(int(j1),7 ,f"{call.message.chat.id}")
      bot.send_message(call.message.chat.id,text=f"Entry {i} Done")
  if call.data=="dltfewpst":
    m = bot.send_message(call.message.chat.id,text="<b>Send me Channels Ids .</b>",parse_mode="HTML")
    bot.register_next_step_handler(m,dltonepst2)
  if call.data=="dltpstall":
    values_list3 = sheet1.col_values(2)
    Pass = 0
    Fail = 0
    AlredyDelete=""
    failedlist=""
    for i1 in values_list3:
      time.sleep(1)
      man_detail1 = i1.strip()
      cells = sheet1.find(man_detail1)
      row = cells.row
      stats = sheet1.get(f"I{row}").first()
      if f"{stats}" == "Shared":
        try:
          mid = sheet1.get(f"J{row}").first()
          #if int(mid) >=1:
          if int(mid) == 0:
            AlredyDelete+=f"\n{man_detail1}"
            bot.send_message(call.message.chat.id,f"{man_detail1} Already Deleted")
          else:
            try:
              bot.delete_message(man_detail1,mid)
              sheet1.update(f"I{row}","Deleted")
              sheet1.update(f"J{row}","0")
              Pass+=1
              time.sleep(2)
            except Exception as e:
              time.sleep(2)
              bot.send_message(call.message.chat.id,f"{man_detail1} Failed & list id {mid} and error is {e}")
        except Exception as e:
          time.sleep(2)
          failedlist+=f"\n{man_detail1}"
          bot.send_message(call.message.chat.id,f"{man_detail1} failed with error {e}\n")
        time.sleep(1)
      else:
        m = bot.send_message(call.message.chat.id,text=f"<b>Failed bcz previous Status is {stats}</b>",parse_mode="HTML")
    bot.send_message(call.message.chat.id,text=f"<b>List Of Already Deleted Channels</b> \n\n <code>{AlredyDelete}</code>",parse_mode="HTML")
    bot.send_message(call.message.chat.id,text=f"<b>List Of Failed Channels</b> \n\n <code>{failedlist}</code>",parse_mode="HTML")
    bot.send_message(call.message.chat.id,text=normaltext.ListdeleteSucess.format(Pass,Fail),parse_mode="HTML")
  if call.data=="frwrdpstfew":
    m = bot.send_message(call.message.chat.id,text="<b>Send me post ids.</b>",parse_mode="HTML")
    bot.register_next_step_handler(m,frwrdpstfew1)
  if call.data=="frwrdpstall":
    values_list1 = sheet1.col_values(2)
    values_list2 = sheet1.col_values(8)
    Pass = 0
    Fail = 0
    AlredyPost=""
    failedlist=""
    for i1,i2 in zip(values_list1,values_list2):
      man_detail1 = i1.strip()
      man_detail2 = i2.strip()
      cells = sheet1.find(man_detail1)
      row = cells.row
      stats = sheet1.get(f"I{row}").first()
      if f"{stats}" == "Deleted" or "None":
        try:
          aa = bot.forward_message(chat_id = f"{man_detail1}", from_chat_id =Config.ListChannel, message_id = man_detail2)
          sheet1.update(f"I{row}","Shared")
          sheet1.update(f"J{row}",f"{aa.message_id}")
          time.sleep(1)
          Pass+=1
          time.sleep(2)
        except Exception as e:
          Fail+=1
          time.sleep(2)
          failedlist+=f"\n{man_detail1}"
          bot.send_message(call.message.chat.id,text=f"{man_detail1} Failed with error {e}")
      else:
        failedlist+=f"\n{man_detail1}"
        time.sleep(2)
        m = bot.send_message(call.message.chat.id,text=f"<b>Failed bcz previous Status is {stats}</b>",parse_mode="HTML")
    bot.send_message(call.message.chat.id,text=f"<b>List Of Already Posted Channels</b> \n\n <code>{AlredyPost}</code>",parse_mode="HTML")
    bot.send_message(call.message.chat.id,text=f"<b>List Of Failed Channels</b> \n\n <code>{failedlist}</code>",parse_mode="HTML")
    bot.send_message(call.message.chat.id,text=normaltext.ListForwardSucess.format(Pass,Fail),parse_mode="HTML")
  if call.data=="userinfo":
    m = bot.send_message(call.message.chat.id,text="<b>Send me user Id.</b>",parse_mode="HTML")
    bot.register_next_step_handler(m,userdtl)
  if call.data=="chnlinfo":
    ak = bot.send_message(call.message.chat.id,text="Send me Channel Id")
    bot.register_next_step_handler(ak,ChnlInfo)
  if call.data=="updtsubs":
    values_list3 = sheet1.col_values(2)
    while("" in values_list3):
      values_list3.remove("")
    failed=""
    for i in values_list3:
      try:
        subcount= bot.get_chat_members_count(chat_id=i)
        cells = sheet1.find(i)
        row = cells.row
        sheet1.update(f"I{row}",subcount)
        time.sleep(2)
      except Exception as e:
        failed+=f"{i} {e}\n"
    bot.send_message(call.message.chat.id,text=f"Failed Status: \n{failed}")
    bot.send_message(call.message.chat.id,text=f"Subscribers Update Done")
  if call.data=="rearrngechnl":
    sheet1.sort((6, 'des'),range='A1:K999')
    values_list3 = sheet1.col_values(2)
    while("" in values_list3):
      values_list3.remove("")
    total_count = len(values_list3)
    print(total_count)
    for i in range(1,total_count+1):
      print(i)
      sheet1.update(f"A{i}",i)
    bot.send_message(call.message.chat.id,text=f"✅ Rearranged All\nTotal Channels : {total_count}")
  if call.data=="rmvchnl":
    ak = bot.send_message(call.message.chat.id,text="Send me Channel Ids T9 Remove")
    bot.register_next_step_handler(ak,Chnl2Remove)
  if call.data=="clsewndw":
    cid = call.message.chat.id
    mid = call.message.message_id
    bot.delete_message(cid,mid)
    

def Chnl2Remove(m):
  #chnlid1 = f"{m.text}"
  chnlids = m.text
  allchannellist = chnlids.splitlines()
  for chnlid1 in allchannellist:
    prefix = chnlid1[0:4]
    prefix1 = chnlid1[0:3]
    chnlid=""
    if prefix=="-100":
      chnlid+=chnlid1
    elif prefix1=="100":
      chnlid+=f"-{chnlid1}"
    else:
      chnlid+=f"-100{chnlid1}"
    try:
      celluccuser = sheet1.find(chnlid)
      cellurowuser = celluccuser.row
      chnlname1 = sheet1.get(f"C{cellurowuser}").first()
      AdminId = sheet1.get(f"G{cellurowuser}").first()
      sheet1.batch_clear([f"A{cellurowuser}:K{cellurowuser}"])
      ak = client.open(Config.sheetname)
      sheetyyy = ak.worksheet(f"{AdminId}")
      celluccuser1 = sheetyyy.find(chnlid)
      cellurowuser1 = celluccuser1.row
      sheetyyy.batch_clear([f"A{cellurowuser1}:E{cellurowuser1}"])
      bot.send_message(m.chat.id,text=f"Channel Removed\n{chnlid} - {chnlname1}")
    except Exception as e:
      print(e)
      bot.send_message(m.chat.id,text=f"Channel Failed/Not Found\n{chnlid}")
    ak = client.open(Config.sheetname)
    sheetyyy1 = ak.worksheet(f"{AdminId}")
    h = sheetyyy1.get('A11').first()
    if int(h) == 0:
      ak.del_worksheet(sheetyyy1)
    else:
      print("..")
    
def ChnlInfo(m):
  chnlid1 = f"{m.text}"
  prefix = chnlid1[0:4]
  prefix1 = chnlid1[0:3]
  chnlid=""
  if prefix=="-100":
    chnlid+=chnlid1
  elif prefix1=="100":
    chnlid+=f"-{chnlid1}"
  else:
    chnlid+=f"-100{chnlid1}"
  try:
    celluccuser = sheet1.find(chnlid)
    cellurowuser = celluccuser.row
    chnlname1 = sheet1.get(f"C{cellurowuser}").first()
    chnlUname1 = sheet1.get(f"D{cellurowuser}").first()
    privtlnk = sheet1.get(f"E{cellurowuser}").first()
    AdminId = sheet1.get(f"G{cellurowuser}").first()
    subcount = bot.get_chat_members_count(chat_id=chnlid)
    bot.send_message(m.chat.id,text=normaltext.AbouTChnl.format(chnlname1,chnlid,chnlUname1,subcount,privtlnk,AdminId),reply_markup=buttons.Clswndw.key,parse_mode="HTML",disable_web_page_preview=True)
  except Exception as e:
    print(e)
    bot.send_message(m.chat.id,text="<b>Not Found In Database</b>",parse_mode="HTML")
    
  
  
  
def userdtl(m):
  Id = int(m.text)
  text = bot.escape("akhil")
  usrlnk = f"<a href='tg://user?id={Id}'>{text}</a>"
  #bot.delete_message(m.chat.id,m.message_id)
  bot.send_message(m.chat.id,text=f"{usrlnk}",parse_mode="HTML")

def dltonepst2(m):
  chnlids = m.text
  allchannellist = chnlids.splitlines()
  Pass = 0
  Fail = 0
  AlredyDelete=""
  failedlist=""
  for i1 in allchannellist:
    time.sleep(1)
    man_detail1 = i1.strip()
    cells = sheet1.find(man_detail1)
    row = cells.row
    stats = sheet1.get(f"I{row}").first()
    if f"{stats}" == "Shared":
      try:
        mid = sheet1.get(f"J{row}").first()
        if int(mid) >=1:
          bot.delete_message(man_detail1,mid)
          sheet1.update(f"I{row}","Deleted")
          sheet1.update(f"J{row}","0")
          Pass+=1
          time.sleep(2)
        elif int(mid) == 0:
          time.sleep(2)
          AlredyDelete+=f"\n{man_detail1}"
          bot.send_message(m.chat.id,f"{man_detail1} Already Deleted")
        else:
          bot.send_message(m.chat.id,f"{man_detail1} Failed bcz list id {mid}")
      except Exception as e:
        time.sleep(2)
        failedlist+=f"\n{man_detail1}"
        bot.send_message(m.chat.id,f"{man_detail1} failed with error {e}")
      time.sleep(1)
    else:
      m = bot.send_message(m.chat.id,text=f"<b>Failed bcz previous Status is {stats}</b>",parse_mode="HTML")
  bot.send_message(m.chat.id,text=f"<b>List Of Already Deleted Channels</b> \n\n <code>{AlredyDelete}</code>",parse_mode="HTML")
  bot.send_message(m.chat.id,text=f"<b>List Of Failed Channels</b> \n\n <code>{failedlist}</code>",parse_mode="HTML")
  bot.send_message(m.chat.id,text=normaltext.ListdeleteSucess.format(Pass,Fail),parse_mode="HTML")
    
    
def frwrdpstfew1(m):
  chnlids = m.text
  allchannellist = chnlids.splitlines()
  Pass = 0
  Fail = 0
  AlredyPost=""
  failedlist=""
  for man_detail1 in allchannellist:
    cells = sheet1.find(man_detail1)
    row = cells.row
    man_detail2 = sheet1.get(f"H{row}").first()
    stats = sheet1.get(f"I{row}").first()
    if f"{stats}" == "Deleted" or "None":
      try:
        aa = bot.forward_message(chat_id = f"{man_detail1}", from_chat_id =Config.ListChannel, message_id = man_detail2)
        sheet1.update(f"I{row}","shared")
        sheet1.update(f"J{row}",f"{aa.message_id}")
        time.sleep(1)
        Pass+=1
        time.sleep(2)
      except Exception as e:
        time.sleep(2)
        Fail+=1
        failedlist+=man_detail1
        bot.send_message(m.chat.id,text=f"{man_detail1} Failed with error {e}")
    else:
      failedlist+=man_detail1
      m = bot.send_message(m.chat.id,text=f"<b>Failed bcz previous Status is {stats}</b>",parse_mode="HTML")
  bot.send_message(m.chat.id,text=f"<b>List Of Failed Channels</b> \n\n <code>{stats}</code>",parse_mode="HTML")
  bot.send_message(m.chat.id,text=normaltext.ListForwardSucess.format(Pass,Fail),parse_mode="HTML")


def updthdr(m):
  try:
    ok = bot.send_message(m.chat.id,text=m.text,parse_mode="HTML",disable_web_page_preview=True)
    bot.delete_message(m.chat.id,ok.message_id)
    if f"{m.text}" in cancellist:
      qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
      bot.delete_message(chat_id=m.chat.id,message_id=qk.message_id)
      bot.send_message(m.chat.id,text="<b>🤷Operation Cancelled. /start Again</b>",reply_markup=buttons.OrtnCancel.key,parse_mode="HTML")
    else:
      sheet3.update("B4",m.text)
      bot.reply_to(m,text="<b>✅ Update</b>",parse_mode="HTML",reply_markup=buttons.AdminHome.key)
  except Exception as e:
    sk = bot.send_message(m.chat.id,text=f"<b>Failed to update with error</b> /n/n{e}",parse_mode="HTML")
    bot.register_next_step_handler(sk,updthdr)

def updtftr(m):
  try:
    ok = bot.send_message(m.chat.id,text=m.text,parse_mode="HTML",disable_web_page_preview=True)
    bot.delete_message(m.chat.id,ok.message_id)
    if f"{m.text}" in cancellist:
      qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
      bot.delete_message(chat_id=m.chat.id,message_id=qk.message_id)
      bot.send_message(m.chat.id,text="<b>🤷Operation Cancelled. /start Again</b>",reply_markup=buttons.OrtnCancel.key,parse_mode="HTML")
    else:
      sheet3.update("B5",m.text)
      bot.reply_to(m,text="<b>✅ Update</b>",parse_mode="HTML",reply_markup=buttons.AdminHome.key)
  except Exception as e:
    sk = bot.send_message(m.chat.id,text=f"<b>Failed to update with error</b> /n/n{e}",parse_mode="HTML")
    bot.register_next_step_handler(sk,updtftr)


def updtemoji(m):
  try:
    ok = bot.send_message(m.chat.id,text=m.text,parse_mode="HTML",disable_web_page_preview=True)
    bot.delete_message(m.chat.id,ok.message_id)
    if f"{m.text}" in cancellist:
      qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
      bot.delete_message(chat_id=m.chat.id,message_id=qk.message_id)
      bot.send_message(m.chat.id,text="<b>🤷Operation Cancelled. /start Again</b>",reply_markup=buttons.OrtnCancel.key,parse_mode="HTML")
    else:
      sheet3.update("B6",m.text)
      bot.reply_to(m,text="<b>✅ Update</b>",parse_mode="HTML",reply_markup=buttons.AdminHome.key)
  except Exception as e:
    sk = bot.send_message(m.chat.id,text=f"<b>Failed to update with error</b> /n/n{e}",parse_mode="HTML")
    bot.register_next_step_handler(sk,updtemoji)

def updtcptn(m):
  try:
    ok = bot.send_message(m.chat.id,text=m.text,parse_mode="HTML",disable_web_page_preview=True)
    bot.delete_message(m.chat.id,ok.message_id)
    if f"{m.text}" in cancellist:
      qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
      bot.delete_message(chat_id=m.chat.id,message_id=qk.message_id)
      bot.send_message(m.chat.id,text="<b>🤷Operation Cancelled. /start Again</b>",reply_markup=buttons.OrtnCancel.key,parse_mode="HTML")
    else:
      sheet3.update("B7",m.text)
      bot.reply_to(m,text="<b>✅ Update</b>",parse_mode="HTML",reply_markup=buttons.AdminHome.key)
  except Exception as e:
    sk = bot.send_message(m.chat.id,text=f"<b>Failed to update with error</b> /n/n{e}",parse_mode="HTML")
    bot.register_next_step_handler(sk,updtcptn)

def updtchnlinalist(m):
  if f"{m.text}" in cancellist:
      qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
      bot.delete_message(chat_id=m.chat.id,message_id=qk.message_id)
      bot.send_message(m.chat.id,text="<b>🤷Operation Cancelled. /start Again</b>",reply_markup=buttons.OrtnCancel.key,parse_mode="HTML")
  else:
      py = m.text.isdigit()
      if py == True:
        totalchanl = sheet1.get('A1000').first()
        if  1 <= int(m.text) <= int(totalchanl):
          sheet3.update("B10",m.text)
          bot.reply_to(m,text="<b>✅ Update</b>",parse_mode="HTML",reply_markup=buttons.AdminHome.key)
        else:
          sk = bot.send_message(m.chat.id,text=f"<b>Send me a number in range of {totalchanl}</b>",parse_mode="HTML")
          bot.register_next_step_handler(sk,updtchnlinalist)
      else:
        sk = bot.send_message(m.chat.id,text=f"<b>send me number not text</b>",parse_mode="HTML")
        bot.register_next_step_handler(sk,updtchnlinalist)

def updtreqsub(m):
  if f"{m.text}" in cancellist:
      qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
      bot.delete_message(chat_id=m.chat.id,message_id=qk.message_id)
      bot.send_message(m.chat.id,text="<b>🤷Operation Cancelled. /start Again</b>",reply_markup=buttons.OrtnCancel.key,parse_mode="HTML")
  else:
      py = m.text.isdigit()
      if py == True:
        sheet3.update("B13",m.text)
        bot.reply_to(m,text="<b>✅ Update</b>",parse_mode="HTML",reply_markup=buttons.AdminHome.key)
      else:
        sk = bot.send_message(m.chat.id,text=f"<b>send me number not text</b>",parse_mode="HTML")
        bot.register_next_step_handler(sk,updtreqsub)


def updtpic(m):
  try:
    picid = m.photo[-1].file_id
    sheet3.update("B8",picid)
    bot.reply_to(m,text="<b>✅ Update</b>",parse_mode="HTML")#,eply_markup=keyboard)
  except:
    if f"{m.text}" in cancellist:
      qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
      bot.delete_message(chat_id=m.chat.id,message_id=qk.message_id)
      bot.send_message(m.chat.id,text="<b>🤷Operation Cancelled. /start Again</b>",reply_markup=buttons.OrtnCancel.key,parse_mode="HTML")
    else:
      bot.send_message(m.chat.id,text="<b>Invalid Format, Send me again</b>",parse_mode="HTML")#,eply_markup=keyboard)

def setBtntText(m):
  if f"{m.text}" in cancellist:
    qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
    bot.delete_message(chat_id=m.chat.id,message_id=qk.message_id)
    bot.send_message(m.chat.id,text="<b>🤷Operation Cancelled. /start Again</b>",reply_markup=buttons.OrtnCancel.key,parse_mode="HTML")
  else:
    try:
      pakshi = f"{m.text}"
      tag_split = pakshi.splitlines()
      keyboard = types.InlineKeyboardMarkup()
      for each_cn in tag_split:
        new_cn = each_cn.strip()
        splitter = " | "
        if splitter in each_cn:
          manybtn = (new_cn.split("|"))
          row = []
          for i in manybtn:
            c_detail, c_link = (i.split("="))
            channel_detail = c_detail.strip()
            channel_link = c_link.strip()
            row.append(types.InlineKeyboardButton(text=channel_detail, url=channel_link))
          keyboard.row(*row)
        else:
          c_detail, c_link = (new_cn.split("="))
          channel_detail = c_detail.strip()
          channel_link = c_link.strip()
          btn = types.InlineKeyboardButton(text=channel_detail,url = channel_link)
          keyboard.add(btn)
      keyboard.add(types.InlineKeyboardButton(text="❌ Close",callback_data = "clsewndw"))
      bot.send_message(m.chat.id,text="🍉 This is Below Buttons for List",reply_markup=keyboard)
      qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
      bot.delete_message(chat_id=m.chat.id,message_id=qk.message_id)
      sheet3.update("B2",m.text)
      bot.reply_to(m,text="<b>✅ Update</b>",parse_mode="HTML")#,eply_markup=keyboard)
    except Exception as e:
      sk = bot.send_message(m.chat.id,text=f"{e}\n\nWrong Format...please send me again")
      bot.register_next_step_handler(sk,setBtntText)



def channeladd1(m):
  if f"{m.text}" in cancellist:
    qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
    bot.delete_message(chat_id=m.chat.id,message_id=qk.message_id)
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
        msgid = a.message_id
        bot.delete_message(chnlid,msgid)
        qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
        bot.delete_message(chat_id=m.chat.id,message_id=qk.message_id)
        cellsp = sheet1.findall(f"{chnlid}")
        if len(cellsp) > 0:
          bot.send_message(m.chat.id,text =normaltext.ChnlAlrdyInDTbse,reply_markup=buttons.Ntanychnl.key,parse_mode="HTML")
        else:
          subcount= bot.get_chat_members_count(chat_id=chnlid)
          Min = sheet3.get('B13').first()#normaltext.MaxLimitUser
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
            sheet1.update_cell(int(j1),4 ,f"{chnlusername}")
            sheet1.update_cell(int(j1),5 ,"")
            sheet1.update_cell(int(j1),6 ,f"{subcount}")
            sheet1.update_cell(int(j1),7 ,f"{adminid}")
            sheet1.update_cell(int(j1),8 ,"0")
            sheet1.update_cell(int(j1),9 ,"Deleted")
            sheet1.update_cell(int(j1),10 ,"0")
            try:
              #create_chat_invite_link
              #invitelnk = bot.create_chat_invite_link(chnlid, member_limit=9999)
              invitelnk1 = bot.create_chat_invite_link(chnlid)
              invitelnk = invitelnk1.invite_link
              #bot.send_message(m.chat.id,invitelnk)
              sheet1.update_cell(int(j1),5 ,invitelnk)
              bot.send_message(m.chat.id,text=normaltext.ChnlAdSucess.format(invitelnk,chnlname),disable_web_page_preview=True,reply_markup=buttons.Sucessaddchnl.key,parse_mode="HTML")
              usrlnk = f"<a href='tg://user?id={m.chat.id}'>{m.from_user.first_name}</a>"
              #chnlusrnm1 = sheet1.get(f"D{cellurowcc}").first()
              chnlusrnm=""
              if chnlusername == "None":
                chnlusrnm+="-"
              else:
                chnlusrnm+=f"@{chnlusername}"
              #subcount= bot.get_chat_members_count(chat_id=chnldid)
              bot.send_message(chat_id=Config.sponcergroup,text=normaltext.chnlsccnotifytogroup.format(chnlname,chnlid,chnlusrnm,subcount,invitelnk,usrlnk),disable_web_page_preview=True,parse_mode="HTML")
            except Exception as e:
              print(e)
              m = bot.send_message(m.chat.id,text = "<b>Send private link of your channel</b>",reply_markup=buttons.CancelKey.keyboard,parse_mode="HTML")
              bot.register_next_step_handler(m,addlink)
          else:
            ak = bot.send_message(m.chat.id,text=normaltext.NotEnfSub.format(Min,subcount),reply_markup=buttons.Ntanychnl.key,parse_mode="HTML")
      except:
        ak = bot.send_message(m.chat.id,text="<b>Error:</b> <code>Please authrise me with the rights of Post & Delete and Forward The Post Again. Please Try Again</code>",parse_mode="HTML")
        bot.register_next_step_handler(ak, channeladd1)
    except:
      ak = bot.send_message(m.chat.id,text="<b>This message is not forwarded from channel. Please Try Again</b>",parse_mode="HTML")
      bot.register_next_step_handler(ak, channeladd1)

def addlink(m):
  time.sleep(5)
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
    sheetyyy.batch_clear([f"A{cellurowuser}:E{cellurowuser}"])
    qk = bot.send_message(m.chat.id,text="🐛",reply_markup=buttons.RmvKeyBrd.key,parse_mode="HTML")
    bot.delete_message(chat_id=m.chat.id,message_id=qk.message_id)
    bot.send_message(m.chat.id,text="<b>🤷Operation Cancelled. /start Again</b>",reply_markup=buttons.OrtnCancel.key,parse_mode="HTML")
    sheet1.batch_clear([f"A{cellurowcc}:K{cellurowcc}"])
  else:
    myre = '^(http|https|t.me)://'
    if re.search(myre,lnk):
      cellidc = "E" + f"{cellurowcc}"
      chnlnamex = "C" + f"{cellurowcc}"
      chnlname1 = sheet1.get(chnlnamex).first()
      sheet1.update(cellidc,lnk)
      bot.send_message(m.chat.id,text=normaltext.ChnlAdSucess.format(lnk,chnlname1),disable_web_page_preview=True,reply_markup=buttons.Sucessaddchnl.key,parse_mode="HTML")
      usrlnk = f"<a href='tg://user?id={m.chat.id}'>{m.from_user.first_name}</a>"
      chnlusrnm1 = sheet1.get(f"D{cellurowcc}").first()
      chnlusrnm=""
      if chnlusrnm1 == "None":
        chnlusrnm+="-"
      else:
        chnlusrnm+=f"@{chnlusrnm1}"
      subcount= bot.get_chat_members_count(chat_id=chnldid)
      bot.send_message(chat_id=Config.sponcergroup,text=normaltext.chnlsccnotifytogroup.format(chnlname1,chnldid,chnlusrnm,subcount,lnk,usrlnk),disable_web_page_preview=True,parse_mode="HTML")
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
  am = bot.send_message(m.chat.id,text="⏳",reply_markup=buttons.RmvKeyBrd.key)
  bot.delete_message(chat_id=m.chat.id,message_id=am.message_id)


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
