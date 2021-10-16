from telebot import types

#user
btnaddcnnl = types.InlineKeyboardButton(text=" ➕ ADD CHANNEL ", callback_data="chnladd")
btnmychnl = types.InlineKeyboardButton(text=" 🗂️ MY CHANNELS ", callback_data="mychnl")
btnbotstatus= types.InlineKeyboardButton(text=" 📊 Bot Status ", callback_data="btstts")
btnhelp = types.InlineKeyboardButton(text=" 🆘 Help  ", callback_data="hlp")
btnshrebot = types.InlineKeyboardButton(text="🔄 Share Bot  ", switch_inline_query="")
btnabtdev = types.InlineKeyboardButton("About Dev ❤️", callback_data="strtDevEdt")

Closewndw = types.InlineKeyboardButton(text="❌ Close",callback_data = "clsewndw")
#admin
btnhome = types.InlineKeyboardButton(" 🔙 ", callback_data="backtohome")
btnadmnhome = types.InlineKeyboardButton(" 🔙 ", callback_data="backadminhome")
adminuseropt = types.InlineKeyboardButton(" 👥 User ", callback_data="useropt")
adminchnlopt = types.InlineKeyboardButton(" 💬 Channels ", callback_data="chnlopt")
adminlistopt = types.InlineKeyboardButton(" 🗒️ Lists ", callback_data="listopt")
FakeChannelEntry = types.InlineKeyboardButton(" 😉 Fake Registration ", callback_data="fakeentery")
vrfyuser = types.InlineKeyboardButton(" 🔁 Verify Users ", callback_data="vrfyusrs")
brdcastUser = types.InlineKeyboardButton(" 📢 Broadcast ", callback_data="brdcstusrs")
UserInfo = types.InlineKeyboardButton(" 👦 User Info ", callback_data="userinfo")
vrfychnl = types.InlineKeyboardButton(" 🔁 Verify Channels ", callback_data="vrfychnls")
MnmRqrdSubs = types.InlineKeyboardButton("📶 Minimum Req. Subs. ", callback_data="mnmreqsubs")
ChnlInfo = types.InlineKeyboardButton(" ⚠️ Channel Info ", callback_data="chnlinfo")
RmvChnl = types.InlineKeyboardButton(" ⛔ Remove A Channel ", callback_data="rmvchnl")
UpdtSubs = types.InlineKeyboardButton(" 🔄 Update Subscribers ", callback_data="updtsubs")
Rearrngechnl = types.InlineKeyboardButton(" ☢️ Rearrange Channels ", callback_data="rearrngechnl")
LstWebPrvw = types.InlineKeyboardButton(" List Web preview ", callback_data="lstwebprvw")
setListType = types.InlineKeyboardButton(" 💡 List Type ", callback_data="listtypeset")
ClassicUNameListY = types.InlineKeyboardButton(" ✅ Classic  UUname List ", callback_data="clicknotagn")#"clsklUnameistY")
ClassicNameListY = types.InlineKeyboardButton(" ✅ Classic  UCname List ", callback_data="clicknotagn")#"clsklCnameistY")
StandardListY = types.InlineKeyboardButton(" ✅ Standard  List ", callback_data="clicknotagn")#"StandardlistY")
ButtonListY = types.InlineKeyboardButton(" ✅ Button  List ", callback_data="clicknotagn")#"ButtonlistY")
ClassicUNameListN = types.InlineKeyboardButton(" ◻️ Classic UName  List ", callback_data="clskUnamelistN")
ClassicNameListN = types.InlineKeyboardButton(" ◻️ Classic CName  List ", callback_data="clskCnamelistN")
StandardListN = types.InlineKeyboardButton(" ◻️ Standard  List ", callback_data="StandardlistN")
ButtonListN = types.InlineKeyboardButton(" ◻️ Button  List ", callback_data="ButtonlistN")
FrwdList = types.InlineKeyboardButton(text=" ➡️📋 Forward List ", callback_data="frwdlists")
CreateList = types.InlineKeyboardButton(text=" ☣️ Create List  ", callback_data="createlist")
Setblwbtn = types.InlineKeyboardButton(text="➡️ Set Buttons ", callback_data="setblwbtns")
UpdtBtns = types.InlineKeyboardButton(text="🔄 Update Buttons ", callback_data="updtbtns")
Hdrspncr = types.InlineKeyboardButton(text="⬆️ Header Sponcer ", callback_data="hdrspncr")
Ftrspncr = types.InlineKeyboardButton(text="⬇️ Footer Sponcer ", callback_data="ftrspncr")
SetEmoji = types.InlineKeyboardButton(text="♐ Emoji ", callback_data="setemoji")
SetCptn = types.InlineKeyboardButton(text="♎ Set Captions ", callback_data="setcptn")
ChnlInaList = types.InlineKeyboardButton(text="Channels In One List", callback_data="chnlinalist")
SetPic = types.InlineKeyboardButton(text="▶️ Set Pic ", callback_data="setpic")
FxdButtonN = types.InlineKeyboardButton(" ◻️ Add Buttons ", callback_data="FxdButtonN")
FxdButtonY = types.InlineKeyboardButton(" ✅ Remove Buttons ", callback_data="FxdButtonY")
picN = types.InlineKeyboardButton(" ◻️ Add Pic In List ", callback_data="picy")
picY = types.InlineKeyboardButton(" ✅ Remove Pic  From List", callback_data="picn")
captN = types.InlineKeyboardButton(" ◻️ Add Caption in List ", callback_data="capty")
captY = types.InlineKeyboardButton(" ✅ Remove Caption From List", callback_data="captn")
EnblPrvw = types.InlineKeyboardButton(" ◻️ Enable Preview ", callback_data="enbleprvw")
DsblPrvw = types.InlineKeyboardButton(" ✅ Disable Preview ", callback_data="dsblprvw")
FxdButtonYPrvw = types.InlineKeyboardButton(" 🔰 Preview Of Buttons", callback_data="FxdButtonYPrvw")
DltList = types.InlineKeyboardButton(text=" 🗑️ Delete List ", callback_data="dltlists")
FrwdAll = types.InlineKeyboardButton(text=" ➡️ To All ", callback_data="frwrdpstall")
FrwdFew = types.InlineKeyboardButton(text=" ☯️ To Few ", callback_data="frwrdpstfew")
DltAll = types.InlineKeyboardButton(text=" 🗑️ To All ", callback_data="dltpstall")
DltFew = types.InlineKeyboardButton(text=" 🗑️ To Few ", callback_data="dltpstfew")
btncncl = types.KeyboardButton('🚫 Cancel')
UpdatwCapt = types.InlineKeyboardButton(text="🔄 Update Caption ", callback_data="updtcptn")
UpdatwPic = types.InlineKeyboardButton(text="🔄 Update Pic ", callback_data="updtpic")


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

