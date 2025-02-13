from google.oauth2 import service_account
from googleapiclient.discovery import build
import random
import requests
import re

# Define the scope and credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = "C:/Users/pawnl/Downloads/testagain-444816-afedf2734772.json"

# Authenticate and build the service
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Define the spreadsheet ID and range
SPREADSHEET_ID = '1XZp80mRFTSn7gRZJlLCEm04l2AXfkZjFB7veyPOolV0'
RANGE_NAME = 'spanishpy!A1:I1154'  # Adjust the range as needed

# Fetch the data from Google Sheets
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

# Convert data into the format your script expects
headers = values[0] if values else []
data = [
    dict(zip(headers, row)) for row in values[1:]
] if values else []

a2 = ['tocar', 'ubicar', 'verificar', 'acercarse', 'aplicar', 'atacar', 'buscar', 'colocar', 'comunicar', 'dedicar', 'enfocar', 'explicar', 'fabricar', 'identificar', 'indicar', 'practicar', 'publicar', 'sacar', 'significar', 'simplificar']
a3 = ['apagar', 'entregar', 'llegar', 'arriesgar', 'descargar', 'investigar', 'obligar', 'pagar']
a10 = ['acostarse', 'contar', 'demostrar', 'mostrar', 'acordar', 'comprobar', 'costar', 'encontrar', 'probar', 'recordar', 'soltar', 'soñar', 'volar']
a11 = ['almorzar', 'forzar']
e3 = ['agradecer', 'conocer', 'crecer', 'desaparecer', 'nacer', 'aparecer', 'establecer', 'ofrecer', 'parecer', 'permanecer', 'reconocer']
i11 = ['sentir', 'sentirse', 'sugerir', 'convertir', 'herir', 'mentir', 'preferir','referir']
a4 = ['abrazar', 'alcanzar', 'aterrizar', 'avanzar', 'cruzar', 'lanzar', 'realizar', 'rechazar', 'utilizar']

translations = {
    'tocar': 'touch, play',
    'ubicar': 'locate',
    'verificar': 'check, verify',
    'acercarse': 'get (closer), come, approach',
    'aplicar': 'apply',
    'atacar': 'attack',
    'buscar': 'search, look, seek',
    'colocar': 'place, put, position, set, attach, affix',
    'comunicar': 'tell, pass on, transmit',
    'dedicar': 'devote, dedicate',
    'enfocar': 'focus, consider',
    'explicar': 'explain',
    'fabricar': 'produce, make, manufacture',
    'identificar': 'identify',
    'indicar': 'indicate',
    'practicar': 'practice',
    'publicar': 'post, publish',
    'sacar': 'draw, take, take out, remove',
    'significar': 'means, mean',
    'simplificar': 'simplify',
    'apagar': 'turn off',
    'arriesgar': 'risk',
    'descargar': 'download',
    'entregar': 'hand, hand over, submit, give, deliver',
    'investigar': 'research',
    'llegar': 'get (somewhere), arrive',
    'obligar': 'force, compel, oblige, obligate',
    'pagar': 'pay',
    'abrazar': 'hug',
    'alcanzar': 'achieve',
    'aterrizar': 'land, touch down',
    'avanzar': 'proceed, go forward, move, advance, progress',
    'cruzar': 'cross',
    'lanzar': 'launch, throw, start, set in motion',
    'realizar': 'carry out, realize, instantiate, manifest, actualize, make',
    'rechazar': 'reject',
    'utilizar': 'utilize, harness, use',
    'acordar': 'agree',
    'acostarse': 'go to bed, lie down',
    'comprobar': 'check, find out, test',
    'contar': 'recount, count, tell',
    'costar': 'cost',
    'demostrar': 'demonstrate, prove',
    'encontrar': 'find, meet, encounter, spot',
    'mostrar': 'show',
    'probar': 'test, prove, taste, try',
    'recordar': 'remember',
    'soltar': 'release, let go',
    'soñar': 'dream',
    'volar': 'fly',
    'almorzar': 'have lunch, lunch',
    'forzar': 'force',
    'agradecer': 'thank, appreciate',
    'aparecer': 'appear, seem',
    'conocer': 'know (familiar with)',
    'crecer': 'grow',
    'desaparecer': 'disappear, vanish, go away',
    'establecer': 'set, establish, set up',
    'nacer': 'born, be born, rise, originate',
    'ofrecer': 'offer',
    'parecer': 'seem',
    'permanecer': 'remain',
    'reconocer': 'recognize',
    'convertir': 'become, convert, change',
    'herir': 'hurt (active)',
    'preferir': 'prefer',
    'referir': 'refer, recount, recite',
    'sentirse': 'feel',
    'mentir': 'lie',
    'sentir': 'feel, sense',
    'sugerir': 'suggest'
}

