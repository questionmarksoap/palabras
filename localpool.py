from flask import Flask, render_template, request, redirect, url_for
import random
import riddleapi
import re
import bye_imgapi2 as img
import conjallapi3 as conjall
import irregapi3 as abnorm
import riddleapi as riddle
import time
import logging
import json

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Read data from local file
with open('getdata.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Data length: " + str(len(data)))

for i, row in enumerate(data):
    row['id'] = i

gjob = "\n¡Buen trabajo! La respuesta correcta es:"
theans = "La respuesta correcta es:"
oops = "**aún no hay frase disponible**"
examp3 = "Ejemplo de frase en inglés"
examp4 = "Ejemplo de frase en español"

used_entries = set()
missd = set()
ans_words = {}
corr_ans = 0
incor_ans = 0
nomore = False
duced = False
riddle_index = 0
riddle_attempts = 0

def get_entry(data, fltr_pos=None, fltr_vtype=None, syl_filter=False):
    global used_entries
    if not data:
        print("Error: Data is empty")
        return None

    filtered_data = [
        row for row in data
        if (not syl_filter or int(row.get('syl', 0)) > 4)
        and (fltr_pos is None or row.get('pos', '').lower() == fltr_pos.lower())
        and (fltr_vtype is None or row.get('vtype', '').lower() == fltr_vtype.lower())
        and row.get('id') not in used_entries
    ]
    number_entries = len(filtered_data)
    print(f"Initial data length: {len(data)}")
    print(f"Filtered data length: {number_entries}")
    print(f"Used entries: {used_entries}")

    if not filtered_data:
        print("the program didn't retrieve the data")
        return None
    entry = random.choice(filtered_data)
    used_entries.add(entry['id'])
    return entry

def get_current_question_details_conjugation():
    global current_entry, current_verb, current_tense, current_pronoun, mode

    current_entry = get_entry(data, fltr_pos='verb', fltr_vtype='regular')
    if not current_entry:
        prompt = "no hay más entradas disponibles."
        feedback = ""
        answer = ""
    else:
        if mode == '14':
            current_mode = random.choice(['5', '6', '7', '8', '9', '10', '11', '12', '13'])
        else:
            current_mode = mode

        tense_ind = {
            '5': '',
            '6': 'fut',
            '7': 'past',
            '8': 'perf',
            '9': 'subju',
            '10': 'ppsub',
            '11': 'imperf',
            '12': 'orders',
            '13': 'cond'
        }[current_mode]

        forms = {pronoun: getattr(conjall, f'make_{pronoun}_{tense_ind}' if tense_ind else f'make_{pronoun}') for pronoun in ['yo', 'tu', 'usted', 'nos', 'ustedes']}
        current_pronoun, corr_form = random.choice(list(forms.items()))
        current_tense = {
            '5': "Presente",
            '6': "Futuro",
            '7': "Pasado",
            '8': "Presente Perfecto",
            '9': "Presente Subjunctivo",
            '10': "Pasado Perfecto Subjunctivo",
            '11': "Imperfectivo",
            '12': "Imperativo",
            '13': "Condicional"
        }[current_mode]

        current_verb = corr_form(current_entry['esp'])
        if current_mode == '9' or mode == '9' or current_tense == 'Presente Subjunctivo':
            prompt = f"[{current_tense}] ¿Cómo se dice '<b>que {current_entry['esp']}</b>' ({current_entry['eng']}) para '{current_pronoun}'?", "", "" 
        else:
            prompt = f"[{current_tense}] ¿Cómo se dice '<b>{current_entry['esp']}</b>' ({current_entry['eng']}) para '{current_pronoun}'?"
        feedback = ""
        answer = ""
    return prompt, feedback, answer

def get_current_question_details_translation(fltr_pos=None, syl_filter=False): # Removed hard=False
    global current_entry
    current_entry = get_entry(data, fltr_pos=fltr_pos, syl_filter=syl_filter) # Removed hard=hard
    if not current_entry:
        return "no hay más entradas disponibles.", "", ""
    gram = current_entry.get('pos', '')
    return f"¿Cuál es la traducción al inglés de '{current_entry['esp']}' ({gram})?", "", ""
def get_sent_hint(entry):
    sent_parts = entry.get('1sent', '').split(',') if entry.get('1sent') else []
    return (sent_parts[1].strip() if len(sent_parts) > 1 else oops, entry.get('hint', '').strip())

def hint2(entry):
    sent_parts = entry['1sent'].split(',') if entry['1sent'] else []
    return (sent_parts[0].strip() if entry['1sent'] else oops, sent_parts[1].strip() if len(sent_parts) > 1 else oops, entry.get('hint', '').strip())

def norm_input(input_str):
    subs = str.maketrans("ñáéíóúÁÉÍÓÚ", "naeiouAEIOU")
    input_str = input_str.translate(subs)
    no_paren = re.sub(r'\([^)]*\)', '', input_str).strip()
    return re.sub(r'[^\w\s]', '', input_str).strip().lower(), re.sub(r'[^\w\s]', '', no_paren).strip().lower()

def check_conj(usr_in, corr_form):
    normd_usr_in, normd_usr_in_no_paren = norm_input(usr_in)
    normd_ans, normd_ans_no_paren = norm_input(corr_form)
    return normd_usr_in in {normd_ans, normd_ans_no_paren} or normd_usr_in_no_paren in {normd_ans, normd_ans_no_paren}

def check_transl(usr_in, eng_words):
    normd_usr_in, normd_usr_in_no_paren = norm_input(usr_in)
    normd_eng_words = [norm_input(word) for word in eng_words]
    normd_eng_words_flat = {word for sublist in normd_eng_words for word in sublist}
    return normd_usr_in in normd_eng_words_flat or normd_usr_in_no_paren in normd_eng_words_flat

def dis_bye(corr_ans, missd, ans_words, nomore):
    img.dis_random_ascii()
    total_ans = corr_ans + len(missd)
    accuracy = (corr_ans / total_ans) * 100 if total_ans > 0 else 0
    accuracy = round(accuracy, 2)
    if accuracy >= 100:
        special_img = "¡Bien hecho!" + img.art_28
        print(special_img)
        print(accuracy)
        print("test")
    else:
        special_img = ""
    if nomore:
        print("No hay más palabras en este modo de juego. ¡Bien hecho!")
    print(f"Las palabras incorrectas ({len(missd)}): \n\n{''.join([f'{word} ({ans_words[word]}),\n' for word in missd])}")
    print(f"{corr_ans} palabras correctas.")
    print(f"{len(missd)} palabras incorrectas.")
    print(f"Precisión: {accuracy:.2f}%")
    print(f"{corr_ans} de {total_ans} palabras correctas.\n\n¡Gracias por jugar! -Zorro\n")
def intro(mode):
    global duced
    if not duced:
        howto_funcs = {
            '5': conjall.howto_pres,
            '6': conjall.howto_fut,
            '7': conjall.howto_past,
            '8': conjall.howto_perf,
            '9': conjall.howto_subju,
            '10': conjall.howto_ppsub,
            '11': conjall.howto_imperf,
            '12': conjall.howto_orders,
            '13': conjall.howto_cond
        }
        if mode in howto_funcs:
            howto_funcs[mode]()
        duced = True
def quiz():
    global missd, ans_words, corr_ans, incor_ans, nomore, duced, mode, current_entry, current_verb, current_tense, current_pronoun

    nomore = False
    conj_modes = list(map(str, range(5, 14)))
    conj_funct = {str(i): conjall for i in range(5, 14)}

    ogmode = mode
    intro(mode)

    while True:
        if ogmode == '14':
            mode = random.choice(conj_modes)
            duced = False
            intro(mode)

        if mode == '15':
            prompt, feedback, answer = get_current_question_details()

            while True:
                user_input = request.form.get('user_input').strip().lower()
                normalized_input, normalized_no_paren = norm_input(user_input)
                normalized_conj_verb, normalized_conj_no_paren = norm_input(current_verb)

                if normalized_input in {normalized_conj_verb, normalized_conj_no_paren} or normalized_no_paren in {normalized_conj_verb, normalized_conj_no_paren}:
                    corr_ans += 1
                    print("----------------CORRECT!----------------")
                    feedback = "\n¡Buen trabajo!\n"
                    if current_tense == 'Imperativo':
                        answer = f"{theans} ¡{current_verb}!"
                    else:
                        answer = f"{theans} {current_verb}"
                    return render_template('quiz.html', prompt=prompt, feedback=feedback, answer=answer)

                else:
                    feedback = "\nIncorrecto."
                    missd.add(current_entry['esp'])  # Add to missd
                    ans_words[current_entry['esp']] = current_verb  # Map incorrect answer to correct answer
                    print("----------------NOT CORRECT!----------------")

                    # Log to terminal
                    logging.debug(f"Incorrect Answer Given: {user_input}")
                    logging.info(f"Incorrecto: {current_entry['esp']} ({current_verb})")
                    give_up = request.form.get('give_up').strip().lower()
                    if give_up == 'salida':
                        dis_bye(corr_ans, missd, ans_words, nomore)
                        return render_template('bye.html')
                    elif give_up == 'y':
                        feedback = f"{theans} {current_verb}"
                        return render_template('quiz.html', prompt=prompt, feedback=feedback, answer=answer)

        else:
            entry = get_entry(data, hard=(mode == '3'), fltr_pos='verb' if mode in conj_modes or mode == '4' else 'phrase' if mode == '2' else None, fltr_vtype='regular' if mode in map(str, range(5, 14)) else None)
            if not entry:
                print("no entries? BUG!")
                nomore = True
                dis_bye(corr_ans, missd, ans_words, nomore)
                return render_template('bye.html')
            used_entries.add(entry['esp'])
            if mode in conj_modes:
                tense_ind = {
                    '5': '',
                    '6': 'fut',
                    '7': 'past',
                    '8': 'perf',
                    '9': 'subju',
                    '10': 'ppsub',
                    '11': 'imperf',
                    '12': 'orders',
                    '13': 'cond'
                }[mode]
                forms = {pronoun: getattr(conj_funct[mode], f'make_{pronoun}_{tense_ind}' if tense_ind else f'make_{pronoun}') for pronoun in ['yo', 'tu', 'usted', 'nos', 'ustedes']}
                pronoun, corr_form = random.choice(list(forms.items()))
                tense = {
                    '5': "Presente",
                    '6': "Futuro (will ___)",
                    '7': "Pasado (___ed)",
                    '8': "Presente Perfecto (have ___)",
                    '9': "Presente Subjuntivo (that (pronoun) would ___)",
                    '10': "Pasado Perfecto Subjuntivo (would have)",
                    '11': "Imperfectivo (used to)",
                    '12': "Imperativo (Do ___!)",
                    '13': "Condicional (would ___)"
                }[mode]
                while True:
                    eng_words = entry['eng'].split(', ')
                    prompt = "\n[{}] ¿Cómo se dice '<b>{}</b> ({})' para '{}'? \n".format(tense, "que " + entry['esp'] if mode == '9' else entry['esp'], ', '.join(eng_words), 'no (tú)' if mode == '12' and pronoun == 'yo' else pronoun)
                    usr_in = request.form.get('usr_in').strip().lower()
                    if check_conj(usr_in, corr_form(entry['esp'])):
                        corr_ans += 1
                        print("----------------CORRECT!----------------")
                        if mode == '12':
                            feedback = "{} ¡{}!".format(gjob, corr_form(entry['esp']))
                        elif mode == '10':
                            feedback = "{} {}, pero ...".format(gjob, corr_form(entry['esp']))
                        else:
                            feedback = "{} {}".format(gjob, corr_form(entry['esp']))
                        if ogmode == '14':
                            mode = '14'
                            duced = False
                        return render_template('quiz.html', prompt=prompt, feedback=feedback)
                    else:
                        feedback = "\nIncorrecto."
                        missd.add(entry['esp'])
                        ans_words[entry['esp']] = corr_form(entry['esp'])
                        # Log to terminal
                        logging.debug(f"Incorrect Answer Given: {usr_in}")
                        logging.info(f"Incorrecto: {entry['esp']} ({corr_form(entry['esp'])})")
                        give_up = request.form.get('give_up').strip().lower()
                        if give_up == 'salida':
                            dis_bye(corr_ans, missd, ans_words, nomore)
                            return render_template('bye.html')
                        elif give_up == 'y':
                            if mode == '12':
                                answer = f"{theans} ¡{corr_form(entry['esp'])}!"
                            elif mode == '10':
                                answer = f"{theans} {corr_form(entry['esp'])}, pero ... "
                            else:
                                answer = f"{theans} {corr_form(entry['esp'])}"
                            if ogmode == '14':
                                mode = '14'
                                duced = False
                            return render_template('quiz.html', prompt=prompt, feedback=feedback, answer=answer)
            else:
                while True:
                    eng_words = entry['eng'].split(', ')
                    gram = entry.get('pos', '')
                    esp_sent, hint = get_sent_hint(entry)
                    prompt = f"\n¿Cuál es la traducción al inglés de '{entry['esp']}' ({gram})? \n"
                    usr_in = request.form.get('usr_in').strip().lower()
                    if check_transl(usr_in, eng_words):
                        corr_ans += 1
                        print("----------------CORRECT!----------------")
                        eng_sent = entry.get('1sent', '').split(',')[0].strip() if entry.get('1sent') else oops
                        if mode != '10' and mode != '12':
                            feedback = f"{gjob}  {', '.join(eng_words)}\n{examp3}:               {eng_sent}\n{examp4}:              {esp_sent}"
                        elif mode == '12':
                            feedback = f"{gjob}  ¡{', '.join(eng_words)}!\n{examp3}:      {eng_sent}\n{examp4}:     {esp_sent}"
                        else:
                            feedback = f"{gjob}  {', '.join(eng_words)}, pero ... \n{examp3}:      {eng_sent}\n{examp4}:     {esp_sent}"
                        if hint:
                            feedback += f"\nConsejo:                                  {hint}"
                        if ogmode == '14':
                            mode = '14'
                            duced = False
                        return render_template('quiz.html', prompt=prompt, feedback=feedback)
                    else: 
                        feedback = "\nIncorrecto."
                        missd.add(entry['esp'])
                        ans_words[entry['esp']] = ', '.join(eng_words)
                        # Log to terminal
                        logging.debug(f"Incorrect Answer Given: {usr_in}")
                        logging.info(f"Incorrecto: {entry['esp']} ({', '.join(eng_words)})")
                        give_up = request.form.get('give_up').strip().lower()
                        if give_up == 'salida':
                            dis_bye(corr_ans, missd, ans_words, nomore)
                            return render_template('bye.html')

@app.route('/menu')
def menu():
    global corr_ans, incor_ans
    corr_ans = 0
    incor_ans = 0
    games = """
    
    TRADUCCIÓN:
    1.  Todas las palabras
    2.  Solo las frases
    3.  Palabras desafiantes
    4.  Solo los verbos

    CONJUGACIÓN:
    5.  Tiempo presente
    6.  Tiempo futuro
    7.  Tiempo pasado
    8.  Tiempo presente perfecto
    9.  Tiempo presente subjunctivo
    10. Tiempo pasado perfecto subjunctivo
    11. Tiempo imperfectivo
    12. Tiempo imperativo
    13. Tiempo condicional
    14. Juego de tiempos aleatorios
    15. Juego de verbos irregulares

    OTRA:
    16. Imprimir todos los verbos
    17. Acertijos
    18. Galería de arte
    """
    return render_template('menu.html', games=games)

@app.route('/')
def index():
    return redirect(url_for('menu'))

@app.route('/art_gallery')
def art_gallery():
    all_ascii_art = img.get_all_ascii()
    return render_template('art_gallery.html', all_ascii_art=all_ascii_art)

@app.route('/select_mode', methods=['POST'])
def select_mode():
    global mode, used_entries, riddle_index, corr_ans, incor_ans, missd, ans_words  # Add missd, ans_words
    mode = request.form.get('mode')

    if mode == 'listo':
        return render_template('listo.html')
    if mode is None or not mode.isdigit() or not 1 <= int(mode) <= 18:  # Check if mode is valid
        return redirect(url_for('menu'))  # Redirect back to menu if invalid

    corr_ans = 0
    incor_ans = 0

    # Validate numeric modes
    if mode not in map(str, range(1, 19)):
        return render_template('main_screen.html', message="Por favor ingresa una opción válida.")

    if mode == '18':
        return redirect(url_for('art_gallery'))
    elif mode == '16':
        return render_template('verbs.html', regular_verbs=conjall.printem(all), irregular_verbs=abnorm.print_conj(all))
    elif mode == '17':
        riddle_index = 0
        return redirect(url_for('riddle_route'))
    else:
        if mode == '15':
            abnorm.show_irr()
        if mode in map(str, range(5, 14)):
            filter_vtype = 'regular'
        elif mode == '4':
            filter_vtype = None
        else:
            filter_vtype = None
        duced = False
        used_entries.clear()
        missd.clear()  # Clear missd
        ans_words.clear()  # Clear ans_words
        corr_ans = 0
        incor_ans = 0
        nomore = False
        return redirect(url_for('quiz_route'))


def process_exit():
    global used_entries, missd, ans_words
    used_entries.clear()

    total_ans = corr_ans + incor_ans
    accuracy = (corr_ans / total_ans) * 100 if total_ans > 0 else 0
    accuracy = round(accuracy, 2)
    if accuracy >= 100:
        special_img = "¡Bien hecho!" + img.art_28
        print(special_img)
        print(accuracy)
        print("test")
    else:
        special_img = ""

    # Print incorrect words to the terminal
    if missd:
        print("Las palabras incorrectas:")
        for word in missd:
            print(f"{word} ({ans_words[word]})")
    else:
        print("No incorrect answers recorded.")

    ascii_art = img.dis_random_ascii()

    return render_template(
        'bye.html',
        correct=corr_ans,
        incorrect=incor_ans,
        total=total_ans,
        accuracy=accuracy,
        special_img=special_img,
        ascii_art=ascii_art,
        ans_words=ans_words  # Pass ans_words to the template context
    )
@app.route('/bye') # New route for bye.html
def bye():
    global ans_words, current_tense, current_pronoun # Access global variables
    accuracy = (corr_ans / (corr_ans + len(missd))) * 100 if (corr_ans + len(missd)) >= 0 else 1
    accuracy = round(accuracy, 2)
    return render_template('bye.html', ans_words=ans_words, correct=corr_ans, incorrect=len(missd), accuracy=accuracy, tense=current_tense, pronoun=current_pronoun) # Pass variables to template

@app.route('/riddle', methods=['GET', 'POST'])
def riddle_route():
    global riddle_index, riddle_attempts

    riddles = [
        (riddleapi.riddle_1, riddleapi.answer_1, riddleapi.img_1),
        (riddleapi.riddle_2, riddleapi.answer_2, riddleapi.img_2),
        (riddleapi.riddle_3, riddleapi.answer_3, riddleapi.img_3)
    ]

    if request.method == 'POST':
        user_answer = request.form.get('user_answer').lower().strip()
        correct_answers = [ans.strip() for ans in riddles[riddle_index][1].split(",")]

        if user_answer in correct_answers:
            feedback = "¡Buen trabajo! La respuesta correcta es: " + riddles[riddle_index][1]
            img = riddles[riddle_index][2]
            if riddle_index == len(riddles) - 1:
                riddle_index = 0
                return render_template('riddle.html', riddle="", feedback=feedback, img=img, final=True)
            else:
                riddle_index += 1
                return render_template('riddle.html', riddle=riddles[riddle_index][0], feedback=feedback, img=img)

        elif user_answer == 'salida':
            return render_template('bye.html', message="¡Gracias por jugar! -Zorro")
        else:
            feedback = "Incorrecto. Inténtalo de nuevo, o escribe 'salida'."
            img = ""
            return render_template('riddle.html', riddle=riddles[riddle_index][0], feedback=feedback, img=img)

    return render_template('riddle.html', riddle=riddles[riddle_index][0], feedback="", img="")
import time

def process_input(user_input):
    global missd, ans_words, corr_ans, incor_ans, current_entry, current_verb, current_tense, current_pronoun, mode, previous_correct_answer, previous_example_sentence

    if current_entry is None:
        return "no hay más entradas disponibles.", "", "", True

    time.sleep(0.4)

    if mode in map(str, range(5, 15)) or mode == '15':  # Conjugation (including Mode 15)
        if check_conj(user_input, current_verb):
            if current_entry['esp'] not in ans_words:  # Check if already answered incorrectly
                corr_ans += 1
                print("----------------CORRECT!----------------")
            feedback = f"¡Buen trabajo! La respuesta correcta es: {current_verb} ({current_entry['eng']})"
            translation_fifteen = abnorm.translate_verb(current_entry['esp'])
            if mode == '15':
                if translation_fifteen:  # Check if translation_fifteen is not None
                    previous_correct_answer = f"{current_entry['esp']} ({translation_fifteen}) <br> <b>{current_verb}</b> para {current_pronoun} en <em>{current_tense}</em>"
                else:
                    previous_correct_answer = f"{current_entry['esp']} ({current_entry['eng']}) <br> <b>{current_verb}</b> para {current_pronoun} en <em>{current_tense}</em>" 
            else:
                previous_correct_answer = f"{current_entry['esp']} ({current_entry['eng']}) <br> <b>{current_verb}</b> para {current_pronoun} en <em>{current_tense}</em>"  
            previous_correct_answer = f"{current_entry['esp']} ({current_entry['eng']}) <br> <b>{current_verb}</b> para {current_pronoun} en <em>{current_tense}</em>"  # Include tense and pronoun

            previous_example_sentence = "**aún no hay frase disponible**"

            return "", feedback, feedback, True  # Correct, move to next question
        else:  # Incorrect conjugation attempt or "Me rindo"
            if user_input == 'me rindo':  # Check for "Me rindo" explicitly
                if current_entry['esp'] not in missd:
                    incor_ans += 1
                    missd.add(current_entry['esp'])
                    ans_words[current_entry['esp']] = {"verb": current_verb, "tense": current_tense, "pronoun": current_pronoun}
                    print("----------------NOT CORRECT!----------------")
                
                correct_answer = current_verb
                translation_fifteen = abnorm.translate_verb(current_entry['esp'])
                if mode == '15':
                    if translation_fifteen:  # Check if translation_fifteen is not None
                        previous_correct_answer = f"{current_entry['esp']} ({translation_fifteen}) <br> <b>{current_verb}</b> para {current_pronoun} en <em>{current_tense}</em>"
                    else:
                        previous_correct_answer = f"{current_entry['esp']} ({current_entry['eng']}) <br> <b>{current_verb}</b> para {current_pronoun} en <em>{current_tense}</em>" 
                else:
                    previous_correct_answer = f"{current_entry['esp']} ({current_entry['eng']}) <br> <b>{current_verb}</b> para {current_pronoun} en <em>{current_tense}</em>"  
                previous_example_sentence = "**aún no hay frase disponible**"
                return "", previous_correct_answer, previous_correct_answer, True  # Show correct answer, move to next

            if current_entry['esp'] not in missd:  # Incorrect guess
                incor_ans += 1
                missd.add(current_entry['esp'])
                ans_words[current_entry['esp']] = {"verb": current_verb, "tense": current_tense, "pronoun": current_pronoun}
                print("----------------NOT CORRECT!----------------")

            feedback = "Incorrecto. ¡Inténtalo de nuevo!!"
            gram = current_entry.get('pos', '')
            ans_eng = abnorm.translate_verb(current_entry['esp'])
            print(ans_eng)
            if mode == '15':
                if mode == '9' or current_tense == 'Presente Subjunctivo':
                    prompt = f"[{current_tense}] ¿Cómo se dice '<b>que {current_entry['esp']}</b>' ({ans_eng}) para '{current_pronoun}'?" if gram else f"[{current_tense}] ¿Cómo se dice '<b>que {current_entry['esp']}</b>' ({ans_eng}) para '{current_pronoun}'?"
                else:
                    prompt = f"[{current_tense}] ¿Cómo se dice '<b>{current_entry['esp']}</b>' ({ans_eng}) para '{current_pronoun}'?" if gram else f"[{current_tense}] ¿Cómo se dice '<b>{current_entry['esp']}</b>' ({ans_eng}) para '{current_pronoun}'?"
                return prompt, feedback, "", False  # Same prompt, feedback, no answer yet
            else:
                if mode == '9' or current_tense == 'Presente Subjunctivo':
                    prompt = f"[{current_tense}] ¿Cómo se dice '<b>que {current_entry['esp']}</b>' ({current_entry['eng']}) para '{current_pronoun}'?" if gram else f"[{current_tense}] ¿Cómo se dice '<b>que {current_entry['esp']}</b>' ({current_entry['eng']}) para '{current_pronoun}'?"
                else:
                    prompt = f"[{current_tense}] ¿Cómo se dice '<b>{current_entry['esp']}</b>' ({current_entry['eng']}) para '{current_pronoun}'?" if gram else f"[{current_tense}] ¿Cómo se dice '<b>{current_entry['esp']}</b>' ({current_entry['eng']}) para '{current_pronoun}'?"
                return prompt, feedback, "", False  # Same prompt, feedback, no answer yet

    else:  # Translation (Modes 1, 2, 3, 4)
        eng_words = current_entry['eng'].split(', ')
        if user_input == 'me rindo':
            if current_entry['esp'] not in missd:
                incor_ans += 1
                missd.add(current_entry['esp'])
                ans_words[current_entry['esp']] = {"translation": ' / '.join(eng_words)}
                print("----------------NOT CORRECT!----------------")

            correct_answer = ' / '.join(eng_words)
            previous_correct_answer = f"<b>{correct_answer}</b> ({current_entry['esp']})"
            sentence = current_entry.get('1sent')
            if sentence is None:
                sentence = "**aún no hay frase disponible**, **aún no hay frase disponible**"
            previous_example_sentence = sentence
            return "", previous_correct_answer, previous_correct_answer, True

        if check_transl(user_input, eng_words):
            if current_entry['esp'] not in ans_words:
                corr_ans += 1
                print("----------------CORRECT!----------------")
            feedback = f"¡Buen trabajo! La respuesta correcta es: {'/'.join(eng_words)} ({current_entry['esp']})"
            previous_correct_answer = feedback
            sentence = current_entry.get('1sent')
            if sentence is None:
                sentence = "**aún no hay frase disponible**, **aún no hay frase disponible**"
            previous_example_sentence = sentence
            return "", feedback, feedback, True
        else:  # Incorrect translation attempt
            if current_entry['esp'] not in missd:
                incor_ans += 1
                missd.add(current_entry['esp'])
                ans_words[current_entry['esp']] = {"translation": ', '.join(eng_words)}
                print("----------------NOT CORRECT!----------------")
            feedback = "Incorrecto. ¡Inténtalo de nuevo!"
            sentence = current_entry.get('1sent')
            if sentence is None:
                sentence = "**aún no hay frase disponible**, **aún no hay frase disponible**"
            previous_example_sentence = sentence

            gram = current_entry.get('pos', '')
            prompt = f"¿Cuál es la traducción al inglés de '{current_entry['esp']}' ({gram})?" if gram else f"¿Cuál es la traducción al inglés de '{current_entry['esp']}' ({gram})?"
            return prompt, feedback, "", False

    return "", "", "", False  # Should not normally reach here
@app.route('/listo')
def listo():
    return render_template('listo.html')
@app.route('/quiz', methods=['GET', 'POST'])
def quiz_route():
    global corr_ans, incor_ans, previous_correct_answer, previous_example_sentence, current_entry, mode, current_tense, current_pronoun

    previous_correct_answer = ""  # Initialize outside the conditional
    previous_example_sentence = ""  # Initialize outside the conditional
    tense_for_bye = ""  # Initialize outside the conditional
    pronoun_for_bye = "" #Initialize outside the conditional

    if request.method == 'POST':
        user_input = request.form.get('user_input').strip().lower()
        if user_input == 'salida':
            return process_exit()

        prompt, feedback, answer, next_question = process_input(user_input)

        if next_question:
            current_entry = get_entry(data, fltr_pos='verb' if mode in map(str, range(5, 14)) or mode == '4' else 'phrase' if mode == '2' else None, fltr_vtype='regular' if mode in map(str, range(5, 14)) else None) # hard=(mode == '3')
            if current_entry:
                prompt, feedback, answer = get_current_question_details()
                if mode not in ['1', '2', '3', '4']:  # Only set for conjugation modes
                    tense_for_bye = current_tense
                    pronoun_for_bye = current_pronoun
            else:
                return process_exit()

            return render_template('quiz.html', prompt=prompt, feedback=feedback, answer=answer,
                                   previous_correct_answer=previous_correct_answer,
                                   previous_example_sentence=previous_example_sentence,
                                   tense=tense_for_bye, pronoun=pronoun_for_bye)

        return render_template('quiz.html', prompt=prompt, feedback=feedback, answer=answer, 
                               previous_correct_answer=previous_correct_answer, 
                               previous_example_sentence=previous_example_sentence,
                               tense=tense_for_bye, pronoun=pronoun_for_bye)

    # Handle initial GET request (no user input yet)
    current_entry = get_entry(data, fltr_pos='verb' if mode in map(str, range(5, 14)) or mode == '4' else 'phrase' if mode == '2' else None, fltr_vtype='regular' if mode in map(str, range(5, 14)) else None) # hard=(mode == '3')
    if current_entry:
        prompt, feedback, answer = get_current_question_details()
        if mode not in ['1', '2', '3', '4']: #Only set for conjugation modes
            tense_for_bye = current_tense
            pronoun_for_bye = current_pronoun
    else:
        return process_exit()

    return render_template('quiz.html', prompt=prompt, feedback=feedback, answer=answer, 
                           previous_correct_answer=previous_correct_answer, 
                           previous_example_sentence=previous_example_sentence,
                           tense=tense_for_bye, pronoun=pronoun_for_bye)  # tense_for_bye is now defined
def quiz():  # This function is no longer needed if you call quiz_route directly
    pass # Since you call quiz_route, you probably don't need this quiz function anymore.
def get_current_question_details():
    if mode == '1':
        return get_current_question_details_translation()
    elif mode == '2':
        return get_current_question_details_translation(fltr_pos='phrase')
    elif mode == '3':
        return get_current_question_details_translation(syl_filter=True)
    elif mode == '4':
        return get_current_question_details_translation(fltr_pos='verb')
    elif mode in map(str, range(5, 14)):
        return get_current_question_details_conjugation()
    elif mode == '14':
        return get_current_question_details_conjugation()
    elif mode == '15':
        return get_current_question_details_conjugation_irregular()  # Logic for irregulars
    else:
        return get_current_question_details_translation()  # Default mode (translation)

def get_current_question_details_conjugation_irregular():
    global current_entry, current_verb, current_tense, current_pronoun, mode

    verb, pronoun, tense, conjugated_verb = abnorm.random_verb_pronoun_tense()

    neg_imperative = (pronoun == 'yo' and tense == 'Imperativo')

    current_tense = tense
    current_verb = conjugated_verb

    if conjugated_verb:
        verb_translation = abnorm.translate_verb(verb)  # Get the translation

        if not neg_imperative:
            if mode == '9' or current_tense == 'Presente Subjunctivo' or conjugated_verb.startswith("que"):
                prompt = f"\n[{current_tense}] ¿Cómo se dice '<b>que {verb}</b>' ({verb_translation}) para '{pronoun}'? \n"  # Add translation to prompt
            else:
                prompt = f"\n[{current_tense}] ¿Cómo se dice '<b>{verb}</b>' ({verb_translation}) para '{pronoun}'? \n"  # Add translation to prompt
        else:
            if mode == '9' or current_tense == 'Presente Subjunctivo' or conjugated_verb.startswith("que"):
                prompt = f"\n[{current_tense}] ¿Cómo se dice '<b>que {verb}</b>' ({verb_translation}) para 'no (tú)'? \n"  # Add translation to prompt
            else:
                prompt = f"\n[{current_tense}] ¿Cómo se dice '<b>{verb}</b>' ({verb_translation}) para 'no (tú)'? \n"  # Add translation to prompt

        current_entry = {'esp': verb, 'eng': conjugated_verb}
        current_pronoun = pronoun
        feedback = ""
        answer = ""
        return prompt, feedback, answer

    else: 
        verb = "hablar"
        pronoun = "yo"
        tense = "Presente"
        conjugated_verb = "hablo"

        current_entry = {'esp': verb, 'eng': 'to ' + verb}
        current_verb = conjugated_verb
        current_tense = tense
        current_pronoun = pronoun
        feedback = "\nNo se encontró un verbo irregular para conjugar. Usando 'hablar' como ejemplo.\n" 
        answer = "" 
        if current_tense == "Presente Subjunctivo":
            prompt = f"\n[{tense}] ¿Cómo se dice '<b>que {verb}</b>' para '{pronoun}'? \n" 
        else:
            prompt = f"\n[{tense}] ¿Cómo se dice '<b>{verb}</b>' para '{pronoun}'? \n"

        return prompt, feedback, answer
def get_current_question_details_all_entries():
    global current_entry
    current_entry = get_entry(data)
    if not current_entry:
        return "no hay más entradas disponibles.", "", ""
    gram = current_entry.get('pos', '')
    return f"¿Cuál es la traducción al inglés de '{current_entry['esp']}' ({gram})?", "", ""

def get_current_question_details_regular_verbs():
    global current_entry
    current_entry = get_entry(data, fltr_pos='verb', fltr_vtype=None)
    if not current_entry:
        return "no hay más entradas disponibles.", "", ""
    gram = current_entry.get('pos', '')
    return f"¿Cuál es la traducción al inglés de '{current_entry['esp']}' ({gram})?", "", ""

def get_current_question_details_conjugation(current_mode=None):
    global current_entry, current_verb, current_tense, current_pronoun, mode

    if current_mode is not None:
        mode = current_mode

    current_entry = get_entry(data, fltr_pos='verb', fltr_vtype='regular')
    if not current_entry:
        return "no hay más entradas disponibles.", "", ""
    
    if mode == '14': 
        current_mode = random.choice(['5', '6', '7', '8', '9', '10', '11', '12', '13'])
    else:
        current_mode = mode

    tense_ind = {
            '5': '',
            '6': 'fut',
            '7': 'past',
            '8': 'perf',
            '9': 'subju',
            '10': 'ppsub',
            '11': 'imperf',
            '12': 'orders',
            '13': 'cond'
    }[current_mode]

    forms = {pronoun: getattr(conjall, f'make_{pronoun}_{tense_ind}') for pronoun in ['yo', 'tu', 'usted', 'nos', 'ustedes']}
    current_pronoun, corr_form = random.choice(list(forms.items()))
    current_tense = {
        '5': "Presente",
        '6': "Futuro",
        '7': "Pasado",
        '8': "Presente Perfecto",
        '9': "Presente Subjuntivo",
        '10': "Pasado Perfecto Subjuntivo",
        '11': "Imperfecto",
        '12': "Imperativo",
        '13': "Condicional"
    }[current_mode]

    current_verb = corr_form(current_entry['esp'])
    if current_mode == '9' or current_tense == 'Presente Subjunctivo':
        return f"[{current_tense}] ¿Cómo se dice '<b>que {current_entry['esp']}</b>' ({current_entry['eng']}) para '{current_pronoun}'?", "", "" 
    elif current_mode == '12':
        if current_pronoun == 'yo':
            return f"[{current_tense}] ¿Cómo se dice '<b>{current_entry['esp']}</b>' ({current_entry['eng']}) para 'no tú'?", "", ""
        elif not current_pronoun == 'yo':
            return f"[{current_tense}] ¿Cómo se dice '<b>{current_entry['esp']}</b>' ({current_entry['eng']}) para '{current_pronoun}'?", "", "" 
    else:
        if current_mode == '14' or current_mode == '9' or mode == '9' or current_tense == 'Presente Subjunctivo':
            return f"[{current_tense}] ¿Cómo se dice '<b>que {current_entry['esp']}</b>' ({current_entry['eng']}) para '{current_pronoun}'?", "", "" 
        else:
            return f"[{current_tense}] ¿Cómo se dice '<b>{current_entry['esp']}</b>' ({current_entry['eng']}) para '{current_pronoun}'?", "", ""

if __name__ == '__main__':
    app.run(debug=True)