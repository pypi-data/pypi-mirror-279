#Reachability for 1-conservative petri nets







        # Initialize the queue and visited set

        # Perform breadth-first search

            # Check if the current marking matches the target marking

            # Generate next possible markings

                # Check if the transition is enabled

                    # Consume tokens from input places

                    # Produce tokens to output places

                    # Check if the new marking has been visited


# Example usage

# Define places

# Define transitions

# Add places and transitions to the Petri net

# Define the target marking to check for reachability


if __name__ == '__main__':
    from collections import deque
    class Place:
        def __init__(self, name, marking=0):
            self.name = name
            self.marking = marking
    class Transition:
        def __init__(self, name, input_places, output_places):
            self.name = name
            self.input_places = input_places
            self.output_places = output_places
    class PetriNet:
        def __init__(self):
            self.places = []
            self.transitions = []
        def add_place(self, place):
            self.places.append(place)
        def add_transition(self, transition):
            self.transitions.append(transition)
        def is_reachable(self, target_marking):
            queue = deque([(place.marking,) for place in self.places])
            visited = set(queue)
            while queue:
                current_marking = queue.popleft()
                if current_marking == target_marking:
                    return True
                for transition in self.transitions:
                    input_markings = [current_marking[self.places.index(place)] for place in transition.input_places]
                    output_markings = [current_marking[self.places.index(place)] for place in transition.output_places]
                    if all(input_markings) and not any(output_markings):
                        new_marking = list(current_marking)
                        for place in transition.input_places:
                            index = self.places.index(place)
                            new_marking[index] -= 1
                        for place in transition.output_places:
                            index = self.places.index(place)
                            new_marking[index] += 1
                        new_marking_tuple = tuple(new_marking)
                        if new_marking_tuple not in visited:
                            visited.add(new_marking_tuple)
                            queue.append(new_marking_tuple)
            return False
    net = PetriNet()
    p1 = Place('p1', 1)
    p2 = Place('p2')
    p3 = Place('p3')
    t1 = Transition('t1', [p1], [p2])
    t2 = Transition('t2', [p2], [p3])
    net.add_place(p1)
    net.add_place(p2)
    net.add_place(p3)
    net.add_transition(t1)
    net.add_transition(t2)
    target_marking = (0, 0, 1)
    if net.is_reachable(target_marking):
        print("The target marking is reachable.")
    else:
        print("The target marking is not reachable.")
