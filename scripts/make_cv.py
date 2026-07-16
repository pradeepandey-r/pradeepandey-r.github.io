# CV generator: rebuilds Target_Pradeep_Pandey_CV.tex content as an
# ATS-optimized PDF in a choice of standard professional fonts.
#
#   python scripts/make_cv.py                 -> public/cv.pdf in FINAL_FONT
#   python scripts/make_cv.py --font georgia  -> public/cv.pdf in that font
#   python scripts/make_cv.py --all           -> one PDF per font in cv-variants/
#
# ATS rules followed: single-column flow, no tables or text boxes, plain
# uppercase section headings (no letter-spacing tricks: "R E S E A R C H"
# parses as gibberish), standard round bullets, real embedded text.
# Typography per the standard CV spec: name 20-26pt bold, sections 13-15pt
# bold, subheads 11-12pt (italic meta lines for serif), body 10-11.5pt,
# line-height 1.25, 6pt space after paragraphs, 0.75in margins.
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, HRFlowable

FINAL_FONT = "garamond"  # serif, fits one page; change and rerun to switch

SITE_DIR = Path(__file__).resolve().parent.parent
WINFONTS = Path("C:/Windows/Fonts")

ACCENT = HexColor("#1F4E5F")
FADED = HexColor("#7A7A7A")
INK = HexColor("#111111")

