# -*- coding: utf-8 -*-

from pylab import *
import random
import bibliotheque as bib

close('all')

"""
But : montrer aux étudiants comment se passe le traitement des incertitudes en 
simulant des processus de mesures via la génération de nombres aléatoires.
Le but est que les graphs s'incrémentent en temps réel au fil des tirages.

Améliorations :
- animer la partie sur la régression linéaire : un graph s'affiche avec les
  premières "valeurs mesurées" (premier tirage) et affiche la régression avec
  son résultat puis un deuxième tirage a lieu la courbe s'affiche aussi
- faire en sorte que les histogrammes des "mesures" et de a,b,et chi_sq 
  s'affichent un par un.
"""

################################################################################
# 1 - Répétition d'une mesure :
################################################################################
"""
But : montrer aux étudiants le fait que plus on fait de mesures, moins la 
moyenne a de chances de s'écarter de la valeur vraie.

Méthode : on réalise un tirage de n nombres selon une loi de probabilité
gaussienne de moyenne m et d'écart-type s. On trace l'histogramme des valeurs et
l'évolution de la moyenne en fonction de k, nombre de mesures déjà effectuées.
"""
n=1000
m=10.
s=1.

mesures=[] # contient les mesures
moyennes=[] # contient les moyennes sur les mesures
k=bib.next_puissance_de_2(sqrt(n)) # nombre de cases pour l'histogramme
# définition axes des abscisses
x_min=m-5*s
x_max=m+5*s
x=linspace(x_min,x_max,k)
dx=(x_max-x_min)/(k-1)
fig=figure(u"Répétition d'une mesure")
histo_subplot = fig.add_subplot(1,2,1)
moyenne_subplot = fig.add_subplot(1,2,2)
h=zeros(len(x)) #histogramme vide au départ
suite=bib.suite_constructeur(n)
for i in range(1,n+1):
    mesure=random.gauss(m,s) # on fait une nouvelle mesure
    h=bib.incremente_histo(x,mesure,h)
    mesures.append(mesure)
    moyenne=mean(mesures)
    moyennes.append(moyenne)
    if i in suite :
        print float(i)/n*100.,'%'
        
        histo_subplot.cla()
        histo_subplot.set_xlim([x_min,x_max])
        histo_titre='Histogramme des mesures\nnombre de tirages = {}'
        histo_titre=histo_titre.format(i)
        histo_subplot.set_title(histo_titre)
        histo_subplot.bar(x,h,dx)
        
        moyenne_subplot.cla()
        #moyenne_subplot.set_xlim([0,n])
        moyenne_subplot.plot(moyennes)
        moyenne_titre='Moyenne en fonction du nombre de tirages\n'
        moyenne_titre+='nombre de tirages = {}'
        moyenne_titre=moyenne_titre.format(i)
        moyenne_subplot.set_title(moyenne_titre)
        
        pause(0.1) # pour laisser le temps aux graphs de se construire
        if i==10 : raw_input('Pause') # pour pouvoir donner explications

raw_input('On passe à la suite ?')
################################################################################
# 2 - Distribution de la moyenne
################################################################################
"""
But : montrer que l'écart-type sur la moyenne est plus faible que l'écart-type
sur les mesures individuelles.

Méthode : on répète le processus précédent (sans tracer les graphs) N fois.
On observe l'histogramme des moyennes. On calcul la moyenne des moyennes 
et l'écart type des moyennes. On vérifie que s_m=s/sqrt(n).

Rq : on peut aussi utiliser une loi de probabilité non gaussienne pour le
processus de mesure et concstater que la moyenne est toujours distribuée selon
un truc qui ressemble à une gaussienne.
"""

