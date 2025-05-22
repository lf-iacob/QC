from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler




#ESERCIZIO1


qc=QuantumCircuit(2,2)
qc.h(0)
qc.cx(0,1)
qc.draw()
qc.measure([0,1],[0,1])
qc.draw()


sim=StatevectorSampler()
job=sim.run([qc])
res=job.result()[0]
res
counts=res.data.c.get_counts()
counts



#ESERCIZIO2

def crea_circuito():
    qc=QuantumCircuit(3,3)
    qc.x(1)
    qc.h(0)
    qc.cx(0,1)
    qc.cx(0,2)
    qc.measure([0,1,2],[0,1,2])
    return qc

qc2=crea_circuito()




s=Statevector.from_label("000")
s
s=s.evolve(qc2)
s
qc2.measure([0,1,2], [0,1,2])
qc2.draw()




job=sim.run([qc2])
res=job.result()[0]
counts=res.data.c.get_counts()
counts



#ESERCIZIO3

def oracolo(a, qc):
    if a==0:
        pass
    elif a==1:
        qc.cx(0,1)
    elif a==2:
        qc.cx(0,1)
        qc.x(1)
    elif a==3:
        qc.x(1)

def controlla():
    #controlla che effettivamente funziona l'oracolo come ci aspettiamo
    for k in range(0,4):
        for x in range(0,2):
            if x==0:
                s=Statevector.from_label("00")
            else:
                s=Statevector-from_label("01")
            qc=QuantumCircuit(2)
            oracolo(a,qc)
            s1=s.evolve(qc)
            print(a, s.to_dict(), s1-to_dict())

def deutsch(a):
    qc=QuantumCircuit(2,1)
    qc.h(0)
    qc.x(1)
    qc.h(1)
    oracolo(a,qc)
    qc.h(0)
    qc.measure(0,0)
    return qc


def simula(qc, sim):
    job=sim.run([qc])
    res=job.results()[0]
    return res.data.c.get_counts()
  



#ESERCIZIO4

qc4=QuantumCircuit(1,1)
import numpy as np
theta=30*np.pi/180
qc4.ry(theta,0)
qc4.measure(0,0)
simula(qc4, sim)


def teletrasporto(theta):
    qc=QuantumCircuit(3,2)
    qc.ry(theta, 0)
    qc.h(1)
    qc.cx(1,2)
    qc.cx(0,1)
    qc.h(0)
    qc.measure([0,1],[0,1])
#non ci sono le misure condizionate, da aggiungere nella versione successiva



#VERSIONE AGGIORNATA con le misure condizionate
from qiskit import QuantumRegister, ClassicalRegister
from qiskit_aer import StatevectorSimulator

def teletrasporto(theta):
    c=ClassicalRegister(3)
    q=QuantumRegister(3)
    qc=QuantumCircuit(3,c)
    qc.ry(theta, q[0])
    qc.h(q[1])
    qc.cx(q[1],q[2])
    qc.cx(q[0],q[1])
    qc.h(q[0])
    qc.measure(q[0], c[0])
    qc.measure(q[1], c[1])
    with qc.if_test((c[1],q[1])):
        qc.z(q[2])
    qc.measure(q[2], c[2])

"""NON FUNZIONA: LASCIATO PER LA PROSSIMA VOLTA
Si tratta di un circuito dinamico,
un protocollo in cui dovrebbero essere degli if,
ma ancora non può essere inserito al momento,
quindi dovrebbero essere fatti step successivi particolari"""




"""Prova a fare Deutsch-Josza e poi la QFT.
La QFT non si misura perchè produce uno stato di interesse.
Provare a vedere se viene riprodotto lo stato
in base al segnale in ingresso.
Si possono provare a fare degli esercizi sugli
algoritmi di tipo NISQ, come VQE o QAOA (questo
lo abbiamo studiato con MaxCut, ma si potrebbero
fare altri problemi: lì si dovrebbe studiare
l'hamiltoniana del problema specifico).
QML lo abbiamo visto nello specifico su Iris,
ci sono altre situazioni testabili, es. circuito
quantistico che distingue numeri scritti a mano (problema
qui è che si hanno delle immagini da caricare,
ma devono esserne ridotte le dimensioni tipo a 4 pixerl)."
