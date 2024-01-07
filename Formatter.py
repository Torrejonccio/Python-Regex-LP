import re

### Expresiones Regulares ###
numero_entero = r"\b[1-9]\d*\b"
nombre_variable = r"[a-zA-Z]\w*"
booleano = r"\b(true|false)\b"
string = r"#\w*#"
espacio = r"(\s|\t|\n)*"
operadores = r"(\*|\/|\+|==|<|-)"
oper_bin = rf"({numero_entero}|{booleano}|{string}|{nombre_variable}){espacio}({operadores}){espacio}({numero_entero}|{booleano}|{string}|{nombre_variable})"
condicion = rf"({numero_entero}|{booleano}|{string}|{nombre_variable}){espacio}(<|==){espacio}({numero_entero}|{booleano}|{string}|{nombre_variable})"
else_ = rf"else{espacio}{{(.*}})?"
declaracion = rf"(int|bool|str){espacio}{nombre_variable}{espacio};"
igual = rf"{nombre_variable}{espacio}={espacio}{oper_bin}{espacio};"
igual_sin_puntocoma = rf"{nombre_variable}{espacio}={espacio}{oper_bin}{espacio}"
condicional = rf"if{espacio}\({espacio}{condicion}{espacio}\){espacio}{{(.*}})?|{else_}"
ciclo = rf"while{espacio}\({espacio}{condicion}{espacio}\){espacio}{{(.*}})?"
varias_oper = rf"({igual_sin_puntocoma}({espacio}{operadores}{espacio}({numero_entero}|{booleano}|{string}|{nombre_variable}))*);"
main = rf"^int\b{espacio}main\(\){espacio}{{[\s\S]*\breturn{espacio}0{espacio};{espacio}}}$"
linea  = rf"({declaracion}|{igual}|{condicional}|{ciclo})+"
### Expresiones Regulares ###

### Compilados ###
declaracion = re.compile(declaracion)
igual = re.compile(igual)
condicional = re.compile(condicional)
ciclo = re.compile(ciclo)
main = re.compile(main)
linea = re.compile(linea)
### Compilados ###

### Funciones ###
'''
obtenerConfigDe()
————————
Sin parámetros
————————
Obtiene la configuración del archivo "config.txt" y la guarda en un diccionario global (no retorna nada) '''
def obtenerConfigDe():
    archivo = open("config.txt", "r")
    linea = archivo.readline()
    config["espacios"] = linea[0]
    config["saltos"] = linea[2]
    config["tabs"] = linea[4]
    archivo.close()
    return


'''
Corchetes(txt)
————————
Parametro 1: String del archivo txt
————————
Revisa si hay igualdad de corchetes en el txt (no retorna nada) '''
def Corchetes(txt):
    with open(txt, "r") as archivo:
        num_linea = 0
        corchetes = 0
        corchete_abierto = []
        for linea in archivo:
            num_linea += 1
            for simbolo in linea:
                if simbolo == "{":
                    corchete_abierto.append((simbolo, num_linea))
                elif simbolo == "}":
                    if bool(corchete_abierto) == False:
                        print("Sobra } en linea", num_linea)
                        return
                    else:
                        corchete_abierto.pop()
        return


'''
Revisar_main(txt)
————————
Parametro 1: String del archivo txt
————————
Revisa si el main dentro del archivo es correcto (no retorna nada) '''
def Revisar_main(txt):
    with open(txt, "r") as archivo:
        archivo = archivo.read()
        buscar_main = main.match(archivo)
        if buscar_main == None:
            print("Función Main() incorrecta, no se hará formateo del archivo entregado")
            exit()
        else:
            return


'''
Revisar(txt)
————————
Parametro 1: String del archivo txt
————————
Revisa los errores que hay en el archivo txt y retorna una tupla con la linea 
y posición, respectivamente, del primer error que se tope, de la forma: (linea, posición) '''
def Revisar(txt):
    Revisar_main(txt)
    #cor = Corchetes(txt)  # Si cor > 0: hay más corch izq
    cor = 0
    if cor == 0:
        with open(txt, "r") as archivo:

            cont = 1

            for linea_arch in archivo:
                list = []
                #nueva_linea = re.sub(r"\t+", "", linea_arch)
                nueva_linea = re.sub(r"\s+", " ", linea_arch)

                if nueva_linea[0] == " ":
                    a = re.search(r"\w", nueva_linea)
                    nueva_linea = nueva_linea[a.start():]

                iterador = linea.finditer(nueva_linea)
                nueva_linea += " "

                for encontrado in iterador:
                    #print(encontrado)
                    inicio = encontrado.start()
                    final = encontrado.end()

                    if nueva_linea[final] == "}":
                        final = final + 1
                    list.append((inicio,final+1))

                if list:
                    for i in range(1, len(list)):
                        if i == 1:

                            if list[i - 1][1] != list[i][0]:
                                print("Error de sintaxis en linea", cont,", en la posición", list[i - 1][1])
                                return (cont, list[i - 1][1])

                        else:

                            if list[i - 1][1] != list[i][0]:
                                print("Error de sintaxis en linea", cont,", en la posición", list[i - 1][1])
                                return (cont, list[i - 1][1])

                    if list[0][0] != 0:
                        print("Error de sintaxis en la primera sentencia de la linea", cont)
                        return (cont, 0)

                    if list[-1][1] != len(nueva_linea)-1:
                        print("Error de sintaxis en la última sentencia de la linea", cont,"a partir de la posición", -((len(nueva_linea)-1)-list[-1][1]))
                        return (cont, -((len(nueva_linea)-1)-list[-1][1]))

                else:

                    if len(nueva_linea) != 0 and "main" not in nueva_linea and "return" not in nueva_linea:
                        print("Error de sintaxis en toda la linea", cont)
                        return (cont, 0)

                cont += 1


