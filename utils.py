from graphviz import Digraph
import streamlit as st
import time

# List of regular expressions assigned to our group
regex_options = [
    "--- Select ---",
    "(a+b)(a+b)*(aa+bb)(ab+ba)(a+b)*(aba+baa)",
    "(11+00)(1+0)*(101+111+01)(00*+11*)(1+0+11)"
]

# DFA for (a+b)(a+b)*(aa+bb)(ab+ba)(a+b)*(aba+baa)
dfa_1 = {
    "states": ["q0","q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q15", "q16"],
    "alphabet": ["a", "b"],
    "start_state": "q0",
    "end_states": ["q14", "q16"],
    "transitions": {
        ("q0", "a,b"): "q1",

        ("q1", "a"): "q2",
        ("q1", "b"): "q3",

        ("q2", "a"): "q4",
        ("q2", "b"): "q3",

        ("q3", "a"): "q2",
        ("q3", "b"): "q5",

        ("q4", "a"): "q7",
        ("q4", "b"): "q8",

        ("q5", "a"): "q6",
        ("q5", "b"): "q9",

        ("q6", "a"): "q4",
        ("q6", "b"): "q10",

        ("q7", "a"): "q7",
        ("q7", "b"): "q10",

        ("q8", "a"): "q10",
        ("q8", "b"): "q5",

        ("q9", "a"): "q10",
        ("q9", "b"): "q9",

        ("q10", "a"): "q11",
        ("q10", "b"): "q12",

        ("q11", "a"): "q11",
        ("q11", "b"): "q13",

        ("q12", "a"): "q15",
        ("q12", "b"): "q12",

        ("q13", "a"): "q14",
        ("q13", "b"): "q12",

        ("q14", "a"): "q16",
        ("q14", "b"): "q13",

        ("q15", "a"): "q16",
        ("q15", "b"): "q13",

        ("q16", "a"): "q11",
        ("q16", "b"): "q13",
    }
}

# DFA for (11+00)(1+0)*(101+111+01)(00*+11*)(1+0+11)
dfa_2 = {
    "states": ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q15", "q16"],
    "alphabet": ["0", "1"],
    "start_state": "q0",
    "end_states": ["q11","q12", "q14", "q15", "q16"],
    "transitions": {
        ("q0", "1"): "q1",
        ("q0", "0"): "q2",

        ("q1", "0"): "T",
        ("q1", "1"): "q3",

        ("T", "0,1"): "T",

        ("q2", "1"): "T",
        ("q2", "0"): "q3",

        ("q3", "1"): "q4",
        ("q3", "0"): "q5",

        ("q4", "0"): "q5",
        ("q4", "1"): "q6",

        ("q5", "0"): "q5",
        ("q5", "1"): "q7",

        ("q6", "0"): "q5",
        ("q6", "1"): "q8",

        ("q7", "0"): "q9",
        ("q7", "1"): "q13",

        ("q8", "1"): "q10",
        ("q8", "0"): "q9",

        ("q9", "0"): "q11",
        ("q9", "1"): "q14",

        ("q10", "0"): "q11",
        ("q10", "1"): "q12",

        ("q11", "0"): "q11",
        ("q11", "1"): "q14",

        ("q12", "0"): "q11",
        ("q12", "1"): "q12",

        ("q13", "0"): "q16",
        ("q13", "1"): "q12",

        ("q14", "1"): "q15",


        ("q15", "0"): "q16",
        ("q15", "1"): "q12",

        ("q16", "0"): "q5",
        ("q16", "1"): "q7",


    }
}

# CFG for (a+b)(a+b)*(aa+bb)(ab+ba)(a+b)*(aba+baa)
cfg_1 = '''
        S -> WXbabXYZ \n
        W -> aba | bab \n
        X -> aX | bX | ^ \n
        Y -> a | b | ab | ba \n
        Z -> aZ | bZ | aaZ | ^
        '''

# CFG for (11+00)(1+0)*(101+111+01)(00*+11*)(1+0+11)
cfg_2 = '''
        S -> WXYZ \n
        W -> 101 | 111 | 1 | 0 | 11 \n
        X -> 1X | 0X | 01X | ^ \n
        Y -> 111 | 000 | 101 \n
        Z -> 1Z | 0Z | ^
        '''

# PDA for (a+b)(a+b)*(aa+bb)(ab+ba)(a+b)*(aba+baa)
pda_1 = {
    "states": ["Start", "Read1", "Read2", "Read3", "Read4", "Read5", "Read6", "Read7", 
               "Read8", "Read9", "Read10", "Read11", "Read12", "Read13", "Accept1", "Accept2"],
    "alphabet": ["a", "b"],
    "start_state": "Start",
    "push_states": [None],
    "pop_states": [None],
    "accept_states": ["Accept1", "Accept2"],
    "transitions": {
        ("Start", ""): "Read1",
        ("Read1", "a"): "Read2",
        ("Read1", "b"): "Read3",
        ("Read2", "b"): "Read4",
        ("Read3", "a"): "Read5",
        ("Read4", "a"): "Read6",
        ("Read5", "b"): "Read6",
        ("Read6", "b"): "Read7",
        ("Read7", "a"): "Read8",
        ("Read8", "b"): "Read9",
        ("Read9", "a"): "Read10",
        ("Read9", "b"): "Read11",
        ("Read10", "b"): "Read12",
        ("Read11", "a"): "Read13",
        ("Read10", "^"): "Accept1",
        ("Read11", "^"): "Accept1",
        ("Read12", "a, b, ^"): "Accept2",
        ("Read13", "a, b, ^"): "Accept2",
        ("Read6", "a"): "Read6",
        ("Read7", "b"): "Read7",
        ("Read8", "a"): "Read6",
        ("Read10", "a"): "Read10",
        ("Read11", "b"): "Read11",
    }
}

