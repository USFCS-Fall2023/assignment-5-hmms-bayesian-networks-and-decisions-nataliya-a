

import random
import argparse
import codecs
import os
import numpy

# observations
class Observation:
    def __init__(self, stateseq, outputseq):
        self.stateseq  = stateseq   # sequence of states
        self.outputseq = outputseq  # sequence of outputs
    def __str__(self):
        return ' '.join(self.stateseq)+'\n'+' '.join(self.outputseq)+'\n'
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.outputseq)

# hmm model
class HMM:
    def __init__(self, transitions={}, emissions={}):
        """creates a model from transition and emission probabilities"""
        ## Both of these are dictionaries of dictionaries. e.g. :
        # {'#': {'C': 0.814506898514, 'V': 0.185493101486},
        #  'C': {'C': 0.625840873591, 'V': 0.374159126409},
        #  'V': {'C': 0.603126993184, 'V': 0.396873006816}}

        self.transitions = transitions
        self.emissions = emissions
        self.states = {}

    ## part 1 - you do this.
    def load(self, basename):
        """reads HMM structure from transition (basename.trans),
        and emission (basename.emit) files,
        as well as the probabilities."""

        trans_file = basename + ".trans"
        emit_file = basename + ".emit"

        transitions = {}
        emissions = {}

        with open(trans_file, 'r') as f_trans:
            for line in f_trans:
                line = line.split()
                if len(line) == 3:
                    from_state, to_state, prob = line
                    prob = float(prob)  # convert to float
                    if from_state not in transitions:
                        transitions[from_state] = {}
                    transitions[from_state][to_state] = prob

        with open(emit_file, 'r') as f_emit:
            for line in f_emit:
                line = line.split()
                if len(line) == 3:
                    state, output, prob = line
                    prob = float(prob)
                    if state not in emissions:
                        emissions[state] = {}
                    emissions[state][output] = prob

        self.transitions = transitions
        self.emissions = emissions
        self.states = {state: index for index, state in enumerate(transitions.keys())}

        # print("transitions: ", self.transitions)
        
        



   ## you do this.
    def generate(self, n):
        """return an n-length observation by randomly sampling from this HMM."""
        if not self.transitions or not self.emissions:
            raise ValueError("HMM model is not properly initialized")

        # Initialize sequences for states and outputs
        state_sequence = []
        output_sequence = []

        # Start with the initial state (assumed to be '#')
        current_state = '#'

        for _ in range(n):
            # Sample the next state based on transition probabilities
            next_state = random.choices(
                list(self.transitions[current_state].keys()),
                weights=self.transitions[current_state].values()
            )[0]

            # Sample the output based on emission probabilities
            output = random.choices(
                list(self.emissions[next_state].keys()),
                weights=self.emissions[next_state].values()
            )[0]

            # Append the state and output to their respective sequences
            state_sequence.append(next_state)
            output_sequence.append(output)

            # Update the current state for the next iteration
            current_state = next_state

        return Observation(state_sequence, output_sequence)
    
    def forward(self, observation):

        if not observation.outputseq:
            return None, 0

        num_states = len(self.transitions)
        forward_probs = numpy.zeros((len(observation), num_states))

        # Initialize with starting probabilities
        for state, index in self.states.items():
            if state != "#":  # Exclude start state
                forward_probs[0][index] = self.transitions["#"][state] * self.emissions[
                    state
                ].get(observation.outputseq[0], 0)

        # Iterate over the sequence
        for t in range(1, len(observation)):
            for curr_state, curr_index in self.states.items():
                if curr_state != "#":  # Exclude start state
                    forward_probs[t][curr_index] = sum(
                        forward_probs[t - 1][prev_index]
                        * self.transitions[prev_state].get(curr_state, 0)
                        * (
                            self.emissions[curr_state].get(observation.outputseq[t], 0)
                            if curr_state in self.emissions
                            else 0
                        )
                        for prev_state, prev_index in self.states.items()
                        if prev_state != "#"
                    )

        final_prob = sum(forward_probs[-1])
        return forward_probs, final_prob
    

    def viterbi(self, observation):
        if not observation.outputseq:
            return None
        # Map state labels to indices
        states = list(self.transitions.keys())
        state_indices = {state: i for i, state in enumerate(states)}

        # Initialize viterbi probabilities and path pointers
        n_states = len(states)
        viterbi_probs = numpy.zeros((len(observation), n_states))
        backpointers = numpy.zeros((len(observation), n_states), dtype=int)

        # Initialize with starting probabilities
        for state in states:
            state_idx = state_indices[state]
            if (
                state in self.emissions
                and observation.outputseq[0] in self.emissions[state]
            ):
                viterbi_probs[0][state_idx] = (
                    1.0 / n_states * self.emissions[state][observation.outputseq[0]]
                )
            else:
                viterbi_probs[0][
                    state_idx
                ] = 0  # Set to zero if emission probability is not defined

        # Iterate over the sequence
        for t in range(1, len(observation)):
            for curr_state in states:
                curr_idx = state_indices[curr_state]
                if curr_state in self.emissions:
                    max_prob, best_prev_state = max(
                        (
                            viterbi_probs[t - 1][state_indices[prev_state]]
                            * self.transitions[prev_state].get(curr_state, 0)
                            * self.emissions[curr_state].get(
                                observation.outputseq[t], 0
                            ),
                            prev_state,
                        )
                        for prev_state in states
                    )
                    viterbi_probs[t][curr_idx] = max_prob
                    backpointers[t][curr_idx] = state_indices[best_prev_state]
                else:
                    # Set to zero if the current state has no emission probabilities defined
                    viterbi_probs[t][curr_idx] = 0

        # Find the best final state
        best_final_state = numpy.argmax(viterbi_probs[-1])

        # Trace back the path
        best_path = [best_final_state]
        for t in range(len(observation) - 1, 0, -1):
            best_path.insert(0, backpointers[t][best_path[0]])

        # Convert indices back to state labels
        best_path_labels = [states[i] for i in best_path]
        return best_path_labels



    
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HMM')
    parser.add_argument('filename', type=str, help='filename to generate')
    parser.add_argument('--generate', type=int, help='generate random n observations')
    parser.add_argument('--viterbi', type=str, help='run viterbi algorithm on an observation')
    parser.add_argument('--forward', type=str, help='run forward algorithm on an observation')

    args = parser.parse_args()
    print(args)

    model = HMM()

    model.load(args.filename)

    if args.generate is not None:
        # Generate n observations
        for _ in range(args.generate):
            observation = model.generate(20)  # Modify the number 20 as needed
            print(observation)

    if args.viterbi:
        # Run Viterbi on the specified input observation file
        with open(args.viterbi, 'r') as f:
            lines = f.readlines()
            for line in lines:
                words = line.strip().split()
                observation = Observation([''] * len(words), words)
                best_path = model.viterbi(observation)
                print("Most likely sequence of states:", best_path)

    if args.forward:
        # Run forward algorithm on the specified input observation file
        with open(args.forward, 'r') as f:
            lines = f.readlines()
            for line in lines:
                words = line.strip().split()
                observation = Observation([''] * len(words), words)
                final_state, final_prob = model.forward(observation)
                print("Most likely final state:", final_state)
                print("Probability of the observation:", final_prob)
    


    




