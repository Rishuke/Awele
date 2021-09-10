#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    
    game.affiche(jeu)
    j = game.getJoueur(jeu)
    print("  Vous êtes le joueur {}".format(j))

    coups_valides = game.getCoupsValides(jeu)
    print(" Coups valides:", [i[1] for i in coups_valides])
    
    coup_valide = False
    while(not coup_valide):
        print("  Saisir coup:")
        y = int(input("    case="))
        coup = (j-1,y)
        coup_valide = coup in coups_valides
        if not coup_valide:
            print("    coup invalide! rejouez...")
            
    return coup