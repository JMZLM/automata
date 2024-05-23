import streamlit as st
import utils
import requests
from PIL import Image
from io import BytesIO

# Streamlit interface
def main():
    # Set page title and icon
    st.set_page_config(
        page_title="G1 Compiler",
        page_icon="🔀"
    )

    st.markdown(
        """
        <style>
        body {
            font-family: 'Josefin Sans', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .nav ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #333;
            border-radius: 5px;
        }
        .nav li {
            float: left;
        }
        .nav li a {
            display: block;
            color: #f4c2ab;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
        }
        .nav li a:hover {
            background-color: #DE739E;
        }
        .nav li a.active {
            background-color: #a33852;
        }
        .nav li:last-child {
            float: right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )









    # Initialize streamlit session state values
    if len(st.session_state) == 0:
        st.session_state.disabled = True
        st.session_state.placeholder_text = ""

    # Callback function for regex_input
    def regex_input_callbk():
        # Set disable for string_input and validate_button
        if st.session_state.regex_input == "--- Select ---":
            st.session_state.disabled = True
        else:
            st.session_state.disabled = False

        # Set placeholder text for string_input
        if st.session_state.regex_input == utils.regex_options[1]:
            st.session_state.placeholder_text = "aabbaaababbaa"
        elif st.session_state.regex_input == utils.regex_options[2]:
            st.session_state.placeholder_text = "11100111"
        else:
            st.session_state.placeholder_text = ""

        # Clear string_input
        st.session_state.string_input = ""


    # Create container to group blocks of code
    title_con = st.container()
    st.divider()
    regex_to_dfa_con = st.container()


    # Code block for title and description
    with title_con:
        st.title("G1 Compiler")
        st.markdown(
            '''
            This project is a web application that will convert the given regular expressions below to Deterministic Finite Automata (DFA), 
            Context-Free Grammars (CFG), and Pushdown Automata (PDA).

            **Regular Expressions**
            1. `(a+b)(a+b)*(aa+bb)(ab+ba)(a+b)*(aba+baa)`
            2. `(11+00)(1+0)*(101+111+01)(00*+11*)(1+0+11)`

            '''
            )

    # Code block for regex to dfa feature
    with regex_to_dfa_con:
        st.subheader("Regex to DFA")
        st.markdown(
            '''
            1. Select a given Regex from the select box. The application will perform the conversion and display 
            the resulting DFA on the screen.
            2. Enter a string to check if it is valid for the DFA and then the program will check the 
            validity of the string by checking each state through an animation.
            '''
            )

        # Select box input to select regex
        regex_input = st.selectbox(
            label = "Select a Regular Expression",
            options = utils.regex_options,
            key="regex_input",
            on_change=regex_input_callbk
        )

        # Text input for string validation
        string_input = st.text_input(
            label = "Enter a string to check its validity for displayed DFA",
            key="string_input",
            disabled=st.session_state.disabled,
            placeholder=st.session_state.placeholder_text
        )

        # Validate button to run string validation
        validate_button = st.button(
            label = "Validate",
            disabled=st.session_state.disabled
        )

        # Output for regex_input, display dfa, cfg, and pda of selected regex
        if regex_input == utils.regex_options[1]:
            current_dfa = utils.dfa_1
            st.write("**Deterministic Finite Automaton**")
            if not string_input:
                dfa = utils.generate_dfa_visualization(current_dfa)
                st.graphviz_chart(dfa)



        elif regex_input == utils.regex_options[2]:
            current_dfa = utils.dfa_2
            st.write("**Deterministic Finite Automaton**")
            if not string_input:
                dfa = utils.generate_dfa_visualization(current_dfa)
                st.graphviz_chart(dfa)



        # Output for string_input, play validation animation on displayed dfa
        if validate_button or string_input:
            string_input = string_input.replace(" ", "")  # Removes any whitespaces

            # Check if string_input is empty
            if len(string_input) == 0:
                st.error("Empty/Invalid Input", icon="❌")

            # Check if string_input has characters not in the alphabet of selected regex
            elif not all(char in current_dfa["alphabet"] for char in string_input):
                st.error(f"String '{string_input}' contains invalid characters, please only use characters from the alphabet: {current_dfa['alphabet']}", icon="❌")

            else:
                st.write(f"Entered String: `{string_input}`")
                is_valid, state_checks = utils.validate_dfa(current_dfa, string_input)
                utils.animate_dfa_validation(current_dfa, state_checks)
                if is_valid:
                    st.success(f"The string '{string_input}' is valid for the DFA.", icon="✔️")
                else:
                    st.error(f"The string '{string_input}' is not valid for the DFA.", icon="❌")

        image_url = "https://drive.google.com/uc?export=download&id=1VFB5uFRxs2JQpPLOQZCrxlEZFilz-AKQ"

        # Function to fetch and display image
        def display_image_from_url(url, width=500):
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption="", width=width, use_column_width=True)

        # Display the image
        display_image_from_url(image_url, width=840)

if __name__ == "__main__":
    main()
