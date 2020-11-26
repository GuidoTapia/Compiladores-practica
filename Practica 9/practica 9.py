"""
Link github : https://github.com/GuidoTapia/Compiladores-practica
Practica 9 - El ingreso de la gramatica es mediente el archivo gramatica.txt
Avance Conseguido: Se logro la creacion dinamica de todas las clases que conformaman la gramatica, no obstante no se pudo replicar el arbol
Estudiantes : Jose Manuel Cornejo Lupa , Guido Luis Tapia Oré , Jose Eduardo Zenteno Monteagudo
Correo : jose.cornejo.lupa@ucsp.edu.pe , guido.tapia@ucsp.edu.pe , jose.zenteno@ucsp.edu.pe
Curso : Compiladores - CCOMP 8-1
"""

#operadores=",=;{}"
dolar='$'
class Token:
    palabra = "" #almacena una copia de la palabra
    indice = -1 #en donde apareció en la sentencia
    tipo = '' #int (entero), #float (flotante), variable (variable), O (operador), string (string), time (time), X (error)
    def __init__(self,cadena, i, t):
        self.palabra=cadena
        self.indice=i
        self.tipo=t
    def toString(self):
        return "Token["+self.palabra+"]: pos = "+str(self.indice)+", tipo ="+self.tipo

def analizadorLexico(texto):
    tokens=[]
    for linea in texto:
        idx=0
        while idx<len(linea):
            if linea[idx].isnumeric():
                aux=""
                inicio=idx
                while (idx< len(linea) and linea[idx] != ' ' and linea[idx]!='\t' and linea[idx]!='\n'):
                    aux+=linea[idx]
                    idx=idx+1
                tokens.append(Token(aux,inicio,"num"))
            elif (linea[idx] == ' ' or linea[idx]=='\t' or linea[idx]=='\n'):
                idx=idx+1
            else:
                aux=""
                inicio=idx
                while (idx< len(linea) and linea[idx] != ' ' and linea[idx]!='\t' and linea[idx]!='\n'):
                    aux+=linea[idx]
                    idx=idx+1
                tokens.append(Token(aux,inicio,aux))
    return tokens

class Produccion:
    izq=""
    der=[]
    def __init__(self,i,d):
        self.izq=i
        self.der=d
    def getString(self):
        return self.izq+" -> "+' '.join(map(str, self.der))

class TAS:
    tablaSintactica={}
    terminales=[]
    noterminales=[]
    def __init__(self,gram):
        self.terminales=list(gram.terminales)
        #self.terminales.append("$")
        self.noterminales=list(gram.noterminales)
        for nT in self.noterminales:
            self.tablaSintactica[nT]={}
            for t in self.terminales:
                self.tablaSintactica[nT][t]=[]
        self.terminales.sort()
        self.noterminales.sort()
    def llenarEstaticamente(self,gram):
        self.terminales=list(gram.terminales)
        self.noterminales=list(gram.noterminales)
        for nT in gram.noterminales:
            self.tablaSintactica[nT]={}
            for t in gram.terminales:
                self.tablaSintactica[nT][t]=[]
        for p in gram.produccion:
            self.tablaSintactica[p.izq][p.der[0]]=p.der
        self.terminales.sort()
        self.noterminales.sort()
        #print(self.tablaSintactica)
    def print(self):
        aux='\t|'
        for t in self.terminales:
            if t!="lambda":
                aux+=t+'\t|'
        print (aux)
        for nT in self.noterminales:
            aux=nT+'\t|'
            for t in self.terminales:
                if t!="lambda":
                    aux+=' '.join(map(str, self.tablaSintactica[nT][t]))
                    aux+='\t|'
            print (aux)


def opera1(pivote, literales):
    for l in reversed(literales):
        pivote.hijos.insert(0,Nodo(l,pivote))
        #print(pivote,pivote.hijos)
        #print(pivote.hijos[0],pivote.hijos[0].hijos)
        if(len(pivote.hijos)>1):
            pivote.hijos[0].siguiente=pivote.hijos[1]
    return pivote.hijos[0]

def opera2(pivote):
    if(pivote.siguiente!=None):
        return pivote.siguiente
    while(pivote.padre!=None):
        if(pivote.padre.siguiente!=None):
            return pivote.padre.siguiente
        else:
            pivote=pivote.padre
    return None
        
def opera3(pivote):

    pivote.hijos.append(Nodo('lambda',pivote))
    return opera2(pivote)


