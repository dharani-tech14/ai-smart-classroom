import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import streamlit as st

class NLPProcessor:
    """Process text using NLP."""

    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))

    def extract_keywords(self, text, num_keywords=5):
        """Extract important keywords from text."""
        try:
            words = word_tokenize(text.lower())

            filtered_words = [
                w for w in words 
                if w.isalnum() and w not in self.stop_words
            ]

            freq_dist = FreqDist(filtered_words)
            keywords = freq_dist.most_common(num_keywords)

            return [kw[0] for kw in keywords]

        except Exception as e:
            st.error(f"Keyword Error: {str(e)}")
            return []

    def summarize_text(self, text, num_sentences=3):
        """Summarize text using frequency scoring."""
        try:
            sentences = sent_tokenize(text)

            if len(sentences) <= num_sentences:
                return text

            words = word_tokenize(text.lower())

            filtered_words = [
                w for w in words 
                if w.isalnum() and w not in self.stop_words
            ]

            freq_dist = FreqDist(filtered_words)

            # Score sentences
            sentence_scores = {}

            for sentence in sentences:
                for word in word_tokenize(sentence.lower()):
                    if word in freq_dist:
                        if sentence not in sentence_scores:
                            sentence_scores[sentence] = freq_dist[word]
                        else:
                            sentence_scores[sentence] += freq_dist[word]

            # Sort sentences by score
            sorted_sentences = sorted(
                sentence_scores, 
                key=sentence_scores.get, 
                reverse=True
            )

            summary = " ".join(sorted_sentences[:num_sentences])

            return summary

        except Exception as e:
            st.error(f"Summarization Error: {str(e)}")
            return text