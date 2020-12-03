"""
Link github : https://github.com/GuidoTapia/Compiladores-practica
Practica 10 - El ingreso de la gramatica es mediente el archivo gramatica.txt
Estudiantes : Jose Manuel Cornejo Lupa , Guido Luis Tapia Oré , Jose Eduardo Zenteno Monteagudo
Correo : jose.cornejo.lupa@ucsp.edu.pe , guido.tapia@ucsp.edu.pe , jose.zenteno@ucsp.edu.pe
Curso : Compiladores - CCOMP 8-1
"""

operadores="*/()+-"
dolar='$'

DiccionarioError={1:'Sintaxis de Numero equivocada',\
                  2:'Operador no valido equivocada',\
                  3:'Variable contiene caracteres invalidos',\
                  4:'Desbalance, operador parentesis de cierre faltante',\
                  5:'Desbalance, operador parentesis de apertura faltante'}
class Log:
    lista_errores=[]
    lista_warnigs=[]
    f=None
    def inicializar(self):
        self.lista_errores=[]
        self.lista_warnigs=[]
        self.f = open("errores.txt", "w")
    def addError(self, codigo, errorParametro):
        self.lista_errores.append( (errorParametro.indice,codigo) )
        self.f.write("Error "+str(codigo) +" en la posicion "+str(errorParametro.indice)+ "\nToken:" +errorParametro.palabra+"\n"+str(DiccionarioError[codigo])+"\n")
    def addWarning(self, codigo, warningParametro):
        self.lista_warnigs.append( (warningParametro.indice,codigo) )
        self.f.write("Warning "+str(codigo) +" en la posicion "+str(errorParametro.indice)+ "\nToken:" +errorParametro.palabra+"\n"+str(DiccionarioError[codigo])+"\n")
    def print(self):
        if(len(self.lista_errores)==0 and len(self.lista_warnigs)==0):
            return True
        for e in self.lista_errores:
            print("Error "+str(e[1]) +" en la posicion "+str(e[0])+ "\n"+DiccionarioError[e[1]])
        for e in self.lista_warnigs:
            print("Error "+str(e[1]) +" en la posicion "+str(e[0])+ "\n"+DiccionarioError[e[1]])
        return False

errorLog=Log()

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


def reconoceNumero(linea,idx):
    iAux=idx
    palabra=""
    flagError=0
    while(iAux<len(linea) and linea[iAux]!=' ' and linea[iAux] not in operadores):
        if (not linea[iAux].isnumeric()):
            if(flagError==0 and not linea[iAux].isalpha()):
                flagError=1
            else:
                flagError=2
        palabra+=linea[iAux]
        iAux=iAux+1
    if(flagError==0):
        return Token(palabra,idx,'num'),iAux
    elif(flagError==1):
        return Token(palabra,idx,'errorOperador'),iAux
    else:
        return Token(palabra,idx,'errorNumero'),iAux

def reconoceAlphanum(linea,idx):
    iAux=idx
    palabra=""
    flagError=0
    while(iAux<len(linea) and linea[iAux]!=' ' and linea[iAux] not in operadores):
        if (not linea[iAux].isalnum()):
            flagError=1
        palabra+=linea[iAux]
        iAux=iAux+1
    if(flagError==0):
        return Token(palabra,idx,'id'),iAux
    else:
        return Token(palabra,idx,'errorVariable'),iAux


def analizadorLexico(texto):
    tokens=[]
    for linea in texto:
        idx=0
        while idx<len(linea):
            if (linea[idx] == ' ' or linea[idx]=='\t' or linea[idx]=='\n'):
                idx=idx+1
            elif linea[idx].isnumeric():
                token,idx=reconoceNumero(linea,idx)
                if token.tipo=='errorOperador':
                    errorLog.addError(2,token)
                    token.tipo='num'
                elif token.tipo=='errorNumero':
                    errorLog.addError(1,token)
                    token.tipo='num'
                tokens.append(token)
            elif linea[idx].isalpha():
                token,idx=reconoceAlphanum(linea,idx)
                if token !=0:
                    errorLog.addError(3,token)
                    token.tipo='id'
                tokens.append(token)
            elif linea[idx] in operadores:
                tokens.append(Token(linea[idx],idx,linea[idx]))
                idx=idx+1
                aux=""
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

class Nodo:
    etiqueta = ''
    hijos = []
    padre = None
    siguiente = None

    def __init__(self,etiqueta,padre):
        self.etiqueta=etiqueta
        self.padre=padre
        self.hijos=[]
        self.siguiente = None
    def imprimir(self):
        pivote=self
        while(True):
            if(len(pivote.hijos)>0):
                print(pivote.etiqueta,"->",end='')
                for h in pivote.hijos:
                    print(" ",h.etiqueta,end='')
                print()
            if(len(pivote.hijos)>0):
                pivote=pivote.hijos[0]
                #print(11111111)
            elif(pivote.siguiente!=None):
                pivote=pivote.siguiente
                #print(22222222)
            else:
                #print(33333333)
                while(pivote.siguiente==None):
                    if(pivote.padre==None):
                        return
                    pivote=pivote.padre
                pivote=pivote.siguiente


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
    contador=0
    pila=[]
    cola=[]
    raiz=Nodo(gramatica.inicial,None)
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
            contador+=1
                
        elif(pila[0] in gramatica.noterminales and cola[0] in gramatica.terminales):
            tmp=pila.pop(0)
            copiatmp=tmp
            if(copiatmp[0:5]=="Error"):
                print("Modo Panico Activado: Desvalance en parentesis")
                if(tmp=="ErrorDBI"):
                    errorLog.addError(4,tokens[contador])
                elif(tmp=="ErrorDBD"):
                    errorLog.addError(5,tokens[contador])
                return False
            elif len(gramatica.tas.tablaSintactica[tmp][cola[0]])>0:
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
                print("Modo Panico Activado: No correspondencia con la gramatica")
                return False
        else:
            print()
            print("Modo Panico Activado: No correspondencia con la gramatica")
            return False
    print()
    print("Arbol sintactico generado:")
    raiz.imprimir()
    return True




def main():
    gramaticaEditor=Gramatica()
    gramaticaEditor.cargar(open("gramatica.txt","r"))
    tabla=gramaticaEditor.crearTabla()
    errorLog.inicializar()
    
    tokens = analizadorLexico( open("code.txt","r") )
    
    if ( analizar(gramaticaEditor,tokens) and errorLog.print()):
        print("-------- codigo analizado con exito --------")
    else:
        print("-------- Error Semantico en code1 --------")
    errorLog.print()
    errorLog.f.close()
main()


