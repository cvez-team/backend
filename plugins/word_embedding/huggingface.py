class HuggingFaceEmbedder:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None

    def embed_query(self, data: str):
        '''
        Embeds the data.
        '''
        raise NotImplementedError("This method is not implemented yet.")


embedder = HuggingFaceEmbedder(model_name="bert-base-uncased")
