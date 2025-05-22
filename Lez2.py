
#LEZIONE2_QC




#ESERCIZIO5: Teletrasporto quantistico




#Codice scritto dal professore
import numpy as np
from qiskit import QuantumCircuit

from qiskit.quantum_info import Statevector

def crea_circuito(theta):
    qc=QuantumCircuit(3,3)
    qc.ry(theta, 0)
    qc.h(1)
    qc.cx(1,2)    
    qc=prepara(theta)
    qc.cx(0,1)
    qc.h(0)
    return qc

def teletrasporto(theta):
    qc=crea_circuito(theta)
    s=Statevector.from_label("000")
    s1=s.evolve(qc)
    r,s2=s1.measure([0,1])
    qc2=QuantumCircuit(3)
    if r[0]=='1':
        qc2.x(2)
    if r[1]=='1':
        qc2.z(2)
    return s2.evolve(qc2)

print("per provare l'algoritmo, scegliere un angolo theta per creare uno stato iniziale")
print("cos(theta/2)|0> + sin(theta/2) |1> da teletrasportare dal qubit 0 al qubit 2")
print("dare il comando s=teletrasporto(theta)")
print("per vedere lo stato risultante digitare s.to_dict()")
print("si deve vedere uno stato del tipo ")
print("cos(theta/2)|0xx>+sin(theta/2)|1xx>, ove xx è una combinazione di bit ")
print("effetto della misura sui bit 0 e 1, che non ci interessa")    

#Vediamo quali azioni eseguire da console




import math
s=teletrasporto(30*math.pi/180)
s.to_dict()



theta=30*math.pi/180
math.cos(theta/2)
math.sin(theta/2)




#Uno dei quattro possibili stati finali: |01> x (cos theta/2 |0> + sin theta/2 |1>)
#A partire dallo stato iniziale (cos theta/2 |0> + sin theta/2 |1>) x (1/sqrt 2 |00> + 1/sqrt 2 |11>)




#Creo il circuito
qc=crea_circuito(theta)
qc.draw()
s0=Statevector.from_label("000")
s1=s0.evolve(qc)
s1.to_dict() #conversione in dizionario per vedere solo i coefficienti diversi da 0




#Misuriamo lo stato s1
r, s2=s1.measure([0,1]) # lista dei qubit che voglio misurare
r
#Ho ottenuto come risultato '01', ricorda che i qubit sono numerati al contrario: primo bit è 1 ed il secondo è 0
s2.to_dict()
#Vedo come sono '001' e '101' con i coefficienti corrispondenti: non va bene perchè coefficiente è negativo

#Dobbiamo correggerlo, quindi facciamo un altro circuito aggiungendo una porta Z
qc2=QuantumCircuit(3)
qc2.z(2)
s3=s2.evolve(qc2)
s3.to_dict()
#Ho ottenuto il teletrasporto
r



#ESERCIZIO6: Triangulum su Esempio

'''Il triangulum è il nostro computer quantistico a 3 qubit (perchè molecola ha una determinata forma specifica),
basato sulla risonanza magnetica nucleare. E' alloggiato in una delle sale server del nostro dipartimento.'''



#Codice scritto dal prof
'''Le librerie sono completamente differenti, linguaggio anche un po' diverso.
si devono anche importare tutte le porte che si vogliono utilizzare'''
from spinqit import get_nmr, get_compiler, Circuit, NMRConfig
from spinqit import H, CX, X

engine = get_nmr()
print("engine caricata")
comp = get_compiler("native")
print("compilatore caricato")

def crea_circuito():
    '''Si crea oggetto della classe Citcuit.
    Poi si devono allocare i qubit, devono essere allocati tutti e 3, così funziona meglio.
    Sintassi strana per mettere i gate sul circuito: si usa ooperatore di C++.
    Vuole coppia: primo elemento è la porta ed il secondo è un singolo qubit o coppia di qubit coinvolti.
    Poi si restituisce come il risultato il circuito stesso.
    '''
    circ = Circuit()
    q = circ.allocateQubits(3)
    #circ << (X, q[1])
    circ << (H, q[0])
    circ << (CX, (q[0], q[1]))
    circ << (CX, (q[1], q[2]))
    return circ

'''E' necessario creare oggetto config, dove si devono specificare più cose.
Una di queste è il numero di shots, cioè quante volte si vuole ripetere il circuito (in qiskit 1024 standard).
Si va a configurare l'IP, indirizzo. Poi una porta con cui si comunica.
Poi si crea l'account con due argomenti: login e password.
'''
config = NMRConfig()
config.configure_shots(1024)
config.configure_ip("spinq.fisgeo.unipg.it")
config.configure_port(55444)
config.configure_account("student", "student")
    
'''Esecuzione divisa in due parti.
Nella prima parte si passa il nome del task, dove poi si ha la descrizione completa del task.
Nella seconda parte si compila: si prende il circuito e poi lo si deve tradurre nelle porte supportato in effetti dal triangulum:
circuito tradotto in una forma eseguibile dalla macchina.
Poi engine è quello che comunica con la macchina, a cui viene passato l'eseguibile.
Quando ha finito, si ottiene probabilities: divide i conteggi per i numeri di shot, frequenza relativa.
Poi fa un print con un ciclo for
'''
def esegui(circ, nome_task="prova"):
    config.configure_task(nome_task, nome_task)
    exe = comp.compile(circ, 0)
    print("circuito compilato, ora lancio il job")
    result = engine.execute(exe, config)
    print("job finito, ecco i risultati ")
    m=result.probabilities
    for k in m.keys():
    	print(k, m[k])
    return result

