# Plot Persuit

import streamlit as st
import google.generativeai as genai
import PIL.Image

# Main function
def main():
    st.title("Plot Persuit - Unveiling Novels Before You Dive In")
 # Sidebar for inputs
    with st.sidebar:   
        st.write("Please insert the full Book Title (with author if possible) below or upload an image of the book cover and we'll provide you with information.")
        
        # Set Google API key
        genai.configure(api_key="AIzaSyBIOWxD8l5vQouhPh5zc398pPu7EWgjNNs")

        model = genai.GenerativeModel("gemini-pro")

        # Accept user input
        
        query = st.text_input("Insert Book Title Here:")
        uploaded_file = st.file_uploader("Upload an image of the book cover", type=["jpg", "jpeg", "png"], accept_multiple_files=False)


        search_clicked = st.button("🔍 Search")
        clear_clicked = st.button("🗑️ Clear my search")

    # Main area for displaying outputs
    st.markdown("---")
    with st.container():
        if clear_clicked:
            query = ""
            uploaded_file = None
            st.text_input = ""
            st.file_uploader = ""


        elif search_clicked:
            # Check if both query and uploaded_file are empty
            if not query and not uploaded_file:
                return  # Do nothing and wait for user input

            # Calling the Function when Input is Provided
            if query:
                # Process the query and generate response
                response = model.generate_content([f"Please list all my requirements: Give the book summary, tell who is the author and publisher, year it was published, the theme of the story in the novel, where is the setting of the story with description,what readers should expect while reading the book, list the characters with description if possible,  how many chapters and a summary of the chapters combined in only few parts, and state whether there are any series related to this novel (show where this novel is placed in the series) in the book '{query}'"])

                # Display response
                st.markdown(response.text)
            
            elif uploaded_file is not None:

                image = PIL.Image.open(uploaded_file)

                vision_model = genai.GenerativeModel('gemini-pro-vision')
                response = vision_model.generate_content([f"Please list all my requirements: Give the book summary, tell who is the author and publisher, year it was published, the theme of the story in the novel, where is the setting of the story with description,what readers should expect while reading the book, list the characters with description if possible,  how many chapters and a summary of the chapters combined in only few parts, and state whether there are any series related to this novel (show where this novel is placed in the series) in the book ", image])

                # Display response
                st.markdown(response.text)

if __name__ == "__main__":
    main()
