"""
Practica 7 - El ingreso de la gramatica es mediente el archivo gramatica.txt
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
            if (linea[idx] == ' ' or linea[idx]=='\t' or linea[idx]=='\n'):
                idx=idx+1
            else:
                aux=""
                inicio=idx
                while (idx< len(linea) and linea[idx] != ' ' and linea[idx]!='\t' and linea[idx]!='\n'):
                    aux+=linea[idx]
                    idx=idx+1
                tokens.append(Token(aux,idx,aux))
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
        while(len(cola) and len(pila)):
            print("cola",cola)
            print("pila",pila)
            #print()
            if(cola[0]==pila[0]):
                cola.pop(0)
                pila.pop(0)
            elif(pila[0] in self.noterminales and cola[0] in self.terminales):
                tmp=pila.pop(0)
                
                #print(tmp,cola[0],self.tas.tablaSintactica[tmp][cola[0]])
                if len(self.tas.tablaSintactica[tmp][cola[0]])>0:
                    #print("Nodo: ",tmp," Hijos: ", self.tas.tablaSintactica[tmp][cola[0]])
                    for t in reversed(self.tas.tablaSintactica[tmp][cola[0]]):
                        if t!="lambda":
                            pila.insert(0,t)
                else:
                    print("Error en Parser")
                    return False
            else:
                print("Error en Parser")
                return False
        return True
#Clase que construye clases en carpeta, se uso el ejemplo de nltk
class Constructor:
    def __init__(self,gram):
        for e in gram.noterminales:
            f = open("clasesGramatica/"+e+".py", "w")
            f.write("class "+e+"(AbstractExpressionNT):\
\n\t#diccionario<NombreClase, Objeto >\
\n\tdef interprets(val1,val2,val3):\
\n\t\treturn (0,0,0)")
            f.close()
        for e in gram.terminales:
            f = open("clasesGramatica/"+e+".py", "w")
            f.write("class "+e+"(AbstractExpressionT):\
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
    rutinaReflection("EstadoInicial")

main()
