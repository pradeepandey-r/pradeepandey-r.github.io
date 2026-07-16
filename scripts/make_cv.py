# Recreates Target_Pradeep_Pandey_CV.tex as a one-page A4 PDF (no LaTeX needed).
# Faithful to the source, including its self-labeling as a demonstration/target
# profile. Contacts normalized to the real handles used on the site.
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)

ACCENT = HexColor("#1F4E5F")
FADED = HexColor("#7A7A7A")
INK = HexColor("#111111")

OUT = r"K:\research-roadmap\personal-website\public\cv.pdf"

W, H = A4
ML, MR, MT, MB = 1.4 * cm, 1.4 * cm, 1.0 * cm, 1.35 * cm
USABLE = W - ML - MR

S = dict(
    name=ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=16.5, leading=19,
                        alignment=TA_CENTER, textColor=INK, spaceAfter=1),
    tagline=ParagraphStyle("tagline", fontName="Helvetica", fontSize=7.6, leading=9.5,
                           alignment=TA_CENTER, textColor=FADED, spaceAfter=2),
    contact=ParagraphStyle("contact", fontName="Helvetica", fontSize=8.6, leading=11,
                           alignment=TA_CENTER, textColor=INK, spaceAfter=0),
    section=ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=8.2, leading=10,
                           textColor=ACCENT, spaceBefore=7, spaceAfter=1),
    body=ParagraphStyle("body", fontName="Helvetica", fontSize=8.7, leading=10.8,
                        textColor=INK, spaceAfter=2),
    entryL=ParagraphStyle("entryL", fontName="Helvetica-Bold", fontSize=8.9, leading=10.8, textColor=INK),
    entryR=ParagraphStyle("entryR", fontName="Helvetica", fontSize=8.2, leading=10.8,
                          textColor=FADED, alignment=2),
    bullet=ParagraphStyle("bullet", fontName="Helvetica", fontSize=8.7, leading=10.7,
                          textColor=INK, leftIndent=10, bulletIndent=2, spaceAfter=1,
                          bulletFontName="Helvetica-Bold", bulletFontSize=8.7, bulletColor=ACCENT),
)

def sp(text):  # letterspaced small-caps-ish section title, word gaps preserved
    return "&nbsp;&nbsp;&nbsp;".join(" ".join(word) for word in text.upper().split())

def section(title):
    return [
        Paragraph(sp(title), S["section"]),
        HRFlowable(width="100%", thickness=0.6, color=ACCENT, spaceBefore=0, spaceAfter=3.5),
    ]

def entry(left, right):
    t = Table(
        [[Paragraph(left, S["entryL"]), Paragraph(right, S["entryR"])]],
        colWidths=[USABLE * 0.60, USABLE * 0.40],
    )
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t

def bullets(items):
    return [Paragraph(i, S["bullet"], bulletText="•") for i in items]

A = f'color="#1F4E5F"'
story = []

# ---------- header ----------
story.append(Paragraph("PRADEEP PANDEY", S["name"]))
story.append(Paragraph("T A R G E T&nbsp;&nbsp;P R O F I L E&nbsp;&nbsp;·&nbsp;&nbsp;N O V E M B E R&nbsp;&nbsp;2 0 2 8", S["tagline"]))
story.append(Paragraph(
    'Kathmandu, Nepal · +977 9867716735 · '
    f'<a href="mailto:pradeepandey.r@gmail.com"><font {A}>pradeepandey.r@gmail.com</font></a> · '
    f'<a href="https://pradeepandey-r.github.io"><font {A}>pradeepandey-r.github.io</font></a> · '
    f'<a href="https://github.com/pradeepandey-r"><font {A}>github.com/pradeepandey-r</font></a>',
    S["contact"]))
story.append(Spacer(1, 2))

# ---------- research interests ----------
story += section("Research Interests")
story.append(Paragraph(
    "Robustness and interpretability of aligned behavior in open-weight language models: how refusal and other "
    "safety behaviors hold up under perturbation, what activation-level structure underlies them, and how to "
    "evaluate both rigorously at low compute.", S["body"]))

# ---------- education ----------
story += section("Education")
story.append(entry("Tribhuvan University: Bachelor of Computer Application (BCA)", "Kathmandu, Nepal · Nov 2028"))
story += bullets([
    "Final-year project: an activation-probing evaluation suite for small open-weight LLMs, co-supervised with "
    "TU faculty as a companion study to the preprint below.",
    "Additional training: ARENA Chapters 0, 1, 3 (self-directed, 2027–2028); NPTEL (IIT) certified Calculus, "
    "credit-bearing (2026).",
])