# PDA for (11+00)(1+0)*(101+111+01)(00*+11*)(1+0+11)
pda_2 = {
    "states": ["Start", "Read1", "Read2", "Read3", "Read4", "Read5", "Read6", "Read7", "Read8", "Accept"],
    "alphabet": ["1", "0"],
    "start_state": "Start",
    "push_states": [None],
    "pop_states": [None],
    "accept_states": ["Accept"],
    "transitions": {
        ("Start", ""): "Read1",
        ("Read1", "0,1"): "Read2",
        ("Read2", "0"): "Read3",
        ("Read2", "1"): "Read4",
        ("Read3", "0"): "Read5",
        ("Read3", "1"): "Read4",
        ("Read4", "0"): "Read7",
        ("Read4", "1"): "Read6",
        ("Read6", "0"): "Read7",
        ("Read5", "0"): "Read8",
        ("Read5", "1"): "Read4",
        ("Read6", "1"): "Read8",
        ("Read7", "1"): "Read8",
        ("Read7", "0"): "Read3",
        ("Read8", "0,1"): "Read8",
        ("Read8", "^"): "Accept",
    }
}



# Generate DFA visualization using Graphviz
def generate_dfa_visualization(dfa):
    dot = Digraph(engine="dot", graph_attr={'rankdir': 'LR'}, renderer="gd")

    # Add graph nodes for the states
    for state in dfa["states"]:
        if state in dfa["end_states"]:
            dot.node(state, shape="doublecircle")
        else:
            dot.node(state, shape="circle")

    # Add edges/transitions
    for transition, target_state in dfa["transitions"].items():
        source_state, symbol = transition
        dot.edge(source_state, target_state, label=symbol)

    # Return the Graphviz graph for the DFA visualization
    return dot


# Generate PDA visualization using Graphviz
def generate_pda_visualization(pda):
    dot = Digraph(engine="dot", renderer="gd")

    # Add graph nodes for the states
    for state in pda["states"]:
        if state in pda["start_state"] or state in pda["accept_states"]:
            dot.node(state, shape="ellipse")
        elif state in pda["push_states"]:
            dot.node(state, shape="rectangle")
        else:
            dot.node(state, shape="diamond")

    # Add edges/transitions
    for transition, target_state in pda["transitions"].items():
        source_state, symbol = transition
        dot.edge(source_state, target_state, label=symbol)

    # Return the Graphviz graph for the DFA visualization
    return dot


# Validate given string for DFA 
def validate_dfa(dfa, string):
    state_checks = []
    current_state = dfa["start_state"]

    # Iterate through each character in string
    for char in string:
        # Check if transition has "0,1", if so replace char with "0,1"
        if (current_state,"0,1") in dfa["transitions"].keys():
            char = "0,1"
        
        # Check if transition has "a,b", if so replace char with "a,b"
        if (current_state,"a,b") in dfa["transitions"].keys():
            char = "a,b"
        
        transition = (current_state, char)
        transition_exists = transition in dfa["transitions"].keys()
        state_checks.append((current_state, transition_exists))

        # Check if current char is in transitions
        if transition_exists:
            current_state = dfa["transitions"][transition]
        # Return False if current character in the string is not in the dfa transitions
        else:
            return False
    
    # Add state check for last transition
    if current_state in dfa["end_states"]:
        state_checks.append((current_state, True))
    else:
        state_checks.append((current_state, False))

    result = current_state in dfa["end_states"] # Checks if last current_state is in dfa end_states

    # Return the validation result and state_checks array
    return (result, state_checks)


# Generate validation animation
def animate_dfa_validation(dfa, state_checks):
    dot = generate_dfa_visualization(dfa)  # Generate the DFA visualization
    graph = st.graphviz_chart(dot.source, use_container_width=True)  # Create a Streamlit Graphviz component

    previous_state = None  # Variable to keep track of the previously marked state

    # Iterate through each state in state_checks
    for state_check in state_checks:
        state, is_valid = state_check

        time.sleep(1)  # Add a delay for visualization purposes

        if previous_state:
            dot.node(previous_state, style="filled", fillcolor="white")  # Reset previous state color to white

        if is_valid and state in dfa["end_states"]:
            dot.node(state, style="filled", fillcolor="green")  # Set end state to green
        elif not is_valid:
            dot.node(state, style="filled", fillcolor="red")  # Set invalid state to red
        else:
            dot.node(state, style="filled", fillcolor="yellow")  # Set state to yellow if True

        previous_state = state  # Update previous state
        graph.graphviz_chart(dot.source, use_container_width=True)  # Render the updated visualization
