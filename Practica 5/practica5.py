"""
Practica 5 - El ingreso de la gramatica es mediente el archivo gramatica.txt
Estudiante : Guido Luis Tapia Oré
Correo : guido.tapia@ucsp.edu.pe
Curso : Compiladores - CCOMP 8-1
"""
dolar='$'
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
        self.noterminales=list(gram.noterminales)
        for nT in gram.noterminales:
            self.tablaSintactica[nT]={}
            for t in gram.terminales:
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
            aux+=t+'\t|'
        print (aux)
        for nT in self.noterminales:
            aux=nT+'\t|'
            for t in self.terminales:
                aux+=' '.join(map(str, self.tablaSintactica[nT][t]))
                aux+='\t|'
            print (aux)
            
class Gramatica:
    produccion = [] #Lista de producciones
    terminales = set() #Conjunto de terminales
    noterminales = set() #no terminales
    inicial = ""
    primeros={}
    siguientes = {}
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
        for p in self.produccion:
            for i in range(len(p.der)-1):
                if p.der[i] in self.noterminales:
                    if p.der[i+1] in self.noterminales:
                        self.siguientes[p.der[i]].update(self.primeros[p.der[i+1]])
                        if "lambda" in self.primeros[p.der[i+1]]:
                            self.siguientes[p.der[i]].remove("lambda")
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
        tas = TAS(self)
        for nodoNt in self.noterminales:
            for nodoT in self.primeros[nodoNt]:
                if nodoT != "lambda":
                    tas.tablaSintactica[ nodoNt ][ nodoT ] = self.buscarProduccion( nodoNt, nodoT)
                else:
                    for nodoT2 in self.siguientes[nodoNt]:
                        tas.tablaSintactica[nodoNt][nodoT2] = ["lambda"]
                # tas[?][?] = ? depende de su implementación
        print(tas.tablaSintactica)
        tas.print()

algo=Gramatica()
algo.cargar(open("gramatica.txt","r"))
algo.print()
#tabla=TAS()
#tabla.llenarEstaticamente(algo)
#tabla.print()
print("Primeros")
print(algo.getPrimeros())
print("Siguientes")
print(algo.getSiguientes())
algo.crearTabla()
