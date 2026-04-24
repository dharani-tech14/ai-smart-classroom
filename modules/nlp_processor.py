import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from config import STOPWORDS
import re

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class NLPProcessor:
    def __init__(self):
        self.stopwords = STOPWORDS
    
    def extract_keywords(self, text, top_n=10):
        """Extract top keywords from text"""
        words = text.lower().split()
        filtered = [w for w in words if w not in self.stopwords and len(w) > 3]
        keywords = Counter(filtered).most_common(top_n)
        return [w[0] for w in keywords]
    
    def generate_summary(self, text, num_sentences=3):
        """Generate summary from text"""
        sentences = sent_tokenize(text)
        
        if len(sentences) <= num_sentences:
            return text
        
        # Score sentences
        word_freq = Counter()
        for word in word_tokenize(text.lower()):
            if word not in self.stopwords and word.isalpha():
                word_freq[word] += 1
        
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    sentence_scores[i] = sentence_scores.get(i, 0) + word_freq[word]
        
        # Get top sentences
        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        top_sentences.sort()
        
        summary = " ".join([sentences[i] for i in top_sentences])
        return summary
    
    def highlight_keywords(self, text, keywords):
        """Highlight keywords in text"""
        highlighted = text
        for keyword in keywords:
            pattern = f"\\b{keyword}\\b"
            highlighted = re.sub(pattern, f"<mark>{keyword}</mark>", highlighted, flags=re.IGNORECASE)
        return highlighted
    
    def generate_smart_notes(self, text, max_notes=5):
        """Generate smart notes from text"""
        sentences = sent_tokenize(text)
        notes = []
        
        for sentence in sentences:
            if len(sentence.split()) > 6:
                notes.append(f"• {sentence.strip()}")
            
            if len(notes) >= max_notes:
                break
        
        return notes
    
    def extract_main_concepts(self, text):
        """Extract main concepts using noun phrases"""
        words = word_tokenize(text)
        pos_tags = nltk.pos_tag(words)
        
        concepts = []
        for word, pos in pos_tags:
            if pos.startswith('NN'):  # Nouns
                concepts.append(word)
        
        # Remove duplicates and return top concepts
        unique_concepts = list(set(concepts))
        return unique_concepts[:10]