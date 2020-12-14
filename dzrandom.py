# AsenaUserBot - @Xacnio #

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.errors.common import AlreadyInConversationError
from userbot import bot
from userbot.cmdhelp import CmdHelp
from userbot.events import register
from random import randint
from asyncio.exceptions import TimeoutError


@register(outgoing=True, pattern="^.dzrandom$")
@register(outgoing=True, pattern="^.dzrandom (.*)$")
@register(outgoing=True, pattern="^.dzrand$")
@register(outgoing=True, pattern="^.dzrand (.*)$")
async def dzrandom(event):
    try:
        artist = event.pattern_match.group(1)
    except IndexError:
        return await event.edit("`Komutu `__.dzrand <Şarkıcı(lar)>__` formatında yazmalısınız!`")

    reply_to = None
    if event.is_reply:
        reply_to = await event.get_reply_message()

    artists_note = ""
    if artist.count(",") > 0:
        artistler = artist.split(",")
        for index, element in enumerate(artistler):
            string = element.strip()
            if len(string) == 0:
                artistler.remove(element)
        if len(artistler) > 0:
            artists_note = "__" + str(len(artistler)) + " şarkıcı arasından__ ve "
            await event.edit(f"__Yazılan şarkıcılardan rastgele bir şarkıcı seçiliyor...__")
            artist = artistler[randint(0, len(artistler)-1)]


    await event.edit(f"__{artist} adlı şarkıcıdan rastgele bir şarkı seçiliyor...__")
    chat = "@DeezerMusicBot"
    try:
        async with bot.conversation(chat) as conv:
            try:     
                mesaj = await conv.send_message(str(randint(31,62)))
                test = await conv.get_response()
                await mesaj.delete()
                await test.delete()
            except YouBlockedUserError:
                await event.edit(f"`Mmmh sanırım` {chat} `engellemişsin. Lütfen engeli aç.`")
                return
            await conv.send_message(artist)
            firstStep = await conv.wait_event(events.NewMessage(incoming=True,from_users=595898211))
            await event.client.send_read_acknowledge(conv.chat_id)
            buton1 = None
            buton2 = None
            if not firstStep.buttons:
                return await event.edit(f"`Uygun şekilde şarkıcı araması yapılamadı! Bota gidip botun yanıtına bakabilirsin. ({chat})`") 
            try:
                for i, butonH in enumerate(firstStep.buttons):
                    if buton1 is not None:
                        break
                    for j, butonV in enumerate(butonH):
                        if str(butonV.text).find("Artists") != -1:
                            buton1 = i
                            buton2 = j
            except TypeError:
                return await event.edit(f"`Şarkıcı araması yapılamadı!`")     

            if buton1 is None:
                return await event.edit(f"`Şarkıcı araması yapılamadı!`")         

            await firstStep.click(buton1, buton2)
            try:
                performers = await conv.wait_event(events.MessageEdited(incoming=True,from_users=595898211))
            except TimeoutError:
                return await event.edit(f"`İstek zaman aşımına uğradı, şarkıcı getirilemedi!`")
            if performers.buttons[0][0].text == "No results":
                return await event.edit(f"`Şarkıcı bulunamadı!`")
            sanatci = str(performers.buttons[0][0].text).split(". ", 1)[1]
            await event.edit(f"__{sanatci} adlı şarkıcının albümleri getiriliyor...__")           
            await performers.click(0)
            try:
                sarkici = await conv.wait_event(events.NewMessage(incoming=True,from_users=595898211))
            except TimeoutError:
                return await event.edit(f"`İstek zaman aşımına uğradı, şarkıcının albümleri getirilemedi!`")
            await performers.delete()
            await event.client.send_read_acknowledge(conv.chat_id)
            if sarkici.buttons[0][1].text != "Albums":
                return await event.edit(f"`Şarkıcının albümleri bulunamadı!`")
            await sarkici.click(0, 1)
            try:
                albumler = await conv.wait_event(events.MessageEdited(incoming=True,from_users=595898211))
            except TimeoutError:
                return await event.edit(f"`İstek zaman aşımına uğradı, şarkıcının albümleri getirilemedi!`")
            albumler.buttons.pop()
            if len(albumler.buttons) < 1:
                return await event.edit(f"`Şarkıcının albümleri bulunamadı!`")
            randomAlbum = randint(0, len(albumler.buttons)-1)
            album = str(albumler.buttons[randomAlbum][0].text)
            await event.edit(f"__{sanatci} - {album} adlı albümünden bir parça getiriliyor...__")
            await albumler.click(randomAlbum)
            try:
                sarkilar = await conv.wait_event(events.NewMessage(incoming=True,from_users=595898211))
            except TimeoutError:
                return await event.edit(f"`İstek zaman aşımına uğradı, albüm getirilemedi!`")
            await albumler.delete()
            await event.client.send_read_acknowledge(conv.chat_id)
            sarkilar.buttons.pop()
            sarkilar.buttons.pop()
            if len(sarkilar.buttons) < 1:
                return await event.edit(f"`Şarkıcının seçilen albümündeki şarkılar bulunamadı!`")
            randomSarki = randint(0, len(sarkilar.buttons)-1)
            title = str(sarkilar.buttons[randomSarki][0].text).split(". ", 1)[1]
            secilensarki = f"{sanatci} - {title}"
            await event.edit(f"__{secilensarki} adlı parça seçildi. MP3 getiriliyor...__")
            await sarkilar.click(randomSarki)
            try:
                sarki = await conv.wait_event(events.NewMessage(incoming=True,from_users=595898211))
            except TimeoutError:
                return await event.edit(f"`İstek zaman aşımına uğradı, şarkı getirilemedi!\n__Seçilen Şarkı:__ `{secilensarki}`")
            await sarkilar.delete()
            await event.client.send_read_acknowledge(conv.chat_id)
            if sarki.audio:
                title = sarki.audio.attributes[0].title
                performer = sarki.audio.attributes[0].performer
                await event.client.send_file(event.chat_id, sarki.audio, caption=f"@AsenaUserBot sizin için {artists_note}__{performer}__ adlı şarkıcıdan bir parça seçti :)", reply_to=reply_to)
                await event.delete()
            else:
                return await event.edit(f"`Şarkı bir hatadan dolayı getirilemedi!\n__Seçilen Şarkı:__ `{secilensarki}`")
    except AlreadyInConversationError:
        return await event.edit(f"`Şu anda botunuz mevcut olarak başka bir chat işlemi yapıyor. Hata varsa botu yeniden başlatın.`")



Help = CmdHelp('dzrandom')
Help.add_command('dzrand', 
    '<Şarkıcı(lar)>', 
    'Yazdığınız şarkıcıdan veya virgülle ayırarak yazdığınız şarkıcılardan rastgele bir parça getirir. Şarkıcı ismini tam yazdığınızdan emin olun aksi taktirde istediğiniz şarkıcının şarkıları çıkmayabilir.',
    'dzrand Sagopa,Ceza').add()
Help.add_info('Yapımcı: @Xacnio')
Help.add_warning('Plugin @DeezerMusicBot tarafından çalışmaktadır. Dolayısıyla Deezer Music Bot\'ta sorun var ise plugin çalışmaz.')
Help.add()