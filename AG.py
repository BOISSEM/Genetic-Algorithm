from decimal import *
from math import *
from random import *
from pylab import *



#Given two points A and B in a vertical plane,
# assign a path AMB to the moving body M,
#along which the body will arrive to point B,
#falling by its own gravity and beginning from A, in the least time.


#fonction de calculs

def angleteta(liste): #cette fonction calcule les angles tetai. elle demande la liste des genes d un individu.
    tetai = []
    for i in range (1, len(liste)):
        teta = atan((liste[i - 1] - liste[i])/(1/Nbindi+1)) #attention, on divise par 1/3, a modifier (voir note 2)
        tetai.append(teta)
    return(tetai)
    print("tetai = ",tetai)


def vitesse(liste): #Ici, on va, a partir de la liste des gene d un individu, obtenir la liste des vitesses.
    vi = [0]
    g = 9.81 #on peut changer la gravite, ici.
    for i in range (1 , len(liste)):
        v = sqrt((2*g*(liste[i - 1] - liste[i]))+(vi[i - 1]**2))
        vi.append(v)
    return(vi)
    print("vi = ",vi)

def tempsetape(liste1 , liste2): #on trouve le temps d une etape avec la liste des angles (liste1) et des vitesses (liste2) d un individu
    ti = []
    g = 9.81
    for i in range (1 , len(liste2)):#a noter que liste2 a une valeur de plus que liste1 
        deltat = ((liste2[i] - liste2[i - 1])*(1/(g * sin(liste1[i - 1]))))
        ti.append(deltat)
    return(ti)
    print("ti = ",ti)

def tempsindi(liste): #avec la liste des temps etape, on va trouver le temps de parcours d un individu
    T = 0
    for i in range (0,len(liste)):
        T = T + liste[i]
    return(T)
    print("le temps de parcours est de ", T," secondes")



def elimination(liste1 , liste2): #on elimine les deux moins bon a partir de la liste des temps et de la liste des individus
    Max = 0
    q = 0
    for i in range (0 , len(liste1)):#on recherche le moins bon individu
        #print(liste1,i)
        if liste1[i] > Max:
            Max = liste1[i]
            q = i
    del liste1[q]
    del liste2[q]
    Max = 0
    q = 0
    for i in range ( 0 , len(liste1)):#le deuxieme moins bon individu 
        #print(liste1,i)
        if liste1[i] > Max:
            Max = liste1[i]
            q = i
    del liste1[q]
    del liste2[q]
    return(liste1 , liste2)


def tempstotal(liste): #les temps de parcours a partir de la liste principale des individus et de toutes les autres fonctionc
    tetai = []
    vi = []
    ti = []
    tempsfinal = []
    for r in range(0,len(liste)):#on applique les fonctions de calcul une par une
        teta = angleteta(liste[r])
        tetai.append(teta)
        v = vitesse(liste[r])
        vi.append(v)
        t = tempsetape(tetai[r],vi[r])
        ti.append(t)
        T = tempsindi(ti[r])
        tempsfinal.append(T)
    return(tempsfinal)

def trace(liste, n):#fonction trace de courbe 
    gene = []#les abscisses 
    for i in range (0 , n + 2):
        gene.append(i)
    x = array(gene)
    y = array(liste)#les ordonnees

    plot(x,y)
    show()

def trace2(liste1 , liste2):#trace de la courbe grace a l individu et ces points(gene)
    x = array(liste2)
    y = array(liste1)

    plot(x,y)
    show()
              
def lissage (liste,liste2): #va permettre de lisser la courbe a partir d un individu et des points qu on lui rajoute. 
    for i in range(0,len(liste)-1): # le -1 est pour pas sortir de la liste. 
        m = (liste[i] + liste[i+1])/2
        liste2.append(m)
        liste2.append(0)#on rajoute des 0 pour apres 
    return (liste2)

nbexperience = 1 
M = [] #liste des meilleurs individus 

