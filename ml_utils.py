import re
from textblob import TextBlob
import nltk
from collections import Counter
nltk.download('punkt', quiet=True)
nltk.download('brown', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

class NLPProcessor:
    @staticmethod
    def analyze_sentiment(text):
        """
        Analyzes the sentiment of the given text using TextBlob.
        Returns a dictionary with polarity, subjectivity, and a label.
        """
        if not text:
            return {"error": "No text provided"}
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.1:
            label = "Positive"
        elif polarity < -0.1:
            label = "Negative"
        else:
            label = "Neutral"
            
        return {
            "polarity": round(polarity, 2),
            "subjectivity": round(subjectivity, 2),
            "label": label
        }

    @staticmethod
    def mine_text(text):
        """
        Extracts key information from text:
        - Keywords (Frequent words excluding stopwords)
        - Entities (Simulated for this demo using Noun Phrase extraction)
        """
        if not text:
            return {"error": "No text provided"}
            
        blob = TextBlob(text)
        noun_phrases = list(blob.noun_phrases)
        
        # Simple frequency distribution for "keywords"
        words = [w.lower() for w in blob.words if len(w) > 3]
        word_counts = Counter(words).most_common(10)
        
        return {
            "noun_phrases": noun_phrases[:10], # Top 10 extracted entities
            "top_keywords": word_counts
        }

class LogAnalyzer:
    @staticmethod
    def analyze_log(log_line):
        """
        Analyzes a single log line (or snippet) for potential security threats.
        Uses regex patterns to identify common attack vectors.
        """
        threats = []
        severity = "Low"
        
        # Patterns for common threats
        patterns = {
            "SQL Injection": r"(?i)(union\s+select|OR\s+1=1|drop\s+table|--)",
            "XSS": r"(?i)(<script>|javascript:|onerror=)",
            "Failed Login": r"(?i)(failed\s+password|authentication\s+failure|invalid\s+user)",
            "Privilege Escalation": r"(?i)(sudo|root|chmod\s+777)",
            "Directory Traversal": r"(?i)(\.\./\.\./|/etc/passwd|c:\\windows)"
        }
        
        for threat_name, pattern in patterns.items():
            if re.search(pattern, log_line):
                threats.append(threat_name)
        
        if threats:
            if any(t in ["SQL Injection", "XSS", "Privilege Escalation"] for t in threats):
                severity = "High"
            else:
                severity = "Medium"
        
        return {
            "is_threat": len(threats) > 0,
            "detected_threats": threats,
            "severity": severity if threats else "None"
        }
