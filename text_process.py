with open("data/transcripts/transcript.txt", "r", encoding="utf-8") as f:
    transcript = f.read().replace("\n", "").replace("\r", "").strip()

from rag_core.embedding import Embeddings
from rag_core.chunking import Chunking
from utils.logger import Logger
import time
from models.models import Models

chunking = Chunking()
model = Models()
embedding = Embeddings()
log = Logger().get_logger()



log.info("Starting the embedding process...\n")
chunks = chunking.chunking(transcript, chunk_size=900, chunk_overlap=180)
time.sleep(1)  # Simulate processing time
log.info(f"Total chunks created: {len(chunks)}\n")
time.sleep(1)  # Simulate processing time
log.info(f"First chunk preview: {chunks[0]}...\n")  
time.sleep(1)  # Simulate processing time
embedding_vector = embedding.embed_batch(chunks)  
time.sleep(1)  # Simulate processing time
print(embedding_vector[0])
time.sleep(1)  # Simulate processing time
log.info(f"Embedding vector for first chunk: {len(embedding_vector[0])} dimensions\n")


log.info("Embedding process completed successfully.\n")
log.info("===" * 50 + "\n")

while True:
    question = input("Enter a question (or type 'exit' to quit): ")
    if question.lower() == 'exit':
        break
    context = embedding.get_context(question, chunks, embedding_vector)
    answer = model.generate_answers(context, question)
    time.sleep(1.5)  # Simulate processing time
    log.info(f"Answer for question '{question}': {answer}\n")
    