class Gramatica:
    produccion = [] #Lista de producciones
    terminales = set("$") #Conjunto de terminales
    noterminales = set() #no terminales
    inicial = ""
    primeros={}
    siguientes = {}
    tas=0
    def print(self): #Crear una función para imprimir
        for p in self.produccion:
            print (p.getString())
    def cargar(self,texto):
        for linea in texto:
            izqProdTemp =""
            strTemp = ""
            derProdTemp =[]
            idx=0
            while idx<len(linea):
                if (linea[idx]==':' and linea[idx+1]=='='):
                    izqProdTemp = strTemp
                    self.noterminales.add(strTemp)
                    if self.inicial=="":
                        self.inicial=strTemp
                    strTemp=""
                    idx+=1
                elif (linea[idx]=='|'):
                    if(len(strTemp)):
                        derProdTemp.append(strTemp)
                    self.produccion.append(Produccion(izqProdTemp,derProdTemp))
                    derProdTemp =[]
                elif (linea[idx]==' ' or linea[idx]=='\t' or linea[idx]=='\n'):
                    if (len(izqProdTemp) and len(strTemp)):
                        derProdTemp.append(strTemp)
                        self.terminales.add(strTemp)
                        strTemp=""
                else:
                    strTemp+=linea[idx]
                idx+=1
            if(len(strTemp)):
                derProdTemp.append(strTemp)
                self.terminales.add(strTemp)
            self.produccion.append(Produccion(izqProdTemp,derProdTemp))
            izqProdTemp =""
            derProdTemp =[]
        for e in self.noterminales:
            if e in self.terminales:
                self.terminales.remove(e)
        #Descomentar para ver primeros y siguientes
        #print(self.terminales)
        #print(self.noterminales)
    def getProduccion(self,izq):
        aux=""
        for p in self.produccion:
            if (p.izq==izq):
                aux+=" | "*(len(aux)>0)+ p.der
        return aux
    def getProducciones(self,izq):
        aux=[]
        for p in self.produccion:
            if (p.izq==izq):
                aux.append( p.der)
        return aux
    def printProducciones(self):
        for p in self.produccion:
            print(p.getString())
    def getPrimero(self,izq):
        producciones = self.getProducciones(izq)
        primeros=set()
        primNoTerm=[]
        for p in producciones:
            if p[0] in self.terminales:
                primeros.add( p[0])
            elif p[0] not in primNoTerm:
                primNoTerm.append( p[0])
        for nT in primNoTerm:
            producciones = self.getProducciones(nT)
            for p in producciones:
                if p[0] in self.terminales:
                    primeros.add( p[0])
                elif p[0] not in primNoTerm:
                    primNoTerm.append( p[0])
        return primeros       
    def getPrimeros(self):
        self.primeros={}
        for nodo in self.noterminales:
            self.primeros[nodo]=self.getPrimero(nodo)
        return self.primeros
    def getSiguientes(self):
        
        self.siguientes = {}
        for nT in self.noterminales:
            self.siguientes[nT] = set()
        self.siguientes[self.inicial] = {dolar}
        self.getPrimeros()
        for r in range(3):
            for p in self.produccion:
                for i in range(len(p.der)-1):
                    if p.der[i] in self.noterminales:
                        if p.der[i+1] in self.noterminales:
                            self.siguientes[p.der[i]].update(self.primeros[p.der[i+1]])
                            while "lambda" in self.siguientes[p.der[i]]:
                                iAux=1
                                self.siguientes[p.der[i]].remove("lambda")
                                self.siguientes[p.der[i]].update(self.siguientes[p.der[i+iAux]])
                                iAux+=1
                        else:
                            self.siguientes[p.der[i]].add(p.der[i+1])
                if p.der[len(p.der)-1] in self.noterminales:
                    self.siguientes[p.der[len(p.der)-1]].update(self.siguientes[p.izq])
        return self.siguientes
    def buscarProduccion(self, nodoNt, nodoT):
        prod=self.getProducciones(nodoNt)
        for p in prod:
            if (p[0] in self.terminales and p[0]==nodoT) or (p[0] in self.noterminales and nodoT in self.primeros[p[0]]):
                return p
        return []
    def crearTabla(self):
        self.getSiguientes()
        self.tas = TAS(self)
        for nodoNt in self.noterminales:
            for nodoT in self.primeros[nodoNt]:
                if nodoT != "lambda":
                    self.tas.tablaSintactica[ nodoNt ][ nodoT ] = self.buscarProduccion( nodoNt, nodoT)
                else:
                    for nodoT2 in self.siguientes[nodoNt]:
                        self.tas.tablaSintactica[nodoNt][nodoT2] = ["lambda"]
        #Descomentar para visualizar tabla
        self.tas.print()
        return self.tas
    def analizar(self, tokens ):
        pila=[]
        cola=[]
        for t in tokens:
            cola.append(t.tipo)
        cola.append('$')
        pila.insert(0,'$')
        pila.insert(0,self.inicial)
        print("Tabla analisis sintactico:")
        print("Pila"+' '*36+"Entrada"+' '*33+"Operacion"+'\t'+"Adicionar")
        while(len(cola) and len(pila)):
            #print("cola",cola)
            #print("pila",pila)
            auxPila=' '.join(map(str, reversed(pila)))
            auxCola=' '.join(map(str, cola))
            print(auxPila+' '*(40-len(auxPila))+auxCola+' '*(40-len(auxCola)),end='')
            if(cola[0]==pila[0]):
                if(cola[0]!='$'):
                    print('2')
                else:
                    print()
                cola.pop(0)
                pila.pop(0)
                
            elif(pila[0] in self.noterminales and cola[0] in self.terminales):
                tmp=pila.pop(0)
                
                #print(tmp,cola[0],self.tas.tablaSintactica[tmp][cola[0]])
                if len(self.tas.tablaSintactica[tmp][cola[0]])>0:
                    if self.tas.tablaSintactica[tmp][cola[0]][0]!="lambda":
                        print('1\t\t',end='')
                    else:
                        print("3\t\t''",end='')
                    #print("Nodo: ",tmp," Hijos: ", self.tas.tablaSintactica[tmp][cola[0]])
                    for t in reversed(self.tas.tablaSintactica[tmp][cola[0]]):
                        if t!="lambda":
                            pila.insert(0,t)
                            print(t,end='')
                    print()
                else:
                    print()
                    print("Error en Parser")
                    return False
            else:
                print()
                print("Error en Parser")
                return False
        return True