for r in range (0 , nbexperience):

    #initialisation
    Nbindi = 50
    Nbgene = 12
    #creation des Nbindi individus (pour deux genes)
    L = []
    for i in range (0 , Nbindi):
        i = []
        L.append(i)
    #print(L)

    #remplissage des listes individus (genes)
    for r in range(0,len(L)):#on remplie toutes les listes
        for i in range(0,Nbgene):#chaque sous liste comporte deux genes (on peut prendre 0 comme 1,2,..,19)
            i = randint(-2,2)#on peut descendre plus bas que 0
            i = i + random()#Mais on ne peut pas descendre plus bas que -1
            L[r].append(i)
    #print("                               ", L)

    #on rajoute en queu de liste le point de depart (A=3) et d arrivee (B=0)
    for r in range (0,len(L)):
        L[r].insert(0,3) #ajout en debut de liste de la coordonnee du point A
        L[r].insert(len(L[r]),0) #ajout en fin de liste de la coordonnee du point B

    #print("                                ",L)       


    #Creation des fils et remplissage de leurs genes
    # on sait deja qu il partent de 3..




    Nbgeneration = 25000
    nbmutation = 0

    for i in range (0 , Nbgeneration):

        Fils1 = []
        Fils2 = []

        #methode du croisement multi point

        #selection des 4 parents (2 par fils)

        a = randint(0,len(L)-1) #L[len(L)] n existe pas ! donc -1
        b = randint(0,len(L)-1)
        c = randint(0,len(L)-1)
        d = randint(0,len(L)-1)

        alea = [a,b,c,d] #liste du rang des parents 

        #print("voici les 4 parents : " ,L[a] , L[b] , L[c] , L[d])

        #fils 1

        p = randint(0,len(L[a])) #on prend un point au hasard dans les genes du parents (on coupe en deux)
        #print(p)
        if p == 0:
            p = p + 1 #on evite le cas ou p = 0 car ca gene pour la liste en dessous

        for i in range(0 , p):#premiere partie du fils1 remplie par une partie de taille [0,p] du parents a
            i = L[a][i]
            Fils1.append(i) #on apporte a fils1 les p premiers genes du parents
        
     
        for i in range (p , len(L[b]) ):#l autre partie de taille [p,len(L[b])] est remplie par les genes du parents b
            i = L[b][i]
            Fils1.append(i)
        
        #print(Fils1)

        #on fait la meme chose mais avec les autres valeurs de c et d

        q = randint(0, len(L[c]))
        #print(q)
        
        if q == 0 :
            q = q + 1
        
        for i in range(0, q):
            i = L[c][i]
            Fils2.append(i)

        for i in range(q , len(L[d])):
            i = L[d][i]
            Fils2.append(i)

        #print(Fils2)

        #mutation fils1
        #va compter le nombre de mutation
        
        #print(list(Fils1))

        q = random() #mutation aleatoire
        #print(q)
        
        if q < 0.1 :
            nbmutation = nbmutation + 1
            a = randint(1, len(Fils1)-1)
            #print(a)
            Fils1[a] = randint(-2 , 2) + random()

        #print(Fils1[a])
        #print(Fils1)

        #mutation fils2
        
        #print(list(Fils2))

        p = random()
        #print(p)

        if p > 0.9 : #mutation rare 
            nbmutation = nbmutation + 1
            a = randint(1 , len(Fils2)-1)
            #print(a)
            Fils2[a] = randint(-2 , 2) + random()

        #print(Fils2[a])
        #print(Fils2)

        #on replace les 2 nouveaus fils dans la population initiale

        L.append(Fils1)
        L.append(Fils2)

        #print(L)

        G = tempstotal(L) #calcul des temps de la population
        #print(G)
        #print(len(G))

        elimination(G,L) #on elimine les deux moins bons
        

    #print("voici la derniere population trouvee : ",L)

    #selection du meilleur

    Min = 1000
    p = 0
    for i in range (0 , len(G)):
        if G[i] < Min:
            Min = G[i]
            p = i
    #print("le meilleur individu est :", L[p])

    #print("il y a eu dans cette experience: ", nbmutation, "mutation pour ", Nbgeneration , " generation.")
    #trace de la courbe

    #trace(L[p], Nbgene)

    M.append(L[p])

    #print(M)
        

G = tempstotal(M)#calcul du temps de la liste des meilleurs. 

Min = 1000
p = 0
for i in range (0 , len(G)):
    if G[i] < Min:
        Min = G[i]
        p = i
print("le meilleur des meilleurs est: ", M[p])
print(G[p])

trace(M[p], Nbgene)


