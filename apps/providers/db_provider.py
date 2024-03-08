from ..configs.firebase_config import db


class DatabaseProvider:
    '''
    DatabaseProvider is a class that provides a connection 
    to the Database provider.
    '''

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.id_field = "_id"
        # Initialize collection
        self.collection = db.collection(collection_name)

    def getAll(self):
        '''
        Get all documents from the collection.
        Return a list of documents.
        '''
        docs = self.collection.stream()
        doc_list = []
        for doc in docs:
            doc_dict = doc.to_dict()
            # Append the id to the document dictionary
            doc_dict[self.id_field] = doc.id
            doc_list.append(doc_dict)
        return doc_list

    def getById(self, doc_id: str):
        '''
        Get a document from the collection.
        Return the document if it exists, otherwise return None.
        '''
        doc = self.collection.document(doc_id).get()
        if doc.exists:
            doc_dict = doc.to_dict()
            # Append the id to the document dictionary
            doc_dict[self.id_field] = doc_id
            return doc_dict
        else:
            return None

    def queryEqual(self, key: str, value: str):
        '''
        Query the collection for documents where the key is equal to the value.
        Return a list of documents.
        '''
        docs = self.collection.where(key, "==", value).stream()
        doc_list = []
        for doc in docs:
            doc_dict = doc.to_dict()
            # Append the id to the document dictionary
            doc_dict[self.id_field] = doc.id
            doc_list.append(doc_dict)
        return doc_list

    def create(self, data: dict) -> str:
        '''
        Create a new document in the collection.
        Return the document id.
        '''
        doc_ref = self.collection.add(data)
        return doc_ref[1].id

    def update(self, doc_id: str, data: dict):
        '''
        Update a document in the collection.
        Return the document id.
        '''
        self.collection.document(doc_id).set(data, merge=True)
        return doc_id

    def delete(self, doc_id: str):
        '''
        Delete a document from the collection.
        Return the document id.
        '''
        self.collection.document(doc_id).delete()
        return doc_id
