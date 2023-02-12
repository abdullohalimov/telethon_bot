
# from collections import Counter 
  
# # counts word frequency
# def count_words(text):                  
#     skips = [".", ", ", ":", ";", "'", '"', "\n", '\xa0'] 
#     for ch in skips: 
#         text = text.replace(ch, " ") 
#     word_counts = {} 
#     for word in text.split(" "): 
#         if word in word_counts: 
#             word_counts[word]+= 1 
#         else: 
#             word_counts[word]= 1 
#     return word_counts 
  
#     # >>>count_words(text) You can check the function 
  
# # counts word frequency using
# # Counter from collections 
# def count_words_fast(text):     
#     text = text.lower() 
#     skips = [".", ", ", ":", ";", "'", '"', '\n'] 
#     for ch in skips: 
#         text = text.replace(ch, " ") 
#     word_counts = Counter(text.split(" ")) 
#     return word_counts 
  
#     # >>>count_words_fast(text) You can check the function 

# txt = """
# [ Album ]
# Diqqat sotiladi
# 🦬  Buqacha yeb ichiwi zoʻr sogʻlom
# 💵Narxi: 10 mln keliwamiz
# 🏠Manzil: Parkent tuamni ( Tambalak )
# Tel:📲 +998943678171





# Admin @FURQAT_T
# Bizning kanal
# @Parkent_molbozor
# Dostlarga ulawing
# """
# print(count_words(text=txt))

from database import Person

select = Person.select()

print(select[207 -1].message_text)