"""precision = 5

for r in range(0 , precision):
    nouveaupoint = [] #liste des nouveaux points que l on va rajouter.

    lissage(M[p], nouveaupoint)

    for i in range (0 , len(nouveaupoint),2):#un pas de 2 pour placer les nouvelles valeurs entre chaque ancien point
        #Ce pas de deux explique pourqioi on voulais rajouter des 0 une fois sur deux, pour pas perdre de valeurs. 
        q = nouveaupoint[i]
        M[p].insert(i+1,q)
    print(M[p])
    print(len(M[p]))
        
    
    gene = []
    for i in range (0 , len(M[p])): #generaliser pour tout le programme (c est fait pour une precision de 1)
        n = i * (Nbgene / len(M[p]))
        gene.append(n)
    #print(gene)
    #print(len(gene))
    #print(M[p])
    #print(len(M[p]))

trace2(M[p],gene)

#trace(M[p],len(M[p])-2)

#print(M[p])
#print(len(M[p]))
    

L = []    
for i in range ( 0 , 2): #creation d une population de deux individus tres performant.
    L.append(M[p])

print(L)

M = [] #liste des meilleurs individus 

for r in range (0 , nbexperience):

    Nbgeneration = 10000
    nbmutation = 0

    for i in range (0 , Nbgeneration):

        Fils1 = []
        Fils2 = []

        #methode du croisement multi point

        #selection des 4 parents (2 par fils)

        a = randint(0,len(L)-1) #L[len(L)] n existe pas ! donc -1
        b = randint(0,len(L)-1)
        c = randint(0,len(L)-1)
        d = randint(0,len(L)-1)

        alea = [a,b,c,d] #liste du rang des parents 

        #print("voici les 4 parents : " ,L[a] , L[b] , L[c] , L[d])

        #fils 1

        p = randint(0,len(L[a])) #on prend un point au hasard dans les genes du parents (on coupe en deux)
        #print(p)
        if p == 0:
            p = p + 1 #on evite le cas ou p = 0 car ca gene pour la liste en dessous

        for i in range(0 , p):#premiere partie du fils1 remplie par une partie de taille [0,p] du parents a
            i = L[a][i]
            Fils1.append(i) #on apporte a fils1 les p premiers genes du parents
        
     
        for i in range (p , len(L[b]) ):#l autre partie de taille [p,len(L[b])] est remplie par les genes du parents b
            i = L[b][i]
            Fils1.append(i)
        
        #print(Fils1)

        #on fait la meme chose mais avec les autres valeurs de c et d

        q = randint(0, len(L[c]))
        #print(q)
        
        if q == 0 :
            q = q + 1
        
        for i in range(0, q):
            i = L[c][i]
            Fils2.append(i)

        for i in range(q , len(L[d])):
            i = L[d][i]
            Fils2.append(i)

        #print(Fils2)

        #mutation fils1
        #va compter le nombre de mutation
        
        #print(list(Fils1))

        q = random() #mutation aleatoire
        #print(q)
        
        if q < 0.01 :
            nbmutation = nbmutation + 1
            a = randint(1, len(Fils1)-1)
            #print(a)
            Fils1[a] = randint(-2 , 2) + random()

        #print(Fils1[a])
        #print(Fils1)

        #mutation fils2
        
        #print(list(Fils2))

        p = random()
        #print(p)

        if p > 0.09 : #mutation rare 
            nbmutation = nbmutation + 1
            a = randint(1 , len(Fils2)-1)
            #print(a)
            Fils2[a] = randint(-2 , 2) + random()

        #print(Fils2[a])
        #print(Fils2)

        #on replace les 2 nouveaus fils dans la population initiale

        L.append(Fils1)
        L.append(Fils2)

        #print(L)

        G = tempstotal(L) #calcul des temps de la population
        #print(G)
        #print(len(G))

        elimination(G,L) #on elimine les deux moins bons
        

    #print("voici la derniere population trouvee : ",L)

    #selection du meilleur

    Min = 1000
    p = 0
    for i in range (0 , len(G)):
        if G[i] < Min:
            Min = G[i]
            p = i
    #print("le meilleur individu est :", L[p])

    #print("il y a eu dans cette experience: ", nbmutation, "mutation pour ", Nbgeneration , " generation.")
    #trace de la courbe

    #trace(L[p], Nbgene)

    M.append(L[p])

    print(M)
        

G = tempstotal(M)#calcul du temps de la liste des meilleurs. 

Min = 1000
p = 0
for i in range (0 , len(G)):
    if G[i] < Min:
        Min = G[i]
        p = i
print("le meilleur des meilleurs est: ", M[p])

#print(len(M[p]))

trace(M[p], len(M[p])-2)"""

    