# ---------- publications ----------
story += section("Publications & Preprints")
story += bullets([
    "<b>[1] Pandey, P.</b> (2028). <i>How Stable Is Refusal? Behavioral and Activation-Level Robustness in Small "
    "Open-Weight Language Models.</i> arXiv:2808.04217 [cs.LG]. Accepted at <b>BlackboxNLP 2028</b> (co-located "
    f'with EMNLP 2028). Code and data: <a href="https://github.com/pradeepandey-r"><font {A}>github.com/pradeepandey-r/'
    "refusal-stability</font></a>.",
    "<b>[2] Pandey, P.</b> (2027). <i>Independent Replication of “Refusal in Language Models Is Mediated by a "
    "Single Direction” (Arditi et al., 2024), extended to Gemma-2-2B and Qwen2.5-1.5B.</i> Technical note. "
    f'Code: <a href="https://github.com/pradeepandey-r"><font {A}>github.com/pradeepandey-r/refusal-direction-replication</font></a>.',
])

# ---------- research experience ----------
story += section("Research Experience")
story.append(entry("Independent Researcher: Refusal-Robustness Study", "Kathmandu, Nepal · Mar – Aug 2028"))
story += bullets([
    "Designed and pre-registered a robustness study of refusal behavior: 240 refusal-eliciting base prompts from "
    "public safety benchmarks under 5 semantics-preserving perturbation families, run against six open-weight "
    "models (1.5B–9B); 8,640 completions scored on an automated Inspect harness for $287 of a $500 compute envelope.",
    "Core finding of [1]: worst-case behavioral refusal consistency fell by 31 percentage points under multi-turn "
    "decomposition, while linear probes on residual-stream activations (TransformerLens) retained AUC at or above "
    "0.92; behavioral robustness and internal detectability come apart under perturbation.",
])
story.append(entry("SPAR (Supervised Program for Alignment Research): Research Fellow", "Remote · Sep – Dec 2027"))
story += bullets([
    "Selected for the Fall 2027 cohort. Investigated scale-sensitivity of refusal-direction ablation across three "
    "open-weight model families under the mentorship of an alignment researcher; the cohort project's experimental "
    "design became the seed of [1].",
])
story.append(entry("NAAMII: Research Intern, Applied ML", "Lalitpur, Nepal · Mar – May 2028"))
story += bullets([
    "Built the group's internal robustness-evaluation pipeline for open-weight LLMs on Inspect (14 task suites, "
    "versioned datasets, cached generations), replacing ad-hoc per-project scripts; the pipeline is reused across "
    "two ongoing projects at the institute.",
])

# ---------- industry ----------
story += section("Industry Experience")
story.append(entry("Flipkart: Machine Learning Intern, Trust & Safety (Remote)", "Bengaluru, India · Jun – Aug 2027"))
story += bullets([
    "Shipped an offline regression-evaluation suite for a production abuse-text classifier: frozen evaluation sets, "
    "drift checks against weekly traffic samples, and a release scorecard the team adopted for model sign-off.",
])

# ---------- open source ----------
story += section("Open-Source Contributions")
story.append(entry("TransformerLens: Contributor (feature merged)", "Remote · Jan 2028"))
story += bullets([
    "Wrote, tested, and merged a batched activation-caching utility for the hooks API, with documentation and CI "
    "tests; the same code path drives the analysis pipelines behind [1] and [2].",
])

# ---------- writing ----------
story += section("Selected Writing & Grants")
story.append(Paragraph(
    f'Nine technical articles at <a href="https://pradeepandey-r.github.io"><font {A}>pradeepandey-r.github.io</font></a> '
    "and six LessWrong / Alignment Forum posts on evaluation methodology and interpretability, including "
    "<i>Designing a Small-Scale Safety Experiment</i> (2028) and <i>Anatomy of the Transformer</i> (2027). "
    "Manifund micro-grant: independent compute funding for the refusal-robustness study (2027).", S["body"]))

# ---------- skills ----------
story += section("Technical Skills")
story.append(Paragraph(
    "Python · PyTorch · TransformerLens · Inspect (UK AISI) · lm-evaluation-harness · "
    "Hugging Face Transformers · NumPy / pandas · Git · Linux · LaTeX", S["body"]))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(FADED)
    canvas.drawCentredString(
        W / 2, 0.55 * cm,
        "Demonstration CV: target profile of a 30-month research roadmap (June 2026 – November 2028).")
    canvas.restoreState()


doc = BaseDocTemplate(
    OUT, pagesize=A4, leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
    title="Pradeep Pandey: CV (Target Profile, November 2028)", author="Pradeep Pandey",
    subject="Demonstration CV: roadmap target profile",
)
frame = Frame(ML, MB, USABLE, H - MT - MB, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="cv", frames=[frame], onPage=footer)])
doc.build(story)

from pypdf import PdfReader
r = PdfReader(OUT)
print(f"OK: {OUT}")
print(f"pages: {len(r.pages)}")
print(f"title: {r.metadata.title}")
