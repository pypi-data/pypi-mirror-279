# Non-Liveness of free choice petri nets

from petrinet import PetriNet, Place, Transition

def is_non_live(petrinet):
    # Mark all places as initially unmarked
    for place in petrinet.places:
        place.marking = 0

    # Check for non-liveness
    initial_marking = tuple(place.marking for place in petrinet.places)
    successors = petrinet.fireable_successors(initial_marking)
    if not successors:
        return True

    return False

# Example usage
net = PetriNet()

# Define places
p1 = Place('p1')
p2 = Place('p2')

# Define transitions
t1 = Transition('t1')
t2 = Transition('t2')

# Define arcs
net.add_arc(p1, t1)
net.add_arc(t1, p2)
net.add_arc(p2, t2)

# Set initial marking
p1.marking = 1

if is_non_live(net):
    print("The Petri net is non-live.")
else:
    print("The Petri net is live.")