class Clswndw:
  key = types.InlineKeyboardMarkup()
  key.add(Closewndw)

class CancelKey:
  keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
  keyboard.add(btncncl)

class RmvKeyBrd:
  key = types.ReplyKeyboardRemove()
  
class Ntanychnl:
  key = types.InlineKeyboardMarkup()
  key.add(btnaddcnnl,btnhome)

class AdminMenu:
  key = types.InlineKeyboardMarkup()
  key.add(adminuseropt,adminchnlopt)
  key.add(adminlistopt)
  #key.add(FakeChannelEntry)

class Adminuserpnl:
  key = types.InlineKeyboardMarkup()
  key.add(vrfyuser,brdcastUser)
  key.add(UserInfo)
  key.add(btnadmnhome)

class Adminchnlpnl:
  key = types.InlineKeyboardMarkup()
  key.add(vrfychnl,ChnlInfo)
  key.add(RmvChnl,UpdtSubs)
  key.add(MnmRqrdSubs,Rearrngechnl)
  key.add(btnadmnhome)

class AdminListpnl:
  key = types.InlineKeyboardMarkup()
  key.add(setListType)
  key.add(CreateList,Setblwbtn)
  key.add(Hdrspncr,Ftrspncr)
  key.add(SetEmoji,SetCptn)
  key.add(SetPic,LstWebPrvw)
  key.add(FrwdList,DltList)
  key.add(ChnlInaList)
  key.add(btnadmnhome)
  
class ClassicUListY:
  key = types.InlineKeyboardMarkup()
  key.add(ClassicUNameListY)
  key.add(ClassicNameListN)
  key.add(StandardListN,ButtonListN)
  key.add(btnadmnhome)
  
class ClassicNListY:
  key = types.InlineKeyboardMarkup()
  key.add(ClassicUNameListN)
  key.add(ClassicNameListY)
  key.add(StandardListN,ButtonListN)
  key.add(btnadmnhome)

class StandardListY:
  key = types.InlineKeyboardMarkup()
  key.add(ClassicUNameListN)
  key.add(ClassicNameListN)
  key.add(StandardListY,ButtonListN)
  key.add(btnadmnhome)

class ButtonListY:
  key = types.InlineKeyboardMarkup()
  key.add(ClassicUNameListN)
  key.add(ClassicNameListN)
  key.add(StandardListN,ButtonListY)
  key.add(btnadmnhome)

class FrwdListopt:
  key = types.InlineKeyboardMarkup()
  key.add(FrwdAll,FrwdFew)
  key.add(btnadmnhome)

class DltListopt:
  key = types.InlineKeyboardMarkup()
  key.add(DltAll,DltFew)
  key.add(btnadmnhome)
  
class FxdListN:
  key = types.InlineKeyboardMarkup()
  key.add(UpdtBtns,FxdButtonN)
  key.add(FxdButtonYPrvw)
  key.add(btnadmnhome)

class FxdListY:
  key = types.InlineKeyboardMarkup()
  key.add(UpdtBtns,FxdButtonY)
  key.add(FxdButtonYPrvw)
  key.add(btnadmnhome)

class EblPrvw:
  key = types.InlineKeyboardMarkup()
  key.add(EnblPrvw)
  key.add(btnadmnhome)

class Dblprvw:
  key = types.InlineKeyboardMarkup()
  key.add(DsblPrvw)
  key.add(btnadmnhome)

class AdminHome:
  key = types.InlineKeyboardMarkup()
  key.add(btnadmnhome)

class SponcerpicY:
  key = types.InlineKeyboardMarkup()
  key.add(picN)
  key.add(UpdatwPic,Closewndw)

class SponcerpicN:
  key = types.InlineKeyboardMarkup()
  key.add(picY)
  key.add(UpdatwPic,Closewndw)
  
class CaptsY:
  key = types.InlineKeyboardMarkup()
  key.add(captN)
  key.add(UpdatwCapt,Closewndw)

class CaptsN:
  key = types.InlineKeyboardMarkup()
  key.add(captY)
  key.add(UpdatwCapt,Closewndw)
