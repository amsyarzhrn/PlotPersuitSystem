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
                prompt = f"""
                
                ### Book Summary:
                Based on '{query}', provide a summary of the book.

                ### Author and Publisher:
                Who is the author and what is the publisher of the book? Also, provide the year it was published.

                ### Genre and Theme:
                Identify the genre and theme of the story in the novel.

                ## Main Conflict 
                Identify the main conflict of the story and brief description

                ### Setting of the Story:
                Describe where the story is set and provide a brief description of the setting.

                ### Expectations for Readers:
                What should readers expect while reading the book?

                ### Characters:
                List the characters and provide a description if possible.

                ### Chapters:
                How many chapters does the book have? Provide a summary of the chapters combined in only a few parts.

                ### Series Information:
                Is this novel part of a series? If so, where does it fit in the series?

                ### Similar Books:
                Recommend four other books that are similar to '{query}' based on genre and theme.
                """



                response = model.generate_content([prompt])

                
                st.markdown(response.text)
                
            
            
            elif uploaded_file is not None:

                image = PIL.Image.open(uploaded_file)

                vision_model = genai.GenerativeModel('gemini-pro-vision')

                prompt = f"""
                ### **Please list all my requirements based on the image provided:**

                ### Book Name:
                What is the book name recognised based on the image
                
                ### Book Summary:
                Based on the image, provide a summary of the book.

                ### Author and Publisher:
                Who is the author and what is the publisher of the book? Also, provide the year it was published. Make bullet point.

                ### Genre and Theme:
                Identify the genre and theme of the story in the novel. Describe a bit.

                ## Main Conflict 
                Identify the main conflict of the story and brief description

                ### Setting of the Story:
                Describe where the story is set and provide a brief description of the setting.

                ### Expectations for Readers:
                What should readers expect while reading the book?

                ### Characters:
                List the characters and provide a description if possible. make bullet point for all characters available

                ### Chapters:
                How many chapters does the book have? Provide a summary of the chapters combined in only a few parts.

                ### Series Information:
                Is this novel part of a series? If so, where does it fit in the series? Make list of series it related to. 

                ### Similar Books:
                Recommend four other books that are similar to the one depicted in the image based on genre and theme. Make bullet points
                """

                # Generate content using the prompt and the image
                response = vision_model.generate_content([prompt, image])

                # Check if the response contains the expected book title
                if query.lower() in response.text.lower():
                    # Display response
                    st.markdown(response.text)
                else:
                    # Book not found error message
                    st.error(f"The context you provided does not mention the book '{query}'. Therefore, I cannot extract the requested data from the provided context. Please try again with another novel.")

if __name__ == "__main__":
    main()