n=1000
N=1000
moyennes=[]
k=bib.next_puissance_de_2(sqrt(n)) # nombre de cases pour l'histogramme
# définition axes des abscisses
x_min_mesures=m-5.*s
x_max_mesures=m+5.*s
x_mesures=linspace(x_min_mesures,x_max_mesures,k)
x_min_moyenne=m-5.*s/k
x_max_moyenne=m+5.*s/k
x_moyenne=linspace(x_min_moyenne,x_max_moyenne,k)
dx_mesures=(x_max_mesures-x_min_mesures)/(k-1)
dx_moyenne=(x_max_moyenne-x_min_moyenne)/(k-1)
h_moyenne=zeros(len(x_moyenne))
h_mesures=zeros(len(x_mesures))
fig=figure(u"Distribution de la moyenne")
histo_mesure_subplot = fig.add_subplot(2,2,1)
histo_moyenne_subplot = fig.add_subplot(2,2,2)
histo_mesures_subplot = fig.add_subplot(2,2,3)
histo_moyenne_zoom_subplot = fig.add_subplot(2,2,4)

suite=bib.suite_constructeur(N)
for i in range(1,N+1) :
    mesure=normal(m,s,(n,))
    h_mesure=zeros(len(x_mesures))
    moyenne=mean(mesure)
    moyennes.append(moyenne)
    h_moyenne=bib.incremente_histo(x_moyenne,moyenne,h_moyenne)
    for elmt in mesure :
        h_mesure=bib.incremente_histo(x_mesures,elmt,h_mesure)
        h_mesures=h_mesures+h_mesure
    if i in suite :
        print float(i)/N*100.,'%'
        limits=[x_min_mesures,x_max_mesures]
        titre = 'Histogramme des mesures\nnombre de mesures = {}'.format(n)
        bib.subplot_histo(histo_mesure_subplot,limits,titre,x_mesures,h_mesure,
                      dx_mesures)
        titre = 'Histogramme des mesures cumulees\nnombre de mesures = {}'
        titre=titre.format(i*n)
        bib.subplot_histo(histo_mesures_subplot,limits,titre,x_mesures,h_mesures,
                    dx_mesures)
        
        limits=[x_min_mesures,x_max_mesures]
        titre = 'Histogramme des moyennes\nnombre de moyennes = {}'.format(i)
        bib.subplot_histo(histo_moyenne_subplot,limits,titre,x_moyenne,h_moyenne,
                    dx_moyenne)
        limits=[x_min_moyenne,x_max_moyenne]
        titre = 'Histogramme des moyennes - Zoom\nnombre de moyennes = {}'
        titre=titre.format(i)
        bib.subplot_histo(histo_moyenne_zoom_subplot,limits,titre,x_moyenne,
                    h_moyenne,dx_moyenne)
        
        pause(0.1) # pour laisser le temps aux graphs de se construire
        if i==10 : raw_input('Pause') # pour pouvoir donner explications


"""
Avant de passer à la suite, il faut insister sur le fait que si je refais une
mesure individuelle : l'incertitude est sigma.
Si je refais n mesures et que je prends la moyenne : l'incertitude est
sigma/sqrt(n).
"""

print 'Ecart-type sur {0} mesures = {1}'.format(n,std(mesures))
print 'Ecart-type sur {0} moyennes = {1}'.format(N,std(moyennes))
print 'Ecart_type/racine(N) = {}'.format(std(mesures)/sqrt(N))

raw_input('On passe à la suite ?')
################################################################################
# 3 - Ajustement de données, cas de la régression linéaire
################################################################################
"""
But : Montrer aux étudiants le lien entre les incertitudes sur les points 
de mesure et les incertitudes sur les paramètres.

Méthode : on définit un modèle (fonction linéaire de coefficient directeur a
et d'ordonée à l'origine b). On tire aléatoirement n points régulièrement
espacés sur l'ensemble de définition choisi et on calcule les paramètres de
l'ajustement en tenant compte des barres d'erreur.
On répète ce processus N fois en conservant les mêmes paramètres (en
particulier les incertitudes sur chaque point de mesure) et on étudie la
distribution des valeurs des paramètres. On doit constater que les incertitudes
sorties par les formules donnent bien l'écart-type de la distribution.

Idée : choisir n =(le nombre d'étudiants - 2) et laisser les étudiants choisir
les valeurs de a et b et des incertitudes sur les points de mesure 
"""
a=3.
b=1.
print 'On a choisi : a = {} et b = {}'.format(a,b)
n=10
N=100000 # nombre "d'opérations de mesures" 

