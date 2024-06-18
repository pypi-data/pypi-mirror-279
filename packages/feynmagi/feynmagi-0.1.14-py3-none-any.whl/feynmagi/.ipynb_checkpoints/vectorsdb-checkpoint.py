import numpy as np
from numpy.linalg import norm
import pickle
import os
import helper
import  llmsapis 
import config as cfg


def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

class VectorDB:  # Short Term memeoy, I dont save this to disk as it's session history todo ==> ? 
    def __init__(self):
        self.data = {}  # Stocke les données
        self.vectors = {}  # Stocke les vecteurs avec des ID uniques comme clés
        self.ids = 0  # Compteur pour générer des ID uniques

        
    def add_vector_data(self, vector, data):
        """Ajouter un vecteur et des données associées à la base de données."""
        self.data[self.ids] = data
        self.vectors[self.ids] = vector
        self.ids += 1
        return self.ids - 1  # Retourne l'ID du vecteur ajouté

    def add_data(self, data):
        """Ajouter un vecteur et des données associées à la base de données."""
        self.data[self.ids] = data
        self.vectors[self.ids] = np.array(llmsapis.embeddings(data))
        self.ids += 1
        return self.ids - 1  # Retourne l'ID du vecteur ajouté

    def find_similar_v(self, query_vector, n=10, min_similarity=0.5):
        """Retrouver les n vecteurs les plus similaires au vecteur de requête."""
        similarities = []
        for vector_id, vector in self.vectors.items():
            sim = cosine_similarity(query_vector, vector)
            if sim >= min_similarity:  # Filtrer par similarité minimale
                similarities.append((vector_id, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)  # Trier par similarité décroissante
        return similarities[:n]

    def find_similar_d(self, query_text, n=2, min_similarity=0.6):
        """Retrouver les n données les plus similaires au texte de requête."""
        dsimilarities = []       
        query_vector = np.array(llmsapis.embeddings(query_text))
        vsimilarities = self.find_similar_v(query_vector, n, min_similarity)
        for v in vsimilarities:
            dsimilarities.append((self.data[v[0]], v[1]))
        return dsimilarities

    def get_stats(self):
        """Obtenir des statistiques de la base de données."""
        return self.ids
      
class RagVectorDB:  # Long term memeory ==> todo : use multi bases, a base per agent ? 
    def __init__(self,base_name: str):
        self.vectors = {}  # Stocke les vecteurs avec des ID uniques comme clés
        self.refs = {}  # Stocke les vecteurs avec des ID uniques comme clés
        self.ids = 0  # Compteur pour générer des ID uniques
        try:
            self.vdb_dir=f"{base_name}_dir"
            self.vdb_name=f"{base_name}_dir/{base_name}.pkl"
            cfg.logger.debug("Loading Long Term Memory index")
            print("Loading Long Term Memory index")
            self.load_from_disk(self.vdb_name)
        except Exception as e:
            cfg.logger.debug("Creating Long Term Memory index")
            print("Creating Long Term Memory index")
            # Check if the directory exists
            if not os.path.exists(self.vdb_dir):
                # If it does not exist, create it
                os.makedirs(self.vdb_dir)
                print(f"Directory '{self.vdb_dir}' was created.")
            else:
                # If it exists, print that it already exists
                print(f"Directory '{self.vdb_dir}' already exists.")
            self.save_to_disk(self.vdb_name)

    def dump(self):
        self.save_to_disk(self.vdb_name)
        
    def add_data(self, data, ref):
        """Ajouter un vecteur et des données associées à la base de données."""
        file_name=f"{self.vdb_dir}/{self.ids}.txt"
        with open(file_name,"w") as f:
            f.write(data)
            f.close 
        self.vectors[self.ids] = np.array(llmsapis.embeddings(data))
        self.refs[self.ids] = ref
        self.ids += 1
        self.dump()
        return self.ids - 1  # Retourne l'ID du vecteur ajouté

    def find_similar_v(self, query_vector, n=10, min_similarity=0.5):
        """Retrouver les n vecteurs les plus similaires au vecteur de requête."""
        similarities = []
        for vector_id, vector in self.vectors.items():
            # print("vector_id, vector",vector_id, vector)
            if vector.shape[0] == 0 :
                continue
            sim = cosine_similarity(query_vector, vector)
            if sim >= min_similarity:  # Filtrer par similarité minimale
                similarities.append((vector_id, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)  # Trier par similarité décroissante
        return similarities[:n]

    def find_similar_d(self, query_text, n=1, min_similarity=0.6):
        """Retrouver les n données les plus similaires au texte de requête."""
        dsimilarities = []       
        query_vector = np.array(llmsapis.embeddings(query_text))
        #print("query_vector",query_vector)
        vsimilarities = self.find_similar_v(query_vector, n, min_similarity)
        for v in vsimilarities:
            file_name=f"{self.vdb_dir}/{v[0]}.txt"
            txt=""
            with open(file_name,"r") as f:
                txt=f.read()
                f.close
                
            dsimilarities.append((txt, v[1],self.refs[v[0]]))
        return dsimilarities

    def save_to_disk(self, filename):
        """Sauvegarder l'état actuel dans un fichier."""
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def load_from_disk(self, filename):
        """Charger l'état depuis un fichier."""
        with open(filename, 'rb') as f:
            temp_dict = pickle.load(f)
            self.__dict__.clear()
            self.__dict__.update(temp_dict)

    def clear(self):
        """Réinitialiser la base de données."""
        self.refs.clear()
        self.vectors.clear()
        self.ids = 0

    def get_stats(self):
        """Obtenir des statistiques de la base de données."""
        return self.ids
    
    def get_data(self):
        
        return self.refs
        

