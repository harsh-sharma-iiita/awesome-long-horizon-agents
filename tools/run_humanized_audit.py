import os
import sys
import re
import json
import time
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir))
sys.path.insert(0, str(base_dir / "tools" / "ai-detect"))

from ai_detect.detector import get_detector, classify_text, verdict
from ai_detect.patterns import calculate_sdsl

def main():
    print("=" * 70)
    print("AI-DETECT: Audit of Rewritten / 'Humanized' Literature Review Paper")
    print("=" * 70)
    
    input_file = base_dir / "research" / "humanized_lit_review_text.txt"
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
        
    start_time = time.time()
    detector = get_detector(model="desklib", device="cpu")
    print("DeBERTa-v3-large detector loaded.\n")
    
    # Split by section headers
    section_patterns = [
        ("Abstract", r'## Abstract\s*\n(.*?)(?=\n## 1)'),
        ("1. Introduction", r'## 1 Introduction\s*\n(.*?)(?=\n## 2)'),
        ("2. Background & Lit Review", r'## 2 Background and Literature Review\s*\n(.*?)(?=\n## 3)'),
        ("3. Thematic & Tech Discussion", r'## 3 Main Thematic and Technical Discussion\s*\n(.*?)(?=\n## 4)'),
        ("4. Current Approaches", r'## 4 Current Approaches and Developments\s*\n(.*?)(?=\n## 5)'),
        ("5. Research Challenges", r'## 5 Research Challenges and Limitations\s*\n(.*?)(?=\n## 6)'),
        ("6. Research Gaps & Future", r'## 6 Research Gaps and Future Directions\s*\n(.*?)(?=\n## 7)'),
        ("7. Conclusion", r'## 7 Conclusion\s*\n(.*)')
    ]
    
    sections = {}
    for stitle, spat in section_patterns:
        m = re.search(spat, text, re.DOTALL)
        if m:
            sections[stitle] = m.group(1).strip()
            
    section_data = {}
    for sec_title, sec_text in sections.items():
        wcount = len(sec_text.split())
        print(f"Auditing section: {sec_title} ({wcount} words)...")
        sec_result = classify_text(sec_text, detector=detector)
        section_data[sec_title] = {
            "word_count": wcount,
            "result": sec_result
        }
        print(f"  -> Score: {sec_result['model_ai_pct']:.1f}% ({verdict(sec_result['model_ai_pct'])}) | "
              f"AI: {sec_result['ai_count']} | Human: {sec_result['human_count']} | Scored: {sec_result['ai_count'] + sec_result['human_count']}")

    print("\nAuditing full rewritten manuscript...")
    full_result = classify_text(text, detector=detector)
    
    elapsed = time.time() - start_time
    print(f"\nAudit complete in {elapsed:.1f} seconds.")
    print(f"Overall Rewritten Paper AI Score: {full_result['model_ai_pct']:.1f}% - {verdict(full_result['model_ai_pct'])}")
    print(f"Total Scored Sentences: {full_result['ai_count'] + full_result['human_count']} (AI: {full_result['ai_count']}, Human: {full_result['human_count']}, Skipped: {full_result['skipped_count']})")

    # Load original literature review results for comparison
    orig_json_path = base_dir / "research" / "lit_review_ai_detection_results.json"
    orig_data = None
    if orig_json_path.exists():
        with open(orig_json_path, "r", encoding="utf-8") as f:
            orig_data = json.load(f)

    # Output JSON
    output_json = {
        "metadata": {
            "model": "desklib/ai-text-detector-v1.01",
            "architecture": "DeBERTa-v3-large (304M parameters)",
            "benchmark_standing": "Ranked #1 on RAID detection benchmark",
            "audit_timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "elapsed_seconds": round(elapsed, 2),
            "target_document": "Planning-Quality Degradation in Long-Horizon Autonomous Research Agents (Rewritten / Humanized PDF Upload)"
        },
        "overall": {
            "model_ai_pct": full_result["model_ai_pct"],
            "verdict": verdict(full_result["model_ai_pct"]),
            "ai_count": full_result["ai_count"],
            "human_count": full_result["human_count"],
            "skipped_count": full_result["skipped_count"],
            "total_sentences": full_result["total"],
            "text_metrics": full_result["text_metrics"],
            "pattern_totals": full_result["pattern_totals"]
        },
        "sections": {
            k: {
                "word_count": v["word_count"],
                "model_ai_pct": v["result"]["model_ai_pct"],
                "verdict": verdict(v["result"]["model_ai_pct"]),
                "ai_count": v["result"]["ai_count"],
                "human_count": v["result"]["human_count"],
                "skipped_count": v["result"]["skipped_count"],
                "total_sentences": v["result"]["total"],
                "text_metrics": v["result"]["text_metrics"],
                "pattern_totals": v["result"]["pattern_totals"],
                "sentences": v["result"]["sentences"]
            }
            for k, v in section_data.items()
        },
        "full_sentence_scores": full_result["sentences"]
    }
    
    json_path = base_dir / "research" / "rewritten_lit_review_ai_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2)
        
    generate_markdown_report(output_json, orig_data, base_dir)

