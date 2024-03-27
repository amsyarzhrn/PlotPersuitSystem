# Plot Persuit

import streamlit as st
import google.generativeai as genai
import PIL.Image
from difflib import SequenceMatcher

# Custom CSS styles 
st.markdown(
    """
    <style>
        /* CSS for the title */
        .title-text {
            font-size: 48px;
            font-weight: bold;
            color: #336699; /* Adjust color as needed */
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* Add a text shadow */
            margin-bottom: 15px; /* Adjust spacing as needed */
        }
        
        /* CSS for clear button */
        /* CSS for the clear button */
        button[data-testid="clear_button"] {
            background-color: #FF474C; /* Red color for clear button */
            color: white; /* Text color */
            border-radius: 5px; /* Rounded corners */
            border: none; /* Remove border */
            padding: 10px 20px; /* Padding */
            margin-top: 10px; /* Adjust spacing as needed */
            cursor: pointer; /* Cursor style */
            transition: background-color 0.3s; /* Smooth transition */
        }

        /* Hover effect for clear button */
        button[data-testid="clear_button"]:hover {
            background-color: #FF6B6E; /* Lighter red on hover */
            transform: scale(1.05); /* Increase button size on hover */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Main function
def main():
    st.markdown("<p class='title-text'>Plot Persuit - Unveiling Novels Before You Dive In</p>", unsafe_allow_html=True)
 # Sidebar for inputs
    with st.sidebar:   
        st.write("Please insert the Book Title (with author if possible) below or upload an image of the book cover and we'll provide you with information about the novel. Happy reading!!!")
        
        # Set Google API key
        genai.configure(api_key = "AIzaSyC0S0mkAzqwhycpf1v0pOjkWJWxDkeqp_Q")

        model = genai.GenerativeModel("gemini-pro")

        # Accept user input
        
        query = st.text_input("Insert book title and author here:")
        uploaded_file = st.file_uploader("Upload an image of the book cover", type=["jpg", "jpeg", "png"], accept_multiple_files=False)


        search_clicked = st.button("🔍 Search")
        clear_clicked = st.button("🗑️ Clear my search" , key="clear_button")

    # Main area for displaying outputs
    st.markdown("---")

    with st.container():
        if clear_clicked:
            query = ""
            uploaded_file = None


        elif search_clicked:
          with st.spinner(" We're fetching book data, please standby...."):
            # Check if both query and uploaded_file are empty
            if not query and not uploaded_file:
                return  # Do nothing and wait for user input

            # Calling the Function when Input is Provided
            if query:
                # Process the query and generate response
                response = model.generate_content([f"Please list all my requirements: Based on  '{query}', give the book summary, tell who is the author and publisher, year it was published, the genre, the theme of the story in the novel, where is the setting of the story with description, what readers should expect while reading the book, list the characters with description of it if possible, how many chapters and a summary of the chapters combined in only a few parts, state whether there are any series related to this novel (show where this novel is placed in the series) in the book, and 4 other book that are similar to it based on genre and theme "])

                
                st.markdown(response.text)
                
            
            
            elif uploaded_file is not None:

                image = PIL.Image.open(uploaded_file)

                vision_model = genai.GenerativeModel('gemini-pro-vision')
                response = vision_model.generate_content([f"Please list all my requirements: Based on  '{image}', give the book summary, tell who is the author and publisher, year it was published, the genre, the theme of the story in the novel, where is the setting of the story with description, what readers should expect while reading the book, list the characters with description of it if possible, how many chapters and a summary of the chapters combined in only a few parts, state whether there are any series related to this novel (show where this novel is placed in the series) in the book, and 4 other book that are similar to it based on genre and theme ", image])

                # Check if the response contains the expected book title
                if query.lower() in response.text.lower():
                    # Display response
                    st.markdown(response.text)
                else:
                    # Book not found error message
                    st.error(f"The context you provided does not mention the book '{query}'. Therefore, I cannot extract the requested data from the provided context. Please try again with another novel.")

if __name__ == "__main__":
    main()
