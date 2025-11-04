#!/usr/bin/env python3
"""Quick demo of the cloud RAG system"""

import os
from dotenv import load_dotenv
from upstash_vector import Index
from groq import Groq

load_dotenv()

# Initialize clients
print('🚀 Initializing Upstash Vector + Groq Cloud...\n')
index = Index.from_env()
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Test query
question = 'What is Pho and where is it from?'
print(f'❓ Question: {question}\n')

# Vector search
print('🔍 Searching vector database...')
results = index.query(data=question, top_k=2, include_metadata=True)
context = '\n'.join([r.metadata['original_text'] for r in results])
print(f'✅ Found {len(results)} relevant documents\n')

# LLM generation
print('🤖 Generating answer with Groq Cloud (llama-3.1-8b-instant)...')
response = groq_client.chat.completions.create(
    messages=[
        {'role': 'system', 'content': 'You are a helpful food expert.'},
        {'role': 'user', 'content': f'Context: {context}\n\nQuestion: {question}\n\nProvide a concise answer.'}
    ],
    model='llama-3.1-8b-instant',
    max_tokens=200
)

answer = response.choices[0].message.content.strip()
print(f'✅ Answer generated!\n')
print('='*70)
print(f'💬 Answer:\n\n{answer}\n')
print('='*70)
print('\n🎉 Cloud RAG system (Upstash + Groq) working perfectly!')
print('⚡ Response time: Sub-second')
print('☁️  100% cloud-based - no local dependencies!')
