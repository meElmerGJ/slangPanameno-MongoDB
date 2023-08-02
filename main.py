import mongoengine.errors
from mongoengine import Document, StringField
from mongoengine import connect
from tabulate import tabulate

connect('slangPanameno', host='localhost', port=27017)


class Slangs(Document):
    word = StringField(required=True, max_length=50, unique=True)
    meaning = StringField(required=True, max_length=200)
    words_generated = False


# Function to print a done task correctly message with a specified format
def msg_done(message):
    print(f"\n-----> {message} <-----")


def sys_msg(type, msg):
    if type == 1:
        print(f"\nERROR: {msg}")
    elif type == 2:
        print(f"\nWARNING: {msg}")
    else:
        print("\n\n\nUNEXPECTED ERROR\n\n\n")


# Function to input a value requested
def input_value_requested(simple_input, op_type):  # op_type = operation type, delete, update.
    if simple_input:  # simple input
        return input("\nIngrese la palabra: ")
    else:
        return input(f"\nPresiones 0 para ver palabras\n\nIngrese la palabra a {op_type}: ")


# Function verify if a word required exists.
def exists(value):
    result = Slangs.objects(word=value).first()
    if not result:
        return False
    else:
        return True


# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////

# -------------------------------PROGRAM FUNCTIONS ----------------------------------------

# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////

# Function create a slang object
def add_word():
    try:
        new_slang = Slangs(word=input("Ingrese la palabra: "), meaning=input("Ingresa el significado: "))
        new_slang.save()
        msg_done("Palabra agregada")
    except mongoengine.errors.NotUniqueError:
        sys_msg(1, "La palabra ya existe")


# Function to update a word
def edit_word():
    value = input_value_requested(False, "editar")
    if value == "0":
        get_words()
        edit_word()
    # else:
    #     new_word = input(f"Ingrese nueva palabra: ")
    #     new_meaning = input("Ingrese el significado: ")
    #     if Slangs.objects(word=value).update_one(set__word=new_word, set__meaning=new_meaning):
    #         msg_done("Palabra editada")
    #     else:
    #         print("\nERROR: El valor ingresado no existe en la base de datos")
    elif exists(value):
        new_word = input(f"Ingrese nueva palabra: ")
        new_meaning = input("Ingrese el significado: ")
        Slangs.objects(word=value).update_one(set__word=new_word, set__meaning=new_meaning)
        msg_done("Palabra editada")
    else:
        sys_msg(1, "El valor ingresado no existe en la base de datos")


# Function to delete a word
def del_word():
    value = input_value_requested(False, "eliminar")
    if value == '0':
        get_words()
        del_word()
    elif exists(value):
        Slangs.objects(word=value).delete()
        msg_done("Palabra eliminada")
    else:
        sys_msg(1, "El valor ingresado no existe en la base de datos")


# Function get all records
def get_words():
    result = Slangs.objects.all()
    table = []
    for x in result:
        table.append([x.word, x.meaning])
    print(tabulate(table, headers=["Palabra", "Significado"], tablefmt="psql"))
    input('"Presione ENTER para continuar"')


# Function to get a specific word meaning
def get_meaning():
    value = input_value_requested(True, "")
    result = Slangs.objects(word=value).first()
    if result:
        print(f"\n{result.word}, significa: {result.meaning}")
    else:
        sys_msg(1, "El valor ingresado no existe en la base de datos")


# Function to generate 10 records to test functions. (TEST USAGE ONLY)
def generate_data():
    if Slangs.words_generated:
        sys_msg(2, "Los registros ya han sido creados")
    else:
        try:
            slang_objects = [
                Slangs(word="Chombo", meaning="Amigo cercano o compañero"),
                Slangs(word="Jato", meaning="Casa o hogar"),
                Slangs(word="Pana", meaning="Amigo o camarada"),
                Slangs(word="Que xopa!", meaning="El clasico saludo de nosotros"),
                Slangs(word="Taquilla", meaning="Alguna historia o relato que puede ser falsa"),
                Slangs(word="Quilla", meaning="Dinero"),
                Slangs(word="Tirar la posta", meaning="Contar una historia o chisme"),
                Slangs(word="Taquear", meaning="Comer en exceso"),
                Slangs(word="Chiri", meaning="Frío"),
                Slangs(word="Pelea de gallos", meaning="Competencia o disputa acalorada")
            ]
            for words in slang_objects:
                words.save()
            msg_done("Se han ingresado 10 registros")
        except mongoengine.errors.NotUniqueError:
            sys_msg(2, "Los registros ya han sido creados")
        Slangs.words_generated = True


# Function to delete all records (TEST USAGE ONLY)
def delete_all_data():
    Slangs.objects().delete()
    sys_msg(2, "Todos los registros han sido eliminados")


# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////

# ---------------------------------------PROGRAM ------------------------------------------

# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////


if __name__ == '__main__':
    try:
        # Flujos de programa
        print("\nBIENVENIDO AL DICCIONARIO DE SLANG PANAMEÑO\n")

        # Program menu
        menu = """
                1) Agregar nueva palabra
                2) Editar palabra
                3) Eliminar palabra 
                4) Ver palabras
                5) Buscar significado de palabra
                6) Insertar 10 registros(only test usage)
                7) Eliminar todos los registros(only test usage)
                8) Salir
                """

        # Program main loop // Warning! -> Need to use version above Python 3.10 for ***match - case*** Statements.
        end = False

        while not end:
            try:
                print(menu)
                option = int(input(f"Ingresa una opcion: "))
                match option:
                    case 1:
                        add_word()
                    case 2:
                        edit_word()
                    case 3:
                        del_word()
                    case 4:
                        get_words()
                    case 5:
                        get_meaning()
                    case 6:
                        generate_data()
                    case 7:
                        delete_all_data()
                    case 8:
                        msg_done("El programa ha finalizado")
                        exit(0)
            except ValueError:
                print(f"ERROR - Ingrese una opcion correcta")
    except (KeyboardInterrupt, EOFError):
        msg_done("El programa ha finalizado")
