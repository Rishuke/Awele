#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
import time

MOI = None
JEU = None

N = 4

TIMEOUT = 1.0
START_TIME = None

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

def EGagne(jeu):
    if not game.getCoupsValides(jeu): #plus de coup valides...
        gg = game.getGagnant(jeu)
        if gg == MOI:
            return 1000
        elif gg == 0: #pas de gagnant
            return 1
        else:#adversaire
            return -1000
    return 1

#old eval
# def evaluation(jeu):
#     w=[0.7, 0.3]
#     f=[EScore(jeu), Egrenier(jeu)]
#     return np.dot(w,f)

def evaluation(jeu):
    w=[0.35, 0.15, 0.5]
    f=[EScore(jeu), Egrenier(jeu), EGagne(jeu)]
    return sum([fi*wi for fi,wi in zip(f,w)])#dot

def estimation(jeu, coup, n):
    next_game = game.getCopieJeu(jeu)
    game.joueCoup(next_game, coup)
    
    #profondeur d'arret
    if n == 0:
        return evaluation(next_game)
    
    #on continue d'explorer l'arbre
    cv = game.getCoupsValides(next_game)
    
    if not cv:
        return evaluation(next_game)
    
    score_coup = 0
    for cp in cv:
        score_coup += estimation(next_game, cp, n-1)
        #ajout 1
        #elagage si timeout
        if (time.time() - START_TIME) > TIMEOUT:
            score_coup = evaluation(next_game)
            break
        
    return score_coup

def decision(jeu):
    cv = game.getCoupsValides(jeu)
    estimations = []
    for cp in cv:
        estimations.append(estimation(jeu, cp, N))
    
    i_max = estimations.index(max(estimations))
    
    coup = cv[i_max]
    
    return coup



def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global MOI
    global JEU
    global START_TIME
    JEU = jeu
    MOI = game.getJoueur(JEU)
    START_TIME = time.time()
    
    coup = decision(jeu)
    
    return coup