def analizar(gramatica, tokens ):
    pila=[]
    cola=[]
    #raiz=Nodo(gramatica.inicial,None)
    pivote=raiz
    for t in tokens:
        cola.append(t.tipo)
    cola.append('$')
    pila.insert(0,'$')
    pila.insert(0,gramatica.inicial)
    print()
    print("Tabla analisis sintactico:")
    print("Pila"+' '*36+"Entrada"+' '*33+"Operacion"+'\t'+"Adicionar")
    while(len(cola) and len(pila)):
        auxPila=' '.join(map(str, reversed(pila)))
        auxCola=' '.join(map(str, cola))
        #raiz.imprimir()
        print(auxPila+' '*(40-len(auxPila))+auxCola+' '*(40-len(auxCola)),end='')
        if(cola[0]==pila[0]):
            if(cola[0]!='$'):
                print('2')
                pivote=opera2(pivote)
            else:
                print()
            cola.pop(0)
            pila.pop(0)
                
        elif(pila[0] in gramatica.noterminales and cola[0] in gramatica.terminales):
            tmp=pila.pop(0)
            if len(gramatica.tas.tablaSintactica[tmp][cola[0]])>0:
                if gramatica.tas.tablaSintactica[tmp][cola[0]][0]!="lambda":
                    print('1\t\t',end='')
                    pivote=opera1(pivote,gramatica.tas.tablaSintactica[tmp][cola[0]])
                    for t in reversed(gramatica.tas.tablaSintactica[tmp][cola[0]]):
                        pila.insert(0,t)
                    for t in gramatica.tas.tablaSintactica[tmp][cola[0]]:
                        print(t+' ',end='')
                else:
                    print("3\t\t''",end='')
                    pivote=opera3(pivote)
                
                print()
            else:
                print()
                print("Error en Parser")
                return False
        else:
            print()
            print("Error en Parser")
            return False
    print()
    print("Arbol sintactico generado:")
    raiz.imprimir()
    return True


