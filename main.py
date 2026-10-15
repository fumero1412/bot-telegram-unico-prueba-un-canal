from telethon import TelegramClient, events
from datetime import datetime, timezone, timedelta
import asyncio

# --- TUS DATOS ---
API_ID = 32695956
API_HASH = '8d939c8130ea03c01cd9abe6a6e83d7a'
SESSION = 'sesion_nube'

CANAL_ORIGEN = 'https://t.me/Horny_J'
GRUPO_DESTINO = 'https://t.me/+aH8ADmCchLYyNzNh'
TOPIC_ID = 713969

# --- FECHA DESDE DONDE CONTINUAR ---
# 7 Agosto 2022 4:38 AM Hora Cuba = 8:38 AM UTC
DESDE_FECHA = datetime(2022, 8, 7, 8, 38, 0, tzinfo=timezone.utc)

client = TelegramClient(SESSION, API_ID, API_HASH)

async def copiar_historial():
    print(f"Iniciando recuperacion desde {DESDE_FECHA}...")
    origen = await client.get_entity(CANAL_ORIGEN)
    destino = await client.get_entity(GRUPO_DESTINO)
    
    count = 0
    # reverse=True = empieza desde esa fecha hacia adelante
    async for msg in client.iter_messages(origen, offset_date=DESDE_FECHA, reverse=True):
        if not msg: continue
        
        texto = (msg.text or msg.message or "").strip()
        tiene_media = msg.media is not None
        es_telegraph = texto.startswith("https://telegra.ph")

        # TU FILTRO: Solo archivos o telegra.ph, ignora "hola, me gusto"
        if not tiene_media and not es_telegraph:
            continue

        try:
            if tiene_media:
                await client.send_file(destino, msg.media, caption=msg.text, reply_to=TOPIC_ID)
            else:
                await client.send_message(destino, msg.text, reply_to=TOPIC_ID)
            
            count += 1
            print(f"[{count}] Copiado ID {msg.id}")
            await asyncio.sleep(1.2) # para que no te banee Telegram
        except Exception as e:
            print(f"Error en {msg.id}: {e}")
            await asyncio.sleep(3)

    print(f"¡Historial terminado! Total: {count} mensajes")

@client.on(events.NewMessage(chats=CANAL_ORIGEN))
async def handler(event):
    texto = (event.message.text or "").strip()
    tiene_media = event.message.media is not None
    es_telegraph = texto.startswith("https://telegra.ph")

    if not tiene_media and not es_telegraph:
        return

    try:
        destino = await client.get_entity(GRUPO_DESTINO)
        if tiene_media:
            await client.send_file(destino, event.message.media, caption=event.message.text, reply_to=TOPIC_ID)
        else:
            await client.send_message(destino, event.message.text, reply_to=TOPIC_ID)
        print("Nuevo mensaje en vivo copiado!")
    except Exception as e:
        print(e)

async def main():
    await client.start()
    await copiar_historial() # Primero se pone al dia
    print("AHORA SI - QUEDANDO VIVO PARA LO NUEVO")
    await client.run_until_disconnected()

asyncio.run(main())