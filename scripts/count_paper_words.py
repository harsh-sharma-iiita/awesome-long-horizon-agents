import re
from pathlib import Path

def count_words():
    sections_dir = Path("paper/sections")
    files = sorted(list(sections_dir.glob("*.tex")))

    total_words = 0
    section_counts = {}

    for f in files:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        
        # Clean latex macros for word count
        text = re.sub(r"%.*", "", content)
        text = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})?", " ", text)
        text = re.sub(r"[{}\\$%&]", " ", text)
        words = text.split()
        count = len(words)
        section_counts[f.name] = count
        total_words += count

    print("=== WORD COUNT BREAKDOWN BY SECTION ===")
    for name, c in section_counts.items():
        print(f"{name:<35}: {c:>5} words")
    print("-----------------------------------------------------")
    print(f"Total Words (Sections, excl. Bib):   {total_words:>5} words")

    # Also count abstract specifically
    abs_count = section_counts.get("01_abstract.tex", 0)
    print(f"Main Body Words (excl. Abstract & Bib): {total_words - abs_count:>5} words")

if __name__ == "__main__":
    count_words()
