import g4f


# print(g4f.Provider.Ails.params) # supported args

# Automatic selection of provider

# streamed completion
# response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', messages=[
#                                      {"role": "user", "content": "Hello world"}], provider=g4f.Provider.AiService)
# print("".join(response))

# response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', messages=[
#                                      {"role": "user", "content": "Hello world"}], provider=g4f.Provider.ChatgptAi)
# print("".join(response))

# response = g4f.ChatCompletion.create(model='falcon-40b', messages=[
#                                      {"role": "user", "content": "Hello world"}], provider=g4f.Provider.H2o)

# print("".join(response))

response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', messages=[
{"role": "user", "content": """
Summarize me next message shortly, determining: 
Is this message about selling or providing service?
Which product or products to sell or service to provide?
Is it have a price?
Is it have contact numbers? 
 
Message may be in uzbek latin, uzbek cyrllic or in russian language

If this message about selling or providing service respond me in format: 
 name of products: <product names>, 
 prices: <prices>, 
 contact numbers: <contact numbers>, 
 category: <category>, 
 sub category: <sub category>  
 
 else 'This message is not about selling or providing service'"""},



{"role": "user", "content": """
Буғдой бор бор 20 тонна рассипной 2700 сом .
Манзил: Олтиариқ.т
Тел: 906314887

"""}], provider=g4f.Provider.Aichat)

print("".join(response))

# response = g4f.ChatCompletion.create(model='falcon-40b', messages=[
#                                      {"role": "user", "content": "Hello world"}], provider=g4f.Provider.Bing)

# print("".join(response))

