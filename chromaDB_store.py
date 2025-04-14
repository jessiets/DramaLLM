import pandas as pd
import csv
import chromadb
from chromadb.utils import embedding_functions

class ChromaDB:

    def __init__(self, collection_name):
        # setup embedding
        self.default_ef = embedding_functions.DefaultEmbeddingFunction()

        # set up chromadb connection
        client = chromadb.EphemeralClient()

        # Since this is a new object, delete existing collection and make a fresh one
        # print(f"Existing collections: {client.list_collections()}")
        # client.delete_collection(name=collection_name)

        self.collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.default_ef
            )
        
        self.genre_map = {}
        self.setUp()

        self.store_to_db()

    def setUp(self):
        # create genre map
        self.genre_map['10759'] = 'Action & Adventure'
        self.genre_map['16'] = 'Animation'
        self.genre_map['35'] = 'Comedy'
        self.genre_map['80'] = 'Crime'
        self.genre_map['99'] = 'Documentary'
        self.genre_map['18'] = 'Drama'
        self.genre_map['10751'] = 'Family'
        self.genre_map['10762'] = 'Kids'
        self.genre_map['9648'] = 'Mystery'
        self.genre_map['10763'] = 'News'
        self.genre_map['10764'] = 'Reality'
        self.genre_map['10765'] = 'Sci-Fi & Fantasy'
        self.genre_map['10766'] = 'Soap'
        self.genre_map['10767'] = 'Talk'
        self.genre_map['10768'] = 'War & Politics'
        self.genre_map['37'] = 'Western'
        


    def add_to_db(self, info, show_id):
        print(f'adding doc {self.collection.count()+1}...')
        self.collection.upsert(
            documents=[info],                    # store generated info as document
            metadatas=[{'show_id': show_id}],   # store show id as metadata
            ids=[f'{self.collection.count() + 1}']
        )


    def store_to_db(self):
        print('storing to db')        
        with open("data/drama_list.csv") as file:
            lines = csv.reader(file)

            for i, line in enumerate(lines):
                
                # skip first row (column titles)
                if i == 0:
                    continue

                # generate document to be stored in ChromaDB
                document = f"The tv show name is: {line[11]}\n"
                
                country = line[5]
                if country == "ko":
                    document += f"The show classifies as: korean drama \n"
                else:
                    document += f"The show classifies as: chinese drama \n"

                genres = ""
                genre_ids = line[2].replace("[", "").replace("]", "")
                if len(genre_ids) > 0:
                    for g in genre_ids.split(", "):
                        genres += f"{self.genre_map[g]}, "
                
                document += f"The genre is: {genres}\nThe air date is: {line[10]}\n"
                document += f"The show is about: {line[7]}\nThe popularity is: {line[8]}"

                # store document in ChromaDB
                self.add_to_db(document, line[3])
        
        print(f'db completed: {self.collection.count()}')


    ''' 
    Fetch best results according to user query.

    @param string
    @return dict with keys: {data, distances, documents, embeddings, ids, included, metadatas, uris}
    '''
    def chromadb_user_query(self, keywords):
        print(f'querying chromadb...')
        results = self.collection.query(
            query_texts=[keywords],  # Chroma will embed this for you
            n_results=10             # how many results to return
        )
        print(f'received results from chromadb...')
        return results