# kind decides the typography profile; files = (regular, bold, italic, boldItalic)
FONTS = {
    "helvetica": {"kind": "sans", "builtin": ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique")},
    "segoe": {"kind": "sans", "files": ("segoeui.ttf", "segoeuib.ttf", "segoeuii.ttf", "segoeuiz.ttf")},
    "calibri": {"kind": "sans", "files": ("calibri.ttf", "calibrib.ttf", "calibrii.ttf", "calibriz.ttf")},
    "arial": {"kind": "sans", "files": ("arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf")},
    "georgia": {"kind": "serif", "files": ("georgia.ttf", "georgiab.ttf", "georgiai.ttf", "georgiaz.ttf")},
    "garamond": {"kind": "serif", "files": ("GARA.TTF", "GARABD.TTF", "GARAIT.TTF", "GARABD.TTF")},
    "palatino": {"kind": "serif", "files": ("pala.ttf", "palab.ttf", "palai.ttf", "palabi.ttf")},
}

# sizes per the CV rules; serif a notch larger to compensate for fine strokes
PROFILES = {
    "sans": {"name": 21, "tag": 8, "contact": 9.5, "section": 13, "subhead": 11, "body": 10},
    "serif": {"name": 22, "tag": 8.5, "contact": 10, "section": 14, "subhead": 11.5, "body": 10.5},
}
LINE_HEIGHT = 1.15    # spec floor 1.15 (holds one page)
SPACE_AFTER = 6       # spec: 6-8pt after paragraphs
MARGIN = 0.5 * inch   # spec range 0.5-1in (compact end, to hold one page)


def register(key):
    """Register the family; returns (regular, bold, italic) font names."""
    spec = FONTS[key]
    if "builtin" in spec:
        return spec["builtin"][:3]
    reg, bold, ital, boldital = (f"{key}", f"{key}-b", f"{key}-i", f"{key}-z")
    files = spec["files"]
    pdfmetrics.registerFont(TTFont(reg, str(WINFONTS / files[0])))
    pdfmetrics.registerFont(TTFont(bold, str(WINFONTS / files[1])))
    pdfmetrics.registerFont(TTFont(ital, str(WINFONTS / files[2])))
    pdfmetrics.registerFont(TTFont(boldital, str(WINFONTS / files[3])))
    registerFontFamily(reg, normal=reg, bold=bold, italic=ital, boldItalic=boldital)
    return reg, bold, ital


def build(key, out_path):
    spec = FONTS[key]
    kind = spec["kind"]
    P = PROFILES[kind]
    REG, BOLD, ITAL = register(key)
    serif = kind == "serif"

    W, H = A4
    M = MARGIN
    USABLE = W - 2 * M
    lh = lambda size: round(size * LINE_HEIGHT, 1)

    S = dict(
        name=ParagraphStyle("name", fontName=BOLD, fontSize=P["name"], leading=lh(P["name"]),
                            alignment=TA_CENTER, textColor=INK, spaceAfter=2),
        tagline=ParagraphStyle("tagline", fontName=REG, fontSize=P["tag"], leading=lh(P["tag"]),
                               alignment=TA_CENTER, textColor=FADED, spaceAfter=3),
        contact=ParagraphStyle("contact", fontName=REG, fontSize=P["contact"], leading=lh(P["contact"]),
                               alignment=TA_CENTER, textColor=INK, spaceAfter=2),
        section=ParagraphStyle("section", fontName=BOLD, fontSize=P["section"], leading=lh(P["section"]),
                               textColor=ACCENT, spaceBefore=5, spaceAfter=2),
        body=ParagraphStyle("body", fontName=REG, fontSize=P["body"], leading=lh(P["body"]),
                            textColor=INK, spaceAfter=SPACE_AFTER),
        entryTitle=ParagraphStyle("entryTitle", fontName=REG, fontSize=P["subhead"], leading=lh(P["subhead"]),
                                  textColor=INK, spaceBefore=2, spaceAfter=2),
        bullet=ParagraphStyle("bullet", fontName=REG, fontSize=P["body"], leading=lh(P["body"]),
                              textColor=INK, leftIndent=12, bulletIndent=2, spaceAfter=3,
                              bulletFontName=REG, bulletFontSize=P["body"], bulletColor=ACCENT),
    )
    S["bullet_end"] = ParagraphStyle("bullet_end", parent=S["bullet"], spaceAfter=SPACE_AFTER)

    def section(title):
        # plain uppercase, no letter-spacing: ATS parsers read spaced caps as gibberish
        return [
            Paragraph(title.upper(), S["section"]),
            HRFlowable(width="100%", thickness=0.7, color=ACCENT, spaceBefore=0, spaceAfter=4),
        ]

    def entry(title, meta):
        # single linear paragraph, no table (ATS-safe): bold title, then the
        # location/dates in smaller muted text (italic for serif families)
        meta_txt = f"<i>{meta}</i>" if serif else meta
        return [Paragraph(
            f'<b>{title}</b> &nbsp;·&nbsp; <font size="{P["subhead"] - 2}" color="#7A7A7A">{meta_txt}</font>',
            S["entryTitle"])]

    def bullets(items):
        out = []
        for i, txt in enumerate(items):
            style = S["bullet_end"] if i == len(items) - 1 else S["bullet"]
            out.append(Paragraph(txt, style, bulletText="•"))
        return out

    A = 'color="#1F4E5F"'
    story = []
    story.append(Paragraph("PRADEEP PANDEY", S["name"]))
    story.append(Paragraph("Target Profile · November 2028", S["tagline"]))
    story.append(Paragraph(
        'Kathmandu, Nepal · +977 9867716735 · '
        f'<a href="mailto:pradeepandey.r@gmail.com"><font {A}>pradeepandey.r@gmail.com</font></a> · '
        f'<a href="https://pradeeppandey.name.np"><font {A}>pradeeppandey.name.np</font></a> · '
        f'<a href="https://github.com/pradeepandey-r"><font {A}>github.com/pradeepandey-r</font></a>',
        S["contact"]))

    story += section("Research Interests")
    story.append(Paragraph(
        "Robustness and interpretability of aligned behavior in open-weight language models: how refusal and other "
        "safety behaviors hold up under perturbation, what activation-level structure underlies them, and how to "
        "evaluate both rigorously at low compute.", S["body"]))

    story += section("Education")
    story += entry("Tribhuvan University: Bachelor of Computer Application (BCA)",
                   "Kathmandu, Nepal · Expected Nov 2028")
    story += bullets([
        "Final-year project: an activation-probing evaluation suite for small open-weight LLMs, co-supervised with "
        "TU faculty as a companion study to the preprint below.",
        "Additional training: ARENA Chapters 0, 1, 3 (self-directed, 2027–2028); NPTEL (IIT) certified Calculus, "
        "credit-bearing (2026).",
    ])

    story += section("Publications and Preprints")
    story += bullets([
        "<b>[1] Pandey, P.</b> (2028). <i>How Stable Is Refusal? Behavioral and Activation-Level Robustness in Small "
        "Open-Weight Language Models.</i> arXiv:2808.04217 [cs.LG]. Accepted at <b>BlackboxNLP 2028</b> (co-located "
        f'with EMNLP 2028). Code and data: <a href="https://github.com/pradeepandey-r"><font {A}>github.com/'
        "pradeepandey-r/refusal-stability</font></a>.",
        "<b>[2] Pandey, P.</b> (2027). <i>Independent Replication of “Refusal in Language Models Is Mediated by a "
        "Single Direction” (Arditi et al., 2024), extended to Gemma-2-2B and Qwen2.5-1.5B.</i> Technical note. "
        f'Code: <a href="https://github.com/pradeepandey-r"><font {A}>github.com/pradeepandey-r/refusal-direction-replication</font></a>.',
    ])

    story += section("Research Experience")
    story += entry("Independent Researcher: Refusal-Robustness Study", "Kathmandu, Nepal · Mar 2028 – Aug 2028")
    story += bullets([
        "Designed and pre-registered a robustness study of refusal behavior: 240 refusal-eliciting base prompts from "
        "public safety benchmarks under 5 semantics-preserving perturbation families, run against six open-weight "
        "models (1.5B–9B); 8,640 completions scored on an automated Inspect harness for $287 of a $500 compute envelope.",
        "Core finding of [1]: worst-case behavioral refusal consistency fell by 31 percentage points under multi-turn "
        "decomposition, while linear probes on residual-stream activations (TransformerLens) retained AUC at or above "
        "0.92; behavioral robustness and internal detectability come apart under perturbation.",
    ])
    story += entry("SPAR (Supervised Program for Alignment Research): Research Fellow", "Remote · Sep 2027 – Dec 2027")
    story += bullets([
        "Selected for the Fall 2027 cohort. Investigated scale-sensitivity of refusal-direction ablation across three "
        "open-weight model families under the mentorship of an alignment researcher; the cohort project's experimental "
        "design became the seed of [1].",
    ])
    story += entry("NAAMII: Research Intern, Applied ML", "Lalitpur, Nepal · Mar 2028 – May 2028")
    story += bullets([
        "Built the group's internal robustness-evaluation pipeline for open-weight LLMs on Inspect (14 task suites, "
        "versioned datasets, cached generations), replacing ad-hoc per-project scripts; the pipeline is reused across "
        "two ongoing projects at the institute.",
    ])

    story += section("Industry Experience")
    story += entry("Flipkart: Machine Learning Intern, Trust and Safety", "Remote (Bengaluru, India) · Jun 2027 – Aug 2027")
    story += bullets([
        "Shipped an offline regression-evaluation suite for a production abuse-text classifier: frozen evaluation sets, "
        "drift checks against weekly traffic samples, and a release scorecard the team adopted for model sign-off.",
    ])

    story += section("Open-Source Contributions")
    story += entry("TransformerLens: Contributor (feature merged)", "Remote · Jan 2028")
    story += bullets([
        "Wrote, tested, and merged a batched activation-caching utility for the hooks API, with documentation and CI "
        "tests; the same code path drives the analysis pipelines behind [1] and [2].",
    ])

    story += section("Selected Writing and Grants")
    story.append(Paragraph(
        f'Nine technical articles at <a href="https://pradeeppandey.name.np"><font {A}>pradeeppandey.name.np</font></a> '
        "and six LessWrong / Alignment Forum posts on evaluation methodology and interpretability, including "
        "<i>Designing a Small-Scale Safety Experiment</i> (2028) and <i>Anatomy of the Transformer</i> (2027). "
        "Manifund micro-grant: independent compute funding for the refusal-robustness study (2027).", S["body"]))

    story += section("Technical Skills")
    story.append(Paragraph(
        "Python, PyTorch, TransformerLens, Inspect (UK AISI), lm-evaluation-harness, "
        "Hugging Face Transformers, NumPy, pandas, Git, Linux, LaTeX", S["body"]))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(REG, 7)
        canvas.setFillColor(FADED)
        canvas.drawCentredString(
            W / 2, 0.45 * cm,
            "Demonstration CV: target profile of a 30-month research roadmap (June 2026 – November 2028).")
        canvas.restoreState()

    doc = BaseDocTemplate(
        str(out_path), pagesize=A4, leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M,
        title="Pradeep Pandey: CV (Target Profile, November 2028)", author="Pradeep Pandey",
        subject="Demonstration CV: roadmap target profile",
    )
    frame = Frame(M, M, USABLE, H - 2 * M, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="cv", frames=[frame], onPage=footer)])
    doc.build(story)

    from pypdf import PdfReader
    pages = len(PdfReader(str(out_path)).pages)
    print(f"{key:10s} ({kind:5s}) -> {out_path}  [{pages} page{'s' if pages > 1 else ''}]")
    return pages


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--all" in args:
        outdir = SITE_DIR / "cv-variants"
        outdir.mkdir(exist_ok=True)
        for key in FONTS:
            build(key, outdir / f"cv-{key}.pdf")
        print(f"\nOpen {outdir} and pick one; then set FINAL_FONT in this script and rerun without --all.")
    else:
        key = args[args.index("--font") + 1] if "--font" in args else FINAL_FONT
        build(key, SITE_DIR / "public" / "cv.pdf")
