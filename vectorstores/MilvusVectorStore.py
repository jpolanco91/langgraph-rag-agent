from pymilvus import (
	MilvusException,
	connections,
	db
)

from langchain_milvus import Milvus

class MilvusVectorStore:

	def __init__(self, URI, index_params, documents, embeddings, consistency_level, drop_old=False):
		self.URI = URI
		self.index_params = index_params
		self.documents = documents
		self.embeddings = embeddings
		self.consistency_level = consistency_level
		self.drop_old = drop_old
		self.vector_store = None
		self.conn = connections.connect(uri=self.URI)

	def db_exists(self, db_name):
		exists_in_db = False
		try:
			existing_databases = db.list_database()

			if db_name in existing_databases:
				exists_in_db = True
		except MilvusException as e:
			print(f"An error occurred: {e}")

		return exists_in_db

	def create_db(self, db_name):
		try:
			if self.db_exists(db_name):
				print(f"Database '{db_name}' already exists")

				# Use database context
				db.using_database(db_name)

				print(f"Using database '{db_name}' ")
			else:
				print(f"Database '{db_name}' does not exist")
				database = db.create_database(db_name)
				print(f"Database '{db_name}' created successfully")

				# Use database context
				db.using_database(db_name)

				print(f"Using database '{db_name}' ")
		except MilvusException as e:
			print(f"An error occurred {e}")

	def create_vector_store_from_db(self, token, db_name):
		try:
			self.vector_store = Milvus(
				embedding_function=self.embeddings,
				connection_args={"uri": self.URI, "token": token, "db_name": db_name},
				index_params=self.index_params,
				consistency_level=self.consistency_level,
				drop_old=self.drop_old
			)
			print(f"Created MilvusDB vector store!")
		except Exception as e:
			print(f"Error setting MilvusDB vector store: {e}")

	def get_retriever(self):
		retriever = self.vector_store.as_retriever(
			search_type="similarity",
			search_kwargs={"k": 5}
		)

		return retriever

