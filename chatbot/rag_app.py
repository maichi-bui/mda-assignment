import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from typing import Optional, List, Dict, Any
from supabase import create_client
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


class Retriever:
    def __init__(self):
        # Initialize clients
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.google_api_key = os.getenv("GEMINI_API_KEY")
        
        self.supabase = create_client(self.supabase_url, self.supabase_key)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004", 
            google_api_key=self.google_api_key
        )
        
        # Cache for embeddings to avoid duplicate API calls
        self.embedding_cache = {}
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding with caching to minimize API calls"""
        if text in self.embedding_cache:
            return self.embedding_cache[text]
        
        embedding = self.embeddings.embed_query(text)
        self.embedding_cache[text] = embedding
        return embedding
    
    def retrieve_documents(
        self,
        query: str,
        project_id: int,
        k: int = 10,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve documents filtered by project_id with optional score threshold"""
        # Get query embedding
        query_embedding = self.get_embedding(query)
        
        # Build the query with project_id filter
        query_builder = self.supabase.rpc(
            'match_documents',  # Your Supabase function name
            {
                'query_embedding': query_embedding,
                'match_count': k,
                'filter': {'project_id': project_id}  # Add project filter
            }
        )
        
        if score_threshold:
            query_builder.gte('similarity', score_threshold)
        
        # Execute the query
        result = query_builder.execute()
        
        if hasattr(result, 'data'):
            return result.data
        return []

def create_chain():
    retriever = Retriever()
    
    # Define prompt template
    template = """You are an assistant for project {project_name}.
    Project description: {description}. 
    Recent conversation history:
    {chat_history}
    Answer the question based on both the context below and our conversation history:
    {context}
    
    Question: {question}
    
    Provide a concise answer
    If you don't know the answer or there is no context, just say that you don't know, do not hallucinate
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    # Initialize Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-001",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3  # Lower for more factual responses
    )
    
    # Create the chain with project_id parameter
    chain = (
        {
            "context": lambda params: "\n\n".join(
                f"Document {i+1}:\n{doc['content']}" 
                for i, doc in enumerate(
                    retriever.retrieve_documents(
                        params["question"],
                        params["project_id"]
                    )
                )
            ),
            "description": lambda params: params["description"],
            "question": lambda params: params["question"],
            "project_name": lambda params: params["project_name"],
            "chat_history": lambda params: params["chat_history"],
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

def load_metadata(project_id):
    project_df = pd.read_csv('../horizon-dataset/cleaned-data/projects.csv')
    project_df = project_df[project_df['id'] == project_id]
    project_name = project_df.title.values[0]
    description = project_df.objective.values[0]
    return project_name, description

# question = st.chat_input()
chain = create_chain()
project_id = 101039226
project_name, description = load_metadata(project_id)

# Initialize chat history in session state if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if question := st.chat_input("Ask about the project..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(question)
    
    # Generate RAG response
    with st.spinner("Thinking..."):
        response = chain.invoke({
            "question": question,
            "project_id": project_id,
            "project_name": project_name,
            "description": description,
            "chat_history": "\n".join([msg["content"] for msg in st.session_state.messages if msg["role"] == "assistant"][-3:])  # Last 3 assistant messages
        })
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})