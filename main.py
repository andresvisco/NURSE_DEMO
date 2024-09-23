import streamlit as st
import os
from openai import AzureOpenAI


endpoint = os.getenv("ENDPOINT_URL")#, "https://openaiavisco.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME")#, "gpt-4o-mini")
search_endpoint = os.getenv("SEARCH_ENDPOINT")#, "https://ais-giatec-vector-demo.search.windows.net")
search_key = os.getenv("SEARCH_KEY")#, "vroP6zdJGb9lH27OAILWy104v29NAmLsJYODptAgOlAzSeAsQqJx")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")#, "70eccac0e4ed42409ac26781cfff474a")


st.sidebar.title("Navigation")
st.sidebar.markdown("**Select an option:**")
option = st.sidebar.radio("", ["Consulta", "CH Query"])

if option == "Consulta":
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version="2024-05-01-preview",
        )

    # Code for the consulta section
    st.title("Nursing Admission Assistant with Azure OpenAI")
    consulta = st.text_input("Enter your query:", placeholder="Describe your query here")

    if consulta:
        # Make the query to OpenAI model
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI Nursing assistant that helps nurses with admission. Based on nurse_protocol.pdf.\nALWAYS your answers should be only max 10 steps to proceed. No additional text"
                },
                {
                    "role": "user",
                    "content": str(consulta)
                }
            ],
            max_tokens=500,
            temperature=0.08,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False,
            extra_body={
                "data_sources": [{
                    "type": "azure_search",
                    "parameters": {
                        "filter": None,
                        "endpoint": f"{search_endpoint}",
                        "index_name": "vector-1726896547803",
                        "semantic_configuration": "vector-1726896547803-semantic-configuration",
                        "authentication": {
                            "type": "api_key",
                            "key": f"{search_key}"
                        },
                        "query_type": "simple",
                        "in_scope": True,
                        "role_information": "You are an AI Nursing assistant that helps nurses with admission. Based on nurse_protocol.pdf.\nALWAYS your answers should be only max 10 steps to proceed. No additional text",
                        "strictness": 3,
                        "top_n_documents": 5
                    }
                }]
            }
        )
        import re
        # Extract the content of the message in the JSON
        message_content = completion.choices[0].message.content
        # Display the result in the Streamlit app
        st.subheader("Assistant Response:")
        
        st.text_area("Result", value=message_content, height=300)

    # ... your code for the consulta section ...
elif option == "CH Query":
    # Code for the empty section
    st.title("CH Query")
    consulta_ch = st.text_input("Paciente: ", placeholder="Describe your query here")
    if consulta_ch:
        
    # Initialize Azure OpenAI client with key-based authentication
        client = AzureOpenAI(
            azure_endpoint = endpoint,
            api_key = subscription_key,
            api_version = "2024-05-01-preview",
        )

        completion = client.chat.completions.create(
            model=deployment,
            messages= [
            {
                "role": "system",
                "content": "You are an AI nursing assistant that helps people find information about clinic history in retrieved data.\nALWAYS your answers should be only a resume of the clinic history. No additional text"
            },
            {
                "role": "user",
                "content": "Necesito busques la historía clínica del paciente: "+str(consulta_ch)+""
            }
            ],
            max_tokens=800,
            temperature=0.11,
            top_p=0.78,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        ,
            extra_body={
            "data_sources": [{
                "type": "azure_search",
                "parameters": {
                    "filter": None,
                    "endpoint": f"{search_endpoint}",
                    "index_name": "great-nut-723ncdwd3g",
                    "semantic_configuration": "azureml-default",
                    "authentication": {
                    "type": "api_key",
                    "key": f"{search_key}"
                    },
                    "embedding_dependency": {
                    "type": "endpoint",
                    "endpoint": "https://openaiavisco.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-07-01-preview",
                    "authentication": {
                        "type": "api_key",
                        "key": "70eccac0e4ed42409ac26781cfff474a"
                    }
                    },
                    "query_type": "vector_simple_hybrid",
                    "in_scope": True,
                    "role_information": "You are an AI nursing assistant that helps people find information about clinic history in retrieved data.\nALWAYS your answers should be only a resume of the clinic history. No additional text",
                    "strictness": 3,
                    "top_n_documents": 6
                }
                }]
            })

        message_content = completion.choices[0].message.content
        st.subheader("Assistant Response:")
        st.markdown(message_content)
        
    # ... your code for the empty section ...
else:
    st.warning("Please select an option from the sidebar.")

# Get environment variables or default values

# Initialize Azure OpenAI client

# Streamlit app interface