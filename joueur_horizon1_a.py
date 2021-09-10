#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
import numpy as np

MOI = None
JEU = None

def getparcoursJoueur(joueur):
    """Int->List[Tuple(Int,Int)]
    Retourne la liste des paires d'indices de cases dans l'ordre du début de la rangée du joueur dont c'est le tour
    """
    IDCJ1 = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5)]
    IDCJ2 = [(1,5), (1,4), (1,3), (1,2), (1,1), (1,0)]
     
    if joueur == 1:
        return IDCJ1 + IDCJ2
    if joueur == 2:
        return IDCJ2 + IDCJ1



def EScore(jeu):
    return game.getScore(jeu, MOI) - game.getScore(JEU, MOI) - (game.getScore(jeu, MOI%2+1) - game.getScore(JEU, MOI%2+1))
    
def Egrenier(jeu):
    plt = game.getPlateau(jeu)
    parcours = getparcoursJoueur(MOI)
    
    ret = 0
    
    for i,j in parcours[:6]:
        case = plt[i][j]
        if 0 < case < 4:
            ret-=1 #on pénalise les config capturables
        if case > 4:
            ret += case-4 #on récompense les greniers
            
    return ret



def evaluation(jeu):
    w=[0.7, 0.3]
    f=[EScore(jeu), Egrenier(jeu)]
    return np.dot(w,f)

def estimation(jeu, coup):
    next_game = game.getCopieJeu(jeu)
    game.joueCoup(next_game, coup)
    return evaluation(next_game)

def decision(jeu):
    cv = game.getCoupsValides(jeu)
    estimations = []
    for cp in cv:
        estimations.append(estimation(jeu, cp))
    
    e = np.array(estimations)
    i_max = np.argmax(e)
    
    coup = cv[i_max]
    
    return coup



def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global MOI
    global JEU
    JEU = jeu
    MOI = game.getJoueur(JEU)
    
    coup = decision(jeu)
    
    return coup