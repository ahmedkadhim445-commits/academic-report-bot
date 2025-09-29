"""Reference formatting module for different citation styles."""

from typing import List, Dict, Any
from datetime import datetime
import random

class Reference:
    """Represents a single reference."""
    
    def __init__(self, title: str, authors: List[str], year: int, 
                 source_type: str = "journal", journal: str = "", 
                 publisher: str = "", url: str = "", volume: str = "", 
                 pages: str = "", doi: str = ""):
        self.title = title
        self.authors = authors
        self.year = year
        self.source_type = source_type  # journal, book, website, conference
        self.journal = journal
        self.publisher = publisher
        self.url = url
        self.volume = volume
        self.pages = pages
        self.doi = doi

class ReferenceFormatter:
    """Formats references according to different citation styles."""
    
    @staticmethod
    def format_authors_apa(authors: List[str]) -> str:
        """Format authors for APA style."""
        if not authors:
            return ""
        
        if len(authors) == 1:
            return authors[0]
        elif len(authors) == 2:
            return f"{authors[0]} & {authors[1]}"
        else:
            return f"{', '.join(authors[:-1])}, & {authors[-1]}"
    
    @staticmethod
    def format_authors_mla(authors: List[str]) -> str:
        """Format authors for MLA style."""
        if not authors:
            return ""
        
        if len(authors) == 1:
            return authors[0]
        elif len(authors) == 2:
            return f"{authors[0]} and {authors[1]}"
        else:
            return f"{authors[0]}, et al."
    
    @staticmethod
    def format_apa(ref: Reference) -> str:
        """Format reference in APA style."""
        authors = ReferenceFormatter.format_authors_apa(ref.authors)
        
        if ref.source_type == "journal":
            result = f"{authors} ({ref.year}). {ref.title}. "
            if ref.journal:
                result += f"*{ref.journal}*"
                if ref.volume:
                    result += f", {ref.volume}"
                if ref.pages:
                    result += f", {ref.pages}"
            if ref.doi:
                result += f". https://doi.org/{ref.doi}"
            return result + "."
            
        elif ref.source_type == "book":
            result = f"{authors} ({ref.year}). *{ref.title}*"
            if ref.publisher:
                result += f". {ref.publisher}"
            return result + "."
            
        elif ref.source_type == "website":
            result = f"{authors} ({ref.year}). {ref.title}. "
            if ref.url:
                result += f"Retrieved from {ref.url}"
            return result
            
        return f"{authors} ({ref.year}). {ref.title}."
    
    @staticmethod
    def format_ieee(ref: Reference) -> str:
        """Format reference in IEEE style."""
        authors = ", ".join(ref.authors) if ref.authors else ""
        
        if ref.source_type == "journal":
            result = f"{authors}, \"{ref.title},\" "
            if ref.journal:
                result += f"*{ref.journal}*"
                if ref.volume:
                    result += f", vol. {ref.volume}"
                if ref.pages:
                    result += f", pp. {ref.pages}"
            result += f", {ref.year}."
            return result
            
        elif ref.source_type == "book":
            result = f"{authors}, *{ref.title}*"
            if ref.publisher:
                result += f". {ref.publisher}"
            result += f", {ref.year}."
            return result
            
        return f"{authors}, \"{ref.title},\" {ref.year}."
    
    @staticmethod
    def format_mla(ref: Reference) -> str:
        """Format reference in MLA style."""
        authors = ReferenceFormatter.format_authors_mla(ref.authors)
        
        if ref.source_type == "journal":
            result = f"{authors}. \"{ref.title}.\" "
            if ref.journal:
                result += f"*{ref.journal}*"
                if ref.volume:
                    result += f", vol. {ref.volume}"
                if ref.pages:
                    result += f", pp. {ref.pages}"
            result += f", {ref.year}."
            return result
            
        elif ref.source_type == "book":
            result = f"{authors}. *{ref.title}*"
            if ref.publisher:
                result += f". {ref.publisher}"
            result += f", {ref.year}."
            return result
            
        return f"{authors}. \"{ref.title}.\" {ref.year}."
    
    @staticmethod
    def format_harvard(ref: Reference) -> str:
        """Format reference in Harvard style."""
        authors = ", ".join(ref.authors) if ref.authors else ""
        
        result = f"{authors} {ref.year}, '{ref.title}'"
        
        if ref.source_type == "journal" and ref.journal:
            result += f", *{ref.journal}*"
            if ref.volume:
                result += f", vol. {ref.volume}"
            if ref.pages:
                result += f", pp. {ref.pages}"
        elif ref.source_type == "book" and ref.publisher:
            result += f", {ref.publisher}"
            
        return result + "."
    
    @staticmethod
    def format_chicago(ref: Reference) -> str:
        """Format reference in Chicago style."""
        authors = ", ".join(ref.authors) if ref.authors else ""
        
        if ref.source_type == "journal":
            result = f"{authors}. \"{ref.title}.\" "
            if ref.journal:
                result += f"*{ref.journal}*"
                if ref.volume:
                    result += f" {ref.volume}"
                if ref.pages:
                    result += f" ({ref.year}): {ref.pages}"
                else:
                    result += f" ({ref.year})"
            return result + "."
            
        elif ref.source_type == "book":
            result = f"{authors}. *{ref.title}*"
            if ref.publisher:
                result += f". {ref.publisher}"
            result += f", {ref.year}."
            return result
            
        return f"{authors}. \"{ref.title}.\" {ref.year}."

