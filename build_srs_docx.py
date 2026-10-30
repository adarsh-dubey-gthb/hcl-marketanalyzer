"""
SRS DOCX Generator — Professional Industry Format (IEEE Std 830-1998)
=====================================================================
Autonomous Agentic Web Scraper & Strategic Market Intelligence Analyzer
HCLTech Career Shaper Programme — III Year Industry Project (2025–26)
ABES Engineering College, Ghaziabad
Candidate: Adarsh Dubey (Roll No: 2400320100061)
Project Mentor / Guide: Radhika Singhal
GitHub Repository: https://github.com/adarsh-dubey-gthb/hcl-marketanalyzer.git
"""

import os
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_FILENAME = "SRS_Market_Intelligence_Analyzer.docx"
SUBMISSION_DOCX_FILENAME = "SRS_Market_Intelligence_Analyzer_Adarsh_Dubey_2400320100061.docx"

# Corporate Color Palette
C_NAVY_RGB     = RGBColor(30, 41, 59)     # #1E293B
C_BLUE_RGB     = RGBColor(37, 99, 235)    # #2563EB
C_GRAY_HVY_RGB = RGBColor(51, 65, 85)     # #334155
C_GRAY_MED_RGB = RGBColor(100, 116, 139)  # #64748B
C_TEAL_RGB     = RGBColor(13, 148, 136)   # #0D9488
C_GREEN_RGB    = RGBColor(22, 163, 74)    # #16A34A
C_AMBER_RGB    = RGBColor(217, 119, 6)    # #D97706

HEX_NAVY       = "1E293B"
HEX_BLUE       = "2563EB"
HEX_BLUE_LIGHT = "EFF6FF"
HEX_GRAY_PALE  = "F8FAFC"
HEX_GRAY_LITE  = "E2E8F0"
HEX_BORDER     = "CBD5E1"
HEX_AMBER_BG   = "FFFBEB"
HEX_AMBER_BRD  = "FDE68A"


