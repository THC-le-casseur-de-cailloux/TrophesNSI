import tkinter as tk
from graphs.SEIR_model import data
import pandas as pd


def action(mainapp,l):
    #Création du bandeau 
    actframe = tk.Frame(mainapp, bg="white")
    actframe.grid(row=3,column=1,sticky="nsew",pady=(0,0.009*l),padx=(0.009*l))

    ######################################################################################################      
    depister = tk.Frame(actframe)
    depister.configure(highlightbackground="black", highlightthickness=1, highlightcolor="black",bg="#202020")
    depister.grid(row=0, column=0,sticky="nsew")


    txtdepister = tk.Label(depister, text="Mesures de dépistage", bg="#202020", font=("Helvetica Neue", 15,"underline"), fg="white",width=45)
    txtdepister.grid(row=0, column=0,padx=10,pady=10)
    data = pd.read_csv("graphs/data.csv",sep=";")
    tests=tk.IntVar()
    isolmt=tk.IntVar()
    rchrch_contacts=tk.IntVar()
    quarantaine=tk.IntVar()
    isolated=False
    confin=False
    checktests = tk.Checkbutton(depister, text=" Mise en place de tests Covid à grande échelle", fg="white",variable=tests,bg="#202020",command=lambda: depistage() if tests.get() else arretdepistage())
    checktests.grid(row=1, column=0,sticky=tk.W,padx=10,pady=12)
    checkisolmt = tk.Checkbutton(depister, text=" Isolement des personnes positives aux tests", fg="white",variable=isolmt,bg="#202020",command=lambda: isolement() if isolmt.get() and tests.get() else arretisolement(isolated))
    checkisolmt.grid(row=2, column=0,sticky=tk.W,padx=10,pady=12)
    checkcontacts = tk.Checkbutton(depister, text=" Recherche des cas contacts de personnes positives",fg="white", variable=rchrch_contacts,bg="#202020")
    checkcontacts.grid(row=3, column=0,sticky=tk.W,padx=10,pady=12)
    checkquarantaine= tk.Checkbutton(depister, text=" Mise en quarantaine des cas et cas contacts",fg="white", variable=quarantaine,bg="#202020",command=lambda: contagion() if quarantaine.get() and rchrch_contacts.get() else lowcontagion(confin))
    checkquarantaine.grid(row=4, column=0,sticky=tk.W,padx=10,pady=(10,20))

    ######################################################################################################      
    redctct = tk.Frame(actframe)
    redctct.configure(highlightbackground="black", highlightthickness=1, highlightcolor="black",bg="#202020")
    redctct.grid(row=1, column=0, sticky="nsew")

    txtdredctct= tk.Label(redctct, text="Mesures de réduction des contacts / confinement", bg="#202020", font=("Helvetica Neue", 15,"underline"), fg="white",width=47)
    txtdredctct.grid(row=0, column=0,padx=10,pady=10)
    
    mask=tk.IntVar()
    gstbarr=tk.IntVar()
    close=tk.IntVar()
    limit_sorties=tk.IntVar()

    checkmask = tk.Checkbutton(redctct, text=" Obligation du port du masque dans les espaces publics", fg="white",variable=mask,bg="#202020",command=lambda: contagion() if mask.get() else lowcontagion(confin))
    checkmask.grid(row=1, column=0,sticky=tk.W,padx=10,pady=12)
    checkgstbarr = tk.Checkbutton(redctct, text=" Sensibilisation aux gestes barrières", fg="white",variable=gstbarr,bg="#202020",command=lambda: contagion() if gstbarr.get() else lowcontagion(confin))
    checkgstbarr.grid(row=2, column=0,sticky=tk.W,padx=10,pady=12)
    checkclose = tk.Checkbutton(redctct, text=" Fermeture des espaces publics et télétravail", fg="white",variable=close,bg="#202020",command=lambda: contagion() if close.get() else lowcontagion(confin))
    checkclose.grid(row=3, column=0,sticky=tk.W,padx=10,pady=12)
    checklimit_sorties= tk.Checkbutton(redctct, text=" Limitation des sorties non indispensables", fg="white",variable=limit_sorties,bg="#202020",command=lambda: contagion() if limit_sorties.get() else lowcontagion(confin))
    checklimit_sorties.grid(row=4, column=0,sticky=tk.W,padx=10,pady=(10,20))



"""
On considère que la mise en place de tests Covid n'a pas d'impact direct sur les paramètres du modèle.
C'est les décisions qui sont permises par ces tests comme l'isolement des personnes positives qui font évoluer les coefficients'
Ainsi, l'isolement des positifs modifie :

- réduire de 15% μ car détecter qu'un malade est atteint du covid permet de le soigner en conséquence et diminuer son risque de mourir
- réduire de 15% β0 et βe car les tests sont le seul moyen pour une personne n'ayant pas de symtomes de savoir qu'elle est infectée pour qu'elle prenne
  en conséquence des mesures pour se protéger et protéger les autres

Il en va de même pour la mise en place de stratégies de dépistage cette fois ci c'est tout les beta
"""
def depistage():
    data.loc[data["nom"]=="tests","val"]=1000000

def arretdepistage():
    data.loc[data["nom"]=="tests","val"]=0


def isolement():
    data.loc[data["nom"]=="μ","val"]=data.loc[data["nom"]=="μ","val"].values[0]*0.85
    data.loc[data["nom"]=="β0","val"]=data.loc[data["nom"]=="β0","val"].values[0]*0.85
    data.loc[data["nom"]=="βe","val"]=data.loc[data["nom"]=="βe","val"].values[0]*0.85
    isolated=True
    return isolated

def arretisolement(isolated):
    if  isolated == True:
        data.loc[data["nom"]=="μ","val"]=data.loc[data["nom"]=="μ","val"].values[0]/0.85
        data.loc[data["nom"]=="β0","val"]=data.loc[data["nom"]=="β0","val"].values[0]/0.85
        data.loc[data["nom"]=="βe","val"]=data.loc[data["nom"]=="βe","val"].values[0]/0.85

def contagion():
    data.loc[data["nom"]=="βe","val"]=data.loc[data["nom"]=="βe","val"].values[0]*0.85
    data.loc[data["nom"]=="β0","val"]=data.loc[data["nom"]=="β0","val"].values[0]*0.85
    data.loc[data["nom"]=="β1","val"]=data.loc[data["nom"]=="β1","val"].values[0]*0.85
    data.loc[data["nom"]=="β2","val"]=data.loc[data["nom"]=="β2","val"].values[0]*0.85
    data.loc[data["nom"]=="β3","val"]=data.loc[data["nom"]=="β3","val"].values[0]*0.85
    confin=True
    return confin

def lowcontagion(confin):
    if confin == True:
      data.loc[data["nom"]=="βe","val"]=data.loc[data["nom"]=="βe","val"].values[0]*0.85
      data.loc[data["nom"]=="β0","val"]=data.loc[data["nom"]=="β0","val"].values[0]*0.85
      data.loc[data["nom"]=="β1","val"]=data.loc[data["nom"]=="β1","val"].values[0]*0.85
      data.loc[data["nom"]=="β2","val"]=data.loc[data["nom"]=="β2","val"].values[0]*0.85
      data.loc[data["nom"]=="β3","val"]=data.loc[data["nom"]=="β3","val"].values[0]*0.85