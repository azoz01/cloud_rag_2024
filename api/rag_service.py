import os

from langchain.chains import RetrievalQA
from langchain_google_vertexai import (
    VectorSearchVectorStore,
    VertexAI,
    VertexAIEmbeddings,
)


class RagService:

    def __init__(self):
        self.embedding = VertexAIEmbeddings(
            model_name="textembedding-gecko@001"
        )
        self.vector_store = VectorSearchVectorStore.from_components(
            project_id=os.environ["PROJECT_ID"],
            region="us-central1",
            gcs_bucket_name=os.environ["VECTOR_INDEX_BUCKET"],
            index_id=os.environ["VECTOR_INDEX_ID"],
            endpoint_id=os.environ["ENDPOINT_ID"],
            embedding=self.embedding,
            stream_update=True,
        )
        self.llm = VertexAI(
            model_name="text-bison@001",
            project=os.environ["PROJECT_ID"],
            temperature=0.0,
            top_p=0,
            top_k=1,
            max_output_tokens=256,
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_type="similarity", search_kwargs={"k": 4}
            ),
            return_source_documents=True,
            input_key="question",
        )

    def get_response(self, prompt):
        result = self.qa_chain(
            {
                "question": f"{prompt}. If this is not present in "
                "documents, say 'I don't know'",
                "include_run_info": True,
            }
        )
        return result["result"]
