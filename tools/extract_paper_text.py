import re
import os

SECTIONS = [
    "01_abstract.tex",
    "02_introduction.tex",
    "03_related_work.tex",
    "04_problem_formulation.tex",
    "05_methodology.tex",
    "06_experimental_setup.tex",
    "07_results.tex",
    "08_discussion.tex",
    "09_threats_to_validity.tex",
    "10_limitations.tex",
    "11_conclusion.tex"
]

def clean_latex(text: str) -> str:
    # Remove comments
    lines = []
    for line in text.splitlines():
        line = re.sub(r'(?<!\\)%.*$', '', line)
        lines.append(line)
    text = '\n'.join(lines)
    
    # Remove tables and figures entirely
    text = re.sub(r'\\begin\{(table|figure)\*?\}.*?\\end\{(table|figure)\*?\}', '', text, flags=re.DOTALL)
    
    # Remove equations
    text = re.sub(r'\\begin\{equation\*?\}.*?\\end\{equation\*?\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{align\*?\}.*?\\end\{align\*?\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
    
    # Remove abstract tags
    text = re.sub(r'\\begin\{abstract\}', '', text)
    text = re.sub(r'\\end\{abstract\}', '', text)
    
    # Extract titles from sectioning commands
    text = re.sub(r'\\section\*?\{([^}]+)\}', r'\n\n\1\n', text)
    text = re.sub(r'\\subsection\*?\{([^}]+)\}', r'\n\n\1\n', text)
    text = re.sub(r'\\subsubsection\*?\{([^}]+)\}', r'\n\n\1\n', text)
    text = re.sub(r'\\paragraph\*?\{([^}]+)\}', r'\n\n\1: ', text)
    
    # Replace citations and references
    text = re.sub(r'\\cite[a-z]*\{[^}]+\}', '', text)
    text = re.sub(r'\\ref\{[^}]+\}', '1', text)
    text = re.sub(r'\\label\{[^}]+\}', '', text)
    
    # Inline formatting commands
    for _ in range(3):  # handle nested commands
        text = re.sub(r'\\(textbf|textit|emph|texttt|textsc|text|mathrm)\{([^}]+)\}', r'\2', text)
    
    # Inline math clean up: e.g. $K=3$ -> K=3, $\mu_{\text{TCF}} = 0.9005$ -> mu_TCF = 0.9005
    text = re.sub(r'\$([^$]+)\$', r'\1', text)
    
    # LaTeX special characters
    text = text.replace(r'\%', '%')
    text = text.replace(r'\&', '&')
    text = text.replace(r'\$', '$')
    text = text.replace(r'\_', '_')
    text = text.replace(r'\#', '#')
    text = text.replace(r'---', '—')
    text = text.replace(r'--', '–')
    text = text.replace(r'``', '"')
    text = text.replace(r"''", '"')
    text = text.replace(r'~', ' ')
    
    # Remove remaining backslash commands with no args or simple args
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = re.sub(r'\{|\}', '', text)
    
    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sections_dir = os.path.join(base_dir, "paper", "sections")
    output_file = os.path.join(base_dir, "paper", "extracted_paper_text.txt")
    
    full_text = []
    
    title = "Verification Scheduling in Long-Horizon Agent Workflows: A Controlled Study of Error Detection, Propagation and Computational Overhead"
    full_text.append(title + "\n\n")
    
    for sec in SECTIONS:
        sec_path = os.path.join(sections_dir, sec)
        if os.path.exists(sec_path):
            with open(sec_path, "r", encoding="utf-8") as f:
                content = f.read()
            cleaned = clean_latex(content)
            full_text.append(cleaned + "\n\n")
        else:
            print(f"Warning: {sec} not found")
            
    combined = "".join(full_text)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(combined)
        
    print(f"Extracted {len(combined.split())} words, {len(combined)} characters to {output_file}")

if __name__ == "__main__":
    main()
