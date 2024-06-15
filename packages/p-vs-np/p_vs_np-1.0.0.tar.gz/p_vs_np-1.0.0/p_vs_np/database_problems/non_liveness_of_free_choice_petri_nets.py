# Non-Liveness of free choice petri nets


    # Mark all places as initially unmarked

    # Check for non-liveness


# Example usage

# Define places

# Define transitions

# Define arcs

# Set initial marking


if __name__ == '__main__':
    from petrinet import PetriNet, Place, Transition
    def is_non_live(petrinet):
        for place in petrinet.places:
            place.marking = 0
        initial_marking = tuple(place.marking for place in petrinet.places)
        successors = petrinet.fireable_successors(initial_marking)
        if not successors:
            return True
        return False
    net = PetriNet()
    p1 = Place('p1')
    p2 = Place('p2')
    t1 = Transition('t1')
    t2 = Transition('t2')
    net.add_arc(p1, t1)
    net.add_arc(t1, p2)
    net.add_arc(p2, t2)
    p1.marking = 1
    if is_non_live(net):
        print("The Petri net is non-live.")
    else:
        print("The Petri net is live.")
