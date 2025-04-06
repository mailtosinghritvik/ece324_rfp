import os
import re
import sys
import fitz  # PyMuPDF for PDF processing
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss  # For vector indexing

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

class RFPPreprocessor:
    def __init__(self, pdf_path, chunk_size=500, overlap=100):
        """
        Initialize the RFP preprocessor.
        
        Args:
            pdf_path (str): Path to the PDF file
            chunk_size (int): Target size of text chunks in characters
            overlap (int): Overlap between chunks in characters
        """
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.text = ""
        self.chunks = []
        self.metadata = {}
        self.embeddings = None
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def extract_text(self):
        """
        Extract text from PDF file while preserving structure.
        """
        print(f"Extracting text from {self.pdf_path}...")
        doc = fitz.open(self.pdf_path)
        
        # Extract metadata if available
        self.metadata["title"] = doc.metadata.get("title", os.path.basename(self.pdf_path))
        self.metadata["author"] = doc.metadata.get("author", "")
        self.metadata["publication_date"] = doc.metadata.get("creationDate", "")
        
        text_content = []
        for page_num, page in enumerate(doc):
            text = page.get_text()
            # Remove headers, footers, page numbers
            text = self._remove_noise(text, page_num)
            text_content.append(text)
        
        self.text = "\n".join(text_content)
        print(f"Extracted {len(self.text)} characters from {len(doc)} pages.")
        return self.text
    
    def _remove_noise(self, text, page_num):
        """
        Remove headers, footers, page numbers, and other noise from text.
        
        Args:
            text (str): Text to clean
            page_num (int): Page number for context
            
        Returns:
            str: Cleaned text
        """
        # Remove page numbers
        text = re.sub(r'\b\d+\s*(?:of|/)\s*\d+\b', '', text)
        text = re.sub(r'\bPage\s*\d+\b', '', text)
        
        # Remove common header/footer patterns
        text = re.sub(r'(?i)confidential', '', text)
        text = re.sub(r'(?i)proprietary', '', text)
        
        # Split by lines to remove headers and footers
        lines = text.split('\n')
        if len(lines) > 4:  # Only process if enough lines
            # Remove top 2 lines (potential header)
            # and bottom 2 lines (potential footer)
            text = '\n'.join(lines[2:-2])
        
        return text
    
    def chunk_text(self):
        """
        Segment the text into smaller, coherent chunks.
        Uses semantic and structural cues to create meaningful chunks.
        """
        print("Chunking text into smaller sections...")
        
        if not self.text:
            print("No text to chunk. Run extract_text() first.")
            return []
        
        # First attempt to split by sections using headings
        section_pattern = r'(?:\n|\r\n)(?:[A-Z0-9][\.\)]\s+[A-Z]|[A-Z]{2,}|(?:SECTION|Section)\s+\d+)'
        sections = re.split(section_pattern, self.text)
        
        # If sections are still too large, further split into chunks
        chunks = []
        for section in sections:
            if len(section) <= self.chunk_size:
                chunks.append(section.strip())
            else:
                # Split by paragraphs
                paragraphs = re.split(r'\n\s*\n', section)
                current_chunk = ""
                
                for para in paragraphs:
                    if len(current_chunk) + len(para) <= self.chunk_size:
                        current_chunk += "\n" + para if current_chunk else para
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = para
                
                if current_chunk:  # Add the last chunk
                    chunks.append(current_chunk.strip())
        
        # Filter out very small or empty chunks
        self.chunks = [chunk for chunk in chunks if len(chunk) > 50]
        print(f"Created {len(self.chunks)} chunks.")
        return self.chunks
    
    def normalize_text(self):
        """
        Standardize text: lowercase, remove punctuation, normalize whitespace.
        """
        print("Normalizing text chunks...")
        normalized_chunks = []
        
        for chunk in self.chunks:
            # Lowercase
            text = chunk.lower()
            
            # Remove punctuation except for alphanumeric and whitespace
            text = re.sub(r'[^\w\s]', ' ', text)
            
            # Normalize whitespace
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            
            normalized_chunks.append(text)
        
        self.chunks = normalized_chunks
        return self.chunks
    
    def extract_keywords(self):
        """
        Extract important keywords and perform stemming.
        Returns a dictionary mapping chunks to their keywords.
        """
        print("Extracting keywords...")
        chunk_keywords = {}
        
        for i, chunk in enumerate(self.chunks):
            # Tokenize
            tokens = word_tokenize(chunk)
            
            # Remove stopwords
            tokens = [token for token in tokens if token.lower() not in self.stop_words]
            
            # Stem words
            stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
            
            # Store both original and stemmed tokens
            chunk_keywords[i] = {
                'original': tokens,
                'stemmed': stemmed_tokens
            }
        
        return chunk_keywords
    
    def tag_geography_category(self):
        """
        Identify and tag geographical and categorical information.
        Returns a dictionary with tags for each chunk.
        """
        print("Tagging geographical and categorical information...")
        
        # Simple pattern matching for Canadian provinces and territories
        provinces = [
            'Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 
            'Newfoundland and Labrador', 'Nova Scotia', 'Ontario', 'Prince Edward Island', 
            'Quebec', 'Saskatchewan', 'Northwest Territories', 'Nunavut', 'Yukon'
        ]
        
        # Common RFP categories
        categories = [
            'Information Technology', 'Construction', 'Healthcare', 'Consulting',
            'Professional Services', 'Engineering', 'Manufacturing', 'Transportation',
            'Education', 'Research', 'Software Development', 'Hardware', 'Infrastructure'
        ]
        
        chunk_tags = {}
        
        for i, chunk in enumerate(self.chunks):
            geo_tags = []
            cat_tags = []
            
            # Check for provinces
            for province in provinces:
                if re.search(r'\b' + re.escape(province) + r'\b', chunk, re.IGNORECASE):
                    geo_tags.append(province)
            
            # Check for categories
            for category in categories:
                if re.search(r'\b' + re.escape(category) + r'\b', chunk, re.IGNORECASE):
                    cat_tags.append(category)
            
            chunk_tags[i] = {
                'geographic': geo_tags,
                'category': cat_tags
            }
        
        return chunk_tags
    
    def generate_embeddings(self):
        """
        Generate vector embeddings for text chunks.
        """
        print("Generating embeddings...")
        
        if not self.chunks:
            print("No chunks to generate embeddings for. Run chunk_text() first.")
            return None
        
        # Generate embeddings using Sentence Transformers
        self.embeddings = self.embedding_model.encode(self.chunks)
        return self.embeddings
    
    def build_faiss_index(self):
        """
        Build a FAISS index for fast similarity search.
        """
        print("Building vector index...")
        
        if self.embeddings is None:
            self.generate_embeddings()
        
        # Normalize embeddings for cosine similarity
        normalized_embeddings = self.embeddings / np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        
        # Build the FAISS index
        dimension = normalized_embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        index.add(normalized_embeddings)
        
        return index
    
    def preprocess(self):
        """
        Run the complete preprocessing pipeline.
        """
        self.extract_text()
        self.chunk_text()
        self.normalize_text()
        keywords = self.extract_keywords()
        tags = self.tag_geography_category()
        self.generate_embeddings()
        index = self.build_faiss_index()
        
        # Combine all preprocessing results
        preprocessed_data = {
            'metadata': self.metadata,
            'chunks': self.chunks,
            'keywords': keywords,
            'tags': tags,
            'embeddings': self.embeddings.tolist() if self.embeddings is not None else None
        }
        
        return preprocessed_data
    
    def save_preprocessed_data(self, output_path):
        """
        Save preprocessed data to disk.
        
        Args:
            output_path (str): Path to save the preprocessed data
        """
        preprocessed_data = self.preprocess()
        
        # Convert to pandas DataFrame for easy storage
        chunks_df = pd.DataFrame({
            'chunk_id': range(len(self.chunks)),
            'text': self.chunks,
            'keywords_original': [preprocessed_data['keywords'][i]['original'] for i in range(len(self.chunks))],
            'keywords_stemmed': [preprocessed_data['keywords'][i]['stemmed'] for i in range(len(self.chunks))],
            'geo_tags': [preprocessed_data['tags'][i]['geographic'] for i in range(len(self.chunks))],
            'category_tags': [preprocessed_data['tags'][i]['category'] for i in range(len(self.chunks))]
        })
        
        # Save to CSV
        chunks_df.to_csv(output_path, index=False)
        print(f"Preprocessed data saved to {output_path}")
        
        return chunks_df

def main():
    if len(sys.argv) < 2:
        print("Usage: python rfp_preprocessor.py <path_to_pdf_file> [output_path]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else pdf_path.replace('.pdf', '_preprocessed.csv')
    
    preprocessor = RFPPreprocessor(pdf_path)
    preprocessor.save_preprocessed_data(output_path)

if __name__ == "__main__":
    main()