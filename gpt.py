from gpt_selenium.gpt import Modelos

class GptOnline:
  def __init__(self):
    self.grupo = Modelos(debug=False)
    
  async def start(self):
    # await self.grupo._start()
    ...
  
  async def create_model(self):
    return await self.grupo.create_model()