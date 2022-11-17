from GET_OLX_APARTMENT import webscrapOLX
from pymongo import MongoClient


MONGODB_CONNECTION_STRING = "PLACE HERE MANGODB CONNECTION STRING"
client = MongoClient(MONGODB_CONNECTION_STRING)
client.server_info()['ok']

id_district = [367, 365, 369, 353, 355, 381, 379, 361, 377, 371, 373, 383, 533, 375, 359, 357, 351, 363]
replace_values = {367 : 'Bemowo', 365 : "Białołęka", 369 : "Bielany", 353 : "Mokotów", 355 : "Ochota", 381 : "Praga Południe", 379 : "Praga Północ", 361 : "Rembertów", 377 : "Targówek", 371 : "Ursus", 373 : "Ursynów", 383 : "Wawer", 533 : "Wesoła", 375 : "Wilanów", 359 : "Wola", 357 : "Włochy", 351 : "Śródmieście", 363 : "Żoliborz"}

df = webscrapOLX("warszawa", id_district)
df = df.drop_duplicates()
df = df.replace({"District": replace_values})
print(df.head())
print(df.describe())

# convert to dictionary for uploading to MongoDB
symbol_dict = df.to_dict('records')
# point to symbolsDB collection 
db = client.symbolsDB
# insert new documents to collection
db.symbols.insert_many(symbol_dict)

print("DATA OBTAINED")