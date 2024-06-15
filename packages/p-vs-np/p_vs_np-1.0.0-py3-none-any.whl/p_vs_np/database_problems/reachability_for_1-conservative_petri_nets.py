#Reachability for 1-conservative petri nets

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
        # Initialize the queue and visited set
        queue = deque([(place.marking,) for place in self.places])
        visited = set(queue)

        # Perform breadth-first search
        while queue:
            current_marking = queue.popleft()

            # Check if the current marking matches the target marking
            if current_marking == target_marking:
                return True

            # Generate next possible markings
            for transition in self.transitions:
                input_markings = [current_marking[self.places.index(place)] for place in transition.input_places]
                output_markings = [current_marking[self.places.index(place)] for place in transition.output_places]

                # Check if the transition is enabled
                if all(input_markings) and not any(output_markings):
                    new_marking = list(current_marking)

                    # Consume tokens from input places
                    for place in transition.input_places:
                        index = self.places.index(place)
                        new_marking[index] -= 1

                    # Produce tokens to output places
                    for place in transition.output_places:
                        index = self.places.index(place)
                        new_marking[index] += 1

                    # Check if the new marking has been visited
                    new_marking_tuple = tuple(new_marking)
                    if new_marking_tuple not in visited:
                        visited.add(new_marking_tuple)
                        queue.append(new_marking_tuple)

        return False

# Example usage
net = PetriNet()

# Define places
p1 = Place('p1', 1)
p2 = Place('p2')
p3 = Place('p3')

# Define transitions
t1 = Transition('t1', [p1], [p2])
t2 = Transition('t2', [p2], [p3])

# Add places and transitions to the Petri net
net.add_place(p1)
net.add_place(p2)
net.add_place(p3)
net.add_transition(t1)
net.add_transition(t2)

# Define the target marking to check for reachability
target_marking = (0, 0, 1)

if net.is_reachable(target_marking):
    print("The target marking is reachable.")
else:
    print("The target marking is not reachable.")