class Constructor:
    def __init__(self,gram):
        f = open("clasesGramatica/NNTerminal.py", "w")
        f.write("class NNTerminal:\
\n\tprod = {}\
\n\tetiqueta = ""\
\n\tpadre = None\
\n\tsiguiente = None\
\n\tdef __init__(self,etiqueta):\
\n\t\tself.padre=None\
\n\t\tself.etiqueta=etiqueta\
\n\t\tself.prod={}\
\n\t\tself.siguiente = None\
\n\tdef imprimir(self):\
\n\t\tpivote=self\
\n\t\twhile(True):\
\n\t\t\tif(len(pivote.hijos)>0):\
\n\t\t\t\tprint(pivote.etiqueta,\"->\",end='')\
\n\t\t\t\tfor h in pivote.hijos:\
\n\t\t\t\t\tprint(" ",h.etiqueta,end='')\
\n\t\t\t\tprint()\
\n\t\t\tif(len(pivote.hijos)>0):\
\n\t\t\t\tpivote=pivote.hijos[0]\
\n\t\t\telif(pivote.siguiente!=None):\
\n\t\t\t\tpivote=pivote.siguiente\
\n\t\t\telse:\
\n\t\t\t\twhile(pivote.siguiente==None):\
\n\t\t\t\t\tif(pivote.padre==None):\
\n\t\t\t\t\t\treturn\
\n\t\t\t\t\tpivote=pivote.padre\
\n\t\t\t\tpivote=pivote.siguiente")
        f.close()
        f = open("clasesGramatica/NTerminal.py", "w")
        f.write("class NTerminal:\
\n\tval = 0\
\n\tetiqueta = ""\
\n\tpadre = None\
\n\tsiguiente = None\
\n\tdef __init__(self,etiqueta):\
\n\t\tself.padre=None\
\n\t\tself.etiqueta=etiqueta\
\n\t\tself.val=0\
\n\t\tself.siguiente = None")
        f.close()
        for e in gram.noterminales:
            f = open("clasesGramatica/"+e+".py", "w")
            f.write("import NNTerminal\
class "+e+"(NNTerminal):\
\n\t#diccionario<NombreClase, Objeto >\
\n\tdef __init__(self):\
\n\t\tsuper().__init__('"+e+"')")
            for p in gram.produccion:
                if (p.izq==e):
                    for pder in p.der:
                        f.write("\n\t\tself.prod['"+pder+"'] = None")
            if e =="E":
                f.write("\n\tdef interpret(self):\
\n\t\treturn self.prod['T'].interpret()+self.prod['Ep'].interpret()")
            elif e =="Ep":
                f.write("\n\tdef interpret(self,anterior):\
\n\t\tif self.prod['+'] != None:\
\n\t\t\treturn self.prod['T'].interpret() + self.prod['Ep'].interpret()\
\n\t\telif self.prod['-'] != None:\
\n\t\t\treturn (-self.prod['T'].interpret())+self.prod['Ep'].interpret()\
\n\t\telse:\
\n\t\t\treturn 0")
            elif e =="T":
                f.write("\n\tdef interpret(self):\
\n\t\treturn self.prod['F'].interpret()*self.prod['Tp'].interpret()")
            elif e =="Tp":
                f.write("\n\tdef interpret(self,anterior):\
\n\t\tif self.prod['*'] != None:\
\n\t\t\treturn self.prod['F'].interpret()*self.prod['Tp'].interpret()\
\n\t\telse:\
\n\t\t\treturn 1")
            elif e =="F":
                f.write("\n\tdef interpret(self,anterior):\
\n\t\tif self.prod['E'] != None:\
\n\t\t\treturn self.prod['E'].interpret()\
\n\t\telse:\
\n\t\t\treturn self.prod['num'].interpret()")
            
            f.close()
        for e in gram.terminales:
            if e[0].isalpha():
                f = open("clasesGramatica/"+e+".py", "w")
                f.write("import NTerminal\
class "+e+"(NTerminal):\
\n\t#valor\
\n\tdef interprets():\
\n\t\treturn valor")
                f.close()
        print("archivos creados con exito en carpeta 'clasesGramatica'")
#Clase abstracta y estado inicial
class AbstractExpressionNT:
    def __init__(self):
        print("Mi nombre es:", self.__class__.__name__)
class EstadoInicial(AbstractExpressionNT):
    def __init__(self):
        super().__init__()
#instanciacion usando string
def rutinaReflection(nombre):
    if (nombre in globals()):
        return globals()[nombre]()

    
def main():
    gramaticaEditor=Gramatica()
    gramaticaEditor.cargar(open("gramatica.txt","r"))
    tabla=gramaticaEditor.crearTabla()
    const=Constructor(gramaticaEditor)
    
"""    tokens = analizadorLexico( open("code1.txt","r") )
    for tk in tokens:
        if(tk.tipo=='X'):
            print("Error Lexico: \""+tk.palabra+"\" no se reconocio como elemento valido")
    if ( analizar(gramaticaEditor,tokens)):
        print("-------- code1 analizado con exito --------")
    else:
        print("-------- Error Semantico en code1 --------")
    tokens = analizadorLexico( open("code2.txt","r") )
    for tk in tokens:
        if(tk.tipo=='X'):
            print("Error Lexico: \""+tk.palabra+"\" no se reconocio como elemento valido")
    if ( analizar(gramaticaEditor,tokens)):
        print("-------- code2 analizado con exito --------")
    else:
        print("-------- Error Semantico en code2 --------")
    tokens = analizadorLexico( open("code3.txt","r") )
    for tk in tokens:
        if(tk.tipo=='X'):
            print("Error Lexico: \""+tk.palabra+"\" no se reconocio como elemento valido")
    if ( analizar(gramaticaEditor,tokens)):
        print("-------- code3 analizado con exito --------")
    else:
        print("-------- Error Semantico en code3 --------")
    tokens = analizadorLexico( open("code4.txt","r") )
    for tk in tokens:
        if(tk.tipo=='X'):
            print("Error Lexico: \""+tk.palabra+"\" no se reconocio como elemento valido")
    if ( analizar(gramaticaEditor,tokens)):
        print("-------- code4 analizado con exito --------")
    else:
        print("-------- Error Semantico en code4 --------")"""
    
main()