def set_cell_background(cell, hex_color):
    shd = f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shd))


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, border_color=HEX_BORDER, sz="4"):
    tblPr = table._tbl.tblPr
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
        <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{border_color}"/>
        <w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{border_color}"/>
        <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{border_color}"/>
        <w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{border_color}"/>
        <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{border_color}"/>
        <w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{border_color}"/>
    </w:tblBorders>
    '''
    tblPr.append(parse_xml(borders_xml))


def add_callout_box(doc, text, title=None, border_color=HEX_BLUE, bg_color=HEX_BLUE_LIGHT):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.8)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    borders_xml = f'''
    <w:tcBorders {nsdecls("w")}>
        <w:top w:val="none"/>
        <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>
        <w:bottom w:val="none"/>
        <w:right w:val="none"/>
    </w:tcBorders>
    '''
    cell._tc.get_or_add_tcPr().append(parse_xml(borders_xml))
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if title:
        run_title = p.add_run(title + "\n")
        run_title.bold = True
        run_title.font.name = "Calibri"
        run_title.font.size = Pt(10)
        run_title.font.color.rgb = RGBColor(37, 99, 235)
    
    run_txt = p.add_run(text)
    run_txt.font.name = "Calibri"
    run_txt.font.size = Pt(9.5)
    run_txt.font.color.rgb = RGBColor(51, 65, 85)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(level=level)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = "Calibri"
    if level == 1:
        run.bold = True
        run.font.size = Pt(14)
        run.font.color.rgb = C_NAVY_RGB
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
    elif level == 2:
        run.bold = True
        run.font.size = Pt(11.5)
        run.font.color.rgb = C_BLUE_RGB
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(3)
    elif level == 3:
        run.bold = True
        run.font.size = Pt(10.5)
        run.font.color.rgb = C_NAVY_RGB
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
    return h


def add_para_styled(doc, text, bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(9.5)
        r_pre.font.color.rgb = C_NAVY_RGB
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.color.rgb = C_GRAY_HVY_RGB
    return p


def add_bullet_styled(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(9.5)
        r_pre.font.color.rgb = C_NAVY_RGB
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.color.rgb = C_GRAY_HVY_RGB
    return p


def add_image_with_caption(doc, img_path, caption_text, width_inches=6.4):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        r_img = p_img.add_run()
        r_img.add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run(caption_text)
        r_cap.italic = True
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(8.5)
        r_cap.font.color.rgb = C_GRAY_MED_RGB


def build_srs_docx():
    doc = Document()
    
    # Page Setup (Letter, 0.75-inch margins)
    for s in doc.sections:
        s.page_width = Inches(8.5)
        s.page_height = Inches(11.0)
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)
        
        # Header / Footer setup
        header = s.header
        p_hdr = header.paragraphs[0]
        p_hdr.text = "SOFTWARE REQUIREMENTS SPECIFICATION (IEEE Std 830-1998) | Project 81"
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.runs[0].font.name = "Calibri"
        p_hdr.runs[0].font.size = Pt(8)
        p_hdr.runs[0].font.color.rgb = C_GRAY_MED_RGB
        
        footer = s.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.text = "HCLTech Career Shaper (2025–26) | ABES Engineering College | Guide: Radhika Singhal"
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_ftr.runs[0].font.name = "Calibri"
        p_ftr.runs[0].font.size = Pt(8)
        p_ftr.runs[0].font.color.rgb = C_GRAY_MED_RGB

    # ═════════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ═════════════════════════════════════════════════════════════════════════
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(8)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("ABES ENGINEERING COLLEGE, GHAZIABAD\n")
    r_inst.bold = True
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(13)
    r_inst.font.color.rgb = C_NAVY_RGB
    
    r_dept = p_inst.add_run("Department of Computer Science & Engineering | Academic Year 2025–26\n")
    r_dept.font.name = "Calibri"
    r_dept.font.size = Pt(9.5)
    r_dept.font.color.rgb = C_GRAY_MED_RGB
    
    r_prog = p_inst.add_run("HCLTech Career Shaper Programme — III Year Industry Project")
    r_prog.bold = True
    r_prog.font.name = "Calibri"
    r_prog.font.size = Pt(10)
    r_prog.font.color.rgb = C_BLUE_RGB

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(2)
    r_t1 = p_title.add_run("SOFTWARE REQUIREMENTS SPECIFICATION\n")
    r_t1.bold = True
    r_t1.font.name = "Calibri"
    r_t1.font.size = Pt(17)
    r_t1.font.color.rgb = C_BLUE_RGB
    
    r_t2 = p_title.add_run("Autonomous Agentic Web Scraper & Strategic Market Intelligence Analyzer\n")
    r_t2.bold = True
    r_t2.font.name = "Calibri"
    r_t2.font.size = Pt(12.5)
    r_t2.font.color.rgb = C_NAVY_RGB
    
    r_t3 = p_title.add_run("A Multi-Stage ReAct Intelligence Agent for Autonomous Web Research, Competitive Benchmarking, and Structured Synthesis")
    r_t3.italic = True
    r_t3.font.name = "Calibri"
    r_t3.font.size = Pt(9)
    r_t3.font.color.rgb = C_GRAY_MED_RGB

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Metadata Table
    cov_rows = [
        ("Project ID & Title", "Project 81: Agentic Web Scraper and Market Intelligence Reporter"),
        ("Programme / Domain", "HCLTech Career Shaper Programme (2025–26) | Agentic AI / Python"),
        ("Student Name", "Adarsh Dubey"),
        ("University Roll No.", "2400320100061"),
        ("Department / College", "Computer Science & Engineering, ABES Engineering College, Ghaziabad"),
        ("Project Mentor / Guide", "Radhika Singhal"),
        ("GitHub Repository", "https://github.com/adarsh-dubey-gthb/hcl-marketanalyzer.git"),
        ("Live Streamlit App", "https://marketanalyzer.streamlit.app/"),
        ("Target Case-Study Entities", "HCL Technologies, TCS, Infosys, Wipro, Accenture"),
        ("Specification Standard", "IEEE Std 830-1998 (Recommended Practice for Software Requirements Specifications)"),
        ("Document Status & Version", "Approved Production Baseline | Version 1.0.0"),
    ]
    t_cov = doc.add_table(rows=len(cov_rows), cols=2)
    t_cov.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cov.autofit = False
    set_table_borders(t_cov, border_color=HEX_NAVY, sz="6")
    
    col_w = [Inches(2.1), Inches(4.7)]
    for r_idx, (f_name, f_val) in enumerate(cov_rows):
        row = t_cov.rows[r_idx]
        for c_idx in range(2):
            cell = row.cells[c_idx]
            cell.width = col_w[c_idx]
            set_cell_margins(cell, top=70, bottom=70, left=120, right=120)
            if c_idx == 0:
                set_cell_background(cell, HEX_GRAY_PALE)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                r = p.add_run(f_name)
                r.bold = True
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                r.font.color.rgb = C_NAVY_RGB
            else:
                set_cell_background(cell, "FFFFFF")
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                r = p.add_run(f_val)
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                if "http" in f_val:
                    r.font.color.rgb = C_BLUE_RGB
                    r.underline = True
                elif f_name in ["Student Name", "University Roll No.", "Project Mentor / Guide"]:
                    r.bold = True
                    r.font.color.rgb = C_NAVY_RGB
                else:
                    r.font.color.rgb = C_GRAY_HVY_RGB

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Executive Summary Callout Box
    add_callout_box(
        doc,
        "This Software Requirements Specification (SRS) establishes the formal engineering baseline for the "
        "Autonomous Agentic Web Scraper & Strategic Market Intelligence Analyzer in strict conformance with IEEE Std 830-1998. "
        "The system converts high-level natural-language research inquiries into autonomous web discovery, automated extraction, "
        "schema validation, and structured strategic synthesis using a LangGraph ReAct orchestration model and Google Gemini 2.5 Flash. "
        "This specification details functional, non-functional, dynamic workflow, and structural requirements for complete "
        "academic evaluation and production replication.",
        title="DOCUMENT EXECUTIVE SUMMARY & IEEE COMPLIANCE STATEMENT",
        border_color=HEX_BLUE,
        bg_color=HEX_BLUE_LIGHT
    )

    # Table of Contents
    toc_data = [
        ("Section", "Specification Content & Deliverables", "Topic"),
        ("Sections 1 - 4", "Introduction, Abstract, Problem Statement, Engineering Objectives (O1 to O7)", "Foundation"),
        ("Sections 5 - 7", "Proposed Solution, Operational Workflow, Scope, Functional Requirements (FR-1 to FR-8)", "Scope & Functions"),
        ("Sections 8 - 9", "Non-Functional Requirements (NFR-1 to NFR-6), Technologies Used & Data Sources", "Quality & Tech"),
        ("Section 10", "System Architecture: Layered View & Walkthrough (Figure 2)", "Architecture"),
        ("Section 11 (Part 1)", "Detailed Design: 8-Stage Workflow (Figure 1) & Use Case Diagram (Figure 3)", "Design & Use Cases"),
        ("Section 11 (Part 2)", "Dynamic Execution: LangGraph ReAct Loop (Figure 4) & UML Class Diagram (Figure 5)", "ReAct & Schema"),
        ("Section 12", "Module Architecture & Functional Breakdown: Modules 1 through 9", "Modules"),
        ("Sections 13 - 14", "Database & Persistence Design, Testing Levels & Sample Test Cases (T1 to T8)", "Data & Testing"),
        ("Sections 15 - 18", "Results & Acceptance Criteria, Limitations, Future Scope, References & Sign-Off", "Evaluation & Sign-Off"),
    ]
    t_toc = doc.add_table(rows=len(toc_data), cols=3)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_toc.autofit = False
    set_table_borders(t_toc, border_color=HEX_BORDER, sz="4")
    toc_w = [Inches(1.4), Inches(4.3), Inches(1.1)]
    for r_idx, row_vals in enumerate(toc_data):
        row = t_toc.rows[r_idx]
        bg = HEX_BLUE_LIGHT if r_idx == 0 else (HEX_GRAY_PALE if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = toc_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if r_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            elif c_idx == 0:
                r.bold = True
                r.font.color.rgb = C_BLUE_RGB
            else:
                r.font.color.rgb = C_GRAY_HVY_RGB

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # 1. INTRODUCTION
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "1. Introduction", level=1)
    add_para_styled(
        doc,
        "Modern enterprise market and competitor research is an inherently complex, multi-source endeavor. Information "
        "necessary to assess corporate trajectory is fragmented across corporate investor portals, financial press releases, "
        "regulatory repositories (e.g., SEC EDGAR, BSE/NSE), technology news sources, and cloud marketplace partner directories. "
        "Human market analysts spend up to 70% of their research bandwidth on low-level browsing, parsing unstructured HTML, "
        "removing advertising artifacts, and reconciling conflicting metrics across spreadsheets. Traditional fixed scrapers "
        "fail rapidly because hardcoded URLs and brittle XPath/CSS selectors break as corporate websites evolve. "
        "This project introduces an Autonomous Agentic Web Scraper & Strategic Market Intelligence Analyzer based on "
        "a state-driven ReAct (Reason + Act) loop that discovers public web sources dynamically, extracts clean text, "
        "validates facts via Pydantic schemas, and synthesizes structured competitive intelligence."
    )

    # ═════════════════════════════════════════════════════════════════════════
    # 2. ABSTRACT
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "2. Abstract", level=1)
    add_para_styled(
        doc,
        "The proposed system establishes an autonomous pipeline combining LangGraph/LangChain agentic orchestration, "
        "DuckDuckGo Web and News discovery, Trafilatura content extraction, Google Gemini 2.5 Flash reasoning, and Pydantic v2 "
        "strict data validation. Given a target entity (e.g., HCL Technologies) or research query, the agent autonomously generates "
        "search queries, fetches relevant articles, strips web clutter, evaluates evidence sufficiency, and recursively triggers secondary "
        "queries if data is inadequate. It delivers an end-to-end intelligence briefing featuring executive summaries, strategic themes, "
        "SWOT analyses, normalized competitor benchmarks across 5 technology peers (HCLTech, TCS, Infosys, Wipro, Accenture), "
        "traceable source citations, and multi-format exports (Plotly radar charts, HTML, Markdown, and JSON)."
    )

    # ═════════════════════════════════════════════════════════════════════════
    # 3. PROBLEM STATEMENT
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "3. Problem Statement", level=1)
    add_para_styled(doc, "Manual corporate research and conventional web scraping exhibit significant systemic limitations:")
    add_bullet_styled(doc, "Public market signals are distributed across corporate filings, investor briefings, and press reports.", bold_prefix="Information Fragmentation: ")
    add_bullet_styled(doc, "Manual querying, page extraction, and source tracking require repetitive manual effort.", bold_prefix="Labor-Intensive Acquisition: ")
    add_bullet_styled(doc, "Raw search engine results contain duplicate reports, irrelevant aggregator spam, and promotional material.", bold_prefix="Search Noise & Duplication: ")
    add_bullet_styled(doc, "Traditional web scrapers break when web layouts change; they lack autonomous content discovery.", bold_prefix="DOM Selector Fragility: ")
    add_bullet_styled(doc, "Raw scraped content is contaminated with navigational links, cookie notices, and advertisements.", bold_prefix="Unstructured Web Clutter: ")
    add_bullet_styled(doc, "Generative LLMs without strict schema enforcement produce hallucinated or malformed JSON responses.", bold_prefix="Lack of Strict Validation: ")

    # ═════════════════════════════════════════════════════════════════════════
    # 4. PROJECT OBJECTIVES
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "4. Project Objectives", level=1)
    add_para_styled(doc, "The project addresses the stated problem through the following verified engineering objectives:")
    add_bullet_styled(doc, "Convert natural-language goals into targeted multi-perspective queries via DuckDuckGo Web & News.", bold_prefix="O1. Autonomous Source Discovery: ")
    add_bullet_styled(doc, "Extract clean main-body article text while stripping ads and navigation via Trafilatura and BS4.", bold_prefix="O2. Resilient Content Extraction: ")
    add_bullet_styled(doc, "Coordinate research using LangGraph in a cyclic ReAct Think-Act-Observe paradigm.", bold_prefix="O3. State-Driven Agentic Orchestration: ")
    add_bullet_styled(doc, "Dynamically assess evidence sufficiency and trigger follow-up web searches when information is thin.", bold_prefix="O4. Recursive Evidence Feedback: ")
    add_bullet_styled(doc, "Guarantee schema conformity for all findings, ensuring zero malformed structures.", bold_prefix="O5. Strict Pydantic v2 Validation: ")
    add_bullet_styled(doc, "Generate normalized competitor metrics across AI Readiness, Cloud Momentum, and Global Scale.", bold_prefix="O6. Multi-Peer Strategic Benchmarking: ")
    add_bullet_styled(doc, "Render Plotly polar radar charts and export HTML, Markdown, and machine-readable JSON.", bold_prefix="O7. Interactive Visualization & Export: ")

    # ═════════════════════════════════════════════════════════════════════════
    # 5. PROPOSED SOLUTION
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "5. Proposed Solution", level=1)
    add_para_styled(
        doc,
        "The proposed solution implements a stateful, autonomous research agent that replaces static scraping scripts with "
        "an intelligent, multi-stage reasoning and execution pipeline. Built with LangGraph and powered by Google Gemini 2.5 Flash, "
        "the agent systematically executes eight sequential stages: accepts plain-English input, plans discovery queries, retrieves live "
        "web/news articles, extracts clean text, synthesizes findings into structured JSON, verifies constraints against Pydantic models, "
        "computes competitor benchmarks, and generates interactive Plotly visualizations and exportable briefing dossiers."
    )

    # ═════════════════════════════════════════════════════════════════════════
    # 6. SCOPE OF THE PROJECT
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "6. Scope of the Project", level=1)
    add_para_styled(
        doc,
        "The project covers autonomous research over publicly accessible information for technology "
        "services companies. It supports natural-language queries, automated search formulation, HTML text extraction, LLM synthesis, "
        "comparative SWOT matrix generation, quantitative benchmarking across five target IT enterprises (HCL Technologies, TCS, "
        "Infosys, Wipro, Accenture), interactive Streamlit visualization, and export in HTML, Markdown, and JSON formats.",
        bold_prefix="In-Scope Capabilities: "
    )
    add_para_styled(
        doc,
        "The system does not bypass user authentication, CAPTCHAs, paywalls, or bot mitigation "
        "systems (e.g., Cloudflare Turnstile). It does not guarantee live availability of third-party domains. All generated intelligence "
        "reflects public data and model synthesis and should be reviewed by an analyst prior to high-stakes capital allocation.",
        bold_prefix="Current Scope Boundaries: "
    )

    # ═════════════════════════════════════════════════════════════════════════
    # 7. FUNCTIONAL REQUIREMENTS
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "7. Functional Requirements", level=1)
    
    fr_data = [
        ("Req ID", "Requirement Title", "Detailed Functional Specification"),
        ("FR-1", "Research Input & Presets", "Accept custom natural-language objectives or preset targets (HCLTech, TCS, Infosys, Wipro, Accenture) via Streamlit UI."),
        ("FR-2", "Dynamic Query Planning", "Agent automatically decomposes objectives into targeted search queries covering financials, AI, cloud, and partnerships."),
        ("FR-3", "Autonomous Web Discovery", "Execute DuckDuckGo Web and News searches (DDGS API); deduplicate URLs and filter out low-relevance domains."),
        ("FR-4", "Clean Content Extraction", "Fetch accessible web pages; use Trafilatura and BeautifulSoup4 to extract clean article text, discarding ads and headers."),
        ("FR-5", "ReAct Synthesis Engine", "Gemini 2.5 Flash synthesizes raw text into structured JSON containing executive summary, strategic pillars, and SWOT items."),
        ("FR-6", "Pydantic Schema Validation", "Validate LLM output against MarketIntelligenceReport schema; retry synthesis if schema fails or fields are missing."),
        ("FR-7", "Competitor Benchmarking", "Compute normalized metrics (AI Readiness, Cloud Momentum, Global Scale) across peer enterprises using Pandas."),
        ("FR-8", "Multi-Format Export", "Generate standalone HTML briefings, Markdown executive reports, raw JSON dumps, and Plotly polar radar charts."),
    ]
    t_fr = doc.add_table(rows=len(fr_data), cols=3)
    t_fr.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_fr.autofit = False
    set_table_borders(t_fr, border_color=HEX_BORDER, sz="4")
    fr_w = [Inches(1.0), Inches(1.8), Inches(4.0)]
    for r_idx, row_vals in enumerate(fr_data):
        row = t_fr.rows[r_idx]
        bg = HEX_BLUE_LIGHT if r_idx == 0 else (HEX_GRAY_PALE if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = fr_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            elif c_idx == 0:
                r.bold = True
                r.font.color.rgb = C_BLUE_RGB
            elif c_idx == 1:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            else:
                r.font.color.rgb = C_GRAY_HVY_RGB

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # 8. NON-FUNCTIONAL REQUIREMENTS
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "8. Non-Functional Requirements", level=1)
    
    nfr_data = [
        ("Category", "Specification & Measurable Metric", "Implementation Mechanism"),
        ("NFR-1: Performance", "Complete end-to-end research, extraction, synthesis, and export within 45 - 90 seconds for standard corporate queries.", "Gemini 2.5 Flash fast inference; concurrent HTTP page fetching via Trafilatura."),
        ("NFR-2: Reliability", "Zero application crash on blocked, slow, or 404/403 web pages; graceful fallback and logging for inaccessible links.", "Trafilatura try/except exception wrappers; safe empty response fallbacks."),
        ("NFR-3: Data Accuracy", "100% of reported strategic findings linked back to source URLs; 0% unvalidated or hallucinated schema structures.", "Pydantic v2 strict schema enforcement; SourceCitation sub-model traceability."),
        ("NFR-4: Usability", "Clean interactive dashboard requiring zero CLI configuration; real-time execution trace display for analyst transparency.", "Streamlit web interface with tabbed views, expandable traces, and one-click exports."),
        ("NFR-5: Modularity", "Pluggable architecture allowing new search tools, scrapers, or LLM providers without altering orchestrator core.", "LangGraph modular tool belt pattern; isolated tool schemas in schemas.py."),
        ("NFR-6: Security", "No hardcoded API credentials; strictly respects website robots.txt and disallows credential stuffing or payload execution.", "Environment-variable configuration via .env; safe HTTP headers and read-only scraping."),
    ]
    t_nfr = doc.add_table(rows=len(nfr_data), cols=3)
    t_nfr.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_nfr.autofit = False
    set_table_borders(t_nfr, border_color=HEX_BORDER, sz="4")
    nfr_w = [Inches(1.5), Inches(3.0), Inches(2.3)]
    for r_idx, row_vals in enumerate(nfr_data):
        row = t_nfr.rows[r_idx]
        bg = HEX_BLUE_LIGHT if r_idx == 0 else (HEX_GRAY_PALE if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = nfr_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            elif c_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            else:
                r.font.color.rgb = C_GRAY_HVY_RGB

    # ═════════════════════════════════════════════════════════════════════════
    # 9. TECHNOLOGIES USED & ARCHITECTURAL STACK
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "9. Technologies Used & Architectural Stack", level=1)
    
    tech_data = [
        ("Category", "Technology / Tool", "Role in Architecture"),
        ("Programming", "Python 3.10+", "Core implementation, tool orchestration, and data pipeline."),
        ("Agentic AI", "LangGraph / LangChain", "State-driven agent workflow and ReAct Think-Act-Observe loop."),
        ("LLM Engine", "Google Gemini 2.5 Flash", "Synthesis, reasoning, query planning, and structured JSON output."),
        ("Search Discovery", "DuckDuckGo / DDGS", "Live web and news discovery without paid API key quotas."),
        ("Web Extraction", "Trafilatura", "Main text body extraction, boilerplate and advertisement removal."),
        ("HTML Parsing", "BeautifulSoup4", "Targeted page parsing and fallback DOM text sanitization."),
        ("Validation", "Pydantic v2", "Strict data validation and schema-compliant JSON enforcement."),
        ("Data Analytics", "Pandas", "Tabular metric processing, score normalization, and comparison."),
        ("Visualization", "Plotly", "Interactive polar radar charts and horizontal competitor benchmarks."),
        ("User Interface", "Streamlit", "Interactive research dashboard with live execution traces."),
    ]
    t_tech = doc.add_table(rows=len(tech_data), cols=3)
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tech.autofit = False
    set_table_borders(t_tech, border_color=HEX_BORDER, sz="4")
    tech_w = [Inches(1.4), Inches(2.0), Inches(3.4)]
    for r_idx, row_vals in enumerate(tech_data):
        row = t_tech.rows[r_idx]
        bg = HEX_BLUE_LIGHT if r_idx == 0 else (HEX_GRAY_PALE if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = tech_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            elif c_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            else:
                r.font.color.rgb = C_GRAY_HVY_RGB

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    add_para_styled(doc, "Primary Public Web Data-Source Categories:", bold_prefix="Data Sources: ")
    add_bullet_styled(doc, "Reuters, Bloomberg, CNBC, TechCrunch, PR Newswire, Business Wire.", bold_prefix="1. Business News: ")
    add_bullet_styled(doc, "HCLTech, TCS, Infosys, Wipro, Accenture IR repositories.", bold_prefix="2. Investor Portals: ")
    add_bullet_styled(doc, "SEC EDGAR, BSE/NSE Corporate Announcements, UK Companies House.", bold_prefix="3. Regulatory Filings: ")
    add_bullet_styled(doc, "Gartner Magic Quadrants, IDC MarketScape, Everest PEAK Matrix.", bold_prefix="4. Industry Benchmarks: ")
    add_bullet_styled(doc, "AWS Partner Network, Microsoft Azure Marketplace, Google Cloud Partner Directory.", bold_prefix="5. Cloud Ecosystems: ")

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # 10. SYSTEM ARCHITECTURE (FIGURE 2)
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "10. System Architecture", level=1)
    add_para_styled(
        doc,
        "The system architecture strictly separates the user interface, agent orchestration brain, external tool belt, "
        "public web sources, and output deliverables. This modular separation enables independent enhancement of individual "
        "layers (e.g., swapping search providers or updating LLM prompts) without breaking pipeline stability."
    )
    
    img_arch = os.path.join("deliverables", "srs_fig2_architecture.png")
    add_image_with_caption(
        doc, img_arch,
        "Figure 2. High-level system architecture (layered view: interface, agent brain, tool belt, public web, results)",
        width_inches=6.4
    )

    add_heading_styled(doc, "How to Read the Architecture Diagram (Numbered Step-by-Step Flow)", level=2)
    arch_steps = [
        ("Step (1)", "The user types a research objective (a company, competitor or market question) into the Streamlit dashboard."),
        ("Step (2)", "The Streamlit dashboard passes the objective to the LangGraph/LangChain agent orchestrator."),
        ("Step (3)", "The orchestrator and Gemini 2.5 Flash reason together in an iterative Think, Act, Observe loop."),
        ("Step (4)", "The orchestrator calls specialized tools from its belt: Search, Scrape, Validate, and Analyze."),
        ("Step (5)", "Search and Scrape reach out to public web sources and bring back clean page text without advertisements."),
        ("Step (6)", "Validated and analyzed findings become Plotly interactive charts and HTML / Markdown / JSON reports."),
        ("Step (7)", "Streamlit displays the deliverables in tabbed views and lets the user download complete report bundles."),
    ]
    for s_num, s_desc in arch_steps:
        add_bullet_styled(doc, s_desc, bold_prefix=f"{s_num}: ")

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # 11. DETAILED SYSTEM DESIGN & WORKFLOWS
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "11. Detailed System Design & Workflows", level=1)
    
    add_heading_styled(doc, "11.1 Agentic Workflow / Data Flow Diagram (DFD)", level=2)
    add_para_styled(
        doc,
        "The workflow is organized as a state-driven agentic pipeline. A research objective initiates source discovery; "
        "extracted evidence is progressively transformed into structured information. The agent revisits discovery when evidence is insufficient."
    )
    img_wf = os.path.join("deliverables", "srs_fig1_workflow.png")
    add_image_with_caption(
        doc, img_wf,
        "Figure 1. Agentic workflow / flow chart of the proposed system (8 stages, colour-coded by phase, with a feedback loop)",
        width_inches=6.4
    )

    add_heading_styled(doc, "11.2 Use Case Diagram", level=2)
    add_para_styled(
        doc,
        "The Use Case model defines the functional boundary between the human Analyst/Researcher and the automated agent subsystem."
    )
    img_uc = os.path.join("deliverables", "srs_fig3_usecase.png")
    add_image_with_caption(
        doc, img_uc,
        "Figure 3. Use case diagram illustrating core analyst interactions, preset workflows, and automated pipeline execution",
        width_inches=6.4
    )

    doc.add_page_break()

    add_heading_styled(doc, "11.3 LangGraph ReAct Agent Loop", level=2)
    add_para_styled(
        doc,
        "The execution engine coordinates reasoning and action through a state-machine loop. When Gemini determines evidence is incomplete, "
        "it dispatches tools (web_search, scrape_webpage) and feeds observations back into memory until sufficiency is achieved."
    )
    img_react = os.path.join("deliverables", "srs_fig4_react.png")
    add_image_with_caption(
        doc, img_react,
        "Figure 4. LangGraph ReAct agent state-machine and feedback loop execution model with tool dispatch and Pydantic validation",
        width_inches=6.4
    )

    add_heading_styled(doc, "11.4 Class & Pydantic Schema Architecture", level=2)
    add_para_styled(
        doc,
        "The object model couples the orchestration agent with strongly typed Pydantic v2 schemas to ensure end-to-end data integrity."
    )
    img_uml = os.path.join("deliverables", "srs_fig5_uml.png")
    add_image_with_caption(
        doc, img_uml,
        "Figure 5. UML class and Pydantic v2 schema relationship diagram illustrating model composition and orchestration dependencies",
        width_inches=6.4
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # 12. MODULE ARCHITECTURE & FUNCTIONAL BREAKDOWN
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "12. Module Architecture & Functional Breakdown", level=1)
    add_para_styled(
        doc,
        "The architecture is partitioned into nine discrete functional modules that isolate specific computational concerns:"
    )

    mod_data = [
        ("Module", "Architectural Responsibility & Implementation Details"),
        ("Module 1: Research Input", "Accepts and structures the user's research objective. Supports arbitrary natural-language market queries as well as pre-configured presets for the five target technology peers (HCL Technologies, TCS, Infosys, Wipro, Accenture). Sanitizes query strings and passes parameters into the LangGraph state graph."),
        ("Module 2: Search / Discovery", "Generates targeted Web and News search queries using DuckDuckGo (DDGS API). Employs boolean modifiers and temporal filters to identify recent earnings calls, press releases, strategic announcements, and industry commentary without incurring API cost."),
        ("Module 3: Web Scraping", "Retrieves and extracts content from accessible public web pages. Utilizes Trafilatura for primary main-text extraction with automated stripping of headers, footers, navigation, cookie banners, and inline advertising. Uses BeautifulSoup4 as fallback."),
        ("Module 4: Evidence Processing", "Cleans, normalizes, and chunks extracted text. Deduplicates overlapping news reports, enforces character window limits to prevent LLM context-window saturation, and structures page metadata (URL, page title, publish date) for downstream auditing."),
        ("Module 5: Validation", "Performs automated checks on source relevance and evidence consistency. Checks that collected articles directly address the research query. If evidence is thin or irrelevant, signals the orchestrator to trigger secondary discovery queries."),
        ("Module 6: Agentic Synthesis", "Employs Google Gemini 2.5 Flash as the core LLM reasoning engine. Guided by a strict synthesis system prompt, converts unstructured evidence chunks into structured JSON conforming to the MarketIntelligenceReport Pydantic schema."),
        ("Module 7: Strategic Analysis", "Produces comparative market-intelligence observations, SWOT matrix categorization (Strengths, Weaknesses, Opportunities, Threats), strategic theme identification, and quantitative benchmark scoring across AI Readiness, Cloud Momentum, and Global Scale."),
        ("Module 8: Visualization", "Constructs interactive data representations using Plotly and Pandas. Renders multi-axis polar radar charts comparing the five technology companies, horizontal benchmark bar charts, and stylized summary scorecards inside the Streamlit dashboard."),
        ("Module 9: Reporting / Export", "Generates exportable research artifacts in three distinct formats: responsive HTML executive briefings with embedded CSS, GitHub-flavored Markdown dossiers with source hyperlinks, and machine-readable JSON dumps for downstream data pipelines."),
    ]
    t_mod = doc.add_table(rows=len(mod_data), cols=2)
    t_mod.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_mod.autofit = False
    set_table_borders(t_mod, border_color=HEX_BORDER, sz="4")
    mod_w = [Inches(1.8), Inches(5.0)]
    for r_idx, (m_title, m_desc) in enumerate(mod_data):
        row = t_mod.rows[r_idx]
        bg = HEX_BLUE_LIGHT if r_idx == 0 else (HEX_GRAY_PALE if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate([m_title, m_desc]):
            cell = row.cells[c_idx]
            cell.width = mod_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            elif c_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            else:
                r.font.color.rgb = C_GRAY_HVY_RGB

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # 13. DATABASE & PERSISTENCE DESIGN
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "13. Database & Data Storage Design", level=1)
    add_para_styled(
        doc,
        "The system operates on a stateless, memory-efficient real-time streaming model. Extracted web content and intermediate "
        "reasoning traces are maintained in-memory within the LangGraph StateGraph dictionary during execution. "
        "Completed intelligence reports are serialized to disk as structured JSON artifacts under the reports/ directory. "
        "This file-based caching model avoids unnecessary relational database overhead while ensuring report provenance and auditability."
    )

    # ═════════════════════════════════════════════════════════════════════════
    # 14. TESTING LEVELS & SAMPLE TEST CASES
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "14. Testing Levels & Verification Strategy", level=1)
    add_para_styled(
        doc,
        "Testing is structured across four rigorous levels to validate isolated components, inter-stage communication, end-to-end "
        "workflow execution, and resilience against hostile web environments:"
    )

    t_levels = [
        ("Level", "What is Tested", "Method & Tooling"),
        ("Unit Testing", "Query generation, text cleaning, Pydantic schemas, URL deduplication, export serializers.", "Automated pytest test suite with static mock inputs."),
        ("Integration Testing", "Hand-offs between pipeline stages: Search to Scrape, Scrape to Synthesis, Synthesis to Validation.", "Sequential execution of connected stages on fixed sample data."),
        ("System Testing", "Complete execution from research objective to HTML/MD/JSON output for the 5 target companies.", "End-to-end automated and manual runs via Streamlit UI."),
        ("Robustness Testing", "Paywalled, blocked, or slow pages, empty search results, irrelevant sources, malformed LLM outputs.", "Injected HTTP failure mocks and edge-case prompt scenarios."),
    ]
    t_tl = doc.add_table(rows=len(t_levels), cols=3)
    t_tl.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tl.autofit = False
    set_table_borders(t_tl, border_color=HEX_BORDER, sz="4")
    tl_w = [Inches(1.5), Inches(3.1), Inches(2.2)]
    for r_idx, row_vals in enumerate(t_levels):
        row = t_tl.rows[r_idx]
        bg = HEX_BLUE_LIGHT if r_idx == 0 else (HEX_GRAY_PALE if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = tl_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            elif c_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            else:
                r.font.color.rgb = C_GRAY_HVY_RGB

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    add_heading_styled(doc, "Sample Test Cases Matrix (T1 through T8)", level=2)
    
    t_cases = [
        ("ID", "Test Case Description", "Expected Verified Result"),
        ("T1", "Enter a valid company research objective.", "Relevant Web and News sources are discovered dynamically."),
        ("T2", "Scrape a normal news article.", "Main text is returned without navigation menus, cookie banners, or ads."),
        ("T3", "Scrape a paywalled or blocked web page.", "Page is skipped gracefully and logged; system does not hang or bypass controls."),
        ("T4", "Search returns duplicate or irrelevant links.", "Duplicates are removed and low-relevance domains are filtered out."),
        ("T5", "Evidence is too thin for a reliable answer.", "Agent returns to discovery stage and generates secondary searches."),
        ("T6", "LLM returns output that violates schema.", "Pydantic validation rejects response and triggers structured retry."),
        ("T7", "Compare all five target technology companies.", "Structured comparison table and Plotly radar charts are generated."),
        ("T8", "Export the final research briefing.", "Valid HTML, Markdown, and JSON files are produced and downloadable."),
    ]
    t_tc = doc.add_table(rows=len(t_cases), cols=3)
    t_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tc.autofit = False
    set_table_borders(t_tc, border_color=HEX_BORDER, sz="4")
    tc_w = [Inches(0.6), Inches(3.2), Inches(3.0)]
    for r_idx, row_vals in enumerate(t_cases):
        row = t_tc.rows[r_idx]
        bg = HEX_BLUE_LIGHT if r_idx == 0 else (HEX_GRAY_PALE if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = tc_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            elif c_idx == 0:
                r.bold = True
                r.font.color.rgb = C_BLUE_RGB
            else:
                r.font.color.rgb = C_GRAY_HVY_RGB

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════════════
    # 15. RESULTS & EVALUATION CRITERIA
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "15. Results & Evaluation Criteria", level=1)
    
    eval_data = [
        ("Evaluation Criterion", "Verification Method", "Target Acceptance Standard"),
        ("Source Relevance", "Reviewer evaluates discovered URLs against objective.", "Over 85% of discovered sources directly relevant to inquiry."),
        ("Extraction Quality", "Inspection of cleaned text samples for advertising clutter.", "Zero navigation text, ads, or cookie banners in extracted content."),
        ("Schema Validity", "Proportion of LLM outputs passing Pydantic validation.", "100% schema compliance; all schema violations caught and retried."),
        ("Evidence Traceability", "Audit of findings back to originating web source URL.", "100% of reported facts cite verified public source URLs."),
        ("Time Saved", "Agent run time vs. human analyst manual search time.", "Complete research report in < 90s (90%+ time reduction vs. manual)."),
        ("Output Completeness", "Integrity of generated HTML, Markdown, and JSON files.", "All three file formats generated without corruption or data loss."),
    ]
    t_eval = doc.add_table(rows=len(eval_data), cols=3)
    t_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_eval.autofit = False
    set_table_borders(t_eval, border_color=HEX_BORDER, sz="4")
    eval_w = [Inches(1.6), Inches(2.8), Inches(2.4)]
    for r_idx, row_vals in enumerate(eval_data):
        row = t_eval.rows[r_idx]
        bg = HEX_BLUE_LIGHT if r_idx == 0 else (HEX_GRAY_PALE if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = eval_w[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            elif c_idx == 0:
                r.bold = True
                r.font.color.rgb = C_NAVY_RGB
            else:
                r.font.color.rgb = C_GRAY_HVY_RGB

    # ═════════════════════════════════════════════════════════════════════════
    # 16. LIMITATIONS
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "16. Limitations", level=1)
    add_bullet_styled(doc, "Output quality is contingent on content accessible to public search engines.", bold_prefix="Public Web Availability: ")
    add_bullet_styled(doc, "The system strictly respects paywalls, CAPTCHAs, and corporate intranet firewalls.", bold_prefix="No Authentication Bypass: ")
    add_bullet_styled(doc, "Real-time multi-page scraping and LLM synthesis requires 45-90 seconds per run.", bold_prefix="Inference Latency: ")
    add_bullet_styled(doc, "High-stakes investment or strategic decisions should review underlying source URLs.", bold_prefix="Human Verification Required: ")

    # ═════════════════════════════════════════════════════════════════════════
    # 17. FUTURE SCOPE & PRODUCT ROADMAP
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "17. Future Scope & Product Roadmap", level=1)
    add_bullet_styled(doc, "Introduce specialized sub-agents for financial statement analysis, patent auditing, and executive synthesis.")
    add_bullet_styled(doc, "Add persistent vector-based memory (ChromaDB / FAISS) for quarter-over-quarter trend analysis and historical tracking.")
    add_bullet_styled(doc, "Integrate direct regulatory API connectors for SEC EDGAR, BSE/NSE filings, and UK Companies House.")
    add_bullet_styled(doc, "Automate board-ready PowerPoint (PPTX) slide deck generation from synthesized research dossiers.")
    add_bullet_styled(doc, "Implement real-time market anomaly alerts and notifications for breaking competitive developments.")

    # ═════════════════════════════════════════════════════════════════════════
    # 18. REFERENCES & FORMAL SIGN-OFF BLOCK
    # ═════════════════════════════════════════════════════════════════════════
    add_heading_styled(doc, "18. References", level=1)
    refs = [
        "1. Yao, S. et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR 2023 / arXiv:2210.03629.",
        "2. Barbaresi, A. (2021). Trafilatura: A Web Scraping Library and Tool for Text Discovery and Extraction. ACL.",
        "3. LangChain / LangGraph Official Documentation for Stateful Agentic Workflows (2024).",
        "4. Google Gemini 2.5 Flash Official Technical Documentation and Structured Outputs Guide (2024).",
        "5. Pydantic v2 Official Documentation for Robust Schema Validation and Settings Management.",
        "6. Streamlit & Plotly Official Documentation for Python Interactive Visualization and Dashboards.",
        "7. IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications.",
    ]
    for rf in refs:
        p_rf = doc.add_paragraph()
        p_rf.paragraph_format.space_before = Pt(0)
        p_rf.paragraph_format.space_after = Pt(2)
        r_rf = p_rf.add_run(rf)
        r_rf.font.name = "Calibri"
        r_rf.font.size = Pt(8.5)
        r_rf.font.color.rgb = C_GRAY_HVY_RGB

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Formal Approval Block
    add_heading_styled(doc, "Institutional Approval & Sign-Off", level=2)
    t_sign = doc.add_table(rows=3, cols=2)
    t_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sign.autofit = False
    set_table_borders(t_sign, border_color=HEX_NAVY, sz="6")
    sign_w = [Inches(3.4), Inches(3.4)]
    
    # Header row
    for c_idx, h_text in enumerate(["Prepared By (Candidate)", "Reviewed & Approved By (Project Mentor)"]):
        cell = t_sign.rows[0].cells[c_idx]
        cell.width = sign_w[c_idx]
        set_cell_background(cell, HEX_BLUE_LIGHT)
        set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = C_NAVY_RGB

    # Info row
    cand_info = "Adarsh Dubey\nUniversity Roll No: 2400320100061\nB.Tech III Year, Computer Science & Engineering\nABES Engineering College, Ghaziabad"
    guide_info = "Radhika Singhal\nProject Mentor / Guide\nDepartment of Computer Science & Engineering\nABES Engineering College, Ghaziabad"
    for c_idx, info in enumerate([cand_info, guide_info]):
        cell = t_sign.rows[1].cells[c_idx]
        cell.width = sign_w[c_idx]
        set_cell_background(cell, "FFFFFF")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(info)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = C_GRAY_HVY_RGB

    # Signature row
    for c_idx in range(2):
        cell = t_sign.rows[2].cells[c_idx]
        cell.width = sign_w[c_idx]
        set_cell_background(cell, HEX_GRAY_PALE)
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run("Signature: ___________________________\nDate: 30 October 2026")
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = C_NAVY_RGB

    # Save to root and deliverables
    try:
        doc.save(DOCX_FILENAME)
        shutil.copy2(DOCX_FILENAME, SUBMISSION_DOCX_FILENAME)
        os.makedirs("deliverables", exist_ok=True)
        shutil.copy2(DOCX_FILENAME, os.path.join("deliverables", DOCX_FILENAME))
        shutil.copy2(SUBMISSION_DOCX_FILENAME, os.path.join("deliverables", SUBMISSION_DOCX_FILENAME))
        print(f"Successfully generated {DOCX_FILENAME} and {SUBMISSION_DOCX_FILENAME} (and copied to deliverables/)")
    except PermissionError:
        print(f"PermissionError: Word file is open. Generated alt copies in deliverables.")


if __name__ == "__main__":
    build_srs_docx()
