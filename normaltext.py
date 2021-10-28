from config import Config

welcome = '''👋 Welcome {} . 
This is Promotion Bot for Registration 
Of channels.'''

adminpnl = '''👤 This is The Admin Pannel'''

nonadminpnl = '''<b>Opps! ☹️ , You are not an admin</b>'''

sharetext = '''<b>I invite You to join The Best Promotion Bot of This Era.
Bot Username : @{}</b>'''

HelpText = '''<b>⚠️ This is Help Pannel:

This Is A Promotion Bot. If u Need any Type of Help about promoting of Your Channel. Your can frequently ask your questions directly Just Ping Me @Jai_Mahakal_Ji .

◼️Promotion Rules
───────────
➤ 24 hours in the channel.
➤ Don't Delete The List Before 24 hours Manually.

● If you want to get unban then contact Admin

🚫 Those who break the rules will be banned from the bot.</b>'''

dvlprText = '''<b>About Me 😎
<b>----------------------------------------------------</b>
🤖 Name :''' + "<a href='t.me/{}'>{}</a>" + '''
👨‍💻 Developer : @Jai_Mahakal_Ji
📝 Language : </b><code>Python 3. 9.7</code>
<b>📲 Version :</b> <code>1.0.2</code>
<b>🧰 Framework :</b> <code>PyTelegramBotAPI</code>
<b>📡 Server :</b> <code>Heroku</code>
<b>----------------------------------------------------</b>
<b>Made With ❤️ In India 🇮🇳 </b>'''

note = "⚠️ Note:- Your default channel description is your channel name. If u want to update it then Go through My channels"
ChnlAdSucess = f"<b>✅ Your channel</b> "+ '<a href="{}">{} </a>' + f"<b>is added successfully. </b> \n\n<code>{note}</code> ."

updateChnlData = "<b>☹️ Its Not For u</b>"

ReisterStepA = '''<b>Now follow the following steps</b>

<code>1. Add bot as Admin with Post , Delete Rights and Invite users By Link .
2. If u will Right Of Invite Users By link then You have not to submit Link by u own.
3. Forward any Parent message from the respective channel</code>'''

NotanyChnl = '''<b>⚠️ You haven't registered any channel with our bot yet Or Channels might have been removed or banned</b>'''

NotEnfSub = "<b>Error:</b> <code>Your Channel Have not Minimum Required Subscribers. Should Have minimum" + " {} " + "Subscribers But Your channel have only {} subscribers.</code>"

ChnlAlrdyInDTbse =  "<b>Channel is already in database Contact " + Config.AdminUsername + " to any queries.</b>"

usrststext = '''<b>Bot Users Statics 📊
➖➖➖➖➖➖➖➖➖➖➖➖➖
Total Users:</b> <code>{}</code>
<b>Active Users:</b> <code>{}</code>
<b>InActive Users:</b> <code>{}</code>'''

Chanlsststext = '''<b>Bot Channesl Statics 📊
➖➖➖➖➖➖➖➖➖➖➖➖➖
Total Channels:</b> <code>{}</code>
<b>Active Channels:</b> <code>{}</code>
<b>InActive Channels:</b> <code>{}</code>'''

setlistType = "<b>✅ Choose the list Type</b>"

listtypesetalert = "List Type Changed Successfully"

SetBtnText = '''<b>Send me The Buttons those you want to add below the list. Format is given below
Example:</b>
  <code>Channel1 😋 = https://t.me/Link1
  Channel2 💐 = https://t.me/Link2
  Channel3 ☺️ = https://t.me/Link3
  Channel4 😍 = https://t.me/Link4</code>'''

ListForwardSucess = '''<b>List Forward Status:
Successful :</b> {}
<b>Failed :</b> {}'''

ListdeleteSucess = '''<b>List Delete Status:
Successful :</b> {}
<b>Failed :</b> {}'''

chnlsccnotifytogroup = '''<b>✅ New Entry Submitted
■□■□■□■□■■□■□■□■□■
Name : {}
🆔 :</b> <code>{}</code>
<b>Username : {}</b>
<b>Subscribers :</b> <code>{}</code>
<b>Link : {}</b>
<b>👤 Admin :</b> {}'''


AbouTChnl = '''<b>Channel Details
■□■□■□■□■■□■□■□■□■
Name : {}
🆔 :</b> <code>{}</code>
<b>Username : {}</b>
<b>Subscribers :</b> <code>{}</code>
<b>Link : {}</b>
<b>👤 Admin :</b> {}'''

subsuptstst = '''<b>Subscribers Update Status:
➖➖➖➖➖➖➖➖➖➖➖➖➖
Total :</b> {}
<b>Success :</b> {}
<b>Failed :</b> {}'''

brcststatus = '''<b>Broad-Casting Status 📊
➖➖➖➖➖➖➖➖➖➖➖➖➖
Total :</b> {}
<b>Success :</b> {}
<b>Failed :</b> {}'''