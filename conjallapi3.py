import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
import random
import re
import time

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = "C:/Users/pawnl/Downloads/testagain-444816-afedf2734772.json"

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1XZp80mRFTSn7gRZJlLCEm04l2AXfkZjFB7veyPOolV0'
RANGE_NAME = 'spanishpy!A1:I1154'

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

headers = values[0] if values else []
data = [
    dict(zip(headers, row)) for row in values[1:]
] if values else []

def list_regular_verbs(data):
    regular_verbs = [entry['esp'] for entry in data if entry.get('vtype') == 'regular']
    return regular_verbs

def make_yo_(verb):
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "o"
    if verb.endswith("arse"):
        return "me " + verb[:-4] + "o"
    elif verb.endswith("irse") or verb.endswith("erse"):
            return "me " + verb[:-4] + "o"
    else:
        return ""
    return verb

def make_tu_(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "as"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "es"
    if verb.endswith("arse"):
        return "te " + verb[:-4] + "as"
    elif verb.endswith("irse") or verb.endswith("erse"):
            return "te " + verb[:-4] + "es"
    else:
        return ""
    return verb
    
def make_usted_(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "a"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "e"
    if verb.endswith("arse"):
        return "se " + verb[:-4] + "a"
    elif verb.endswith("irse") or verb.endswith("erse"):
            return "se " + verb[:-4] + "e"
    else:
        return ""
    return verb
    
def make_nos_(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "amos"
    elif verb.endswith("er"):
        return verb[:-2] + "emos"
    elif verb.endswith("ir"):
        return verb[:-2] + "imos"
    if verb.endswith("arse"):
        return "nos " + verb[:-4] + "amos"
    elif verb.endswith("irse"):
        return "nos " + verb[:-4] + "imos"
    elif verb.endswith("erse"):
        return "nos " + verb[:-4] + "emos"
    else:
        return ""
    return verb
    
def make_ustedes_(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "an"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "en"
    if verb.endswith("arse"):
        return "se " + verb[:-4] + "an"
    elif verb.endswith("irse") or verb.endswith("erse"):
            return "se " + verb[:-4] + "en"
    else:
        return ""
    return verb

def make_yo_fut(verb):
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "é"
    if verb.endswith("arse") or verb.endswith("irse") or verb.endswith("erse"):
        return "me " + verb[:-2] + "é"
    else: 
        return ""
    return verb

def make_tu_fut(verb):
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "ás"
    if verb.endswith("arse") or verb.endswith("irse") or verb.endswith("erse"):
        return "te " + verb[:-2] + "ás"
    else:
        return ""
    return verb
    
def make_usted_fut(verb):
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "á"
    if verb.endswith("arse") or verb.endswith("irse") or verb.endswith("erse"):
        return "se " + verb[:-2] + "á"
    else:
        return ""
    return verb
    
def make_nos_fut(verb):
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "emos"    
    if verb.endswith("arse") or verb.endswith("irse") or verb.endswith("erse"):
        return "nos " + verb[:-2] + "emos"
    else:
        return ""
    return verb
    
def make_ustedes_fut(verb):
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "án"
    if verb.endswith("arse") or verb.endswith("irse") or verb.endswith("erse"):
        return "se " + verb[:-2] + "án"
    else:
        return ""
    return verb

def make_yo_past(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "é"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "í"
    if verb.endswith("arse"):
        return "me " + verb[:-4] + "é"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "me " + verb[:-4] + "í"
    else: 
        return ""
    return verb

def make_tu_past(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "aste"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "iste"
    if verb.endswith("arse"):
        return "te " + verb[:-4] + "aste"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "te " + verb[:-4] + "iste"
    else: 
        return ""
    return verb
    
def make_usted_past(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "ó"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "ió"
    if verb.endswith("arse"):
        return "se " + verb[:-4] + "ó"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "se " + verb[:-4] + "ío"
    else: 
        return ""
    return verb
    
def make_nos_past(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "amos"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "imos"
    if verb.endswith("arse"):
        return "nos " + verb[:-4] + "amos"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "nos " + verb[:-4] + "imos"
    else: 
        return ""
    return verb
    
def make_ustedes_past(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "aron"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "ieron"
    if verb.endswith("arse"):
        return "se " + verb[:-4] + "aron"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "se " + verb[:-4] + "ieron"
    else: 
        return ""
    return verb

def make_yo_perf(verb):
    if verb.endswith("ar"):
        return "he " + verb[:-2] + "ado"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "he " + verb[:-2] + "ido"
    if verb.endswith("arse"):
        return "me he " + verb[:-4] + "ado"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "me he " + verb[:-4] + "ido"
    else: 
        return ""
    return verb

def make_tu_perf(verb):
    if verb.endswith("ar"):
        return "has " + verb[:-2] + "ado"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "has " + verb[:-2] + "ido"
    if verb.endswith("arse"):
        return "te has " + verb[:-4] + "ado"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "te has " + verb[:-4] + "ido"
    else: 
        return ""
    return verb
    
def make_usted_perf(verb):
    if verb.endswith("ar"):
        return "ha " + verb[:-2] + "ado"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "ha " + verb[:-2] + "ido"
    if verb.endswith("arse"):
        return "se ha " + verb[:-4] + "ado"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "se ha " + verb[:-4] + "ido"
    else: 
        return ""
    return verb
    
def make_nos_perf(verb):
    if verb.endswith("ar"):
        return "hemos " + verb[:-2] + "ado"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "hemos " + verb[:-2] + "ido"
    if verb.endswith("arse"):
        return "nos hemos " + verb[:-4] + "ado"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "nos hemos " + verb[:-4] + "ido"
    else: 
        return ""
    return verb
    
def make_ustedes_perf(verb):
    if verb.endswith("ar"):
        return "han " + verb[:-2] + "ado"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "han " + verb[:-2] + "ido"
    if verb.endswith("arse"):
        return "se han " + verb[:-4] + "ado"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "se han " + verb[:-4] + "ido"
    else: 
        return ""
    return verb

def make_yo_subju(verb):
    if verb.endswith("ar"): 
        return "que " + verb[:-2] + "e"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "que " + verb[:-2] + "a"
    if verb.endswith("arse"):
        return "que me " + verb[:-4] + "e"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "que me " + verb[:-4] + "a"
    else: 
        return ""
    return verb
    
def make_tu_subju(verb):
    if verb.endswith("ar"): 
        return "que " + verb[:-2] + "es"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "que " + verb[:-2] + "as"
    if verb.endswith("arse"):
        return "que te " + verb[:-4] + "es"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "que te " + verb[:-4] + "as"
    else: 
        return ""
    return verb
    
def make_usted_subju(verb):
    if verb.endswith("ar"): 
        return "que " + verb[:-2] + "e"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "que " + verb[:-2] + "a"
    if verb.endswith("arse"):
        return "que se " + verb[:-4] + "e"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "que se " + verb[:-4] + "a"
    else: 
        return ""
    return verb
    
def make_nos_subju(verb):
    if verb.endswith("ar"): 
        return "que " + verb[:-2] + "emos"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "que " + verb[:-2] + "amos"
    if verb.endswith("arse"):
        return "que hemos " + verb[:-4] + "emos"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "que hemos " + verb[:-4] + "amos"
    else: 
        return ""
    return verb
    
def make_ustedes_subju(verb):
    if verb.endswith("ar"): 
        return "que " + verb[:-2] + "en"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "que " + verb[:-2] + "an"
    if verb.endswith("arse"):
        return "que se " + verb[:-4] + "en"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "que se " + verb[:-4] + "an"
    else: 
        return ""
    return verb
        
def make_yo_ppsub(verb):
    if verb.endswith("ar"):
        return "hubiera " + verb[:-2] + "ado"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "hubiera " + verb[:-2] + "ido"
    if verb.endswith("arse"):
        return "me hubiera " + verb[:-4] + "ado"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "me hubiera " + verb[:-4] + "ido"
    else: 
        return ""
    return verb

def make_tu_ppsub(verb):
    if verb.endswith("ar"):
        return "hubieras " + verb[:-2] + "ado"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "hubieras " + verb[:-2] + "ido"
    if verb.endswith("arse"):
        return "te hubieras " + verb[:-4] + "ado"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "te hubieras " + verb[:-4] + "ido"
    else: 
        return ""
    return verb
    
def make_usted_ppsub(verb):
    if verb.endswith("ar"):
        return "hubiera " + verb[:-2] + "ado"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "hubiera " + verb[:-2] + "ido"
    if verb.endswith("arse"):
        return "se hubiera " + verb[:-4] + "ado"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "se hubiera " + verb[:-4] + "ido"
    else: 
        return ""
    return verb
    
def make_nos_ppsub(verb):
    if verb.endswith("ar"):
        return "hubiéramos " + verb[:-2] + "ado"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "hubiéramos " + verb[:-2] + "ido"
    if verb.endswith("arse"):
        return "nos hubiéramos " + verb[:-4] + "ado"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "nos hubiéramos " + verb[:-4] + "ido"
    else: 
        return ""
    return verb
    
def make_ustedes_ppsub(verb):
    if verb.endswith("ar"):
        return "hubieran " + verb[:-2] + "ado"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "hubieran " + verb[:-2] + "ido"
    if verb.endswith("arse"):
        return "se hubieran " + verb[:-4] + "ado"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "se hubieran " + verb[:-4] + "ido"
    else: 
        return ""
    return verb

def make_yo_imperf(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "aba"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "ía"
    if verb.endswith("arse"):
        return "me " + verb[:-4] + "aba"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "me " + verb[:-4] + "ía"
    else: 
        return ""
    return verb

def make_tu_imperf(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "abas"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "ías"
    if verb.endswith("arse"):
        return "te " + verb[:-4] + "abas"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "te " + verb[:-4] + "ías"
    else: 
        return ""
    return verb
    
def make_usted_imperf(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "aba"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "ía"
    if verb.endswith("arse"):
        return "se " + verb[:-4] + "aba"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "se " + verb[:-4] + "ía"
    else: 
        return ""
    return verb
    
def make_nos_imperf(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "ábamos"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "íamos"
    if verb.endswith("arse"):
        return "nos " + verb[:-4] + "ábamos"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "nos " + verb[:-4] + "íamos"
    else: 
        return ""
    return verb
    
def make_ustedes_imperf(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "aban"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "ían"
    if verb.endswith("arse"):
        return "se " + verb[:-4] + "aban"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "se " + verb[:-4] + "ían"
    else: 
        return ""
    return verb

def make_yo_orders(verb):
    if verb.endswith("ar"):
        return "no " + verb[:-2] + "es"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "no " + verb[:-2] + "as"
    if verb.endswith("arse"):
        return "no te " + verb[:-4] + "es"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "no te " + verb[:-4] + "as"
    else: 
        return ""
    return verb

def make_tu_orders(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "a"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "e"
    if verb.endswith("arse"):
        return verb[:-4] + "ate"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return verb[:-4] + "ete"
    else: 
        return ""
    return verb
    
def make_usted_orders(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "e"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "a"
    if verb.endswith("arse"):
        return verb[:-4] + "ese"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return verb[:-4] + "ase"
    else: 
        return ""
    return verb
    
def make_nos_orders(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "emos"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "amos"
    if verb.endswith("arse"):
        return verb[:-4] + "emonos"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return verb[:-4] + "amonos"
    else: 
        return ""
    return verb
    
def make_ustedes_orders(verb):
    if verb.endswith("ar"):
        return verb[:-2] + "en"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "an"
    if verb.endswith("arse"):
        return verb[:-4] + "ense"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return verb[:-4] + "anse"
    else: 
        return ""
    return verb

def make_yo_cond(verb):
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "ía"
    if verb.endswith("se"):
        return "me " + verb[:-2] + "ía"
    else:
        return ""
    return verb

def make_tu_cond(verb):
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "ías"
    if verb.endswith("se"):
        return "te " + verb[:-2] + "ías"
    else:
        return ""
    return verb

def make_usted_cond(verb):
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "ía"
    if verb.endswith("se"):
        return "se " + verb[:-2] + "ía"
    else:
        return ""
    return verb
    
def make_nos_cond(verb):
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "íamos"
    if verb.endswith("se"):
        return "nos " + verb[:-2] + "íamos"
    else:
        return ""
    return verb

def make_ustedes_cond(verb):
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "ían"
    if verb.endswith("se"):
        return "se " + verb[:-2] + "ían"
    else:
        return ""
    return verb

def print_conj_pres(all):
    regular_verbs = list_regular_verbs(data)
    result = "Todos los verbos en presente:\n\n"
    for verb in regular_verbs:
        result += str(verb) + "\n\n"
        result += "Yo       | " + str(make_yo_(verb)) + "\n"
        result += "Tu       | " + str(make_tu_(verb)) + "\n"
        result += "Usted    | " + str(make_usted_(verb)) + "\n"
        result += "Nosotros | " + str(make_nos_(verb)) + "\n"
        result += "Ustedes  | " + str(make_ustedes_(verb)) + "\n"
        result += "\n"
    return result

def print_conj_fut(all):
    regular_verbs = list_regular_verbs(data)
    result = "Todos los verbos en futuro:\n\n"
    for verb in regular_verbs:
        result += str(verb) + "\n\n"
        result += "Yo       | " + str(make_yo_fut(verb)) + "\n"
        result += "Tu       | " + str(make_tu_fut(verb)) + "\n"
        result += "Usted    | " + str(make_usted_fut(verb)) + "\n"
        result += "Nosotros | " + str(make_nos_fut(verb)) + "\n"
        result += "Ustedes  | " + str(make_ustedes_fut(verb)) + "\n"
        result += "\n"
    return result

def print_conj_past(all):
    regular_verbs = list_regular_verbs(data)
    result = "Todos los verbos en pasado:\n\n"
    for verb in regular_verbs:
        result += str(verb) + "\n\n"
        result += "Yo       | " + str(make_yo_past(verb)) + "\n"
        result += "Tu       | " + str(make_tu_past(verb)) + "\n"
        result += "Usted    | " + str(make_usted_past(verb)) + "\n"
        result += "Nosotros | " + str(make_nos_past(verb)) + "\n"
        result += "Ustedes  | " + str(make_ustedes_past(verb)) + "\n"
        result += "\n"
    return result

def print_conj_perf(all):
    regular_verbs = list_regular_verbs(data)
    result = "Todos los verbos en pasado perfecto:\n\n"
    for verb in regular_verbs:
        result += str(verb) + "\n\n"
        result += "Yo       | " + str(make_yo_perf(verb)) + "\n"
        result += "Tu       | " + str(make_tu_perf(verb)) + "\n"
        result += "Usted    | " + str(make_usted_perf(verb)) + "\n"
        result += "Nosotros | " + str(make_nos_perf(verb)) + "\n"
        result += "Ustedes  | " + str(make_ustedes_perf(verb)) + "\n"
        result += "\n"
    return result

def print_conj_subju(all):
    regular_verbs = list_regular_verbs(data)
    result = "Todos los verbos en presente de subjunctivo:\n\n"
    for verb in regular_verbs:
        result += str(verb) + "\n\n"
        result += "Yo       | " + str(make_yo_subju(verb)) + "\n"
        result += "Tu       | " + str(make_tu_subju(verb)) + "\n"
        result += "Usted    | " + str(make_usted_subju(verb)) + "\n"
        result += "Nosotros | " + str(make_nos_subju(verb)) + "\n"
        result += "Ustedes  | " + str(make_ustedes_subju(verb)) + "\n"
        result += "\n"
    return result

def print_conj_ppsub(all):
    regular_verbs = list_regular_verbs(data)
    result = "Todos los verbos en pasado perfecto de subjuntivo:\n\n"
    for verb in regular_verbs:
        result += str(verb) + "\n\n"
        result += "Yo       | " + str(make_yo_ppsub(verb)) + "\n"
        result += "Tu       | " + str(make_tu_ppsub(verb)) + "\n"
        result += "Usted    | " + str(make_usted_ppsub(verb)) + "\n"
        result += "Nosotros | " + str(make_nos_ppsub(verb)) + "\n"
        result += "Ustedes  | " + str(make_ustedes_ppsub(verb)) + "\n"
        result += "\n"
    return result

def print_conj_imperf(all):
    regular_verbs = list_regular_verbs(data)
    result = "Todos los verbos imperfectivo:\n\n"
    for verb in regular_verbs:
        result += str(verb) + "\n\n"
        result += "Yo       | " + str(make_yo_imperf(verb)) + "\n"
        result += "Tu       | " + str(make_tu_imperf(verb)) + "\n"
        result += "Usted    | " + str(make_usted_imperf(verb)) + "\n"
        result += "Nosotros | " + str(make_nos_imperf(verb)) + "\n"
        result += "Ustedes  | " + str(make_ustedes_imperf(verb)) + "\n"
        result += "\n"
    return result

def print_conj_orders(all):
    regular_verbs = list_regular_verbs(data)
    result = "Todos los verbos en imperativo:\n\n"
    for verb in regular_verbs:
        result += str(verb) + "\n\n"
        result += "No       | ¡" + str(make_yo_orders(verb)) + "!\n"
        result += "Tu       | ¡" + str(make_tu_orders(verb)) + "!\n"
        result += "Usted    | ¡" + str(make_usted_orders(verb)) + "!\n"
        result += "Nosotros | ¡" + str(make_nos_orders(verb)) + "!\n"
        result += "Ustedes  | ¡" + str(make_ustedes_orders(verb)) + "!\n"
        result += "\n"
    return result

def print_conj_cond(all):
    regular_verbs = list_regular_verbs(data)
    result = "Todos los verbos en condicional:\n\n"
    for verb in regular_verbs:
        result += str(verb) + "\n\n"
        result += "Yo       | " + str(make_yo_cond(verb)) + "\n"
        result += "Tu       | " + str(make_tu_cond(verb)) + "\n"
        result += "Usted    | " + str(make_usted_cond(verb)) + "\n"
        result += "Nosotros | " + str(make_nos_cond(verb)) + "\n"
        result += "Ustedes  | " + str(make_ustedes_cond(verb)) + "\n"
        result += "\n"
    return result

def printem(all):
    result = "\n"
    result += print_conj_pres(all)
    result += print_conj_fut(all)
    result += print_conj_past(all)
    result += print_conj_perf(all)
    result += print_conj_subju(all)
    result += print_conj_ppsub(all)
    result += print_conj_imperf(all)
    result += print_conj_orders(all)
    result += print_conj_cond(all)
    return result

def howto_orders():
    print("\nAsí se conjuga el verbo:\n")
    print("TU (NO):             ¡no hables! | ¡no aprendas!    NOSOTROS:                ¡hablemos! | ¡aprendamos!")
    print("TU:                      ¡habla! | ¡aprende!")
    print("EL, ELLA, USTED:         ¡hable! | ¡aprenda!        ELLOS, ELLAS, USTEDES:     ¡hablen! | ¡aprendan!")
    print("")
    print("YOU (NO):           don't speak! | don't learn!     WE:                    let's speak! | let's learn!")
    print("YOU:                      speak! | learn!")
    print("HE, SHE, IT:              speak! | learn!           THEY, YOU (ALL):             speak! | learn! \n")
    print("No es necesario que uses acentos.")
    
def howto_imperf():
    print("\nAsí se conjuga el verbo:\n")
    print("YO:                        hablaba | aprendía             NOSOTROS:                      hablábamos | aprendíamos")
    print("TU:                       hablabas | aprendías")
    print("EL, ELLA, USTED:           hablaba | aprendía             ELLOS, ELLAS, USTEDES:           hablaban | aprendían")
    print("")
    print("I:                 I used to speak | I used to learn      WE:                      we used to speak | we used to learn")
    print("YOU:             you used to speak | you used to learn")
    print("HE, SHE, IT:      it used to speak | it used to learn     THEY, YOU (ALL):       they used to speak | they used to learn\n")
    print("No es necesario que uses acentos.")
    
def howto_ppsub():
    print("\nAsí se conjuga el verbo:\n")
    print("YO:                    hubiera hablado | hubiera aprendido        NOSOTROS:                    hubiéramos hablado | hubiéramos aprendido")
    print("TU:                   hubieras hablado | hubieras aprendido")
    print("EL, ELLA, USTED:       hubiera hablado | hubiera aprendido        ELLOS, ELLAS, USTEDES:         hubieran hablado | hubieran aprendido")
    print("")
    print("I:                 I would have spoken | I would have learned     WE:                        we would have spoken | we would have learned")
    print("YOU:             you would have spoken | you would have learned")
    print("HE, SHE, IT:      it would have spoken | it would have learned    THEY, YOU (ALL):         they would have spoken | they would have learned\n")
    print("No es necesario que uses acentos.")
    
def howto_subju():
    print("\nAsí se conjuga el verbo:\n")
    print("YO:                        que hable | que aprenda             NOSOTROS:                       que hablemos | que aprendamos")
    print("TU:                       que hables | que aprendas")
    print("EL, ELLA, USTED:           que hable | que aprenda             ELLOS, ELLAS, USTEDES:            que hablen | que aprendan")
    print("")
    print("I:                that I would speak | that I would learn      WE:                      that we would speak | that we would learn")
    print("YOU:            that you would speak | that you would learn")
    print("HE, SHE, IT:     that it would speak | that it would learn     THEY, YOU (ALL):       that they would speak | that they would learn\n")
    print("No es necesario que uses acentos.")
    
def howto_perf():
    print("\nAsí se conjuga el verbo:\n")
    print("YO:                  he hablado | he aprendido        NOSOTROS:                 hemos hablado | hemos aprendido")
    print("TU:                 has hablado | has aprendido")
    print("EL, ELLA, USTED:     ha hablado | ha aprendido        ELLOS, ELLAS, USTEDES:      han hablado | han aprendido")
    print("")
    print("I:                I have spoken | I have learned      WE:                      we have spoken | we have learned")
    print("YOU:            you have spoken | you have learned")
    print("HE, SHE, IT:      it has spoken | it has learned      THEY, YOU (ALL):       they have spoken | they have learned\n")

def howto_past():
    print("\nAsí se conjuga el verbo:\n")
    print("YO:                  hablé | aprendí        NOSOTROS:                hablamos | aprendimos")
    print("TU:               hablaste | aprendiste")
    print("EL, ELLA, USTED:     habló | aprendió       ELLOS, ELLAS, USTEDES:   hablaron | aprendieron")
    print("")
    print("I:                I spoke  | I learned      WE:                      we spoke | we learned")
    print("YOU:             you spoke | you learned")
    print("HE, SHE, IT:      it spoke | it learned     THEY, YOU (ALL):       they spoke | they learned\n")
    
def howto_fut():
    print("\nAsí se conjuga el verbo:\n")
    print("YO:                     hablaré | aprenderé         NOSOTROS:                   hablaremos | aprenderemos")
    print("TU:                    hablarás | aprenderás")
    print("EL, ELLA, USTED:        hablará | aprenderá         ELLOS, ELLAS, USTEDES:        hablarán | aprenderán")
    print("")
    print("I:                I will speak  | I will learn      WE:                      we will speak | we will learn")
    print("YOU:             you will speak | you will learn")
    print("HE, SHE, IT:      it will speak | it will learn     THEY, YOU (ALL):       they will speak | they will learn\n")
    print("No es necesario que uses acentos.")
    
def howto_pres():
    print("\nAsí se conjuga el verbo:\n")
    print("YO:               hablo | aprendo      NOSOTROS:                hablamos | aprendemos")
    print("TU:              hablas | aprendes")
    print("EL, ELLA, USTED:  habla | aprende      ELLOS, ELLAS, USTEDES:     hablan | aprenden")
    print("")
    print("I:              I speak | I learn      WE:                      we speak | we learn")
    print("YOU:          you speak | you learn")
    print("HE, SHE, IT:  it speaks | it learns    THEY, YOU (ALL):       they speak | they learn\n")
    print("No es necesario que uses acentos.")
    
def howto_cond():
    print("\nAsí se conjuga el verbo:\n")
    print("YO:                          hablaría | aprendería           NOSOTROS:                   hablaríamos | aprenderíamos")
    print("TU:                         hablarías | aprenderías")
    print("EL, ELLA, USTED:             hablaría | aprendería           ELLOS, ELLAS, USTEDES:        hablarían | aprenderían")
    print("")
    print("I:                      I would speak | I would learn        WE:                      we would speak | we would learn")
    print("YOU:                  you would speak | you would learn")
    print("HE, SHE, IT:           it would speak | it would learn       THEY, YOU (ALL):       they would speak | they would learn \n")
    print("No es necesario que uses acentos.")