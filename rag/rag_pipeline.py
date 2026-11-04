from rag.rag_retriever import Retriever
from rag.genrator import Genrator

class RAGPipeline:
    def __init__(self):
        self.retriver=Retriever()
        self.genrator=Genrator()

    # ask a question and get an answer
    def get_answer(self,question:str)->str:
        answer=self.genrator.refine_answer(question)
        return answer
    def run(self):
            print("AI portfolio assistantt")
            print("-------------------------")
            while True:
                question=input("Enter your question (or type 'exit' to quit): ")
                if question.strip().lower() == "exit":
                    print("Exiting the assistant. Goodbye!")
                    break
                answer=self.get_answer(question)
                print("\nAnswer:")
                print(answer)
                print("-------------------------")
if __name__ == "__main__":
    pipeline=RAGPipeline()
    pipeline.run()