def generate_sample_references(count: int = 8, topic: str = "academic research") -> List[Reference]:
    """Generate sample references for a given topic."""
    
    # Sample data for generating references
    sample_authors = [
        ["Smith, J.A.", "Johnson, M.B."],
        ["Brown, K.L."],
        ["Davis, R.C.", "Wilson, A.D.", "Miller, S.E."],
        ["Anderson, P.F.", "Taylor, L.M."],
        ["Thompson, C.R."],
        ["Garcia, M.A.", "Rodriguez, J.L."],
        ["Lee, H.K.", "Kim, S.J."],
        ["White, D.B.", "Black, T.G.", "Green, R.H."],
    ]
    
    sample_titles = [
        f"Advanced Methodologies in {topic.title()}",
        f"Contemporary Approaches to {topic.title()} Analysis",
        f"Innovative Frameworks for {topic.title()} Research",
        f"Theoretical Foundations of {topic.title()}",
        f"Empirical Studies in {topic.title()}",
        f"Modern Perspectives on {topic.title()}",
        f"Computational Methods in {topic.title()}",
        f"Interdisciplinary Approaches to {topic.title()}",
    ]
    
    sample_journals = [
        "Journal of Academic Research",
        "International Review of Studies",
        "Research Quarterly",
        "Academic Perspectives",
        "Contemporary Research Journal",
        "International Journal of Analysis",
        "Research Methods Review",
        "Academic Innovation Journal",
    ]
    
    references = []
    current_year = datetime.now().year
    
    for i in range(count):
        ref = Reference(
            title=sample_titles[i % len(sample_titles)],
            authors=sample_authors[i % len(sample_authors)],
            year=random.randint(current_year - 10, current_year),
            source_type="journal",
            journal=sample_journals[i % len(sample_journals)],
            volume=str(random.randint(1, 50)),
            pages=f"{random.randint(1, 100)}-{random.randint(101, 200)}",
        )
        references.append(ref)
    
    return references

def format_references(references: List[Reference], style: str) -> str:
    """Format a list of references in the specified style."""
    style = style.lower()
    formatted_refs = []
    
    for i, ref in enumerate(references, 1):
        if style == "apa":
            formatted_ref = ReferenceFormatter.format_apa(ref)
        elif style == "ieee":
            formatted_ref = f"[{i}] {ReferenceFormatter.format_ieee(ref)}"
        elif style == "mla":
            formatted_ref = ReferenceFormatter.format_mla(ref)
        elif style == "harvard":
            formatted_ref = ReferenceFormatter.format_harvard(ref)
        elif style == "chicago":
            formatted_ref = ReferenceFormatter.format_chicago(ref)
        else:
            formatted_ref = ReferenceFormatter.format_apa(ref)  # Default to APA
            
        formatted_refs.append(formatted_ref)
    
    return "\n\n".join(formatted_refs)