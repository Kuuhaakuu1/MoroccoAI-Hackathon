import os.path
import os
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space 
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
path = "المقاولة والأعمال\الصفقات العمومية"

# Side bar contents
with st.sidebar:
    st.title('Idarati AchbalChat')
    st.markdown('''
    ## About:
    This app is an LLM-Powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://www.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM Model
    - [Idarati dataset](https://www.idarati.ma/)
    ''')
    add_vertical_space(5)
    st.write('Created by AchbalChat Team')
# check if storage already exists
if not os.path.exists("./storage"):
    # load the documents and create the index
    documents = SimpleDirectoryReader(path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist()
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)

# either way we can now query the index
query_engine = index.as_query_engine()
st.title('Idarati AchbalChat')

query = st.text_input("What would you like to know about your PDF?")
    
if query:
    print(type(query))
    response = query_engine.query(query)
    st.write(response) 