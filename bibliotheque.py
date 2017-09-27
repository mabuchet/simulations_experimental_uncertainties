# -*- coding: utf-8 -*-

from __future__ import division
from pylab import *

################################################################################
# Fonctions pour construire les histogrammes en direct :
################################################################################
def next_puissance_de_2(n):
    """ Trouve la puissance de 2 la plus proche de n par excès."""
    x=2
    while (x<n) : x*=2
    return x

def trouve_case(x,y):
    """ Etant donné une série de valeurs ordonnées x et y une valeur comprise
    entre x_min et x_max, renvoie la valeur x[i] telle que :
    x[i]<=y<x[i+1].
    Fonctionne par dichotomie donc attention :
    len(x) doit être un multiple de 2 !!! """
    if len(x)==1 : return x[0]
    else : 
        i=len(x)/2
        if y<=x[i] : return trouve_case(array(x[:i]),y)
        if y>x[i] : return trouve_case(array(x[i:]),y)


def incremente_histo(x,y,h): 
    """ Etant donnée une série de valeurs ordonnées x, y une valeur à tester et
    h le remplissage des cases de l'histogramme des valeurs de y, incrémente
    de un la valeur de h correspondant à la case dans laquelle doit se
    trouver y."""
    indice=list(x).index(trouve_case(x,y))
    h[indice]+=1
    return h

def suite_constructeur(n,demi=True):
    """ Crée une suite d'entiers composées de nombres croissants jusqu'à n,
    d'abord d'unité en unité puis à 10, de dizaines en dizaines, puis à 100,
    de centaines en centaines et ainsi de suite """
    s=[0]
    i=1
    while (i<=n) :
        s.append(i)
        p=int(log10(i))
        if i>=10 and demi: i+=(10**p)/2
        else : i+=10**p
    return s
            
def subplot_histo(ax,limits,titre,x,h,dx):
    """ Actualise le graph de l'histogramme (x,h,dx) dans le subplot ax"""
    ax.cla()
    ax.set_xlim(limits)
    ax.set_title(titre)
    ax.bar(x,h,dx)
    return
    
def histogramme(x,ax,n_series,clear=True):
    """ Trace l'histogramme de x avec sqrt(n_series) échantillons ou 10 si ce
    ce nombre est plus petit que 10."""
    bins=max(int(sqrt(n_series)),10)
    x_hist=histogram(x,bins=bins)
    sca(ax)
    if clear : cla()
    plot(x_hist[1][:-1],x_hist[0])
    return x_hist

################################################################################
# Regression linéaire
################################################################################
def reg_lin(x,y,sigma_y):
    """ Calcule les meilleurs paramètres de la droite y=ax+b et leurs incertitudes
    en tenant compte des incertitudes sur y.
    x,y,sigma : listes ou tableaux 1D """
    # version du 25_09_2015
    x=array(x)
    y=array(y)
    sigma_y=array(sigma_y)
    
    w=(1./sigma_y)**2
    Sw=sum(w)
    Sx=sum(w*x)
    Sy=sum(w*y)
    Sxy=sum(w*x*y)
    Sxx=sum(w*x*x)
    
    delta = Sw*Sxx-Sx**2
    a =(Sw*Sxy-Sx*Sy)/delta 
    b = (Sxx*Sy-Sx*Sxy)/delta
    da = sqrt(Sw/delta)
    db = sqrt(Sxx/delta)
    chisq = sum(w*((y-(a*x+b))**2))
    chisq_red = chisq/(size(x)-2.)
    
    return a,da,b,db,chisq,chisq_red
