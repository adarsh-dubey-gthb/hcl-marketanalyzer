import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.graphics.shapes import (
    Drawing, Rect, String, Line, Group, Polygon
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "SRS_Market_Intelligence_Analyzer.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        page_num = self._pageNumber
        # Running header / footer matching user format
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#333333"))
        
        # Header & Footer text
        # In the provided format:
        # Running footer on every page:
        # Left: B.Tech 3rd Year Mini Project — Software Requirements Specification
        # Right: Page X
        footer_y = 36
        line_y = 50
        
        self.drawString(54, footer_y, "B.Tech 3rd Year Mini Project — Software Requirements Specification")
        page_str = f"Page {page_num}"
        self.drawRightString(letter[0] - 54, footer_y, page_str)
        
        self.restoreState()


def create_srs_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=60
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#111111')
    )
    
    project_title_style = ParagraphStyle(
        'ProjectTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#000000')
    )
    
    sub_title_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#222222')
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#000000'),
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#111111'),
        spaceBefore=8,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#222222')
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#222222')
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#000000')
    )

    story = []

    # ================= PAGE 1: COVER PAGE =================
    story.append(Spacer(1, 100))
    story.append(Paragraph("SOFTWARE REQUIREMENTS SPECIFICATION", title_style))
    story.append(Spacer(1, 24))
    story.append(Paragraph("Autonomous Agentic Web Scraper &amp;<br/>Strategic Market Intelligence Analyzer", project_title_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("B.Tech 3rd Year Mini Project", sub_title_style))
    story.append(Spacer(1, 45))

    cover_table_data = [
        [Paragraph("Student Name", table_cell_bold), Paragraph("Adarsh Dubey", table_cell)],
        [Paragraph("Roll Number", table_cell_bold), Paragraph("2400320100061", table_cell)],
        [Paragraph("Branch / Department", table_cell_bold), Paragraph("Computer Science & Engineering", table_cell)],
        [Paragraph("College Name", table_cell_bold), Paragraph("ABES Engineering College, Ghaziabad", table_cell)],
        [Paragraph("Project Guide", table_cell_bold), Paragraph("Radhika Singhal", table_cell)],
        [Paragraph("Academic Year", table_cell_bold), Paragraph("2026–27", table_cell)],
    ]
    cover_table = Table(cover_table_data, colWidths=[160, 340])
    cover_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#333333')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#555555')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(cover_table)

    story.append(Spacer(1, 55))
    story.append(Paragraph("Prepared according to the provided SRS format.", ParagraphStyle(
        'CoverFooter', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, alignment=TA_CENTER, textColor=colors.HexColor('#444444')
    )))
    story.append(PageBreak())

    # ================= PAGE 2: ABSTRACT & PROBLEM STATEMENT =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("2. Abstract", h1_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The <b>Autonomous Agentic Web Scraper &amp; Strategic Market Intelligence Analyzer</b> is an AI-driven research "
        "system for automating the collection, extraction, validation, synthesis, and analysis of public web information "
        "for market-intelligence tasks. Instead of manually searching several websites, copying relevant content, "
        "comparing sources, and preparing a report, the system coordinates these activities through an agentic workflow.",
        body_style
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "The project uses <b>LangGraph / LangChain</b> for agent orchestration, a <b>ReAct-style workflow</b>, and <b>Google "
        "Gemini 2.5 Flash</b> for reasoning and synthesis. <b>DuckDuckGo/DDGS</b> provides Web and News discovery, while "
        "<b>Trafilatura</b> and <b>BeautifulSoup4</b> support content extraction. <b>Pydantic v2</b> is used for structured "
        "validation, with <b>Pandas</b> and <b>Plotly</b> supporting analysis and visualization. <b>Streamlit</b> provides the "
        "interactive interface, and <b>HTML, Markdown, and JSON</b> are supported as output formats.",
        body_style
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "The expected outcome is a practical prototype that converts scattered public information into structured market "
        "intelligence while reducing repetitive research effort. The system is intended as decision support; final "
        "interpretation remains with the user.",
        body_style
    ))

    story.append(Spacer(1, 24))
    story.append(Paragraph("3. Problem Statement", h1_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Market and competitor research often requires analysts to search news websites, corporate pages, "
        "investor-relations material, regulatory repositories, and industry sources separately. Information is "
        "distributed across different pages and formats, and manual collection requires repeated searching, "
        "reading, copying, comparison, and consolidation.",
        body_style
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "The proposed system addresses this by accepting a research objective and coordinating source discovery, "
        "web extraction, validation, synthesis, analysis, visualization, and output generation in one workflow. "
        "The project focuses on public-source research and does not claim to replace human judgment in business decisions.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 3: OBJECTIVES & PROPOSED SOLUTION =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("4. Objectives", h1_style))
    story.append(Spacer(1, 6))
    objectives = [
        "Develop an interactive application for autonomous web-based market-intelligence research.",
        "Automate discovery of relevant Web and News sources from a research objective.",
        "Extract useful content from accessible public pages.",
        "Validate structured information before downstream analysis.",
        "Synthesize evidence into strategic market insights using an agentic workflow.",
        "Present findings through visualizations and exportable HTML, Markdown, and JSON outputs."
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", bullet_style))

    story.append(Spacer(1, 20))
    story.append(Paragraph("5. Proposed Solution", h1_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The proposed system combines a Streamlit interface with an agentic orchestration layer. The user provides "
        "a research objective. The agent coordinates search and source discovery, retrieves relevant pages, extracts "
        "useful content, validates structured information, synthesizes findings, performs analysis, and presents the result.",
        body_style
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Basic workflow</b>", body_style))
    story.append(Spacer(1, 8))

    flow_data = [
        [
            Paragraph("<b>1. Input</b>", table_cell), Paragraph("→", table_cell_bold),
            Paragraph("<b>2. Search</b>", table_cell), Paragraph("→", table_cell_bold),
            Paragraph("<b>3. Scrape</b>", table_cell), Paragraph("→", table_cell_bold),
            Paragraph("<b>4. Synthesize</b>", table_cell)
        ],
        [
            Paragraph("<b>5. Validate</b>", table_cell), Paragraph("→", table_cell_bold),
            Paragraph("<b>6. Analyze</b>", table_cell), Paragraph("→", table_cell_bold),
            Paragraph("<b>7. Visualize</b>", table_cell), Paragraph("→", table_cell_bold),
            Paragraph("<b>8. Output</b>", table_cell)
        ]
    ]
    flow_table = Table(flow_data, colWidths=[95, 20, 95, 20, 95, 20, 115])
    flow_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#444444')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#666666')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8F9FA')),
    ]))
    story.append(flow_table)
    story.append(Spacer(1, 14))

    sol_bullets = [
        "<b>Users:</b> students, researchers, analysts, and project users needing structured public-source market intelligence.",
        "<b>Main features:</b> discovery, extraction, agentic synthesis, validation, analysis, visualization, and output generation.",
        "<b>Benefits:</b> less repetitive search work, more consistent processing, structured evidence handling, and faster report preparation."
    ]
    for b in sol_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))

    story.append(PageBreak())

    # ================= PAGE 4: SCOPE OF THE PROJECT =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("6. Scope of the Project", h1_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>In scope</b>", h2_style))
    
    in_scope = [
        "Public Web and News discovery through DuckDuckGo/DDGS.",
        "Retrieval and extraction of relevant content from accessible public pages.",
        "Market and competitor information processing for selected research objectives.",
        "Agentic orchestration of search, extraction, validation, synthesis, and analysis.",
        "Structured validation and preparation of collected information.",
        "Interactive visualization using Pandas and Plotly.",
        "Streamlit-based presentation and HTML, Markdown, and JSON outputs."
    ]
    for item in in_scope:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Primary data / scraping targets</b>", h2_style))
    targets = [
        "<b>Business news:</b> Reuters, Bloomberg, CNBC, TechCrunch, PR Newswire, Business Wire.",
        "<b>Corporate / investor sources:</b> HCLTech, TCS, Infosys, Wipro, Accenture investor-relations portals.",
        "<b>Regulatory:</b> SEC EDGAR, BSE/NSE corporate announcements, UK Companies House.",
        "<b>Industry benchmarks:</b> Gartner Magic Quadrants, IDC MarketScapes, Everest Group PEAK matrices.",
        "<b>Cloud ecosystems:</b> AWS Partner Network, Microsoft Azure Marketplace, Google Cloud Partner Directory."
    ]
    for item in targets:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Spacer(1, 14))
    story.append(Paragraph("<b>Outside current scope</b>", h2_style))
    story.append(Paragraph(
        "The current prototype does not define a production-grade enterprise data warehouse, native mobile "
        "application, private-data crawling, unrestricted paywalled-content access, or a full commercial "
        "intelligence subscription platform.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 5: FUNCTIONAL & NON-FUNCTIONAL REQUIREMENTS =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("7. Functional Requirements", h1_style))
    story.append(Paragraph("The requirements below describe the principal functions represented by the current project workflow.", body_style))
    story.append(Spacer(1, 8))

    fr_data = [
        [Paragraph("ID", table_header), Paragraph("Functional Requirement", table_header)],
        [Paragraph("FR-01", table_cell_bold), Paragraph("User can enter a market-research objective or query.", table_cell)],
        [Paragraph("FR-02", table_cell_bold), Paragraph("System discovers relevant Web and News sources.", table_cell)],
        [Paragraph("FR-03", table_cell_bold), Paragraph("System retrieves and extracts content from accessible public pages.", table_cell)],
        [Paragraph("FR-04", table_cell_bold), Paragraph("System synthesizes collected information through the AI agent workflow.", table_cell)],
        [Paragraph("FR-05", table_cell_bold), Paragraph("System validates structured information using defined schemas.", table_cell)],
        [Paragraph("FR-06", table_cell_bold), Paragraph("System performs analytical processing on collected information.", table_cell)],
        [Paragraph("FR-07", table_cell_bold), Paragraph("System presents findings through interactive visualizations.", table_cell)],
        [Paragraph("FR-08", table_cell_bold), Paragraph("System generates HTML, Markdown, and JSON outputs.", table_cell)],
    ]
    fr_table = Table(fr_data, colWidths=[70, 430])
    fr_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#444444')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#666666')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F0F2F5')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(fr_table)

    story.append(Spacer(1, 20))
    story.append(Paragraph("8. Non-Functional Requirements", h1_style))
    story.append(Spacer(1, 4))

    nfr_data = [
        [Paragraph("Attribute", table_header), Paragraph("Requirement", table_header)],
        [
            Paragraph("Performance", table_cell_bold),
            Paragraph("Normal research requests should be processed within practical response times for the available web and model services.", table_cell)
        ],
        [
            Paragraph("Usability", table_cell_bold),
            Paragraph("The Streamlit interface should present inputs, results, analysis, and outputs clearly.", table_cell)
        ],
        [
            Paragraph("Reliability", table_cell_bold),
            Paragraph("Extraction and validation failures should not be silently treated as verified information.", table_cell)
        ],
        [
            Paragraph("Security", table_cell_bold),
            Paragraph("The prototype should avoid exposing credentials or private access information in generated reports.", table_cell)
        ],
        [
            Paragraph("Compatibility", table_cell_bold),
            Paragraph("The interface should work in commonly used modern desktop browsers.", table_cell)
        ],
    ]
    nfr_table = Table(nfr_data, colWidths=[100, 400])
    nfr_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#444444')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#666666')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F0F2F5')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(nfr_table)
    story.append(PageBreak())

    # ================= PAGE 6: TECH STACK & SYSTEM ARCHITECTURE =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("9. Technology Stack", h1_style))
    story.append(Spacer(1, 4))

    tech_data = [
        [Paragraph("Component", table_header), Paragraph("Technology", table_header), Paragraph("Purpose", table_header)],
        [Paragraph("UI", table_cell_bold), Paragraph("Streamlit", table_cell), Paragraph("Interactive interface and result presentation.", table_cell)],
        [Paragraph("Agent orchestration", table_cell_bold), Paragraph("LangGraph / LangChain", table_cell), Paragraph("Coordinate the multi-step agentic workflow.", table_cell)],
        [Paragraph("LLM", table_cell_bold), Paragraph("Google Gemini 2.5 Flash", table_cell), Paragraph("Reasoning, synthesis, and natural-language analysis.", table_cell)],
        [Paragraph("Search", table_cell_bold), Paragraph("DuckDuckGo / DDGS", table_cell), Paragraph("Web and News source discovery.", table_cell)],
        [Paragraph("Extraction", table_cell_bold), Paragraph("Trafilatura, BeautifulSoup4", table_cell), Paragraph("Public page content extraction.", table_cell)],
        [Paragraph("Validation", table_cell_bold), Paragraph("Pydantic v2", table_cell), Paragraph("Structured schema validation.", table_cell)],
        [Paragraph("Analysis", table_cell_bold), Paragraph("Pandas", table_cell), Paragraph("Data preparation and analysis.", table_cell)],
        [Paragraph("Visualization", table_cell_bold), Paragraph("Plotly", table_cell), Paragraph("Interactive charts.", table_cell)],
        [Paragraph("Outputs", table_cell_bold), Paragraph("HTML, Markdown, JSON", table_cell), Paragraph("Readable and structured result formats.", table_cell)],
    ]
    tech_table = Table(tech_data, colWidths=[105, 140, 255])
    tech_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#444444')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#666666')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F0F2F5')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(tech_table)

    story.append(Spacer(1, 16))
    story.append(Paragraph("10. System Architecture", h1_style))
    story.append(Spacer(1, 4))

    # Architecture Diagram Drawing
    d_arch = Drawing(500, 130)
    # Draw boxes
    # Row 1: User -> Streamlit -> Agent Layer -> Web + Analysis
    # User box
    d_arch.add(Rect(0, 75, 105, 45, fillColor=colors.HexColor('#F8F9FA'), strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_arch.add(String(52.5, 102, "User", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle"))
    d_arch.add(String(52.5, 88, "research objective", fontName="Helvetica", fontSize=8, textAnchor="middle"))

    # Arrow 1
    d_arch.add(Line(105, 97.5, 130, 97.5, strokeColor=colors.HexColor('#333333'), strokeWidth=1.5))
    d_arch.add(Polygon([130, 97.5, 124, 101, 124, 94], fillColor=colors.HexColor('#333333'), strokeColor=colors.HexColor('#333333')))

    # Streamlit box
    d_arch.add(Rect(130, 75, 105, 45, fillColor=colors.HexColor('#F8F9FA'), strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_arch.add(String(182.5, 102, "Streamlit", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle"))
    d_arch.add(String(182.5, 88, "interface", fontName="Helvetica", fontSize=8, textAnchor="middle"))

    # Arrow 2
    d_arch.add(Line(235, 97.5, 260, 97.5, strokeColor=colors.HexColor('#333333'), strokeWidth=1.5))
    d_arch.add(Polygon([260, 97.5, 254, 101, 254, 94], fillColor=colors.HexColor('#333333'), strokeColor=colors.HexColor('#333333')))

    # Agent Layer box
    d_arch.add(Rect(260, 75, 105, 45, fillColor=colors.HexColor('#F8F9FA'), strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_arch.add(String(312.5, 102, "Agent Layer", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle"))
    d_arch.add(String(312.5, 88, "LangGraph / ReAct", fontName="Helvetica", fontSize=8, textAnchor="middle"))

    # Arrow 3
    d_arch.add(Line(365, 97.5, 390, 97.5, strokeColor=colors.HexColor('#333333'), strokeWidth=1.5))
    d_arch.add(Polygon([390, 97.5, 384, 101, 384, 94], fillColor=colors.HexColor('#333333'), strokeColor=colors.HexColor('#333333')))

    # Web + Analysis box
    d_arch.add(Rect(390, 75, 110, 45, fillColor=colors.HexColor('#F8F9FA'), strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_arch.add(String(445, 102, "Web + Analysis", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle"))
    d_arch.add(String(445, 88, "search, scrape, validate, analyze", fontName="Helvetica", fontSize=7, textAnchor="middle"))

    # Row 2: Public Sources, Validation, Outputs
    # Public Sources
    d_arch.add(Rect(80, 10, 115, 40, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_arch.add(String(137.5, 33, "Public Sources", fontName="Helvetica-Bold", fontSize=8.5, textAnchor="middle"))
    d_arch.add(String(137.5, 20, "news / corporate / regulatory", fontName="Helvetica", fontSize=7.5, textAnchor="middle"))

    # Validation
    d_arch.add(Rect(235, 10, 115, 40, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_arch.add(String(292.5, 33, "Validation", fontName="Helvetica-Bold", fontSize=8.5, textAnchor="middle"))
    d_arch.add(String(292.5, 20, "Pydantic v2", fontName="Helvetica", fontSize=7.5, textAnchor="middle"))

    # Outputs
    d_arch.add(Rect(390, 10, 110, 40, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_arch.add(String(445, 33, "Outputs", fontName="Helvetica-Bold", fontSize=8.5, textAnchor="middle"))
    d_arch.add(String(445, 20, "HTML / Markdown / JSON", fontName="Helvetica", fontSize=7.5, textAnchor="middle"))

    # Connecting subtle dotted vertical lines between row 1 and row 2
    d_arch.add(Line(137.5, 50, 137.5, 75, strokeColor=colors.HexColor('#888888'), strokeWidth=1, strokeDashArray=[2,2]))
    d_arch.add(Line(312.5, 50, 312.5, 75, strokeColor=colors.HexColor('#888888'), strokeWidth=1, strokeDashArray=[2,2]))
    d_arch.add(Line(445, 50, 445, 75, strokeColor=colors.HexColor('#888888'), strokeWidth=1, strokeDashArray=[2,2]))

    story.append(d_arch)
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Architecture flow:</b> User → Streamlit UI → Agentic orchestration → Web/data acquisition and analysis → validated, visualized outputs.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 7: SYSTEM DESIGN =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("11. System Design", h1_style))
    story.append(Paragraph("11.1 Use Case Diagram", h2_style))
    story.append(Spacer(1, 4))

    # Use Case Diagram
    d_uc = Drawing(500, 140)
    # Background system boundary container
    d_uc.add(Rect(140, 5, 350, 130, fillColor=colors.HexColor('#000000'), strokeColor=colors.HexColor('#000000'), rx=4, ry=4))
    d_uc.add(String(315, 122, "Autonomous Market Intelligence System", fontName="Helvetica-Bold", fontSize=8.5, textAnchor="middle", fillColor=colors.white))

    # Actor: Analyst / Researcher
    d_uc.add(String(65, 80, "Analyst / Researcher", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle"))
    # Actor stick figure or clean marker
    d_uc.add(Rect(45, 95, 40, 24, fillColor=colors.HexColor('#F0F2F5'), strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_uc.add(String(65, 103, "Actor", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle"))
    d_uc.add(Line(85, 107, 140, 107, strokeColor=colors.HexColor('#333333'), strokeWidth=1.2))

    # Inside System boundary: 4 action boxes
    # Top-Left: Enter research objective
    d_uc.add(Rect(160, 68, 140, 38, fillColor=colors.white, strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_uc.add(String(230, 84, "Enter research objective", fontName="Helvetica", fontSize=8, textAnchor="middle"))

    # Top-Right: Review synthesized insights
    d_uc.add(Rect(330, 68, 140, 38, fillColor=colors.white, strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_uc.add(String(400, 84, "Review synthesized insights", fontName="Helvetica", fontSize=8, textAnchor="middle"))

    # Bottom-Left: Run discovery & scraping
    d_uc.add(Rect(160, 18, 140, 38, fillColor=colors.white, strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_uc.add(String(230, 34, "Run discovery & scraping", fontName="Helvetica", fontSize=8, textAnchor="middle"))

    # Bottom-Right: View / export results
    d_uc.add(Rect(330, 18, 140, 38, fillColor=colors.white, strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_uc.add(String(400, 34, "View / export results", fontName="Helvetica", fontSize=8, textAnchor="middle"))

    story.append(d_uc)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "The main actor is an analyst/researcher. The system supports entering an objective, running discovery and extraction, "
        "reviewing synthesized insights, viewing analysis, validating structured information, and exporting results.",
        body_style
    ))

    story.append(Spacer(1, 14))
    story.append(Paragraph("11.2 DFD / Flowchart", h2_style))
    story.append(Spacer(1, 4))

    # DFD / Flowchart
    d_dfd = Drawing(500, 130)
    # Top Row: User -> Agentic Orchestrator -> Result
    d_dfd.add(Rect(10, 80, 100, 40, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_dfd.add(String(60, 97, "User", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle"))

    d_dfd.add(Line(110, 100, 175, 100, strokeColor=colors.HexColor('#333333'), strokeWidth=1.5))
    d_dfd.add(Polygon([175, 100, 169, 103, 169, 97], fillColor=colors.HexColor('#333333'), strokeColor=colors.HexColor('#333333')))

    d_dfd.add(Rect(175, 80, 150, 40, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_dfd.add(String(250, 97, "Agentic Orchestrator", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle"))

    d_dfd.add(Line(325, 100, 390, 100, strokeColor=colors.HexColor('#333333'), strokeWidth=1.5))
    d_dfd.add(Polygon([390, 100, 384, 103, 384, 97], fillColor=colors.HexColor('#333333'), strokeColor=colors.HexColor('#333333')))

    d_dfd.add(Rect(390, 80, 100, 40, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#333333'), strokeWidth=1))
    d_dfd.add(String(440, 97, "Result", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle"))

    # Connecting branches from Agentic Orchestrator to 4 sub-modules
    d_dfd.add(Line(250, 80, 60, 50, strokeColor=colors.HexColor('#555555'), strokeWidth=1))
    d_dfd.add(Line(250, 80, 185, 50, strokeColor=colors.HexColor('#555555'), strokeWidth=1))
    d_dfd.add(Line(250, 80, 315, 50, strokeColor=colors.HexColor('#555555'), strokeWidth=1))
    d_dfd.add(Line(250, 80, 440, 50, strokeColor=colors.HexColor('#555555'), strokeWidth=1))

    # 4 Bottom boxes (Black background with white text matching provided document style)
    # Box 1: Discovery
    d_dfd.add(Rect(10, 5, 105, 45, fillColor=colors.HexColor('#000000'), strokeColor=colors.HexColor('#000000'), rx=2, ry=2))
    d_dfd.add(String(62.5, 32, "Discovery", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=colors.white))
    d_dfd.add(String(62.5, 18, "DuckDuckGo Web / News", fontName="Helvetica", fontSize=6.5, textAnchor="middle", fillColor=colors.white))

    # Box 2: Extraction
    d_dfd.add(Rect(132, 5, 105, 45, fillColor=colors.HexColor('#000000'), strokeColor=colors.HexColor('#000000'), rx=2, ry=2))
    d_dfd.add(String(184.5, 32, "Extraction", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=colors.white))
    d_dfd.add(String(184.5, 18, "Trafilatura / BS4", fontName="Helvetica", fontSize=6.5, textAnchor="middle", fillColor=colors.white))

    # Box 3: Validation
    d_dfd.add(Rect(255, 5, 105, 45, fillColor=colors.HexColor('#000000'), strokeColor=colors.HexColor('#000000'), rx=2, ry=2))
    d_dfd.add(String(307.5, 32, "Validation", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=colors.white))
    d_dfd.add(String(307.5, 18, "Pydantic v2", fontName="Helvetica", fontSize=6.5, textAnchor="middle", fillColor=colors.white))

    # Box 4: Analysis
    d_dfd.add(Rect(377, 5, 110, 45, fillColor=colors.HexColor('#000000'), strokeColor=colors.HexColor('#000000'), rx=2, ry=2))
    d_dfd.add(String(432, 32, "Analysis", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=colors.white))
    d_dfd.add(String(432, 18, "Pandas / agent", fontName="Helvetica", fontSize=6.5, textAnchor="middle", fillColor=colors.white))

    story.append(d_dfd)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "The information flow is: research objective → agentic orchestration → discovery → extraction → validation → analysis → results. "
        "Search results and accessible public pages act as external information inputs.",
        body_style
    ))

    story.append(Spacer(1, 14))
    story.append(Paragraph("11.3 ER Diagram / Database", h2_style))
    story.append(Paragraph(
        "A dedicated relational database is not specified as a core component of the current prototype; therefore, an ER diagram "
        "is not included as an implemented design element.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 8: MODULE DESCRIPTION =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("12. Module Description", h1_style))
    story.append(Spacer(1, 4))

    modules = [
        ("Module 1 — User Interface:", "Streamlit interface for entering the research objective and reviewing generated findings, visualizations, and outputs."),
        ("Module 2 — Query & Discovery:", "Uses the research objective to discover potentially relevant Web and News sources through DuckDuckGo/DDGS."),
        ("Module 3 — Web Extraction:", "Retrieves accessible public pages and extracts useful text using Trafilatura and BeautifulSoup4."),
        ("Module 4 — Agentic Synthesis:", "LangGraph/LangChain coordinates the reasoning workflow, with Gemini 2.5 Flash used for synthesis and analysis."),
        ("Module 5 — Validation:", "Pydantic v2 structures and validates information before downstream use."),
        ("Module 6 — Strategic Analysis:", "Processes collected information and derives market/competitor-oriented analytical observations."),
        ("Module 7 — Visualization & Output:", "Pandas and Plotly support analytical presentation; HTML, Markdown, and JSON provide reusable outputs.")
    ]
    for m_title, m_desc in modules:
        story.append(Paragraph(f"<b>{m_title}</b> {m_desc}", body_style))
        story.append(Spacer(1, 7))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Module interaction</b>", h2_style))
    story.append(Spacer(1, 4))
    interactions = [
        "The UI passes the research objective to the orchestration layer.",
        "The discovery module finds candidate sources and the extraction module prepares page content.",
        "The validation stage checks structured information before analysis.",
        "The synthesis/analysis stage produces findings that are visualized and exported."
    ]
    for item in interactions:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(PageBreak())

    # ================= PAGE 9: DATABASE DESIGN & TESTING =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("13. Database Design &amp; 14. Testing", h1_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Database Design</b>", h2_style))
    story.append(Paragraph(
        "The current prototype does not identify a dedicated relational database as a core implementation component. "
        "Information is processed through the research pipeline and represented in structured outputs; therefore, database "
        "tables and an ER schema are not claimed as implemented features.",
        body_style
    ))

    story.append(Spacer(1, 16))
    story.append(Paragraph("<b>Test Cases</b>", h2_style))
    story.append(Spacer(1, 4))

    tc_data = [
        [Paragraph("Test ID", table_header), Paragraph("Test Case", table_header), Paragraph("Expected Result", table_header), Paragraph("Status", table_header)],
        [
            Paragraph("TC-01", table_cell_bold),
            Paragraph("Submit a valid market-research objective.", table_cell),
            Paragraph("Objective is accepted and workflow starts.", table_cell),
            Paragraph("Pass/Fail", table_cell)
        ],
        [
            Paragraph("TC-02", table_cell_bold),
            Paragraph("Run Web/News discovery.", table_cell),
            Paragraph("Relevant search results are returned.", table_cell),
            Paragraph("Pass/Fail", table_cell)
        ],
        [
            Paragraph("TC-03", table_cell_bold),
            Paragraph("Process an accessible public source.", table_cell),
            Paragraph("Relevant text is extracted.", table_cell),
            Paragraph("Pass/Fail", table_cell)
        ],
        [
            Paragraph("TC-04", table_cell_bold),
            Paragraph("Run synthesis and validation.", table_cell),
            Paragraph("Structured, validated intelligence is produced.", table_cell),
            Paragraph("Pass/Fail", table_cell)
        ],
        [
            Paragraph("TC-05", table_cell_bold),
            Paragraph("Generate visualization and export.", table_cell),
            Paragraph("Visualization is displayed and supported outputs are generated.", table_cell),
            Paragraph("Pass/Fail", table_cell)
        ],
    ]
    tc_table = Table(tc_data, colWidths=[65, 155, 205, 75])
    tc_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#444444')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#666666')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F0F2F5')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(tc_table)

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "<b>Testing note:</b> Status should be marked after execution on the final project build. "
        "The cases above are based on the actual functional workflow described for this project.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 10: LIMITATIONS & FUTURE SCOPE =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("15. Limitations", h1_style))
    story.append(Spacer(1, 4))
    limitations = [
        "Results depend on the availability, accessibility, and quality of public web sources.",
        "Search and extraction may be affected by website structure, dynamic content, access restrictions, or temporary failures.",
        "AI-generated synthesis requires human review before use in high-stakes business decisions.",
        "The prototype is focused on public-source intelligence rather than a complete enterprise data platform.",
        "Analytical quality depends on the relevance and completeness of retrieved evidence."
    ]
    for lim in limitations:
        story.append(Paragraph(f"• {lim}", bullet_style))

    story.append(Spacer(1, 22))
    story.append(Paragraph("16. Future Scope", h1_style))
    story.append(Spacer(1, 4))
    future_scope = [
        "Add stronger source ranking and evidence traceability.",
        "Integrate additional structured market-data providers and APIs.",
        "Support scheduled research workflows and automated monitoring.",
        "Add richer historical trend analysis and comparative dashboards.",
        "Strengthen authentication, access control, deployment, and multi-user support.",
        "Expand integrations for downstream business workflows."
    ]
    for fs in future_scope:
        story.append(Paragraph(f"• {fs}", bullet_style))

    story.append(PageBreak())

    # ================= PAGE 11: REFERENCES & CHECKLIST =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("17. References", h1_style))
    story.append(Spacer(1, 4))
    references = [
        "LangGraph / LangChain documentation — agent orchestration and workflow concepts.",
        "Google Gemini documentation — Gemini 2.5 Flash model and API usage.",
        "DuckDuckGo / DDGS documentation — Web and News search access.",
        "Trafilatura documentation — web-page text extraction.",
        "BeautifulSoup4 documentation — HTML parsing and extraction.",
        "Pydantic v2 documentation — structured data validation.",
        "Pandas documentation — data processing and analysis.",
        "Plotly documentation — interactive visualization.",
        "Streamlit documentation — Python interactive application framework.",
        "Public corporate, regulatory, news, industry, and cloud-ecosystem sources identified in the project scope."
    ]
    for ref in references:
        story.append(Paragraph(f"• {ref}", bullet_style))

    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>SRS Coverage Checklist</b>", h2_style))
    story.append(Spacer(1, 4))

    check_data = [
        [Paragraph("Item", table_header), Paragraph("Included", table_header)],
        [Paragraph("Cover Page / Abstract / Problem / Objectives", table_cell), Paragraph("Yes", table_cell_bold)],
        [Paragraph("Proposed Solution / Scope", table_cell), Paragraph("Yes", table_cell_bold)],
        [Paragraph("Functional / Non-Functional Requirements", table_cell), Paragraph("Yes", table_cell_bold)],
        [Paragraph("Technology Stack / Architecture", table_cell), Paragraph("Yes", table_cell_bold)],
        [Paragraph("Use Case / DFD / Database applicability", table_cell), Paragraph("Yes", table_cell_bold)],
        [Paragraph("Module Description / Testing", table_cell), Paragraph("Yes", table_cell_bold)],
        [Paragraph("Limitations / Future Scope / References", table_cell), Paragraph("Yes", table_cell_bold)],
    ]
    check_table = Table(check_data, colWidths=[380, 120])
    check_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#444444')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#666666')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F0F2F5')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(check_table)

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "The structure follows the uploaded SRS template, which specifies the sequence from cover page and "
        "abstract through requirements, architecture/design, modules, testing, limitations, future scope, and references.",
        body_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully created {PDF_FILENAME}")

if __name__ == "__main__":
    create_srs_pdf()
