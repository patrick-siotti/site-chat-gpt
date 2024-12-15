from fasthtml.common import *

def html(
  title:str, 
  *args, 
  theme=[
          "light",
          "dark",
          "cupcake",
          "bumblebee",
          "emerald",
          "corporate",
          "synthwave",
          "retro",
          "cyberpunk",
          "valentine",
          "halloween",
          "garden",
          "forest",
          "aqua",
          "lofi",
          "pastel",
          "fantasy",
          "wireframe",
          "black",
          "luxury",
          "dracula",
          "cmyk",
          "autumn",
          "business",
          "acid",
          "lemonade",
          "night",
          "coffee",
          "winter",
          "dim",
          "nord",
          "sunset",
        ]
  ):  
  return_html = Title(title), Main(
    Html(      
      *args,
      Link(href='https://cdn.jsdelivr.net/npm/daisyui@4.12.19/dist/full.min.css', rel="stylesheet", type="text/css"),
      Script(src='https://cdn.tailwindcss.com'),
      data_theme=theme if type(theme) == str else 'dark',
    )
  )
  return return_html

def chat(conversa, carregando=False):
  if not conversa:
    return Div(
      H1('nenhuma mensagem!', cls='text-center text-2xl text-inherit'),
      id='chat',
      cls='h-[80vh] flex flex-col-reverse my-4'
    )
  return Div(
    Div(
      Div(
        Span(cls='loading loading-dots loading-md'),
        cls='chat-bubble chat-bubble-secondary'
      ),
      cls='chat chat-start'
    ) if carregando else None,
    *[Div(
        Div(
          P(msg, cls='max-w-[30vh]'),
          cls = f'chat-bubble {"chat-bubble-accent" if usr == "user" else "chat-bubble-secondary"}'
        ),
        cls = f'chat {"chat-end" if usr == "user" else "chat-start"}'
      )
      for usr, msg in reversed(conversa)
    ],
    id='chat',
    cls='h-[80vh] flex flex-col-reverse my-4 scroll-smooth overflow-auto'
  )

def input():
  return Input(type="text", placeholder='falar com o gpt', name='msg', id='input_chat', cls='input input-bordered')

def form_chat():
  return Form(
    Group(
      input(),
      Button('enviar', cls='btn btn-secundary'),
    ),
    ws_send=True
  )

def chat_bot(conversa=None):
  return Div(
    H1('chat bot online', cls='text-center text-2xl text-inherit'),
    chat(conversa),
    form_chat(),
    cls='w-1/2 self-center'
  )