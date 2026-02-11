# RAG Chatbot with LangChain and Hugging Face

A Retrieval Augmented Generation (RAG) chatbot that uses `knowledge base.txt` as its knowledge source.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add content to knowledge base:**
   - Add your knowledge content to `knowledge base.txt`
   - The file can contain any text information you want the chatbot to answer questions about

3. **Get Hugging Face API Token:**
   - Go to https://huggingface.co/settings/tokens
   - Create a new token (read permission is sufficient)
   - Either:
     - Set it as environment variable: `set HUGGINGFACEHUB_API_TOKEN=your_token_here` (Windows)
     - Or enter it when prompted by the script

## Usage

Run the chatbot:
```bash
python rag_chatbot.py
```

The chatbot will:
1. Load and process the knowledge base
2. Create embeddings using Hugging Face sentence transformers
3. Build a vector store for efficient retrieval
4. Start an interactive chat session

## How It Works

1. **Document Loading**: Loads text from `knowledge base.txt`
2. **Text Chunking**: Splits the document into manageable chunks
3. **Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` for vector embeddings
4. **Vector Store**: FAISS stores and retrieves relevant chunks
5. **LLM**: Uses `google/flan-t5-large` from Hugging Face for generation
6. **Retrieval QA**: Combines retrieval and generation to answer questions

## Example Knowledge Base

Add content to `knowledge base.txt` like:
```
Company Name: TechCorp Solutions
Founded: 2020
Location: San Francisco, CA

Products:
- CloudSync: A cloud storage solution
- DataAnalyzer: Business intelligence tool
- SecureChat: Encrypted messaging platform

Mission: To provide innovative technology solutions that empower businesses.
```

Then ask questions like:
- "What products does TechCorp offer?"
- "When was the company founded?"
- "What is the mission?"

## Notes

- The chatbot only answers based on the knowledge base content
- If information isn't in the knowledge base, it will say it doesn't know
- You can modify the LLM model, embeddings model, and chunk size in the code
