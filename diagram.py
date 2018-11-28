import copy
import networkx as nx
from DAGPattern import Pattern

flag = 'f'
extent_mark = 'ex'
intent_mark = 'in'


def print_lattice(L):
    with open('lattice.txt', 'w') as f:
        for n in L.nodes(data=True):
            f.write(str(n) + ' ' + str(L.neighbors(n[0])) + '\n')


def init_diagram():
    L = nx.DiGraph()
    L.add_node(-1, {intent_mark: Pattern(atts={}, dirty=False), extent_mark: [], flag: True})
    L.add_node(-2, {intent_mark: Pattern(atts={}, dirty=False), extent_mark: [], flag: True})
    L.add_edge(-1, -2)
    return L


def clean_flags(L, concept_id):
    for j in L.neighbors(concept_id):
        if not L.node[j][flag]:
            clean_flags(L, j)
    L.node[concept_id][flag] = True


def get_maximal_concept(intent, generator_id, L):
    if intent.size() == 0:
        return -2
    for j in L.neighbors(generator_id):
        # print('GENERATOR {} - SUPER {}'.format(generator,j))
        if intent == L.node[j][intent_mark]:  # THE CONCEPT ALREADY EXISTS. RETURN THE NODE ID OF THAT CONCEPT
            return j
        elif intent <= L.node[j][intent_mark]:  # THE MOST COMMON CASE
            return get_maximal_concept(intent, j, L)
    return generator_id


def add_object(object_concept_id, object_id, L, depth=1):
    if not L.node[object_concept_id][flag]:
        return 0
    #print("-"*depth,object,'->',intent,g.node[intent],'=',)
    L.node[object_concept_id][flag]=False
    L.node[object_concept_id][extent_mark].append(object_id)
    #print(g.node[intent])
    for j in L.neighbors(object_concept_id):
        add_object(j, object_id, L, depth+1)


def add_intent(intent, generator_id, L):
    generator = get_maximal_concept(intent, generator_id, L)
    if generator != -1 and L.node[generator][intent_mark] == intent:
        return generator
    new_parents = []
    for candidate_id in L.neighbors(generator):
        if not L.node[candidate_id][intent_mark] <= intent:
            candidate_intent = L.node[candidate_id][intent_mark].intersect(intent)
            candidate_id = add_intent(candidate_intent, candidate_id, L)
        add_parent = True
        for parent in new_parents:
            if L.node[candidate_id][intent_mark] <= L.node[parent][intent_mark]:
                add_parent = False
                break
            elif L.node[parent][intent_mark] <= L.node[candidate_id][intent_mark]:
                del new_parents[new_parents.index(parent)]
        if add_parent:
            new_parents.append(candidate_id)
    new_concept_id = len(L.nodes()) - 2
    L.add_node(new_concept_id, {extent_mark: copy.copy(L.node[generator][extent_mark]), intent_mark: intent, flag: True})
    for parent in new_parents:
        if parent in L[generator]:
            L.remove_edge(generator, parent)
        L.add_edge(new_concept_id, parent)
    L.add_edge(generator, new_concept_id)
    return new_concept_id
