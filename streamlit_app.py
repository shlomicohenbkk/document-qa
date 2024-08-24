import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📄 Shlomi's SEO Product Description Generator")
st.write("Step 1 - Upload your product information document")

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Step 2 - Ask the AI to write an SEO-optimized product description!",
        placeholder="e.g., Write an SEO-optimized 40-word product description, highlighting key attributes, benefits, and recommended keywords.",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "system",
                "content": "You are an expert SEO writer specializing in product descriptions. Focus on optimizing content for search engines while maintaining readability, Write an SEO-optimized 40-word product description, highlighting key attributes, benefits, and recommended keywords.",
            },
            {
                "role": "user",
                "content": f"Here's the product document:\n\n{document}\n\n---\n\n{question}",
            },
        ]

        # Generate an answer using the OpenAI API.
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=False,
        )

        # Display the AI's SEO-optimized content.
        st.subheader("SEO-Optimized Product Description")
        st.write(response["choices"][0]["message"]["content"])

        # Save the generated content as a text file.
        st.download_button(
            label="Download SEO Description",
            data=response["choices"][0]["message"]["content"],
            file_name="seo_product_description.txt",
            mime="text/plain",
        )
