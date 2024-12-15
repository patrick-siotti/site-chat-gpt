from fasthtml.common import *
from uuid import uuid4
import asyncio

import components
from session import Sessions, Session

app, rt = fast_app(debug=True, live=True, exts='ws')
sessions = Sessions()

@rt('/create_session')
async def get():
  resp = RedirectResponse('/')
  uid = str(uuid4())
  resp.set_cookie('uid', uid)
  sessions.add_session(uid)
  return resp

@rt('/')
async def get(uid:str=None):
  session:Session = sessions.get_session(uid)
  if not session:
    return RedirectResponse('/create_session')
  return components.html(
    'chat com gpt online',
    Main(
      components.chat_bot(session.conversa),
      cls='container flex justify-center',
      hx_ext='ws', ws_connect='/ws'
    ),
    theme='dracula'
  )

async def connect(ws, send):
  uid = ws.cookies.get('uid')
  session:Session = sessions.get_session(uid)
  if session.model == None:
    await sessions.create_model(uid)
  session.send = send
  
  asyncio.create_task(session.spake())
  
  await send(f'session {uid} configured')

async def disconnect(ws):
  uid = ws.cookies.get('uid')
  session:Session = sessions.get_session(uid)
  await session.stop_model()
  session.model = None
  session.send = None

@app.ws('/ws', conn=connect, disconn=disconnect)
async def ws(ws, send, msg:str):
  uid = ws.cookies.get('uid')
  session:Session = sessions.get_session(uid)
  session.conversa.append(['user', msg])
  try:
    await session.send(components.input())
  except:
    session.send = send
    await send(components.input())
  session.perguntas.append(msg)
  await send(f'sessão {uid} enviada')

serve()