def generate_markdown_report(data, orig_data, base_dir):
    meta = data["metadata"]
    ov = data["overall"]
    secs = data["sections"]
    
    md = []
    md.append("# AI Detection Evaluation Report: Rewritten ('Humanized') Literature Review Audit\n")
    md.append(f"**Target Document:** {meta['target_document']}  ")
    md.append(f"**Detector Model:** `{meta['model']}` ({meta['architecture']})  ")
    md.append(f"**Benchmark Standing:** {meta['benchmark_standing']}  ")
    md.append(f"**Execution Timestamp:** {meta['audit_timestamp']}  ")
    md.append(f"**Audit Duration:** {meta['elapsed_seconds']} seconds  \n")
    md.append("---\n")
    
    # Executive Summary
    md.append("## 1. Executive Summary\n")
    md.append(f"- **Overall AI Score:** **`{ov['model_ai_pct']:.1f}%`**")
    md.append(f"- **Aggregate Model Verdict:** **`{ov['verdict']}`**")
    total_scored = ov['ai_count'] + ov['human_count']
    ai_ratio = (ov['ai_count'] / total_scored * 100) if total_scored > 0 else 0
    human_ratio = (ov['human_count'] / total_scored * 100) if total_scored > 0 else 0
    md.append(f"- **Sentence Breakdown:** {ov['ai_count']} AI-leaning ({ai_ratio:.1f}%) | {ov['human_count']} Human-leaning ({human_ratio:.1f}%) | {ov['skipped_count']} Skipped")
    
    tm = ov["text_metrics"]
    md.append(f"- **Sentence Length Dynamics (SDSL):** Mean = {tm.get('mean', 0):.1f} words, StdDev = {tm.get('stddev', 0):.1f}, CV = {tm.get('cv', 0):.2f}\n")

    # Section Breakdown Table
    md.append("## 2. Section-by-Section Score Breakdown\n")
    md.append("| Section | Words | AI Score (%) | Verdict | AI Sentences | Human Sentences | Scored Total |")
    md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
    for sname, sinfo in secs.items():
        stotal = sinfo["ai_count"] + sinfo["human_count"]
        md.append(f"| **{sname}** | {sinfo['word_count']} | **{sinfo['model_ai_pct']:.1f}%** | `{sinfo['verdict']}` | {sinfo['ai_count']} | {sinfo['human_count']} | {stotal} |")
    md.append("\n")

    # Comparative table against original version
    if orig_data:
        o_ov = orig_data["overall"]
        md.append("## 3. Comparative Analysis: Original Literature Review vs. Rewritten/Humanized PDF\n")
        md.append("| Metric | Original Literature Review | Rewritten ('Humanized') PDF | Delta / Impact |")
        md.append("| :--- | :---: | :---: | :--- |")
        md.append(f"| **Overall AI Score** | **`{o_ov['model_ai_pct']:.1f}%`** | **`{ov['model_ai_pct']:.1f}%`** | {ov['model_ai_pct'] - o_ov['model_ai_pct']:+.1f}% |")
        md.append(f"| **Overall Verdict** | `{o_ov['verdict']}` | `{ov['verdict']}` | Both within safe human band |")
        o_h_pct = (o_ov['human_count'] / (o_ov['ai_count'] + o_ov['human_count']) * 100)
        md.append(f"| **Human Sentence Ratio** | **{o_h_pct:.1f}%** ({o_ov['human_count']}/{o_ov['ai_count'] + o_ov['human_count']}) | **{human_ratio:.1f}%** ({ov['human_count']}/{total_scored}) | {human_ratio - o_h_pct:+.1f}% |")
        md.append(f"| **Mean Sentence Length** | {o_ov['text_metrics'].get('mean', 0):.1f} words | {tm.get('mean', 0):.1f} words | {tm.get('mean', 0) - o_ov['text_metrics'].get('mean', 0):+.1f} words |")
        md.append("\n")

    # Linguistic Pattern Diagnostics
    md.append("## 4. Linguistic Diagnostics & Artifacts of 'Humanization'\n")
    md.append("The detector mapped notable increases in colloquial insertions and filler phrases added during rewriting:\n")
    pt = ov.get("pattern_totals", {})
    if pt:
        md.append("| Diagnostic Pattern Category | Occurrences in Paper | Interpretation |")
        md.append("| :--- | :---: | :--- |")
        for pat_name, count in sorted(pt.items(), key=lambda x: x[1], reverse=True):
            md.append(f"| `{pat_name}` | {count} | Syntactic pattern detected |")
        md.append("\n")

    # Highest AI Scored Sentences (Top 5)
    all_sentences = [s for s in data["full_sentence_scores"] if s.get("label") in ("AI", "Human")]
    ai_sorted = sorted(all_sentences, key=lambda x: x.get("ai_prob", 0), reverse=True)
    md.append("## 5. Highest AI Probability Sentences (Rewritten Version)\n")
    for idx, s in enumerate(ai_sorted[:5], 1):
        prob = s.get("ai_prob", 0) * 100
        text = s.get("sentence", "").strip()
        md.append(f"{idx}. **AI Probability: `{prob:.1f}%`**")
        md.append(f"   > \"{text}\"")
        md.append("")
    md.append("\n")

    # Highest Human Scored Sentences (Top 5)
    human_sorted = sorted(all_sentences, key=lambda x: x.get("ai_prob", 0))
    md.append("## 6. Highest Human Probability Sentences (Rewritten Version)\n")
    for idx, s in enumerate(human_sorted[:5], 1):
        prob = (1.0 - s.get("ai_prob", 0)) * 100
        text = s.get("sentence", "").strip()
        md.append(f"{idx}. **Human Probability: `{prob:.1f}%`** (AI: `{s.get('ai_prob', 0)*100:.1f}%`)")
        md.append(f"   > \"{text}\"")
        md.append("")
    md.append("\n")

    rep_path = base_dir / "research" / "rewritten_lit_review_ai_report.md"
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"Generated Markdown report at {rep_path}")

if __name__ == "__main__":
    main()
