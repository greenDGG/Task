# YouTube Telegram Bot

Bot que escucha mensajes en un canal de Telegram, extrae links de YouTube, da like/se suscribe, captura pantalla y envia el resultado a un usuario.

## Requisitos

- Python 3.8+
- Chrome (para setup inicial)
- Playwright + Chromium (para ejecucion)

## Instalacion

```bash
pip install playwright telethon python-dotenv
playwright install
```

## Configuracion

1. Ir a https://my.telegram.org/ y obtener **API_ID** y **API_HASH**
2. Copiar `.env.example` a `.env` y completar los datos

## Uso

### 1. Iniciar sesion en Telegram

```bash
python setup_telegram.py
```

Te pedira numero de telefono y codigo de verificacion. Crea `sessions/telegram_session.session`.

### 2. Identificar canal y usuario destino

```bash
python list_chats.py
```

Muestra todos tus chats con sus IDs. Anota el ID del canal donde llegan las alertas y el @username del destinatario para el `.env`.

### 3. Iniciar sesion en YouTube

```bash
python setup_youtube.py
```

Se abre Chrome. Inicia sesion en YouTube, luego vuelve a la terminal y presiona Enter. Guarda las cookies en `sessions/youtube_cookies.json`.

### 4. Ejecutar el bot

```bash
python main.py
```

El bot escucha mensajes del canal configurado. Cuando detecta un link de YouTube, automaticamente:

1. Abre el video
2. Salta anuncios si aparecen
3. Da like (si no tiene)
4. Se suscribe (si no lo esta)
5. Captura pantalla
6. Envia la imagen a `@usuario` con el texto `T{numero} completado`

Los mensajes sin link de YouTube se ignoran. Las URLs ya procesadas (mismo timestamp + task + url) no se repiten.

## Estructura

```
├── main.py                    # Orquestador
├── setup_telegram.py          # Login Telegram (una vez)
├── setup_youtube.py           # Login YouTube + cookies (una vez)
├── list_chats.py              # Lista chats/IDs
├── parser.py                  # Extrae task number y URL del mensaje
├── history.py                 # Historial de tareas (historial.json)
├── telegram/
│   ├── bot.py                 # Cliente Telegram (Telethon)
├── youtube/
│   ├── browser.py             # Lanzador Chrome/Chromium
│   ├── cookies.py             # Gestion de cookies
│   └── actions.py             # Navegacion, like, subscribe, screenshot
├── sessions/                  # Sesion Telegram + cookies YouTube
├── screenshots/               # Capturas de pantalla
├── .env                       # Configuracion
├── bot.log                    # Log de errores
└── historial.json             # Registro de tareas procesadas
```

## Variables de entorno (.env)

| Variable | Descripcion |
|---|---|
| `API_ID` | De https://my.telegram.org |
| `API_HASH` | De https://my.telegram.org |
| `ALLOWED_CHAT_ID` | ID del canal donde llegan las alertas |
| `ALERT_CHANNEL` | @usuario que recibe las capturas |
| `HEADLESS` | `true` para sin ventana, `false` para ver el navegador |