'''
Formatear_con_error(txt,pos_linea, pos, config)
————————
Parametro 1: String del archivo txt
Parametro 2: Int de la linea dada
Parametro 3: Int de la posición dada
Parametro 4: Diccionario con los valores de config.txt
————————
Formatea el archivo txt cuando este contiene errores, realizandolo
hasta el primer error que aparezca'''
def Formatear_con_error(txt,pos_linea, pos, config):
    cant_espacios = config["espacios"]
    cant_saltos = config["saltos"]
    cant_tabs = config["tabs"]
    lista = []
    escribir = open("formateado.txt", "w")
    with open(txt, "r") as archivo:
        espacios_formateo = int(cant_espacios) * " "
        saltos_formateo = int(cant_saltos) * "\n"
        tabs_formateo = int(cant_tabs) * "\t"
        i = 1
        while i <= pos_linea:
            linea_archivo = archivo.readline()
            linea_archivo = linea_archivo.rstrip("\n")
            linea_archivo = re.sub(r"\s+", espacios_formateo, linea_archivo)

            if i == pos_linea:
                linea_archivo = linea_archivo[:pos]
            #if linea_archivo[0] == " ":
               # primera_letra = re.search(r"\w", linea_archivo)
                #linea_archivo = linea_archivo[primera_letra.start():]

            linea_archivo = re.sub(r";", espacios_formateo + ";" + espacios_formateo, linea_archivo)
            linea_archivo = re.sub(r"\(", espacios_formateo + "(" + espacios_formateo, linea_archivo)
            linea_archivo = re.sub(r"\)", espacios_formateo + ")" + espacios_formateo, linea_archivo)
            linea_archivo = re.sub(r"\s+", espacios_formateo, linea_archivo)

            linea_archivo = re.sub(r"\{", "{" + saltos_formateo, linea_archivo)

            linea_archivo = re.sub(r"\}", "}" + saltos_formateo, linea_archivo)

            linea_archivo = re.sub(r";(\s+)?", ";" + saltos_formateo + "\n", linea_archivo)

            escribir.write(linea_archivo)

            i += 1
        escribir.close()
        return


'''
Formatear_sin_error(txt, config)
————————
Parametro 1: String del archivo txt
Parametro 2: Diccionario con los valores de config.txt
————————
Formatea el archivo txt cuando este NO contiene errores, realizandolo
completamente'''
def Formatear_sin_error(txt, config):
    cant_espacios = config["espacios"]
    cant_saltos = config["saltos"]
    cant_tabs = config["tabs"]

    escribir = open("formateado.txt", "w")
    with open(txt, "r") as archivo:
        espacios_formateo = int(cant_espacios) * " "
        saltos_formateo = int(cant_saltos) * "\n"
        tabs_formateo = int(cant_tabs) * "\t"
        flag = False

        for linea_archivo in archivo:
            if linea_archivo[0] == " ":
                primera_letra = re.search(r"\w", linea_archivo)
                linea_archivo = linea_archivo[primera_letra.start():]

            linea_archivo = re.sub(r";", espacios_formateo + ";" + espacios_formateo, linea_archivo)
            linea_archivo = re.sub(r"\(", espacios_formateo + "(" + espacios_formateo, linea_archivo)
            linea_archivo = re.sub(r"\)", espacios_formateo + ")" + espacios_formateo, linea_archivo)
            linea_archivo = re.sub(r"\s+", espacios_formateo, linea_archivo)

            linea_archivo = re.sub(r"\{", "{" + saltos_formateo, linea_archivo)

            linea_archivo = re.sub(r"\}", "}" + saltos_formateo, linea_archivo)

            linea_archivo = re.sub(r";(\s+)?", ";" + saltos_formateo + "\n", linea_archivo)

            escribir.write(linea_archivo)
        escribir.close()
        return
### Funciones ###

### Ejecución código ###
config = {}
obtenerConfigDe() # Obtención de configuraciones #

tupla_linea_pos = Revisar("codigo.txt") # Obtención de tupla de error (linea, posición) #

if tupla_linea_pos != None: # Si la tupla existe es porque hay error y se ejecuta el formateo con error #

    Formatear_con_error("codigo.txt", tupla_linea_pos[0], tupla_linea_pos[1], config)

else:

    Formatear_sin_error("codigo.txt", config)
### Ejecución código ###