def f(x,a,b):
    return a*x+b

x_min=0.
x_max=10.
x=linspace(x_min,x_max,n)
dy=[.1,.3,.5,.2,.5,.1,.1,.4,.2,.3]
y=[]
a_estime=[]
b_estime=[]
da=[]
db=[]
chisq_red=[]
fig_mesures=figure(u'Quelques opérations de mesures et ajustements')
ax_mesures=fig_mesures.add_subplot(1,1,1)
for i in range(N) :
    y.append([random.gauss(f(val,a,b),s) for val,s in zip(x,dy)])
    aa,daa,bb,dbb,chisqchisq,chisq_redchisq_red=bib.reg_lin(x,y[i],dy)
    a_estime.append(aa)
    b_estime.append(bb)
    da.append(daa)
    db.append(dbb)
    chisq_red.append(chisq_redchisq_red)
    if i in [0,1] :
        ax_mesures.errorbar(x,y[i],dy,fmt='+')
        pause(0.1) 
        raw_input('Pause') # pour explications  
        ax_mesures.plot([x_min,x_max],[f(x_min,aa,bb),f(x_max,aa,bb)])
        pause(0.1) 
        raw_input('Pause') # pour explications  
    if (i%(N/100))==0 : print float(i)/float(N)*100,'%'   
y=array(y)
a_estime=array(a_estime)
b_estime=array(b_estime)
da=array(da)
db=array(db)
chisq_red=array(chisq_red)

# Histogramme des valeurs "mesurées" au bout des N "opérations de mesures"
fig_histo_mesures=figure('histogrammes pour chacun des points')
ax_histo_mesures = fig_histo_mesures.add_subplot(1,1,1)
for i in range(n):
    bib.histogramme(y[:,i],ax_histo_mesures,N,clear=False)
pause(0.1) 
raw_input('Pause') # pour explications

# Histogramme des N valeurs de a obtenues :
fig_a_estime=figure('histogramme des valeurs de a')
ax_a_estime = fig_a_estime.add_subplot(1,1,1)
bib.histogramme(a_estime,ax_a_estime,N)
pause(0.1) 
raw_input('Pause') # pour explications  

# Histogramme des N valeurs de da obtenues : (inutile)
#fig_da_estime=figure('histogramme des valeurs de da')
#ax_da_estime = fig_da_estime.add_subplot(1,1,1)
#bib.histogramme(da,ax_da_estime,N)

# Histogramme des N valeurs de b obtenues :
fig_b_estime=figure('histogramme des valeurs de b')
ax_b_estime = fig_b_estime.add_subplot(1,1,1)
bib.histogramme(b_estime,ax_b_estime,N)
pause(0.1) 
raw_input('Pause') # pour explications

# Histogramme des N valeurs de db obtenues : (inutile)
#fig_db_estime=figure('histogramme des valeurs de db')
#ax_db_estime = fig_db_estime.add_subplot(1,1,1)
#bib.histogramme(db,ax_db_estime,N)

# Histogramme des N valeurs de chi carre réduit obtenues :
fig_chi_sq_red=figure(u'histogramme des valeurs de chi carre réduit')
ax_chis_sq_red = fig_chi_sq_red.add_subplot(1,1,1)
bib.histogramme(chisq_red,ax_chis_sq_red,N)
pause(0.1)
                                            
print 'ecart-type de a :',std(a_estime)
print 'moyenne de da :',mean(da)
print 'occurence au hasard de da :',random.choice(da)
print '\n\n\n'
print 'ecart-type de b :',std(b_estime)
print 'moyenne de db :',mean(db)
print 'occurence au hasard de db :',random.choice(db)

################################################################################
# Conclusion : 
################################################################################
"""
TOUS les processus aléatoires choisis ici sont gaussiens. Les formules apprises
en cours marchent très bien dans ce cas. Si les processus ne sont pas gaussiens,
certains des résultats tiennent, d'autres non, mais en pratique ça mache pas 
mal même si les processus ne sont pas tout à fait gaussiens.
Rq : à tester avec des processus non gaussiens.
""" 