'''Si noti che vuole una versione specifica di Python, la console da usare è la spinquit'''




#Creo il circuito
qc=crea_circuito()
#Guardo il circuito
qc.instructions



#Non so cosa sta facendo... Niente, non importa, non vediamo come è fatto il circuito compilato :/
exe=comp.compile(qc,0)
dir(exe)



#Pronti per eseguirlo
res=esegui(qc)

'''Pronostico: il risultato che deve avere la macchina: ho con pari probabilità 1/2 sia |000> che |111>.
Le macchine sono affette da rumore quindi: 50% e 49% va bene come simulazione.
'''



#ESERCIZIO7:Deutsch su Triangulum



#ProvaIO
#ESERCIZIO7
from spinqit import get_nmr, get_compiler, Circuit, NMRConfig
from spinqit import H, CX, X

engine = get_nmr()
print("engine caricata")
comp = get_compiler("native")
print("compilatore caricato")

def oracolo(a, circ, q):
    if a==0:
        pass
    elif a==1:
        circ << (CX, (q[0], q[1]))
    elif a==2:
        circ << (CX, (q[0], q[1]))
        circ << (X, q[1])
    elif a==3:
        circ << (X, q[1])

def alg_deutsch(a):
    circ = Circuit()
    q = circ.allocateQubits(3)
    circ << (H, q[0])
    circ << (X, q[1])
    circ << (H, q[1])
    oracolo(a, circ, q)
    circ << (H, q[0])
    return circ


config = NMRConfig()
config.configure_shots(1024)
config.configure_ip("spinq.fisgeo.unipg.it")
config.configure_port(55444)
config.configure_account("student", "student")
    
def esegui(circ, nome_task="prova"):
    config.configure_task(nome_task, nome_task)
    exe = comp.compile(circ, 0)
    print("circuito compilato, ora lancio il job")
    result = engine.execute(exe, config)
    print("job finito, ecco i risultati ")
    m=result.probabilities
    for k in m.keys():
    	print(k, m[k])
    return result




qc1=alg_deutsch(0)
qc1.instructions
res=esegui(qc1)




#Prova ma è sbagliato
#ESERCIZIO8: Grover su Triangulum
from spinqit import get_nmr, get_compiler, Circuit, NMRConfig
from spinqit import H, CX, X, MCP, MCX

engine = get_nmr()
print("engine caricata")
comp = get_compiler("native")
print("compilatore caricato")

n=3

def oracle(circ, w, q):
    n=3
    for i in range(n):
        if w[i]=='0':
            circ << (X, q[n-1-i])
    circ << (MCP, (np.pi, list(range(0,n-1)),n-1)) #questa scrittura è sbagliata sicuro pt1
    for i in range(n):
        if w[i]=='0':
            circ << (X, q[n-1-i])


def diffusion(circ, q):
    n=3
    for i in range(n):
        circ<< (H, q[i])
    for i in range(n):
        circ << (X, q[i])
    circ << (H, q[n-1])
    circ << (MCX, (list(range(0,n-1)),n-1)) #questa scrittura è sbagliata sicuro pt2
    circ << (H, q[n-1])
    for i in range(n):
        circ << (X, q[i])
    for i in range(n):
        circ << (H, q[i])
   
def grover(w, t):
    n=3
    circ=Circuit()
    q = circ.allocateQubits(3)
    for i in range(n):
        circ << (H, q[i])
    for i in range(t):
        oracle(circ, w, q)
        diffusion(circ, q)
    return circ


config = NMRConfig()
config.configure_shots(1024)
config.configure_ip("spinq.fisgeo.unipg.it")
config.configure_port(55444)
config.configure_account("student", "student")
    
def esegui(circ, nome_task="Grover"):
    config.configure_task(nome_task, nome_task)
    exe = comp.compile(circ, 0)
    print("circuito compilato, ora lancio il job")
    result = engine.execute(exe, config)
    print("job finito, ecco i risultati ")
    m=result.probabilities
    for k in m.keys():
    	print(k, m[k])
    return result


def ottimo(n):
    return np.floor(np.pi*np.sqrt(2**n)/4)


#ESERCIZIO9: Simulator MATRIX PRODUCT STATE invece che StatevectorSimulator
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from qiskit_aer import AerSimulator
#Simulatore molto più efficiente di qiskit normale

qc=QuantumCircuit(200,200)
sim=AerSimulator()
qc.h(0)
for i in range(199):
    qc.cx(i,i+1)

qc.measure(range(0,200),range(0,200))
time res=sim.run(qc, method='matrix_product_state').result()
'''Ci mette 20 secondi, 1/3 del tempo di spinqit a 3 soli qubit.
Ci sta che ci mette del tempo la macchina reale.
Qui il circuito crea un entanglement gigantesco, però alla fine lo stato finale
è relativamente semplice: dovrei vedere cosa succede se aumento la complessità
dello stato. Un esempio che si potrebbe fare è sperimentare con VQE.
