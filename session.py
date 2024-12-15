import asyncio

from gpt import GptOnline
from gpt_selenium.gpt import Model
import components

class Sessions:
  _sessions = {}
  loaded = False
  is_loading = False
  gpt = GptOnline()
  
  def __init__(self):
    self.gpt = GptOnline()
  
  async def start_gpt(self):
    if self.is_loading == False:
      self.is_loading = True
    else:
      await asyncio.sleep(5)
      return
    
    await self.gpt.start()
    self.loaded = True
  
  def add_session(self, uid):
    self._sessions[uid] = Session()
  
  def get_session(self, uid=None, ws=None):
    if ws:
      uid = ws.cookies.get('sesao')
    if not uid or uid not in self._sessions:
      return None
    return self._sessions[uid]
  
  async def create_model(self, uid):
    if self.loaded == False:
      await self.start_gpt()
    self._sessions[uid].model = await self.gpt.create_model()

class Session:
  def __init__(self):
    self.conversa = []  # Agora é exclusivo para cada instância
    self.model: Model = None
    self.perguntas = []
    self.avisos = []
    self.send = None
  
  async def stop_model(self):
    await self.model.stop()
    
  async def spake(self):
    while True:
      respondidas = []
      if self.perguntas:
        await self.send(components.chat(self.conversa, len(self.perguntas)>0))
        
        for pergunta in self.perguntas:
          
          try:
            resp = await self.model.asq(pergunta)
          except:
            resp = 'desculpe, não consegui encontrar uma resposta pra isso'
          self.conversa.append(['bot', resp])
          
          respondidas.append(pergunta)
          
        for resposta in respondidas:
          del self.perguntas[self.perguntas.index(resposta)]
          
        await self.send(components.chat(self.conversa, len(self.perguntas)>0))
        
      else:
        await asyncio.sleep(1)
