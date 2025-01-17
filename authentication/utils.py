#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
domain_fuzzer.py
------------------------------------------------------
Script Python3 "homemade" pour générer des variations
de type homoglyph + l33t + autres substitutions 
(similaire à dnstwist), en évitant les doublons et en
privilégiant la même longueur que l'input, avec un tri
par ressemblance (d'abord les plus proches visuellement).

Nouveauté:
  - On affiche désormais le score de similarité à côté
    de chaque domaine (score = nombre de caractères
    identiques, position par position).
  - On exporte également les résultats en JSON.

Usage:
    python3 domain_fuzzer.py [DOMAIN]

Exemple:
    python3 domain_fuzzer.py google.com
"""

import sys
import json
from itertools import product

# --------------------------------------------------------------------
# Mappage de caractères (ASCII + quelques "exotiques").
# On ne fait que du "char -> possible variants".
# --------------------------------------------------------------------
TRANSFORM_MAP = {
    'a': ['a', '4', '@', '^', 'à', 'á'],
    'b': ['b', '8', '6', 'ß'],
    'c': ['c', '(', '<', '¢'],
    'd': ['d', ')'],
    'e': ['e', '3', '€', 'ê'],
    'f': ['f', '#', 'ƒ'],
    'g': ['g', '9', '6', '&'],
    'h': ['h', '#'],
    'i': ['i', '1', '!', 'í', 'ì'],
    'j': ['j', ';', '¿'],
    'k': ['k'],
    'l': ['l', '1', '|', '£'],
    'm': ['m', 'µ'],
    'n': ['n', 'η', 'ñ'],
    'o': ['o', '0', '°', 'ø'],
    'p': ['p', '¶', 'ρ'],
    'q': ['q', '9'],
    'r': ['r', '®'],
    's': ['s', '5', '$', '§'],
    't': ['t', '7', '+'],
    'u': ['u', 'µ', 'ù', 'ú'],
    'v': ['v'],
    'w': ['w', 'ω'],
    'x': ['x', '×', 'χ'],
    'y': ['y', '¥', 'γ'],
    'z': ['z', '2'],

    # Majuscules (optionnel) : on peut en rajouter
    'A': ['A', '4', '@'],
    'B': ['B', '8', '6'],
    'C': ['C', '(', '<'],
    'E': ['E', '3'],
    'F': ['F', '#'],
    'G': ['G', '6', '9'],
    'H': ['H', '#'],
    'I': ['I', '1', '!'],
    'L': ['L', '|'],
    'O': ['O', '0'],
    'Q': ['Q', '9'],
    'S': ['S', '5', '$'],
    'T': ['T', '7', '+'],
    'Z': ['Z', '2'],
}


def char_variants(c: str):
    """
    Retourne la liste de substitutions possibles pour le caractère c,
    y compris lui-même.
    """
    if c in TRANSFORM_MAP:
        return list(set(TRANSFORM_MAP[c] + [c]))
    # Si on ne connait pas le char (chiffre, point, etc.), on le garde tel quel
    return [c]


def generate_permutations(domain_part: str):
    """
    Génère toutes les permutations "char by char" 
    en se basant sur TRANSFORM_MAP.
    On ne change pas la longueur du domain_part (pas d'insert/delete).
    Retour brute, sans tri ni dédup.
    """
    if not domain_part:
        return []

    all_subs = []
    for c in domain_part:
        all_subs.append(char_variants(c))

    results = []
    for combo in product(*all_subs):
        candidate = "".join(combo)
        results.append(candidate)

    return results


def compute_similarity_score(original: str, variant: str) -> int:
    """
    Retourne un score = nombre de caractères identiques (position par position)
    entre original et variant.
    """
    same = 0
    for oc, vc in zip(original, variant):
        if oc == vc:
            same += 1
    return same


def parse_domain(domain: str):
    """
    Sépare le domaine en 2 parties:
        - le nom (ex: 'google')
        - l'extension (ex: '.com'), ou '' si pas de '.'.
    On se base sur la dernière occurrence d'un point.
    """
    if '.' not in domain:
        return domain, ''  # pas d'extension
    parts = domain.rsplit('.', 1)
    nom = parts[0]
    extension = '.' + parts[1]
    return nom, extension


def fuzz_domain(domain: str, limit=200):
    """
    - Sépare domain en (nom, extension).
    - Fait les permutations sur 'nom' seulement.
    - Concatène chaque permutation avec extension tel quel.
    - Dédoublonne, retire l'original, trie par ressemblance, limite.
    - Retourne une liste de tuples (permuted_domain, score)
    """
    nom, ext = parse_domain(domain)
    raw_candidates = generate_permutations(nom)
    unique_candidates = set(raw_candidates)

    # Reconstruire en "candidat + extension"
    full_candidates = [f"{c}{ext}" for c in unique_candidates]

    # Retirer l'original
    if domain in full_candidates:
        full_candidates.remove(domain)

    # Construire liste (domain, score) pour trier
    scored_list = []
    for candidate in full_candidates:
        sc = compute_similarity_score(domain, candidate)
        scored_list.append((candidate, sc))

    # Trier par score décroissant, puis alphabétique si égalité
    scored_list.sort(key=lambda x: (-x[1], x[0]))

    # Limiter
    return scored_list[:limit]


def get_domain(domain: str):
    scored_candidates = fuzz_domain(domain, limit=10)

    # Affichage console: <domaine> (score=XX)
    for (name, score) in scored_candidates:
        print(f"{name} (score={score})")

    # Export en JSON
    # On construit une liste d'objets { "domain": ..., "score": ... }
    data = []
    for (name, score) in scored_candidates:
        data.append({
            "name": name,
            "score": score
        })

    # Impression JSON
    # Si tu veux plutôt l'écrire dans un fichier, tu peux faire:
    with open("output.json", "w") as fd:
        json.dump(data, fd, indent=2)
    # print("\n===== JSON OUTPUT =====")
    # print(json.dumps(data, indent=2))
    return data


# if __name__ == "__main__":
#     main(domain)