"""
# Example usage:
for verb_group in [a2, a3, a10, a11, e3, i11, a4]:
    for verb in verb_group:
        print(f"{verb}: {translations[verb]}")
"""

def translate_verb(verb):
    return translations.get(verb, "Translation not found")

    """
    # Example call
    verb_to_translate = 'buscar'
    translation = translate_verb(verb_to_translate)
    print(f"Translation for '{verb_to_translate}': {translation}")
    """

def list_abnormal_verbs(data):
    return [entry['esp'] for entry in data if entry.get('vtype') == 'abnormal']

# Present

def make_yo(verb):
    if verb in a11:
        stem_changes = {'orz': 'uerz'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"me {irr_form[:-4]}o" if verb.endswith("se") else f"{irr_form[:-2]}o"
    elif verb in a10:
        stem_changes = {'con': 'cuen', 'cos': 'cues', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"me {irr_form[:-4]}o" if verb.endswith("se") else f"{irr_form[:-2]}o"
    elif verb in e3:
        stem_changes = {'cer': 'zcer'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"me {irr_form[:-4]}o" if verb.endswith("se") else f"{irr_form[:-2]}o"
    elif verb in i11:
        stem_changes = {'en': 'ien', 'er': 'ier'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"me {irr_form[:-4]}o" if verb.endswith("se") else f"{irr_form[:-2]}o"
    if verb not in a11 and verb not in a10:
        if verb.endswith("ar ") or verb.endswith("er ") or verb.endswith("ir "):
            return verb[:-3] + "o"
        elif verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
            return verb[:-2] + "o"
        elif verb.endswith("arse"):
            return "me " + verb[:-4] + "o"
        elif verb.endswith("irse") or verb.endswith("erse"):
                return "me " + verb[:-4] + "o"
    else:
        return ""
    return verb
    return ""


def make_tu(verb):
    if verb in a11:
        stem_changes = {'orz': 'uerz'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"te {irr_form[:-4]}as" if verb.endswith("se") else f"{irr_form[:-2]}as"
    elif verb in a10:
        stem_changes = {'con': 'cuen', 'cos': 'cues', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"te {irr_form[:-4]}as" if verb.endswith("se") else f"{irr_form[:-2]}as"
    elif verb in i11:
        stem_changes = {'en': 'ien', 'er': 'ier'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"te {irr_form[:-4]}es" if verb.endswith("se") else f"{irr_form[:-2]}es"
    if verb not in a11 and verb not in a10:
        if verb.endswith("ar "):
            return verb[:-3] + "as"
        elif verb.endswith("er ") or verb.endswith("ir "):
            return verb[:-3] + "es"
        elif verb.endswith("ar"):
            return verb[:-2] + "as"
        elif verb.endswith("er") or verb.endswith("ir"):
            return verb[:-2] + "es"
        elif verb.endswith("arse"):
            return "te " + verb[:-4] + "as"
        elif verb.endswith("irse") or verb.endswith("erse"):
                return "te " + verb[:-4] + "es"
    else:
        return ""
    return verb
    return ""
    
def make_usted(verb):
    if verb in a11:
        stem_changes = {'orz': 'uerz'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"se {irr_form[:-4]}a" if verb.endswith("se") else f"{irr_form[:-2]}a"
    elif verb in a10:
        stem_changes = {'con': 'cuen', 'cos': 'cues', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"se {irr_form[:-4]}a" if verb.endswith("se") else f"{irr_form[:-2]}a"
    elif verb in i11:
        stem_changes = {'en': 'ien', 'er': 'ier'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"se {irr_form[:-4]}e" if verb.endswith("se") else f"{irr_form[:-2]}e"
    if verb not in a11 and verb not in a10:
        if verb.endswith("ar "):
            return verb[:-3] + "a"
        elif verb.endswith("er ") or verb.endswith("ir "):
            return verb[:-3] + "e"
        elif verb.endswith("ar"):
            return verb[:-2] + "a"
        elif verb.endswith("er") or verb.endswith("ir"):
            return verb[:-2] + "e"
        elif verb.endswith("arse"):
            return "se " + verb[:-4] + "a"
        elif verb.endswith("irse") or verb.endswith("erse"):
                return "se " + verb[:-4] + "e"
    else:
        return ""
    return verb
    return ""
    
def make_nos(verb):
    if verb.endswith("ar "):
        return verb[:-3] + "amos"
    elif verb.endswith("er "):
        return verb[:-3] + "emos"
    elif verb.endswith("ir "):
        return verb[:-3] + "imos"
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
    
def make_ustedes(verb):
    if verb in a11:
        stem_changes = {'orz': 'uerz'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"se {irr_form[:-4]}an" if verb.endswith("se") else f"{irr_form[:-2]}an"
    elif verb in a10:
        stem_changes = {'con': 'cuen', 'cos': 'cues', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"se {irr_form[:-4]}an" if verb.endswith("se") else f"{irr_form[:-2]}an"
    elif verb in i11:
        stem_changes = {'en': 'ien', 'er': 'ier'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"se {irr_form[:-4]}en" if verb.endswith("se") else f"{irr_form[:-2]}en"
    if verb not in a11 and verb not in a10:
        if verb.endswith("ar "):
            return verb[:-3] + "an"
        elif verb.endswith("er ") or verb.endswith("ir "):
            return verb[:-3] + "en"
        elif verb.endswith("ar"):
            return verb[:-2] + "an"
        elif verb.endswith("er") or verb.endswith("ir"):
            return verb[:-2] + "en"
        elif verb.endswith("arse"):
            return "se " + verb[:-4] + "an"
        elif verb.endswith("irse") or verb.endswith("erse"):
                return "se " + verb[:-4] + "en"
    else:
        return ""
    return verb    
    return ""
    
# Future
    
def make_yo_fut(verb):
    if verb.endswith("ar ") or verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-1] + "é"
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "é"
    if verb.endswith("arse") or verb.endswith("irse") or verb.endswith("erse"):
        return "me " + verb[:-2] + "é"
    else: 
        return ""
    return verb

def make_tu_fut(verb):
    if verb.endswith("ar ") or verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-1] + "ás"
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "ás"
    if verb.endswith("arse") or verb.endswith("irse") or verb.endswith("erse"):
        return "te " + verb[:-2] + "ás"
    else:
        return ""
    return verb
    
def make_usted_fut(verb):
    if verb.endswith("ar ") or verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-1] + "á"
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "á"
    if verb.endswith("arse") or verb.endswith("irse") or verb.endswith("erse"):
        return "se " + verb[:-2] + "á"
    else:
        return ""
    return verb
    
def make_nos_fut(verb):
    if verb.endswith("ar ") or verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-1] + "emos"
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "emos"    
    if verb.endswith("arse") or verb.endswith("irse") or verb.endswith("erse"):
        return "nos " + verb[:-2] + "emos"
    else:
        return ""
    return verb
    
def make_ustedes_fut(verb):
    if verb.endswith("ar ") or verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-1] + "án"
    if verb.endswith("ar") or verb.endswith("er") or verb.endswith("ir"):
        return verb + "án"
    if verb.endswith("arse") or verb.endswith("irse") or verb.endswith("erse"):
        return "se " + verb[:-2] + "án"
    else:
        return ""
    return verb
    
############################### Past
    
def make_yo_past(verb):
    if verb in a2:
        stem_changes = {'car': 'qu', 'carse': 'qu'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"me {irr_form[:-2]}é" if verb.endswith("se") else f"{irr_form}é"
    elif verb in a3:
        stem_changes = {'gar': 'guar'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"me {irr_form[:-4]}é" if verb.endswith("se") else f"{irr_form[:-2]}é"
    elif verb in a4:
        stem_changes = {'zar': 'car'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"me {irr_form[:-4]}é" if verb.endswith("se") else f"{irr_form[:-2]}é"
    if verb.endswith("ar "):
        return verb[:-3] + "é"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-3] + "í"
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
    if verb.endswith("ar "):
        return verb[:-3] + "aste"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-3] + "iste"
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
    if verb in i11:
        stem_changes = {'en': 'in', 'er': 'ir'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"se {irr_form[:-4]}ió" if verb.endswith("se") else f"{irr_form[:-2]}ió"
    if verb.endswith("ar "):
        return verb[:-3] + "ó"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-3] + "ió"
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
    if verb.endswith("ar "):
        return verb[:-3] + "amos"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-3] + "imos"
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
    if verb in i11:
        stem_changes = {'en': 'in', 'er': 'ir'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"se {irr_form[:-4]}ieron" if verb.endswith("se") else f"{irr_form[:-2]}ieron"
    if verb.endswith("ar "):
        return verb[:-3] + "aron"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-3] + "ieron"
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
    
# Perfect

def make_yo_perf(verb):
    if verb.endswith("ar "):
        return "he " + verb[:-3] + "ado"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return "he " + verb[:-3] + "ido"
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
    if verb.endswith("ar "):
        return "has " + verb[:-3] + "ado"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return "has " + verb[:-3] + "ido"
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
    if verb.endswith("ar "):
        return "ha " + verb[:-3] + "ado"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return "ha " + verb[:-3] + "ido"
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
    if verb.endswith("ar "):
        return "hemos " + verb[:-3] + "ado"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return "hemos " + verb[:-3] + "ido"
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
    if verb.endswith("ar "):
        return "han " + verb[:-3] + "ado"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return "han " + verb[:-3] + "ido"
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
    
# Present Subjunctive
    
def make_yo_subju(verb):
    if  verb in a2:
        stem_changes = {'car': 'qu', 'carse': 'qu'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que me {irr_form[:-2]}e" if verb.endswith("se") else f"que {irr_form}e"
    elif verb in a3:
        stem_changes = {'gar': 'guar'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que me {irr_form[:-4]}e" if verb.endswith("se") else f"que {irr_form[:-2]}e"
    elif verb in a11:
        stem_changes = {'orz': 'uerc'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que me {irr_form[:-4]}e" if verb.endswith("se") else f"que {irr_form[:-2]}e"
    elif verb in a10:
        stem_changes = {'con': 'cuen', 'cos': 'cues', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que me {irr_form[:-4]}e" if verb.endswith("se") else f"que {irr_form[:-2]}e"
    elif verb in e3:
        stem_changes = {'cer': 'zcer'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que me {irr_form[:-4]}a" if verb.endswith("se") else f"que {irr_form[:-2]}a"
    elif verb in i11:
        stem_changes = {'en': 'ien', 'er': 'ier'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que me {irr_form[:-4]}a" if verb.endswith("se") else f"que {irr_form[:-2]}a"
    elif verb in a4:
        stem_changes = {'zar': 'car'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que me {irr_form[:-4]}e" if verb.endswith("se") else f"que {irr_form[:-2]}e"
    else:
        return ""
    return irr_form
    
def make_tu_subju(verb):
    if  verb in a2:
        stem_changes = {'car': 'qu', 'carse': 'qu'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que te {irr_form[:-2]}es" if verb.endswith("se") else f"que {irr_form}es"
    elif verb in a3:
        stem_changes = {'gar': 'guar'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que te {irr_form[:-4]}es" if verb.endswith("se") else f"que {irr_form[:-2]}es"
    elif verb in a11:
        stem_changes = {'orz': 'uerc'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que te {irr_form[:-4]}es" if verb.endswith("se") else f"que {irr_form[:-2]}es"
    elif verb in a10:
        stem_changes = {'con': 'cuen', 'cos': 'cues', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que te {irr_form[:-4]}es" if verb.endswith("se") else f"que {irr_form[:-2]}es"
    elif verb in e3:
        stem_changes = {'cer': 'zcer'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que te {irr_form[:-4]}as" if verb.endswith("se") else f"que {irr_form[:-2]}as"
    elif verb in i11:
        stem_changes = {'en': 'ien', 'er': 'ier'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que te {irr_form[:-4]}as" if verb.endswith("se") else f"que {irr_form[:-2]}as"
    elif verb in a4:
        stem_changes = {'zar': 'car'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que te {irr_form[:-4]}es" if verb.endswith("se") else f"que {irr_form[:-2]}es"
    else:
        return ""
    return irr_form
    
def make_usted_subju(verb):
    if  verb in a2:
        stem_changes = {'car': 'qu', 'carse': 'qu'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-2]}e" if verb.endswith("se") else f"que {irr_form}e"
    elif verb in a3:
        stem_changes = {'gar': 'guar'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-4]}e" if verb.endswith("se") else f"que {irr_form[:-2]}e"
    elif verb in a11:
        stem_changes = {'orz': 'uerc'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-4]}e" if verb.endswith("se") else f"que {irr_form[:-2]}e"
    elif verb in a10:
        stem_changes = {'con': 'cuen', 'cos': 'cues', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-4]}e" if verb.endswith("se") else f"que {irr_form[:-2]}e"
    elif verb in e3:
        stem_changes = {'cer': 'zcer'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-4]}a" if verb.endswith("se") else f"que {irr_form[:-2]}a"
    elif verb in i11:
        stem_changes = {'en': 'ien', 'er': 'ier'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-4]}a" if verb.endswith("se") else f"que {irr_form[:-2]}a"
    elif verb in a4:
        stem_changes = {'zar': 'car'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-4]}e" if verb.endswith("se") else f"que {irr_form[:-2]}e"
    else:
        return ""
    return irr_form
    
def make_nos_subju(verb):
    if  verb in a2:
        stem_changes = {'car': 'qu', 'carse': 'qu'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que nos {irr_form[:-2]}emos" if verb.endswith("se") else f"que {irr_form}emos"
    elif verb in a3:
        stem_changes = {'gar': 'guar'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que nos {irr_form[:-4]}emos" if verb.endswith("se") else f"que {irr_form[:-2]}emos"
    elif verb in a11:
        stem_changes = {'orz': 'orc'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que nos {irr_form[:-4]}emos" if verb.endswith("se") else f"que {irr_form[:-2]}emos"
    elif verb in e3:
        stem_changes = {'cer': 'zcer'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que nos {irr_form[:-4]}amos" if verb.endswith("se") else f"que {irr_form[:-2]}amos"
    elif verb in i11:
        stem_changes = {'en': 'in', 'er': 'ir'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que nos {irr_form[:-4]}amos" if verb.endswith("se") else f"que {irr_form[:-2]}amos"
    elif verb in a4:
        stem_changes = {'zar': 'car'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que nos {irr_form[:-4]}emos" if verb.endswith("se") else f"que {irr_form[:-2]}emos"
    elif verb.endswith("ar "): 
        return "que " + verb[:-3] + "emos"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return "que " + verb[:-3] + "amos"
    if verb.endswith("ar"): 
        return "que " + verb[:-2] + "emos"
    elif verb.endswith("er") or verb.endswith("ir"):
        return "que " + verb[:-2] + "amos"
    if verb.endswith("arse"):
        return "que nos " + verb[:-4] + "emos"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return "que nos " + verb[:-4] + "amos"
    else: 
        return ""
    return verb
    
def make_ustedes_subju(verb):
    if  verb in a2:
        stem_changes = {'car': 'qu', 'carse': 'qu'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-2]}en" if verb.endswith("se") else f"que {irr_form}en"
    elif verb in a3:
        stem_changes = {'gar': 'guar'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-4]}en" if verb.endswith("se") else f"que {irr_form[:-2]}en"
    elif verb in a11:
        stem_changes = {'orz': 'uerc'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-4]}en" if verb.endswith("se") else f"que {irr_form[:-2]}en"
    elif verb in a10:
        stem_changes = {'con': 'cuen', 'cos': 'cues', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-4]}en" if verb.endswith("se") else f"que {irr_form[:-2]}en"
    elif verb in e3:
        stem_changes = {'cer': 'zcer'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-4]}an" if verb.endswith("se") else f"que {irr_form[:-2]}an"
    elif verb in i11:
        stem_changes = {'en': 'ien', 'er': 'ier'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-4]}an" if verb.endswith("se") else f"que {irr_form[:-2]}an"
    elif verb in a4:
        stem_changes = {'zar': 'car'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"que se {irr_form[:-4]}en" if verb.endswith("se") else f"que {irr_form[:-2]}en"
    else:
        return ""
    return irr_form
    
# Past Perfect Subjunctive

def make_yo_ppsub(verb):
    if verb.endswith("ar "):
        return "hubiera " + verb[:-3] + "ado"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return "hubiera " + verb[:-3] + "ido"
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
    if verb.endswith("ar "):
        return "hubieras " + verb[:-3] + "ado"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return "hubieras " + verb[:-3] + "ido"
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
    if verb.endswith("ar "):
        return "hubiera " + verb[:-3] + "ado"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return "hubiera " + verb[:-3] + "ido"
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
    if verb.endswith("ar "):
        return "hubiéramos " + verb[:-3] + "ado"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return "hubiéramos " + verb[:-3] + "ido"
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
    if verb.endswith("ar "):
        return "hubieran " + verb[:-3] + "ado"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return "hubieran " + verb[:-3] + "ido"
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

# Imperfect

def make_yo_imperf(verb):
    if verb.endswith("ar "):
        return verb[:-3] + "aba"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-3] + "ía"
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
    if verb.endswith("ar "):
        return verb[:-3] + "abas"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-3] + "ías"
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
    if verb.endswith("ar "):
        return verb[:-3] + "aba"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-3] + "ía"
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
    if verb.endswith("ar "):
        return verb[:-3] + "ábamos"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-3] + "íamos"
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
    if verb.endswith("ar "):
        return verb[:-3] + "aban"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-3] + "ían"
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
    
# Imperative

def make_yo_orders(verb):
    if  verb in a2:
        stem_changes = {'car': 'qu', 'carse': 'qu'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"no te {irr_form[:-2]}es" if verb.endswith("se") else f"no {irr_form}es"
    elif verb in e3:
        stem_changes = {'cer': 'zcer'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"no {irr_form[:-4]}aste" if verb.endswith("se") else f"no {irr_form[:-2]}as"
    elif  verb in a3:
        stem_changes = {'gar': 'guar'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"no {irr_form[:-4]}este" if verb.endswith("se") else f"no {irr_form[:-2]}es"
    elif verb in a11:
        stem_changes = {'orz': 'uerc'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"no te {irr_form[:-4]}es" if verb.endswith("se") else f"no {irr_form[:-2]}es"
    elif verb in a10:
        stem_changes = {'con': 'cuen', 'cos': 'cues', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"no te {irr_form[:-4]}es" if verb.endswith("se") else f"no {irr_form[:-2]}es"
    elif verb in i11:
        stem_changes = {'en': 'ien', 'er': 'ier'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"no te {irr_form[:-4]}as" if verb.endswith("se") else f"no {irr_form[:-2]}as"
    elif verb in a4:
        stem_changes = {'zar': 'car'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"no te {irr_form[:-4]}es" if verb.endswith("se") else f"no {irr_form[:-2]}es"
    else:
        return ""
    return irr_form

def make_tu_orders(verb):
    
    if  verb in a2:
        if verb.endswith("arse"):
            stem_changes = {'acer': 'acér'}
            for orig, change in stem_changes.items():
                if orig in verb:
                    irr_form = verb.replace(orig, change)
                    return f"{irr_form[:-4]}ate"
        else:
            return verb[:-2] + "a" 
    elif verb in a3:
        return verb[:-2] + "a" if verb.endswith("ar") else verb[:-4] + "ate"
    elif verb in a11:
        stem_changes = {'orz': 'uerz'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}ate" if verb.endswith("se") else f"{irr_form[:-2]}a"
    elif verb in e3:
        return verb[:-2] + "e" if verb.endswith("er") else verb[:-4] + "ete"
    elif verb in a10:
        if verb.endswith("arse"):
            stem_changes = {'con': 'cuen', 'cos': 'cués', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        else:
            stem_changes = {'con': 'cuen', 'cos': 'cues', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}ate" if verb.endswith("se") else f"{irr_form[:-2]}a"
    elif verb in i11:
        if verb.endswith("se"):
            stem_changes = {'en': 'ién', 'er': 'iér'} 
            for orig, change in stem_changes.items():
                if orig in verb:
                    irr_form = verb.replace(orig, change)
                    return f"{irr_form[:-4]}ete" if verb.endswith("se") else f"{irr_form[:-2]}e"
        elif verb.endswith('ir'):
            stem_changes = {'en': 'ien', 'er': 'ier'}
            for orig, change in stem_changes.items():
                if orig in verb:
                    irr_form = verb.replace(orig, change)
                    return f"{irr_form[:-4]}ete" if verb.endswith("se") else f"{irr_form[:-2]}e"
    elif verb in a4:
        return verb[:-2] + "a"
    else:
        return ""
    return irr_form
    
def make_usted_orders(verb):
    if  verb in a2:
        if verb.endswith("arse"):
            stem_changes = {'acerc': 'acérqu'}
            for orig, change in stem_changes.items():
                if orig in verb:
                    irr_form = verb.replace(orig, change)
                    return f"{irr_form[:-4]}ese"
        else:
            stem_changes = {'car': 'qu', 'carse': 'qu'}
            for orig, change in stem_changes.items():
                if orig in verb:
                    irr_form = verb.replace(orig, change)
                    return f"{irr_form}e"
    elif verb in e3:
        stem_changes = {'cer': 'zcer'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}ase" if verb.endswith("se") else f"{irr_form[:-2]}a"
    elif verb in a3:
        stem_changes = {'gar': 'guar'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}ese" if verb.endswith("se") else f"{irr_form[:-2]}e"
    elif verb in a11:
        stem_changes = {'orz': 'uerc'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}ete" if verb.endswith("se") else f"{irr_form[:-2]}e"
    elif verb in a10:
        if verb.endswith("arse"):
            stem_changes = {'con': 'cuen', 'cos': 'cués', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        else:
            stem_changes = {'con': 'cuen', 'cos': 'cues', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}ese" if verb.endswith("se") else f"{irr_form[:-2]}e"
    elif verb in i11:
        if verb.endswith("se"):
            stem_changes = {'en': 'ién', 'er': 'iér'}
            for orig, change in stem_changes.items():
                if orig in verb:
                    irr_form = verb.replace(orig, change)
                    return f"{irr_form[:-4]}ase" if verb.endswith("se") else f"{irr_form[:-2]}a"
        elif verb.endswith("ir"):
            stem_changes = {'en': 'ien', 'er': 'ier'}
            for orig, change in stem_changes.items():
                if orig in verb:
                    irr_form = verb.replace(orig, change)
                    return f"{irr_form[:-4]}ase" if verb.endswith("se") else f"{irr_form[:-2]}a"
    elif verb in a4:
        stem_changes = {'zar': 'car'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}ese" if verb.endswith("se") else f"{irr_form[:-2]}e"
    else:
        return ""
    return irr_form
    
def make_nos_orders(verb):
    if  verb in a2:
        stem_changes = {'car': 'qu', 'carse': 'qu'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-2]}émonos" if verb.endswith("se") else f"{irr_form}emos"
    elif verb in a3:
        stem_changes = {'gar': 'guar'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}émonos" if verb.endswith("se") else f"{irr_form[:-2]}emos"
    elif verb in a11:
        stem_changes = {'orz': 'orc'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}émonos" if verb.endswith("se") else f"{irr_form[:-2]}emos"
    elif verb in e3:
        stem_changes = {'cer': 'zcer'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}amanos" if verb.endswith("se") else f"{irr_form[:-2]}amos"
    elif verb in i11:
        stem_changes = {'en': 'in', 'er': 'ir'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}ámonos" if verb.endswith("se") else f"{irr_form[:-2]}amos"
    elif verb in a4:
        stem_changes = {'zar': 'car'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}émonos" if verb.endswith("se") else f"{irr_form[:-2]}emos"
    elif verb.endswith("ar "):
        return verb[:-3] + "emos"
    elif verb.endswith("er ") or verb.endswith("ir "):
        return verb[:-3] + "amos"
    if verb.endswith("ar"):
        return verb[:-2] + "emos"
    elif verb.endswith("er") or verb.endswith("ir"):
        return verb[:-2] + "amos"
    if verb.endswith("arse"):
        return verb[:-4] + "émonos"
    elif verb.endswith("irse") or verb.endswith("erse"):
        return verb[:-4] + "amonos"
    else: 
        return ""
    return verb
    
def make_ustedes_orders(verb):
    if  verb in a2:
        if verb.endswith("arse"):
            stem_changes = {'acerc': 'acérqu'}
            for orig, change in stem_changes.items():
                if orig in verb:
                    irr_form = verb.replace(orig, change)
                    return f"{irr_form[:-4]}ense"
        else:
            stem_changes = {'car': 'qu', 'carse': 'qu'}
            for orig, change in stem_changes.items():
                if orig in verb:
                    irr_form = verb.replace(orig, change)
                    return f"{irr_form}en"
    elif verb in a3:
        stem_changes = {'gar': 'guar'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}ense" if verb.endswith("se") else f"{irr_form[:-2]}en"
    elif verb in a11:
        stem_changes = {'orz': 'uerc'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}ense" if verb.endswith("se") else f"{irr_form[:-2]}en"
    elif verb in e3:
        stem_changes = {'cer': 'zcer'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}anse" if verb.endswith("se") else f"{irr_form[:-2]}an"
    elif verb in a10:
        if verb.endswith("arse"):
            stem_changes = {'con': 'cuen', 'cos': 'cués', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        else:
            stem_changes = {'con': 'cuen', 'cos': 'cues', 'mos': 'mues', 'cor': 'cuer', 'ro': 'rue', 'vo': 'vue', 'so': 'sue'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}ense" if verb.endswith("se") else f"{irr_form[:-2]}en"
    elif verb in i11:
        if verb.endswith("se"):
            stem_changes = {'en': 'ién', 'er': 'iér'}
            for orig, change in stem_changes.items():
                if orig in verb:
                    irr_form = verb.replace(orig, change)
                    return f"{irr_form[:-4]}anse" if verb.endswith("se") else f"{irr_form[:-2]}an"
        elif verb.endswith("ir"):
            stem_changes = {'en': 'ien', 'er': 'ier'}
            for orig, change in stem_changes.items():
                if orig in verb:
                    irr_form = verb.replace(orig, change)
                    return f"{irr_form[:-4]}anse" if verb.endswith("se") else f"{irr_form[:-2]}an"
    elif verb in a4:
        stem_changes = {'zar': 'car'}
        for orig, change in stem_changes.items():
            if orig in verb:
                irr_form = verb.replace(orig, change)
                return f"{irr_form[:-4]}ense" if verb.endswith("se") else f"{irr_form[:-2]}en"
    else:
        return ""
    return irr_form

def print_conj(all):
    def print_tense(verb, make_fn):
        form = make_fn(verb)
        return form

    abnormal_verbs = list_abnormal_verbs(data)

    tense_sets = [
        {'label': 'A10', 'verbs': a10},
        {'label': 'A11', 'verbs': a11},
        {'label': 'E3', 'verbs': e3},
        {'label': 'A2', 'verbs': a2, 'tense_type': 'past'},
        {'label': 'A3', 'verbs': a3, 'tense_type': 'past'},
        {'label': 'I11', 'verbs': i11, 'tense_type': 'past2'},
        {'label': 'A4', 'verbs': a4, 'tense_type': 'past2'},
    ]

    def print_verb_tenses(verb, label, tense_type='present'):
        output = f"{verb} ({label})<br>"

        tenses = {
            'present': [make_yo, make_tu, make_usted, make_nos, make_ustedes],
            'subjunctive': [make_yo_subju, make_tu_subju, make_usted_subju, make_nos_subju, make_ustedes_subju],
            'imperative': [make_yo_orders, make_tu_orders, make_usted_orders, make_nos_orders, make_ustedes_orders]
        }

        tense_order = ['present', 'subjunctive', 'imperative']
        if tense_type == 'past':
            tenses['past'] = [make_yo_past, make_tu_past, make_usted_past, make_nos_past, make_ustedes_past]
            tense_order.insert(1, 'past')
            tense_order.remove('present')

        if tense_type == 'past2':
            tenses['past'] = [make_yo_past, make_tu_past, make_usted_past, make_nos_past, make_ustedes_past]
            tense_order.insert(1, 'past')

        for tense in tense_order:
            output += f"{tense}:<br>"
            for make_fn in tenses[tense]:
                output += f"{print_tense(verb, make_fn)}<br>"
            output += "<br>"

        return output

    results = []
    for verb in abnormal_verbs:
        for tense_set in tense_sets:
            if verb in tense_set['verbs']:
                results.append(print_verb_tenses(verb, tense_set['label'], tense_set.get('tense_type', 'present')))

    return results

import random

# List of pronouns and their corresponding conjugation function prefixes
pronouns = {
  'yo': 'make_yo',
  'tu': 'make_tu',
  'usted': 'make_usted',
  'nos': 'make_nos',
  'ustedes': 'make_ustedes'
}

# List of tenses and their corresponding function suffixes
tenses = {
  'Presente': '',
  'Pasado': '_past',
  'Presente Subjunctivo': '_subju',
  'Imperativo': '_orders'
}

# Function to randomly select and call the conjugation function
def random_verb_pronoun_tense():
    verb = random.choice(a2 + a3 + a10 + a11 + e3 + i11 + a4)
    pronoun = random.choice(list(pronouns.keys()))
    tense = random.choice(list(tenses.keys()))

    func_name = pronouns[pronoun] + tenses[tense]
    conjugate_func = globals().get(func_name)

    if conjugate_func:
        result = conjugate_func(verb)
        return verb, pronoun, tense, result
    return verb, pronoun, tense, None

# Example usage
def ex_use():
    for i in range(10):
        verb, pronoun, tense, conjugated_verb = random_verb_pronoun_tense()
        print("¿Cómo se dice " + verb + " (" + pronoun + ") en tiempo " + tense + "?")
        print("" + conjugated_verb + "")

def show_irr():
    print(str(
        "a2 c→qu tocar ubicar verificar acercarse aplicar atacar buscar colocar comunicar dedicar enfocar explicar fabricar identificar indicar practicar publicar sacar significar simplificar"
        "a3 g→gu apagar entregar llegar arriesgar descargar investigar obligar pagar"
        "a10 o→ue acostarse contar demostrar mostrar acordar comprobar costar encontrar probar recordar soltar soñar volar"
        "a11 o→ue almorzar forzar"
        "e3 c→zc agradecer conocer crecer desaparecer nacer aparecer establecer ofrecer parecer permanecer reconocer"
        "i11 e→ie / e→i sentir arrepentirse sugerir convertir herir mentir preferir referir"
        "a4 z→c abrazar alcanzar aterrizar avanzar cruzar lanzar realizar rechazar utilizar"
    ))
