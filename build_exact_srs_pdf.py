"""
SRS PDF Generator — Professional Industry Format (Referencing Synopsis)
======================================================================
Autonomous Agentic Web Scraper & Strategic Market Intelligence Analyzer
B.Tech 3rd Year Mini Project | Academic Year 2026-27 | ABES Engineering College
Project Guide: Radhika Singhal | Student: Adarsh Dubey (2400320100061)

Incorporates high-fidelity diagrams matching the Project Synopsis:
- Figure 1: 8-Stage Agentic Workflow with Feedback Loop (Color-coded by phase)
- Figure 2: High-Level System Architecture (Interface, Agent Brain, Tool Belt, Public Web, Deliverables)
- Figure 3: Use Case Diagram (Analyst vs System Boundary)
- Figure 4: LangGraph ReAct Agent Execution Loop
- Figure 5: UML Class & Pydantic Schema Diagram
"""

import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import (
    Drawing, Rect, String, Line, Group, Polygon, Circle, Ellipse
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "SRS_Market_Intelligence_Analyzer.pdf"

# ── Color Palette (Matching Synopsis Reference) ──────────────────────────────
C_NAVY          = colors.HexColor("#1E293B")
C_BLUE          = colors.HexColor("#2563EB")
C_BLUE_LIGHT    = colors.HexColor("#EFF6FF")
C_BLUE_BORDER   = colors.HexColor("#BFDBFE")

C_TEAL          = colors.HexColor("#0D9488")
C_TEAL_LIGHT    = colors.HexColor("#F0FDFA")
C_TEAL_BORDER   = colors.HexColor("#99F6E4")

C_PURPLE        = colors.HexColor("#7C3AED")
C_PURPLE_LIGHT  = colors.HexColor("#FAF5FF")
C_PURPLE_BORDER = colors.HexColor("#DDD6FE")

C_GREEN         = colors.HexColor("#16A34A")
C_GREEN_LIGHT   = colors.HexColor("#F0FDF4")
C_GREEN_BORDER  = colors.HexColor("#BBF7D0")

C_AMBER         = colors.HexColor("#D97706")
C_AMBER_LIGHT   = colors.HexColor("#FFFBEB")
C_AMBER_BORDER  = colors.HexColor("#FDE68A")

C_RED           = colors.HexColor("#DC2626")
C_RED_LIGHT     = colors.HexColor("#FEF2F2")

C_GRAY_HVY      = colors.HexColor("#334155")
C_GRAY_MED      = colors.HexColor("#64748B")
C_GRAY_LITE     = colors.HexColor("#E2E8F0")
C_GRAY_PALE     = colors.HexColor("#F8FAFC")
C_WHITE         = colors.white
C_RULE          = colors.HexColor("#CBD5E1")

BOX_COLORS = {
    "blue":   (C_BLUE_LIGHT,   C_BLUE),
    "teal":   (C_TEAL_LIGHT,   C_TEAL),
    "purple": (C_PURPLE_LIGHT, C_PURPLE),
    "green":  (C_GREEN_LIGHT,  C_GREEN),
    "amber":  (C_AMBER_LIGHT,  C_AMBER),
    "red":    (C_RED_LIGHT,    C_RED),
    "gray":   (C_GRAY_PALE,    C_GRAY_HVY),
    "navy":   (C_BLUE_LIGHT,   C_NAVY),
}


# ── Canvas Decorator (Header + Footer + Running Page Number) ─────────────────
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_chrome(total)
            super().showPage()
        super().save()

    def _draw_chrome(self, total):
        p = self._pageNumber
        W, H = letter
        self.saveState()

        if p > 1:
            # Header
            self.setFillColor(C_NAVY)
            self.rect(54, H - 32, W - 108, 1.2, fill=1, stroke=0)
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(C_NAVY)
            self.drawString(54, H - 26, "SOFTWARE REQUIREMENTS SPECIFICATION (IEEE Std 830-1998)")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(C_GRAY_MED)
            self.drawRightString(W - 54, H - 26, "Autonomous Market Intelligence Analyzer")

        # Footer
        self.setFillColor(C_GRAY_LITE)
        self.rect(54, 38, W - 108, 1.2, fill=1, stroke=0)
        self.setFont("Helvetica", 7.5)
        self.setFillColor(C_GRAY_MED)
        self.drawString(54, 26, "B.Tech Mini Project | ABES Engineering College | Guide: Radhika Singhal")
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(C_NAVY)
        self.drawRightString(W - 54, 26, f"Page {p} of {total}")

        self.restoreState()


# ── Vector Icon Drawing Helpers ──────────────────────────────────────────────
def draw_chat_icon(d, cx, cy, col):
    d.add(Rect(cx - 7, cy - 3, 14, 10, rx=2, ry=2, fillColor=col, strokeColor=col, strokeWidth=0))
    d.add(Polygon([cx - 4, cy - 3, cx - 1, cy - 3, cx - 5, cy - 7], fillColor=col, strokeColor=col, strokeWidth=0))
    for dx in (-3, 0, 3):
        d.add(Circle(cx + dx, cy + 2, 1, fillColor=C_WHITE, strokeColor=C_WHITE, strokeWidth=0))

def draw_search_icon(d, cx, cy, col):
    d.add(Circle(cx - 2, cy + 2, 4.5, fillColor=None, strokeColor=col, strokeWidth=1.8))
    d.add(Line(cx + 1.5, cy - 1.5, cx + 5.5, cy - 5.5, strokeColor=col, strokeWidth=2.2))

def draw_doc_icon(d, cx, cy, col):
    d.add(Rect(cx - 5, cy - 6, 10, 13, rx=1, ry=1, fillColor=C_WHITE, strokeColor=col, strokeWidth=1.2))
    d.add(Line(cx - 3, cy + 3, cx + 3, cy + 3, strokeColor=col, strokeWidth=1))
    d.add(Line(cx - 3, cy, cx + 3, cy, strokeColor=col, strokeWidth=1))
    d.add(Line(cx - 3, cy - 3, cx + 1, cy - 3, strokeColor=col, strokeWidth=1))

def draw_sparkle_icon(d, cx, cy, col):
    pts = [cx, cy + 7, cx + 2, cy + 2, cx + 7, cy, cx + 2, cy - 2,
           cx, cy - 7, cx - 2, cy - 2, cx - 7, cy, cx - 2, cy + 2]
    d.add(Polygon(pts, fillColor=col, strokeColor=col, strokeWidth=0))

def draw_check_icon(d, cx, cy, col):
    d.add(Circle(cx, cy, 6.5, fillColor=col, strokeColor=col, strokeWidth=0))
    d.add(Line(cx - 3, cy, cx - 1, cy - 2.5, strokeColor=C_WHITE, strokeWidth=1.5))
    d.add(Line(cx - 1, cy - 2.5, cx + 3.5, cy + 2.5, strokeColor=C_WHITE, strokeWidth=1.5))

def draw_barchart_icon(d, cx, cy, col):
    d.add(Rect(cx - 5, cy - 5, 2.5, 5, fillColor=col, strokeColor=col, strokeWidth=0))
    d.add(Rect(cx - 1.25, cy - 5, 2.5, 10, fillColor=col, strokeColor=col, strokeWidth=0))
    d.add(Rect(cx + 2.5, cy - 5, 2.5, 7.5, fillColor=col, strokeColor=col, strokeWidth=0))

def draw_linechart_icon(d, cx, cy, col):
    d.add(Line(cx - 5, cy - 3, cx - 2, cy + 2, strokeColor=col, strokeWidth=1.5))
    d.add(Line(cx - 2, cy + 2, cx + 1, cy - 1, strokeColor=col, strokeWidth=1.5))
    d.add(Line(cx + 1, cy - 1, cx + 5, cy + 4, strokeColor=col, strokeWidth=1.5))
    for px, py in [(-5, -3), (-2, 2), (1, -1), (5, 4)]:
        d.add(Circle(cx + px, cy + py, 1.2, fillColor=col, strokeColor=col, strokeWidth=0))

def draw_download_icon(d, cx, cy, col):
    d.add(Line(cx, cy + 4, cx, cy - 2, strokeColor=col, strokeWidth=1.5))
    d.add(Polygon([cx, cy - 4, cx - 3, cy - 1, cx + 3, cy - 1], fillColor=col, strokeColor=col, strokeWidth=0))
    d.add(Line(cx - 5, cy - 5, cx + 5, cy - 5, strokeColor=col, strokeWidth=1.5))

def draw_user_icon(d, cx, cy, col):
    d.add(Circle(cx, cy + 4, 4.5, fillColor=col, strokeColor=col, strokeWidth=0))
    d.add(Ellipse(cx, cy - 5, 7.5, 4, fillColor=col, strokeColor=col, strokeWidth=0))

def draw_numbered_badge(d, cx, cy, num, col=C_BLUE, r=7):
    d.add(Circle(cx, cy, r, fillColor=col, strokeColor=C_WHITE, strokeWidth=1.2))
    d.add(String(cx, cy - 3, str(num), fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=C_WHITE))


# ── DIAGRAM 1: HIGH-LEVEL SYSTEM ARCHITECTURE (Figure 2 in Synopsis) ─────────
def make_synopsis_architecture_diagram():
    W, H = 504, 340
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=C_WHITE, strokeColor=C_GRAY_LITE, strokeWidth=1))

    # Top legend bar
    legend_items = [
        (C_BLUE,   "Interface"),
        (C_PURPLE, "Agent brain"),
        (C_TEAL,   "Tool belt"),
        (C_AMBER,  "Public web"),
        (C_GREEN,  "Results"),
    ]
    lx = 14
    ly = H - 18
    for col, text in legend_items:
        d.add(Circle(lx + 4, ly + 3, 4, fillColor=col, strokeColor=col, strokeWidth=0))
        d.add(String(lx + 12, ly, text, fontName="Helvetica-Bold", fontSize=7, fillColor=C_GRAY_HVY))
        lx += 64
    d.add(String(W - 14, ly, "Numbered badges show the order of events",
                 fontName="Helvetica", fontSize=6.5, textAnchor="end", fillColor=C_GRAY_MED))
    d.add(Line(10, H - 25, W - 10, H - 25, strokeColor=C_GRAY_LITE, strokeWidth=0.8))

    tab_w = 18

    # LAYER 1: INTERFACE
    l1_y, l1_h = 246, 64
    d.add(Rect(8, l1_y, W - 16, l1_h, rx=4, ry=4, fillColor=C_BLUE_LIGHT, strokeColor=C_BLUE_BORDER, strokeWidth=1))
    d.add(Rect(8, l1_y, tab_w, l1_h, rx=4, ry=4, fillColor=C_BLUE, strokeColor=C_BLUE, strokeWidth=0))
    d.add(Rect(8 + tab_w - 4, l1_y, 4, l1_h, rx=0, ry=0, fillColor=C_BLUE, strokeColor=C_BLUE, strokeWidth=0))
    for i, ch in enumerate("INTERFACE"):
        d.add(String(8 + tab_w/2, l1_y + l1_h - 10 - i * 6.2, ch,
                     fontName="Helvetica-Bold", fontSize=5.5, textAnchor="middle", fillColor=C_WHITE))

    # User Card
    d.add(Rect(32, l1_y + 6, 92, l1_h - 12, rx=4, ry=4, fillColor=C_WHITE, strokeColor=C_BLUE, strokeWidth=1.2))
    draw_user_icon(d, 48, l1_y + 32, C_BLUE)
    d.add(String(62, l1_y + 34, "USER", fontName="Helvetica-Bold", fontSize=8, fillColor=C_NAVY))
    d.add(String(62, l1_y + 24, "Analyst asks a", fontName="Helvetica", fontSize=6, fillColor=C_GRAY_MED))
    d.add(String(62, l1_y + 15, "research question", fontName="Helvetica", fontSize=6, fillColor=C_GRAY_MED))

    # Arrow User -> Streamlit (Badge 1)
    d.add(Line(124, l1_y + 32, 160, l1_y + 32, strokeColor=C_BLUE, strokeWidth=1.5))
    d.add(Polygon([160, l1_y + 32, 154, l1_y + 35, 154, l1_y + 29], fillColor=C_BLUE, strokeColor=C_BLUE, strokeWidth=0))
    draw_numbered_badge(d, 142, l1_y + 32, 1, col=C_BLUE, r=6.5)

    # Streamlit Card
    d.add(Rect(160, l1_y + 6, 175, l1_h - 12, rx=4, ry=4, fillColor=C_WHITE, strokeColor=C_BLUE, strokeWidth=1.4))
    d.add(Rect(168, l1_y + 31, 14, 14, rx=2, ry=2, fillColor=C_BLUE, strokeColor=C_BLUE, strokeWidth=0))
    d.add(String(175, l1_y + 35, "UI", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=C_WHITE))
    d.add(String(188, l1_y + 34, "STREAMLIT DASHBOARD", fontName="Helvetica-Bold", fontSize=8, fillColor=C_BLUE))
    d.add(String(188, l1_y + 21, "input  |  charts  |  downloads", fontName="Helvetica", fontSize=6.5, fillColor=C_GRAY_HVY))

    # Deliverables Card
    d.add(Rect(375, l1_y + 6, 115, l1_h - 12, rx=4, ry=4, fillColor=C_WHITE, strokeColor=C_GREEN, strokeWidth=1.4))
    draw_download_icon(d, 390, l1_y + 32, C_GREEN)
    d.add(String(402, l1_y + 34, "DELIVERABLES", fontName="Helvetica-Bold", fontSize=7.5, fillColor=C_GREEN))
    d.add(String(402, l1_y + 23, "Plotly charts + tables", fontName="Helvetica", fontSize=6, fillColor=C_GRAY_HVY))
    d.add(String(402, l1_y + 14, "HTML | MD | JSON", fontName="Helvetica-Bold", fontSize=6, fillColor=C_GRAY_MED))

    # Arrow Deliverables -> Streamlit (Badge 7)
    d.add(Line(375, l1_y + 32, 335, l1_y + 32, strokeColor=C_GREEN, strokeWidth=1.5))
    d.add(Polygon([335, l1_y + 32, 341, l1_y + 35, 341, l1_y + 29], fillColor=C_GREEN, strokeColor=C_GREEN, strokeWidth=0))
    draw_numbered_badge(d, 355, l1_y + 32, 7, col=C_GREEN, r=6.5)

    # LAYER 2: AGENT BRAIN
    l2_y, l2_h = 166, 72
    d.add(Rect(8, l2_y, W - 16, l2_h, rx=4, ry=4, fillColor=C_PURPLE_LIGHT, strokeColor=C_PURPLE_BORDER, strokeWidth=1))
    d.add(Rect(8, l2_y, tab_w, l2_h, rx=4, ry=4, fillColor=C_PURPLE, strokeColor=C_PURPLE, strokeWidth=0))
    d.add(Rect(8 + tab_w - 4, l2_y, 4, l2_h, rx=0, ry=0, fillColor=C_PURPLE, strokeColor=C_PURPLE, strokeWidth=0))
    for i, ch in enumerate("AGENT BRAIN"):
        d.add(String(8 + tab_w/2, l2_y + l2_h - 8 - i * 5.8, ch,
                     fontName="Helvetica-Bold", fontSize=5, textAnchor="middle", fillColor=C_WHITE))

    # Flow 2 (Streamlit -> Agent Orchestrator: research objective)
    d.add(Line(230, l1_y, 230, l2_y + l2_h, strokeColor=C_BLUE, strokeWidth=1.5))
    d.add(Polygon([230, l2_y + l2_h, 227, l2_y + l2_h + 5, 233, l2_y + l2_h + 5],
                  fillColor=C_BLUE, strokeColor=C_BLUE, strokeWidth=0))
    draw_numbered_badge(d, 230, l2_y + l2_h + 4, 2, col=C_BLUE, r=6.5)
    d.add(Rect(238, l2_y + l2_h - 1, 80, 11, rx=2, ry=2, fillColor=C_BLUE_LIGHT, strokeColor=C_BLUE_BORDER, strokeWidth=0.8))
    d.add(String(242, l2_y + l2_h + 2, "research objective", fontName="Helvetica-Bold", fontSize=6, fillColor=C_BLUE))

    # Orchestrator Card
    d.add(Rect(32, l2_y + 5, 215, l2_h - 10, rx=4, ry=4, fillColor=C_WHITE, strokeColor=C_PURPLE, strokeWidth=1.4))
    d.add(String(42, l2_y + l2_h - 18, "AGENT ORCHESTRATOR", fontName="Helvetica-Bold", fontSize=8, fillColor=C_PURPLE))
    d.add(String(160, l2_y + l2_h - 18, "LangGraph / ReAct", fontName="Helvetica", fontSize=6.5, fillColor=C_GRAY_MED))

    caps = [(42, "THINK"), (104, "ACT"), (160, "OBSERVE")]
    for cx, txt in caps:
        d.add(Rect(cx, l2_y + 20, 48, 16, rx=8, ry=8, fillColor=colors.HexColor("#EDE9FE"), strokeColor=C_PURPLE, strokeWidth=0.8))
        d.add(String(cx + 24, l2_y + 24, txt, fontName="Helvetica-Bold", fontSize=6.5, textAnchor="middle", fillColor=C_PURPLE))
    d.add(Line(90, l2_y + 28, 102, l2_y + 28, strokeColor=C_PURPLE, strokeWidth=1))
    d.add(Polygon([102, l2_y + 28, 98, l2_y + 30, 98, l2_y + 26], fillColor=C_PURPLE, strokeColor=C_PURPLE, strokeWidth=0))
    d.add(Line(152, l2_y + 28, 158, l2_y + 28, strokeColor=C_PURPLE, strokeWidth=1))
    d.add(Polygon([158, l2_y + 28, 154, l2_y + 30, 154, l2_y + 26], fillColor=C_PURPLE, strokeColor=C_PURPLE, strokeWidth=0))
    d.add(String(139, l2_y + 9, "repeat until enough evidence is gathered",
                 fontName="Helvetica-Oblique", fontSize=5.5, textAnchor="middle", fillColor=C_GRAY_MED))

    # Arrow 3 (Orchestrator <-> Gemini: reason)
    d.add(Line(247, l2_y + 36, 290, l2_y + 36, strokeColor=C_PURPLE, strokeWidth=1.5, strokeDashArray=[3, 1]))
    d.add(Polygon([247, l2_y + 36, 252, l2_y + 38, 252, l2_y + 34], fillColor=C_PURPLE, strokeColor=C_PURPLE, strokeWidth=0))
    d.add(Polygon([290, l2_y + 36, 285, l2_y + 38, 285, l2_y + 34], fillColor=C_PURPLE, strokeColor=C_PURPLE, strokeWidth=0))
    draw_numbered_badge(d, 268, l2_y + 36, 3, col=C_PURPLE, r=6.5)
    d.add(String(268, l2_y + 44, "reason", fontName="Helvetica-Bold", fontSize=6, textAnchor="middle", fillColor=C_PURPLE))

    # Gemini Card
    d.add(Rect(290, l2_y + 5, 200, l2_h - 10, rx=4, ry=4, fillColor=C_WHITE, strokeColor=C_PURPLE, strokeWidth=1.4))
    draw_sparkle_icon(d, 305, l2_y + l2_h - 18, C_PURPLE)
    d.add(String(316, l2_y + l2_h - 17, "GEMINI 2.5 FLASH", fontName="Helvetica-Bold", fontSize=8, fillColor=C_PURPLE))
    d.add(String(316, l2_y + l2_h - 26, "The LLM \"reasoning engine\"", fontName="Helvetica-Bold", fontSize=6.5, fillColor=C_GRAY_HVY))
    d.add(String(300, l2_y + 26, "- Understands the question", fontName="Helvetica", fontSize=6, fillColor=C_GRAY_MED))
    d.add(String(300, l2_y + 17, "- Summarises the evidence", fontName="Helvetica", fontSize=6, fillColor=C_GRAY_MED))
    d.add(String(300, l2_y + 8,  "- Returns structured findings", fontName="Helvetica", fontSize=6, fillColor=C_GRAY_MED))

    # LAYER 3: TOOL BELT
    l3_y, l3_h = 88, 70
    d.add(Rect(8, l3_y, W - 16, l3_h, rx=4, ry=4, fillColor=C_TEAL_LIGHT, strokeColor=C_TEAL_BORDER, strokeWidth=1))
    d.add(Rect(8, l3_y, tab_w, l3_h, rx=4, ry=4, fillColor=C_TEAL, strokeColor=C_TEAL, strokeWidth=0))
    d.add(Rect(8 + tab_w - 4, l3_y, 4, l3_h, rx=0, ry=0, fillColor=C_TEAL, strokeColor=C_TEAL, strokeWidth=0))
    for i, ch in enumerate("TOOL BELT"):
        d.add(String(8 + tab_w/2, l3_y + l3_h - 10 - i * 6.5, ch,
                     fontName="Helvetica-Bold", fontSize=5.5, textAnchor="middle", fillColor=C_WHITE))

    # Arrow 4 (calls tools)
    d.add(Line(139, l2_y + 5, 139, l3_y + l3_h - 2, strokeColor=C_TEAL, strokeWidth=1.5))
    d.add(Polygon([139, l3_y + l3_h - 2, 136, l3_y + l3_h + 3, 142, l3_y + l3_h + 3],
                  fillColor=C_TEAL, strokeColor=C_TEAL, strokeWidth=0))
    draw_numbered_badge(d, 139, (l2_y + l3_y + l3_h)/2 + 2, 4, col=C_TEAL, r=6.5)
    d.add(String(148, (l2_y + l3_y + l3_h)/2, "calls tools", fontName="Helvetica-Bold", fontSize=6, fillColor=C_TEAL))

    # 4 Tool Cards
    tool_cards = [
        (32,  "SEARCH",   "DuckDuckGo",   "Web + News",          draw_search_icon, C_BLUE),
        (148, "SCRAPE",   "Trafilatura",  "+ BeautifulSoup4",    draw_doc_icon,    C_TEAL),
        (264, "VALIDATE", "Pydantic v2",  "evidence checks",     draw_check_icon,  C_PURPLE),
        (380, "ANALYZE",  "Pandas +",     "Plotly benchmark",    draw_barchart_icon, C_GREEN),
    ]
    for tx, ttitle, l1, l2, icon_fn, col in tool_cards:
        tw = 110
        d.add(Rect(tx, l3_y + 6, tw, l3_h - 12, rx=4, ry=4, fillColor=C_WHITE, strokeColor=col, strokeWidth=1.2))
        icon_fn(d, tx + 18, l3_y + l3_h - 22, col)
        d.add(String(tx + 32, l3_y + l3_h - 20, ttitle, fontName="Helvetica-Bold", fontSize=7.5, fillColor=col))
        d.add(String(tx + 12, l3_y + 22, l1, fontName="Helvetica-Bold", fontSize=6.5, fillColor=C_NAVY))
        d.add(String(tx + 12, l3_y + 12, l2, fontName="Helvetica", fontSize=6, fillColor=C_GRAY_MED))

    # LAYER 4: PUBLIC WEB
    l4_y, l4_h = 10, 70
    d.add(Rect(8, l4_y, W - 16, l4_h, rx=4, ry=4, fillColor=C_AMBER_LIGHT, strokeColor=C_AMBER_BORDER, strokeWidth=1))
    d.add(Rect(8, l4_y, tab_w, l4_h, rx=4, ry=4, fillColor=C_AMBER, strokeColor=C_AMBER, strokeWidth=0))
    d.add(Rect(8 + tab_w - 4, l4_y, 4, l4_h, rx=0, ry=0, fillColor=C_AMBER, strokeColor=C_AMBER, strokeWidth=0))
    for i, ch in enumerate("PUBLIC WEB"):
        d.add(String(8 + tab_w/2, l4_y + l4_h - 10 - i * 6, ch,
                     fontName="Helvetica-Bold", fontSize=5.5, textAnchor="middle", fillColor=C_WHITE))

    # Arrow 5 (queries go out, clean pages come back)
    d.add(Line(160, l3_y + 6, 160, l4_y + l4_h - 2, strokeColor=C_AMBER, strokeWidth=1.5))
    d.add(Polygon([160, l4_y + l4_h - 2, 157, l4_y + l4_h + 3, 163, l4_y + l4_h + 3],
                  fillColor=C_AMBER, strokeColor=C_AMBER, strokeWidth=0))
    d.add(Polygon([160, l3_y + 6, 157, l3_y + 1, 163, l3_y + 1],
                  fillColor=C_AMBER, strokeColor=C_AMBER, strokeWidth=0))
    draw_numbered_badge(d, 160, (l3_y + l4_y + l4_h)/2 + 2, 5, col=C_AMBER, r=6.5)
    d.add(String(170, (l3_y + l4_y + l4_h)/2, "queries go out, clean pages come back",
                 fontName="Helvetica-Bold", fontSize=6, fillColor=C_AMBER))

    # 5 Public Web source pills
    web_pills = [
        (32,  "Business news",      "Reuters, CNBC..."),
        (124, "Investor portals",   "TCS, Infosys, HCL..."),
        (216, "Regulators",         "SEC EDGAR, BSE/NSE"),
        (308, "Industry benchmarks", "Gartner, IDC, Everest"),
        (400, "Cloud ecosystems",   "AWS, Azure, GCP"),
    ]
    for px, ptitle, psub in web_pills:
        pw = 90 if px < 400 else 88
        d.add(Rect(px, l4_y + 8, pw, l4_h - 24, rx=4, ry=4, fillColor=C_WHITE, strokeColor=C_AMBER_BORDER, strokeWidth=1))
        d.add(String(px + pw/2, l4_y + l4_h - 28, ptitle, fontName="Helvetica-Bold", fontSize=6.5, textAnchor="middle", fillColor=C_NAVY))
        d.add(String(px + pw/2, l4_y + 14, psub, fontName="Helvetica", fontSize=5.5, textAnchor="middle", fillColor=C_GRAY_MED))

    # Arrow 6 (insights delivered)
    d.add(Line(496, l3_y + 35, 496, l1_y + 25, strokeColor=C_GREEN, strokeWidth=1.5))
    d.add(Line(490, l3_y + 35, 496, l3_y + 35, strokeColor=C_GREEN, strokeWidth=1.5))
    d.add(Line(496, l1_y + 25, 490, l1_y + 25, strokeColor=C_GREEN, strokeWidth=1.5))
    d.add(Polygon([490, l1_y + 25, 494, l1_y + 27, 494, l1_y + 23], fillColor=C_GREEN, strokeColor=C_GREEN, strokeWidth=0))
    draw_numbered_badge(d, 496, (l3_y + l1_y)/2 + 25, 6, col=C_GREEN, r=6.5)
    d.add(String(490, (l3_y + l1_y)/2 + 35, "insights delivered", fontName="Helvetica-Bold", fontSize=6, textAnchor="end", fillColor=C_GREEN))

    return d


# ── DIAGRAM 2: 8-STAGE AGENTIC WORKFLOW & FEEDBACK (Figure 1 in Synopsis) ────
def make_synopsis_workflow_diagram():
    W, H = 504, 255
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=C_WHITE, strokeColor=C_GRAY_LITE, strokeWidth=1))

    r1 = [
        (1, "INPUT",      draw_chat_icon,    "Research objective",   "in plain English",        C_BLUE,   C_BLUE_LIGHT,   C_BLUE_BORDER),
        (2, "SEARCH",     draw_search_icon,  "DuckDuckGo Web +",     "News discovery",          C_BLUE,   C_BLUE_LIGHT,   C_BLUE_BORDER),
        (3, "SCRAPE",     draw_doc_icon,     "Trafilatura + BS4",    "clean page text",         C_TEAL,   C_TEAL_LIGHT,   C_TEAL_BORDER),
        (4, "SYNTHESIZE", draw_sparkle_icon, "Gemini 2.5 Flash",     "structured findings",     C_PURPLE, C_PURPLE_LIGHT, C_PURPLE_BORDER),
    ]

    r2 = [
        (5, "VALIDATE",   draw_check_icon,     "Pydantic v2 checks",  "evidence + sources",      C_PURPLE, C_PURPLE_LIGHT, C_PURPLE_BORDER),
        (6, "ANALYZE",    draw_barchart_icon,  "Compare companies,",  "spot strategic themes",   C_GREEN,  C_GREEN_LIGHT,  C_GREEN_BORDER),
        (7, "VISUALIZE",  draw_linechart_icon, "Pandas tables +",     "Plotly charts",           C_GREEN,  C_GREEN_LIGHT,  C_GREEN_BORDER),
        (8, "OUTPUT",     draw_download_icon,  "HTML / Markdown /",   "JSON reports",            C_GREEN,  C_GREEN_LIGHT,  C_GREEN_BORDER),
    ]

    card_w = 108
    card_h = 74
    gap_x = 18
    start_x = 10
    y_r1 = 150
    y_r2 = 42

    # Draw Row 1
    for i, (num, name, icon_fn, l1, l2, col, bg, border) in enumerate(r1):
        cx = start_x + i * (card_w + gap_x)
        d.add(Rect(cx, y_r1, card_w, card_h, rx=5, ry=5, fillColor=C_WHITE, strokeColor=col, strokeWidth=1.3))
        d.add(Rect(cx, y_r1 + card_h - 18, card_w, 18, rx=5, ry=5, fillColor=col, strokeColor=col, strokeWidth=0))
        d.add(Rect(cx, y_r1 + card_h - 18, card_w, 6, rx=0, ry=0, fillColor=col, strokeColor=col, strokeWidth=0))
        d.add(Circle(cx + 12, y_r1 + card_h - 9, 6.5, fillColor=C_WHITE, strokeColor=C_WHITE, strokeWidth=0))
        d.add(String(cx + 12, y_r1 + card_h - 12, str(num), fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=col))
        d.add(String(cx + 24, y_r1 + card_h - 12, name, fontName="Helvetica-Bold", fontSize=7.5, fillColor=C_WHITE))

        icon_fn(d, cx + card_w/2, y_r1 + card_h - 32, col)
        d.add(String(cx + card_w/2, y_r1 + 18, l1, fontName="Helvetica-Bold", fontSize=6.5, textAnchor="middle", fillColor=C_NAVY))
        d.add(String(cx + card_w/2, y_r1 + 8,  l2, fontName="Helvetica", fontSize=6, textAnchor="middle", fillColor=C_GRAY_MED))

        if i < 3:
            ax1 = cx + card_w + 1
            ax2 = ax1 + gap_x - 3
            ay = y_r1 + card_h/2
            d.add(Line(ax1, ay, ax2, ay, strokeColor=C_NAVY, strokeWidth=1.2))
            d.add(Polygon([ax2, ay, ax2 - 4, ay + 3, ax2 - 4, ay - 3], fillColor=C_NAVY, strokeColor=C_NAVY, strokeWidth=0))

    # Draw Row 2
    for i, (num, name, icon_fn, l1, l2, col, bg, border) in enumerate(r2):
        cx = start_x + i * (card_w + gap_x)
        d.add(Rect(cx, y_r2, card_w, card_h, rx=5, ry=5, fillColor=C_WHITE, strokeColor=col, strokeWidth=1.3))
        d.add(Rect(cx, y_r2 + card_h - 18, card_w, 18, rx=5, ry=5, fillColor=col, strokeColor=col, strokeWidth=0))
        d.add(Rect(cx, y_r2 + card_h - 18, card_w, 6, rx=0, ry=0, fillColor=col, strokeColor=col, strokeWidth=0))
        d.add(Circle(cx + 12, y_r2 + card_h - 9, 6.5, fillColor=C_WHITE, strokeColor=C_WHITE, strokeWidth=0))
        d.add(String(cx + 12, y_r2 + card_h - 12, str(num), fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=col))
        d.add(String(cx + 24, y_r2 + card_h - 12, name, fontName="Helvetica-Bold", fontSize=7.5, fillColor=C_WHITE))

        icon_fn(d, cx + card_w/2, y_r2 + card_h - 32, col)
        d.add(String(cx + card_w/2, y_r2 + 18, l1, fontName="Helvetica-Bold", fontSize=6.5, textAnchor="middle", fillColor=C_NAVY))
        d.add(String(cx + card_w/2, y_r2 + 8,  l2, fontName="Helvetica", fontSize=6, textAnchor="middle", fillColor=C_GRAY_MED))

        if i < 3:
            ax1 = cx + card_w + 1
            ax2 = ax1 + gap_x - 3
            ay = y_r2 + card_h/2
            d.add(Line(ax1, ay, ax2, ay, strokeColor=C_NAVY, strokeWidth=1.2))
            d.add(Polygon([ax2, ay, ax2 - 4, ay + 3, ax2 - 4, ay - 3], fillColor=C_NAVY, strokeColor=C_NAVY, strokeWidth=0))

    # Flow from Row 1 Stage 4 to Row 2 Stage 5
    d.add(Line(442, y_r1, 442, 134, strokeColor=C_PURPLE, strokeWidth=1.3))
    d.add(Line(442, 134, 64, 134, strokeColor=C_PURPLE, strokeWidth=1.3))
    d.add(Line(64, 134, 64, y_r2 + card_h, strokeColor=C_PURPLE, strokeWidth=1.3))
    d.add(Polygon([64, y_r2 + card_h, 61, y_r2 + card_h + 4, 67, y_r2 + card_h + 4],
                  fillColor=C_PURPLE, strokeColor=C_PURPLE, strokeWidth=0))
    d.add(String(253, 137, "findings move on to checking",
                 fontName="Helvetica-Oblique", fontSize=6.5, textAnchor="middle", fillColor=C_PURPLE))

    # Feedback Loop
    fb_x1 = start_x + card_w/2 + 20
    fb_x2 = start_x + (card_w + gap_x) + card_w/2
    d.add(Line(fb_x1, y_r2 + card_h, fb_x1, 126, strokeColor=C_AMBER, strokeWidth=1.4, strokeDashArray=[4, 2]))
    d.add(Line(fb_x1, 126, fb_x2, 126, strokeColor=C_AMBER, strokeWidth=1.4, strokeDashArray=[4, 2]))
    d.add(Line(fb_x2, 126, fb_x2, y_r1, strokeColor=C_AMBER, strokeWidth=1.4, strokeDashArray=[4, 2]))
    d.add(Polygon([fb_x2, y_r1, fb_x2 - 3, y_r1 - 5, fb_x2 + 3, y_r1 - 5],
                  fillColor=C_AMBER, strokeColor=C_AMBER, strokeWidth=0))

    d.add(Rect(118, 121, 110, 11, rx=3, ry=3, fillColor=C_AMBER, strokeColor=C_AMBER, strokeWidth=0))
    d.add(String(173, 124, "Weak evidence? Search again",
                 fontName="Helvetica-Bold", fontSize=6, textAnchor="middle", fillColor=C_WHITE))

    # Bottom Legend bar
    legend_bar = [
        (C_BLUE,   "Discover"),
        (C_TEAL,   "Extract"),
        (C_PURPLE, "Reason & verify"),
        (C_GREEN,  "Insight & output"),
        (C_AMBER,  "Feedback loop", True),
    ]
    lx = 30
    ly = 14
    for item in legend_bar:
        col = item[0]
        text = item[1]
        is_dashed = len(item) > 2 and item[2]
        if is_dashed:
            d.add(Line(lx, ly + 3, lx + 14, ly + 3, strokeColor=col, strokeWidth=1.5, strokeDashArray=[3, 1]))
            d.add(String(lx + 20, ly, text, fontName="Helvetica", fontSize=6.5, fillColor=C_GRAY_HVY))
            lx += 85
        else:
            d.add(Circle(lx + 4, ly + 3, 4, fillColor=col, strokeColor=col, strokeWidth=0))
            d.add(String(lx + 12, ly, text, fontName="Helvetica", fontSize=6.5, fillColor=C_GRAY_HVY))
            lx += 95

    return d


# ── DIAGRAM 3: USE CASE DIAGRAM (Figure 3) ───────────────────────────────────
def make_usecase_diagram():
    W, H = 504, 240
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=C_WHITE, strokeColor=C_GRAY_LITE, strokeWidth=1))

    # Boundary Box
    sb_x, sb_y, sb_w, sb_h = 120, 12, 372, 216
    d.add(Rect(sb_x, sb_y, sb_w, sb_h, rx=5, ry=5, fillColor=C_GRAY_PALE, strokeColor=C_BLUE_BORDER, strokeWidth=1.2))
    d.add(Rect(sb_x, sb_y + sb_h - 22, sb_w, 22, rx=5, ry=5, fillColor=C_BLUE, strokeColor=C_BLUE, strokeWidth=0))
    d.add(Rect(sb_x, sb_y + sb_h - 22, sb_w, 6, rx=0, ry=0, fillColor=C_BLUE, strokeColor=C_BLUE, strokeWidth=0))
    d.add(String(sb_x + sb_w/2, sb_y + sb_h - 15, "AUTONOMOUS MARKET INTELLIGENCE SYSTEM (SYSTEM BOUNDARY)",
                 fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=C_WHITE))

    # Actor
    ax, ay = 60, 100
    draw_user_icon(d, ax, ay + 20, C_BLUE)
    d.add(Line(ax, ay + 15, ax, ay - 10, strokeColor=C_NAVY, strokeWidth=1.3))
    d.add(Line(ax - 14, ay + 5, ax + 14, ay + 5, strokeColor=C_NAVY, strokeWidth=1.3))
    d.add(Line(ax, ay - 10, ax - 10, ay - 30, strokeColor=C_NAVY, strokeWidth=1.3))
    d.add(Line(ax, ay - 10, ax + 10, ay - 30, strokeColor=C_NAVY, strokeWidth=1.3))
    d.add(String(ax, ay - 42, "Analyst /", fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=C_NAVY))
    d.add(String(ax, ay - 52, "Researcher", fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=C_NAVY))

    # 6 Use Cases
    uc_items = [
        (146, 150, 155, 30, "UC1: Enter Research Objective",  C_BLUE,   C_BLUE_LIGHT),
        (320, 150, 155, 30, "UC2: Select Company Preset",     C_NAVY,   C_GRAY_LITE),
        (146, 92,  155, 30, "UC3: Run Discovery & Scraping",  C_PURPLE, C_PURPLE_LIGHT),
        (320, 92,  155, 30, "UC4: View Synthesized Report",   C_TEAL,   C_TEAL_LIGHT),
        (146, 34,  155, 30, "UC5: Explore Radar & SWOT",      C_GREEN,  C_GREEN_LIGHT),
        (320, 34,  155, 30, "UC6: Export HTML / MD / JSON",   C_AMBER,  C_AMBER_LIGHT),
    ]

    uc_connectors = []
    for ecx, ecy, ew, eh, lbl, col, fill in uc_items:
        d.add(Ellipse(ecx + ew/2, ecy + eh/2, ew/2, eh/2, fillColor=fill, strokeColor=col, strokeWidth=1.2))
        d.add(String(ecx + ew/2, ecy + eh/2 - 3, lbl, fontName="Helvetica-Bold", fontSize=6.5, textAnchor="middle", fillColor=col))
        uc_connectors.append((ecx, ecy + eh/2))

    for lx, ly in uc_connectors:
        d.add(Line(ax + 14, ay + 5, lx, ly, strokeColor=C_GRAY_MED, strokeWidth=0.8))

    # <<include>> & <<extend>> relationships
    d.add(Line(146 + 77, 150, 146 + 77, 122, strokeColor=C_GRAY_MED, strokeWidth=0.8, strokeDashArray=[3, 2]))
    d.add(String(146 + 82, 134, "<<include>>", fontName="Helvetica-Oblique", fontSize=5.5, fillColor=C_GRAY_HVY))

    d.add(Line(301, 107, 320, 107, strokeColor=C_GRAY_MED, strokeWidth=0.8, strokeDashArray=[3, 2]))
    d.add(String(310, 111, "<<extend>>", fontName="Helvetica-Oblique", fontSize=5.5, textAnchor="middle", fillColor=C_GRAY_HVY))

    return d


# ── DIAGRAM 4: ReAct EXECUTION LOOP (Figure 4) ───────────────────────────────
def make_react_diagram():
    W, H = 504, 230
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=C_WHITE, strokeColor=C_GRAY_LITE, strokeWidth=1))

    # Title strip
    d.add(Rect(0, H - 22, W, 22, rx=6, ry=6, fillColor=C_NAVY, strokeColor=C_NAVY, strokeWidth=0))
    d.add(Rect(0, H - 22, W, 8, rx=0, ry=0, fillColor=C_NAVY, strokeColor=C_NAVY, strokeWidth=0))
    d.add(String(W/2, H - 14, "LANGGRAPH ReAct AGENT EXECUTION LOOP",
                 fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=C_WHITE))

    # Start Node
    d.add(Ellipse(50, 172, 28, 12, fillColor=C_BLUE, strokeColor=C_BLUE, strokeWidth=0))
    d.add(String(50, 169, "START", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=C_WHITE))

    # Box: Query Formulate
    d.add(Rect(18, 120, 64, 28, rx=4, ry=4, fillColor=C_BLUE_LIGHT, strokeColor=C_BLUE, strokeWidth=1.2))
    d.add(String(50, 136, "Formulate", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=C_BLUE))
    d.add(String(50, 126, "Query Plan", fontName="Helvetica", fontSize=6, textAnchor="middle", fillColor=C_NAVY))
    d.add(Line(50, 160, 50, 148, strokeColor=C_BLUE, strokeWidth=1.2))
    d.add(Polygon([50, 148, 48, 153, 52, 153], fillColor=C_BLUE, strokeColor=C_BLUE, strokeWidth=0))

    # Gemini REASON Box
    d.add(Rect(140, 116, 155, 36, rx=4, ry=4, fillColor=C_PURPLE_LIGHT, strokeColor=C_PURPLE, strokeWidth=1.4))
    draw_sparkle_icon(d, 152, 134, C_PURPLE)
    d.add(String(162, 136, "Gemini 2.5 Flash - REASON", fontName="Helvetica-Bold", fontSize=7.5, fillColor=C_PURPLE))
    d.add(String(162, 124, "Analyse context & plan next action", fontName="Helvetica", fontSize=6, fillColor=C_GRAY_HVY))
    d.add(Line(82, 134, 140, 134, strokeColor=C_PURPLE, strokeWidth=1.2))
    d.add(Polygon([140, 134, 135, 137, 135, 131], fillColor=C_PURPLE, strokeColor=C_PURPLE, strokeWidth=0))

    # Decision Diamond
    cx, cy, hw, hh = 217, 65, 48, 22
    pts = [cx, cy + hh, cx + hw, cy, cx, cy - hh, cx - hw, cy]
    d.add(Polygon(pts, fillColor=C_AMBER_LIGHT, strokeColor=C_AMBER, strokeWidth=1.4))
    d.add(String(cx, cy + 3, "Sufficient", fontName="Helvetica-Bold", fontSize=6.5, textAnchor="middle", fillColor=C_AMBER))
    d.add(String(cx, cy - 6, "evidence?", fontName="Helvetica-Bold", fontSize=6.5, textAnchor="middle", fillColor=C_AMBER))
    d.add(Line(217, 116, 217, 87, strokeColor=C_PURPLE, strokeWidth=1.2))
    d.add(Polygon([217, 87, 214, 92, 220, 92], fillColor=C_PURPLE, strokeColor=C_PURPLE, strokeWidth=0))

    # Branch: NO -> Tool Execution & Observation Loop
    d.add(Line(cx - hw, cy, 95, cy, strokeColor=C_RED, strokeWidth=1.2))
    d.add(Polygon([95, cy, 100, cy + 3, 100, cy - 3], fillColor=C_RED, strokeColor=C_RED, strokeWidth=0))
    d.add(String((cx - hw + 95)/2, cy + 4, "NO", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=C_RED))

    # Tool Belt Frame
    d.add(Rect(8, 14, 88, 80, rx=4, ry=4, fillColor=C_GRAY_PALE, strokeColor=C_TEAL, strokeWidth=1.2))
    d.add(String(52, 82, "TOOL BELT", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=C_TEAL))
    tools_mini = [
        (62, "web_search()", C_BLUE),
        (44, "scrape_webpage()", C_TEAL),
        (26, "gather_competitors()", C_GREEN)
    ]
    for ty, tname, col in tools_mini:
        d.add(Rect(14, ty - 2, 76, 14, rx=2, ry=2, fillColor=C_WHITE, strokeColor=col, strokeWidth=0.8))
        d.add(String(52, ty + 1, tname, fontName="Helvetica-Bold", fontSize=5.5, textAnchor="middle", fillColor=col))

    # Observation Feedback Arrow back to Gemini
    d.add(Line(96, 54, 118, 54, strokeColor=C_TEAL, strokeWidth=1.2))
    d.add(Line(118, 54, 118, 134, strokeColor=C_TEAL, strokeWidth=1.2, strokeDashArray=[3, 1.5]))
    d.add(Line(118, 134, 138, 134, strokeColor=C_TEAL, strokeWidth=1.2))
    d.add(Polygon([138, 134, 133, 137, 133, 131], fillColor=C_TEAL, strokeColor=C_TEAL, strokeWidth=0))
    d.add(String(118, 92, "observation", fontName="Helvetica-Oblique", fontSize=5.5, textAnchor="middle", fillColor=C_TEAL))

    # Branch: YES -> Synthesis & Validation
    d.add(Line(cx + hw, cy, 335, cy, strokeColor=C_GREEN, strokeWidth=1.2))
    d.add(Polygon([335, cy, 330, cy + 3, 330, cy - 3], fillColor=C_GREEN, strokeColor=C_GREEN, strokeWidth=0))
    d.add(String((cx + hw + 335)/2, cy + 4, "YES", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=C_GREEN))

    # Synthesis Box
    d.add(Rect(335, 45, 155, 40, rx=4, ry=4, fillColor=C_GREEN_LIGHT, strokeColor=C_GREEN, strokeWidth=1.4))
    draw_check_icon(d, 348, 65, C_GREEN)
    d.add(String(360, 68, "SYNTHESIS & VALIDATION", fontName="Helvetica-Bold", fontSize=7, fillColor=C_GREEN))
    d.add(String(360, 58, "Pydantic v2 Schema Verification", fontName="Helvetica-Bold", fontSize=6, fillColor=C_NAVY))
    d.add(String(360, 49, "Structured MarketIntelligenceReport", fontName="Helvetica", fontSize=5.5, fillColor=C_GRAY_MED))

    # Export Pipeline Box
    d.add(Rect(335, 114, 155, 38, rx=4, ry=4, fillColor=C_BLUE_LIGHT, strokeColor=C_NAVY, strokeWidth=1.3))
    draw_download_icon(d, 348, 133, C_NAVY)
    d.add(String(360, 136, "MULTI-FORMAT EXPORT", fontName="Helvetica-Bold", fontSize=7, fillColor=C_NAVY))
    d.add(String(360, 126, "Plotly Radar / SWOT / Comparison", fontName="Helvetica", fontSize=5.5, fillColor=C_GRAY_HVY))
    d.add(String(360, 117, "HTML + Markdown + JSON Artifacts", fontName="Helvetica-Bold", fontSize=5.5, fillColor=C_BLUE))

    d.add(Line(412, 85, 412, 114, strokeColor=C_GREEN, strokeWidth=1.2))
    d.add(Polygon([412, 114, 409, 109, 415, 109], fillColor=C_GREEN, strokeColor=C_GREEN, strokeWidth=0))

    return d


# ── DIAGRAM 5: UML CLASS & SCHEMA DIAGRAM (Figure 5) ─────────────────────────
def make_class_diagram():
    W, H = 504, 225
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=C_WHITE, strokeColor=C_GRAY_LITE, strokeWidth=1))

    d.add(Rect(0, H - 22, W, 22, rx=6, ry=6, fillColor=C_NAVY, strokeColor=C_NAVY, strokeWidth=0))
    d.add(Rect(0, H - 22, W, 8, rx=0, ry=0, fillColor=C_NAVY, strokeColor=C_NAVY, strokeWidth=0))
    d.add(String(W/2, H - 14, "UML CLASS & PYDANTIC SCHEMA RELATIONSHIP DIAGRAM",
                 fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=C_WHITE))

    def class_card(x, y, w, title, attrs, methods, col, bg):
        h_hdr = 18
        h_attrs = len(attrs) * 9 + 4
        h_meth = len(methods) * 9 + 4 if methods else 0
        total_h = h_hdr + h_attrs + h_meth
        # Header
        d.add(Rect(x, y + h_attrs + h_meth, w, h_hdr, rx=4, ry=4, fillColor=col, strokeColor=col, strokeWidth=0))
        d.add(Rect(x, y + h_attrs + h_meth, w, 4, rx=0, ry=0, fillColor=col, strokeColor=col, strokeWidth=0))
        d.add(String(x + w/2, y + h_attrs + h_meth + 5, title, fontName="Helvetica-Bold", fontSize=6.5, textAnchor="middle", fillColor=C_WHITE))
        # Attributes
        d.add(Rect(x, y + h_meth, w, h_attrs, rx=0, ry=0, fillColor=bg, strokeColor=col, strokeWidth=0.8))
        for i, a in enumerate(attrs):
            d.add(String(x + 5, y + h_meth + h_attrs - 8 - i * 9, a, fontName="Helvetica", fontSize=5.5, fillColor=C_GRAY_HVY))
        # Methods
        if methods:
            d.add(Line(x, y + h_meth, x + w, y + h_meth, strokeColor=col, strokeWidth=0.6))
            d.add(Rect(x, y, w, h_meth, rx=4, ry=4, fillColor=C_WHITE, strokeColor=col, strokeWidth=0.8))
            d.add(Rect(x, y + h_meth - 4, w, 4, rx=0, ry=0, fillColor=C_WHITE, strokeColor=col, strokeWidth=0))
            for i, m in enumerate(methods):
                d.add(String(x + 5, y + h_meth - 8 - i * 9, m, fontName="Helvetica-Bold", fontSize=5.5, fillColor=col))
        else:
            d.add(Rect(x, y, w, total_h, rx=4, ry=4, fillColor=colors.transparent, strokeColor=col, strokeWidth=1))

    # Class 1: Agent
    class_card(10, 115, 140, "MarketIntelligenceAgent",
               ["+ model_name: str", "+ max_iterations: int", "+ tools: List[Tool]"],
               ["+ run_research(): Report", "+ _dispatch_tool(): str"],
               C_BLUE, C_BLUE_LIGHT)

    # Class 2: Main Report Model
    class_card(180, 115, 155, "MarketIntelligenceReport (Pydantic)",
               ["+ target_entity: str", "+ executive_summary: str", "+ strategic_themes: List[str]",
                "+ swot: SWOTAnalysis", "+ competitors: List[CompetitorInfo]"],
               ["+ model_dump_json(): str", "+ export_markdown(): str"],
               C_TEAL, C_TEAL_LIGHT)

    # Class 3: Streamlit UI
    class_card(360, 115, 134, "StreamlitDashboard",
               ["+ current_company: str", "+ execution_trace: list"],
               ["+ render_radar_chart()", "+ download_bundle()"],
               C_NAVY, C_GRAY_PALE)

    # Sub-models Row
    class_card(10, 20, 140, "SWOTAnalysis (BaseModel)",
               ["+ strengths: List[str]", "+ weaknesses: List[str]", "+ opportunities: List[str]", "+ threats: List[str]"],
               [], C_PURPLE, C_PURPLE_LIGHT)

    class_card(180, 20, 155, "CompetitorInfo (BaseModel)",
               ["+ name: str", "+ ai_readiness: float", "+ cloud_momentum: float", "+ market_position: str"],
               [], C_GREEN, C_GREEN_LIGHT)

    class_card(360, 20, 134, "SourceCitation (BaseModel)",
               ["+ url: str", "+ title: str", "+ publisher: str", "+ relevance_score: float"],
               [], C_AMBER, C_AMBER_LIGHT)

    # Association lines
    d.add(Line(150, 155, 180, 155, strokeColor=C_BLUE, strokeWidth=1.2, strokeDashArray=[3, 1.5]))
    d.add(String(165, 160, "uses", fontName="Helvetica", fontSize=5.5, textAnchor="middle", fillColor=C_BLUE))

    d.add(Line(335, 155, 360, 155, strokeColor=C_NAVY, strokeWidth=1.2, strokeDashArray=[3, 1.5]))
    d.add(String(347, 160, "displays", fontName="Helvetica", fontSize=5.5, textAnchor="middle", fillColor=C_NAVY))

    # Composition lines downwards
    for lx in (80, 255, 427):
        d.add(Line(255, 115, lx, 75, strokeColor=C_TEAL, strokeWidth=1))
        d.add(Polygon([lx, 75, lx - 2.5, 78, lx, 81, lx + 2.5, 78], fillColor=C_TEAL, strokeColor=C_TEAL, strokeWidth=0))

    return d


# ── Styles & Formatting ──────────────────────────────────────────────────────
def make_styles():
    st = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=st["Normal"],
                          fontName="Helvetica-Bold", fontSize=12.5, leading=16,
                          textColor=C_NAVY, spaceBefore=8, spaceAfter=3,
                          keepWithNext=True)
    h2 = ParagraphStyle("H2", parent=st["Normal"],
                          fontName="Helvetica-Bold", fontSize=10, leading=13,
                          textColor=C_BLUE, spaceBefore=6, spaceAfter=2,
                          keepWithNext=True)
    body = ParagraphStyle("Body", parent=st["Normal"],
                            fontName="Helvetica", fontSize=9, leading=12.5,
                            textColor=C_GRAY_HVY, spaceAfter=4, alignment=TA_JUSTIFY)
    bullet = ParagraphStyle("Bullet", parent=body,
                              leftIndent=14, firstLineIndent=-10, spaceAfter=2, alignment=TA_LEFT)
    tc = ParagraphStyle("TC", parent=st["Normal"],
                          fontName="Helvetica", fontSize=8, leading=11,
                          textColor=C_GRAY_HVY)
    tc_bold = ParagraphStyle("TCB", parent=tc,
                               fontName="Helvetica-Bold", textColor=C_NAVY)
    th = ParagraphStyle("TH", parent=st["Normal"],
                          fontName="Helvetica-Bold", fontSize=8, leading=11,
                          textColor=C_NAVY)
    caption = ParagraphStyle("Caption", parent=body,
                               fontSize=7.5, leading=10, textColor=C_GRAY_MED,
                               alignment=TA_CENTER, spaceAfter=4)
    return h1, h2, body, bullet, tc, tc_bold, th, caption


TBL = TableStyle([
    ("BOX",           (0, 0), (-1, -1), 1,   C_BORDER_GRAY := colors.HexColor("#CBD5E1")),
    ("INNERGRID",     (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
    ("BACKGROUND",    (0, 0), (-1,  0), C_BLUE_LIGHT),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
])

def alt_rows(rows):
    return TableStyle([
        ("BACKGROUND", (0, r), (-1, r), colors.HexColor("#F8FAFC"))
        for r in range(1, rows, 2)
    ])

def hr(col=None, lw=0.8):
    return HRFlowable(width="100%", thickness=lw,
                      color=col or C_RULE, spaceAfter=4, spaceBefore=2)


# ── PDF BUILDER ──────────────────────────────────────────────────────────────
def build_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=46, bottomMargin=52
    )

    h1, h2, body, bullet, tc, tc_bold, th, caption = make_styles()
    story = []

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 1: OFFICIAL COVER & SPECIFICATION OVERVIEW
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>ABES ENGINEERING COLLEGE, GHAZIABAD</b>", ParagraphStyle(
        "ColHdr", fontName="Helvetica-Bold", fontSize=11, leading=14,
        textColor=C_NAVY, alignment=TA_CENTER)))
    story.append(Paragraph("Department of Computer Science & Engineering | Academic Year 2026-27", ParagraphStyle(
        "SubHdr", fontName="Helvetica", fontSize=8.5, leading=12,
        textColor=C_GRAY_MED, alignment=TA_CENTER)))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>SOFTWARE REQUIREMENTS SPECIFICATION</b>", ParagraphStyle(
        "SRS_Title", fontName="Helvetica-Bold", fontSize=16, leading=20,
        textColor=C_BLUE, alignment=TA_CENTER)))
    story.append(Paragraph("<b>Autonomous Agentic Web Scraper & Strategic Market Intelligence Analyzer</b>", ParagraphStyle(
        "SRS_Name", fontName="Helvetica-Bold", fontSize=12, leading=16,
        textColor=C_NAVY, alignment=TA_CENTER)))
    story.append(Paragraph("A Multi-Stage ReAct Intelligence Agent for Autonomous Web Research, Competitive Benchmarking, and Structured Synthesis", ParagraphStyle(
        "SRS_Sub", fontName="Helvetica-Oblique", fontSize=8.5, leading=12,
        textColor=C_GRAY_MED, alignment=TA_CENTER)))
    story.append(Spacer(1, 14))

    # Academic Metadata Table
    cov_data = [
        [Paragraph("Project Title", tc_bold), Paragraph("Autonomous Agentic Web Scraper & Strategic Market Intelligence Analyzer", tc)],
        [Paragraph("Project Type / Domain", tc_bold), Paragraph("Agentic AI, Autonomous Agents, NLP, Web Scraping, Strategic Market Intelligence", tc)],
        [Paragraph("Student Name", tc_bold), Paragraph("<b>Adarsh Dubey</b>", tc)],
        [Paragraph("University Roll No.", tc_bold), Paragraph("<b>2400320100061</b>", tc)],
        [Paragraph("Department / College", tc_bold), Paragraph("Computer Science & Engineering, ABES Engineering College, Ghaziabad", tc)],
        [Paragraph("Project Guide", tc_bold), Paragraph("<b>Radhika Singhal</b>", tc)],
        [Paragraph("Target Case-Study Entities", tc_bold), Paragraph("HCL Technologies, TCS, Infosys, Wipro, Accenture", tc)],
        [Paragraph("Specification Standard", tc_bold), Paragraph("IEEE Std 830-1998 (Recommended Practice for SRS)", tc)],
        [Paragraph("Document Status & Version", tc_bold), Paragraph("Approved Production Baseline | Version 1.0.0", tc)],
    ]
    cov_table = Table(cov_data, colWidths=[130, 374])
    cov_table.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 1.2, C_NAVY),
        ("INNERGRID",     (0, 0), (-1, -1), 0.5, C_GRAY_LITE),
        ("BACKGROUND",    (0, 0), (0, -1),  C_GRAY_PALE),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story.append(cov_table)
    story.append(Spacer(1, 14))

    # Executive Overview Callout Box
    story.append(Paragraph("<b>Document Executive Summary & IEEE Compliance Statement</b>", h2))
    story.append(Paragraph(
        "This Software Requirements Specification (SRS) establishes the formal baseline for the <b>Autonomous Agentic Web Scraper "
        "& Strategic Market Intelligence Analyzer</b> in conformance with IEEE Std 830-1998. The system converts high-level "
        "natural-language research inquiries into autonomous web discovery, automated extraction, schema validation, "
        "and structured strategic synthesis using a LangGraph ReAct orchestration model and Google Gemini 2.5 Flash. "
        "This specification details functional, non-functional, dynamic workflow, and structural requirements for full academic and industry reproduction.", body))
    story.append(Spacer(1, 10))

    # Document Structure Table
    toc_data = [
        [Paragraph("<b>Section</b>", th), Paragraph("<b>Specification Content & Deliverables</b>", th), Paragraph("<b>Page</b>", th)],
        [Paragraph("Sections 1 - 4", tc_bold), Paragraph("Introduction, Abstract, Problem Statement, Objectives", tc), Paragraph("Page 2", tc)],
        [Paragraph("Sections 5 - 7", tc_bold), Paragraph("Proposed Solution, Project Scope, Functional Requirements (FR-1 to FR-8)", tc), Paragraph("Page 3", tc)],
        [Paragraph("Sections 8 - 9", tc_bold), Paragraph("Non-Functional Requirements (NFR-1 to NFR-6), Technology Stack & Sources", tc), Paragraph("Page 4", tc)],
        [Paragraph("Section 10", tc_bold), Paragraph("System Architecture: <b>Figure 2 (Layered Architecture & Walkthrough)</b>", tc), Paragraph("Page 5", tc)],
        [Paragraph("Section 11 (Part 1)", tc_bold), Paragraph("Detailed Design: <b>Figure 1 (8-Stage Workflow) & Figure 3 (Use Cases)</b>", tc), Paragraph("Page 6", tc)],
        [Paragraph("Section 11 (Part 2)", tc_bold), Paragraph("Dynamic Execution: <b>Figure 4 (ReAct Loop) & Figure 5 (UML Class Diagram)</b>", tc), Paragraph("Page 7", tc)],
        [Paragraph("Section 12", tc_bold), Paragraph("Module Description: Comprehensive Breakdown of Modules 1 through 9", tc), Paragraph("Page 8", tc)],
        [Paragraph("Sections 13 - 14", tc_bold), Paragraph("Database Architecture, Testing Levels & Test Case Matrix (T1 to T8)", tc), Paragraph("Page 9", tc)],
        [Paragraph("Sections 15 - 19", tc_bold), Paragraph("Results Criteria, Limitations, Future Scope, References & Sign-off Block", tc), Paragraph("Page 10", tc)],
    ]
    toc_table = Table(toc_data, colWidths=[90, 360, 54])
    toc_table.setStyle(TBL)
    toc_table.setStyle(alt_rows(len(toc_data)))
    story.append(toc_table)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 2: INTRODUCTION, ABSTRACT, PROBLEM STATEMENT, OBJECTIVES
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("1. Introduction", h1))
    story.append(hr())
    story.append(Paragraph(
        "Modern enterprise market and competitor research is an inherently complex, multi-source endeavor. Information "
        "necessary to assess corporate trajectory is fragmented across corporate investor portals, financial press releases, "
        "regulatory repositories (e.g., SEC EDGAR, BSE/NSE), technology news sources, and cloud marketplace partner directories. "
        "Human market analysts spend up to 70% of their research bandwidth on low-level browsing, parsing unstructured HTML, "
        "removing advertising artifacts, and reconciling conflicting metrics across spreadsheets. Traditional fixed scrapers "
        "fail rapidly because hardcoded URLs and brittle XPath/CSS selectors break as corporate websites evolve. "
        "This project introduces an <b>Autonomous Agentic Web Scraper & Strategic Market Intelligence Analyzer</b> based on "
        "a state-driven ReAct (Reason + Act) loop that discovers public web sources dynamically, extracts clean text, "
        "validates facts via Pydantic schemas, and synthesizes structured competitive intelligence.", body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Abstract", h1))
    story.append(hr())
    story.append(Paragraph(
        "The proposed system establishes an autonomous pipeline combining LangGraph/LangChain agentic orchestration, "
        "DuckDuckGo Web and News discovery, Trafilatura content extraction, Google Gemini 2.5 Flash reasoning, and Pydantic v2 "
        "strict data validation. Given a target entity (e.g., HCL Technologies) or research query, the agent autonomously generates "
        "search queries, fetches relevant articles, strips web clutter, evaluates evidence sufficiency, and recursively triggers secondary "
        "queries if data is inadequate. It delivers an end-to-end intelligence briefing featuring executive summaries, strategic themes, "
        "SWOT analyses, normalized competitor benchmarks across 5 technology peers (HCLTech, TCS, Infosys, Wipro, Accenture), "
        "traceable source citations, and multi-format exports (Plotly radar charts, HTML, Markdown, and JSON).", body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. Problem Statement", h1))
    story.append(hr())
    story.append(Paragraph(
        "Manual corporate research and conventional web scraping exhibit significant systemic limitations:", body))
    story.append(Paragraph("&bull; <b>Information Fragmentation:</b> Public market signals are distributed across corporate filings, investor briefings, and press reports.", bullet))
    story.append(Paragraph("&bull; <b>Labor-Intensive Acquisition:</b> Manual querying, page extraction, and source tracking require repetitive manual effort.", bullet))
    story.append(Paragraph("&bull; <b>Search Noise & Duplication:</b> Raw search engine results contain duplicate reports, irrelevant aggregator spam, and promotional material.", bullet))
    story.append(Paragraph("&bull; <b>DOM Selector Fragility:</b> Traditional web scrapers break when web layouts change; they lack autonomous content discovery.", bullet))
    story.append(Paragraph("&bull; <b>Unstructured Web Clutter:</b> Raw scraped content is contaminated with navigational links, cookie notices, and advertisements.", bullet))
    story.append(Paragraph("&bull; <b>Lack of Strict Validation:</b> Generative LLMs without strict schema enforcement produce hallucinated or malformed JSON responses.", bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4. Project Objectives", h1))
    story.append(hr())
    story.append(Paragraph(
        "The project addresses the stated problem through the following verified engineering objectives:", body))
    story.append(Paragraph("&bull; <b>O1. Autonomous Source Discovery:</b> Convert natural-language goals into targeted multi-perspective queries via DuckDuckGo Web & News.", bullet))
    story.append(Paragraph("&bull; <b>O2. Resilient Content Extraction:</b> Extract clean main-body article text while stripping ads and navigation via Trafilatura and BS4.", bullet))
    story.append(Paragraph("&bull; <b>O3. State-Driven Agentic Orchestration:</b> Coordinate research using LangGraph in a cyclic ReAct Think-Act-Observe paradigm.", bullet))
    story.append(Paragraph("&bull; <b>O4. Recursive Evidence Feedback:</b> Dynamically assess evidence sufficiency and trigger follow-up web searches when information is thin.", bullet))
    story.append(Paragraph("&bull; <b>O5. Strict Pydantic v2 Validation:</b> Guarantee schema conformity for all findings, ensuring zero malformed structures.", bullet))
    story.append(Paragraph("&bull; <b>O6. Multi-Peer Strategic Benchmarking:</b> Generate normalized competitor metrics across AI Readiness, Cloud Momentum, and Global Scale.", bullet))
    story.append(Paragraph("&bull; <b>O7. Interactive Visualization & Export:</b> Render Plotly polar radar charts and export HTML, Markdown, and machine-readable JSON.", bullet))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 3: PROPOSED SOLUTION, SCOPE, FUNCTIONAL REQUIREMENTS
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("5. Proposed Solution", h1))
    story.append(hr())
    story.append(Paragraph(
        "The proposed solution implements a stateful, autonomous research agent that replaces static scraping scripts with "
        "an intelligent, multi-stage reasoning and execution pipeline. Built with LangGraph and powered by Google Gemini 2.5 Flash, "
        "the agent systematically executes eight sequential stages: accepts plain-English input, plans discovery queries, retrieves live "
        "web/news articles, extracts clean text, synthesizes findings into structured JSON, verifies constraints against Pydantic models, "
        "computes competitor benchmarks, and generates interactive Plotly visualizations and exportable briefing dossiers.", body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("6. Scope of the Project", h1))
    story.append(hr())
    story.append(Paragraph(
        "<b>In-Scope Capabilities:</b> The project covers autonomous research over publicly accessible information for technology "
        "services companies. It supports natural-language queries, automated search formulation, HTML text extraction, LLM synthesis, "
        "comparative SWOT matrix generation, quantitative benchmarking across five target IT enterprises (HCL Technologies, TCS, "
        "Infosys, Wipro, Accenture), interactive Streamlit visualization, and export in HTML, Markdown, and JSON formats.", body))
    story.append(Paragraph(
        "<b>Current Limitations of Scope:</b> The system does not bypass user authentication, CAPTCHAs, paywalls, or bot mitigation "
        "systems (e.g., Cloudflare Turnstile). It does not guarantee live availability of third-party domains. All generated intelligence "
        "reflects public data and model synthesis and should be reviewed by an analyst prior to high-stakes capital allocation.", body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("7. Functional Requirements", h1))
    story.append(hr())
    fr_rows = [
        [Paragraph("<b>Req ID</b>", th), Paragraph("<b>Requirement Title</b>", th), Paragraph("<b>Detailed Functional Specification</b>", th)],
        [Paragraph("FR-1", tc_bold), Paragraph("Research Input & Presets", tc_bold),
         Paragraph("Accept custom natural-language objectives or preset targets (HCLTech, TCS, Infosys, Wipro, Accenture) via Streamlit UI.", tc)],
        [Paragraph("FR-2", tc_bold), Paragraph("Dynamic Query Planning", tc_bold),
         Paragraph("Agent automatically decomposes objectives into targeted search queries covering financials, AI, cloud, and partnerships.", tc)],
        [Paragraph("FR-3", tc_bold), Paragraph("Autonomous Web Discovery", tc_bold),
         Paragraph("Execute DuckDuckGo Web and News searches (DDGS API); deduplicate URLs and filter out low-relevance domains.", tc)],
        [Paragraph("FR-4", tc_bold), Paragraph("Clean Content Extraction", tc_bold),
         Paragraph("Fetch accessible web pages; use Trafilatura and BeautifulSoup4 to extract clean article text, discarding ads and headers.", tc)],
        [Paragraph("FR-5", tc_bold), Paragraph("ReAct Synthesis Engine", tc_bold),
         Paragraph("Gemini 2.5 Flash synthesizes raw text into structured JSON containing executive summary, strategic pillars, and SWOT items.", tc)],
        [Paragraph("FR-6", tc_bold), Paragraph("Pydantic Schema Validation", tc_bold),
         Paragraph("Validate LLM output against MarketIntelligenceReport schema; retry synthesis if schema fails or fields are missing.", tc)],
        [Paragraph("FR-7", tc_bold), Paragraph("Competitor Benchmarking", tc_bold),
         Paragraph("Compute normalized metrics (AI Readiness, Cloud Momentum, Global Scale) across peer enterprises using Pandas.", tc)],
        [Paragraph("FR-8", tc_bold), Paragraph("Multi-Format Export", tc_bold),
         Paragraph("Generate standalone HTML briefings, Markdown executive reports, raw JSON dumps, and Plotly polar radar charts.", tc)],
    ]
    fr_table = Table(fr_rows, colWidths=[52, 130, 322])
    fr_table.setStyle(TBL)
    fr_table.setStyle(alt_rows(len(fr_rows)))
    story.append(fr_table)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 4: NON-FUNCTIONAL REQUIREMENTS & TECHNOLOGIES USED
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("8. Non-Functional Requirements", h1))
    story.append(hr())
    nfr_rows = [
        [Paragraph("<b>Category</b>", th), Paragraph("<b>Specification & Measurable Metric</b>", th), Paragraph("<b>Implementation Mechanism</b>", th)],
        [Paragraph("NFR-1: Performance", tc_bold),
         Paragraph("Complete end-to-end research, extraction, synthesis, and export within 45 - 90 seconds for standard corporate queries.", tc),
         Paragraph("Gemini 2.5 Flash fast inference; concurrent HTTP page fetching via Trafilatura.", tc)],
        [Paragraph("NFR-2: Reliability", tc_bold),
         Paragraph("Zero application crash on blocked, slow, or 404/403 web pages; graceful fallback and logging for inaccessible links.", tc),
         Paragraph("Trafilatura try/except exception wrappers; safe empty response fallbacks.", tc)],
        [Paragraph("NFR-3: Data Accuracy", tc_bold),
         Paragraph("100% of reported strategic findings linked back to source URLs; 0% unvalidated or hallucinated schema structures.", tc),
         Paragraph("Pydantic v2 strict schema enforcement; SourceCitation sub-model traceability.", tc)],
        [Paragraph("NFR-4: Usability", tc_bold),
         Paragraph("Clean interactive dashboard requiring zero CLI configuration; real-time execution trace display for analyst transparency.", tc),
         Paragraph("Streamlit web interface with tabbed views, expandable traces, and one-click exports.", tc)],
        [Paragraph("NFR-5: Modularity", tc_bold),
         Paragraph("Pluggable architecture allowing new search tools, scrapers, or LLM providers without altering orchestrator core.", tc),
         Paragraph("LangGraph modular tool belt pattern; isolated tool schemas in schemas.py.", tc)],
        [Paragraph("NFR-6: Security", tc_bold),
         Paragraph("No hardcoded API credentials; strictly respects website robots.txt and disallows credential stuffing or payload execution.", tc),
         Paragraph("Environment-variable configuration via .env; safe HTTP headers and read-only scraping.", tc)],
    ]
    nfr_table = Table(nfr_rows, colWidths=[95, 225, 184])
    nfr_table.setStyle(TBL)
    nfr_table.setStyle(alt_rows(len(nfr_rows)))
    story.append(nfr_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("9. Technologies Used (Matching Synopsis Table 9)", h1))
    story.append(hr())
    tech_rows = [
        [Paragraph("<b>Category</b>", th), Paragraph("<b>Technology / Tool</b>", th), Paragraph("<b>Role in Architecture</b>", th)],
        [Paragraph("Programming", tc_bold), Paragraph("Python 3.10+", tc), Paragraph("Core implementation, tool orchestration, and data pipeline.", tc)],
        [Paragraph("Agentic AI", tc_bold), Paragraph("LangGraph / LangChain", tc), Paragraph("State-driven agent workflow and ReAct Think-Act-Observe loop.", tc)],
        [Paragraph("LLM Engine", tc_bold), Paragraph("Google Gemini 2.5 Flash", tc), Paragraph("Synthesis, reasoning, query planning, and structured JSON output.", tc)],
        [Paragraph("Search Discovery", tc_bold), Paragraph("DuckDuckGo / DDGS", tc), Paragraph("Live web and news discovery without paid API key quotas.", tc)],
        [Paragraph("Web Extraction", tc_bold), Paragraph("Trafilatura", tc), Paragraph("Main text body extraction, boilerplate and advertisement removal.", tc)],
        [Paragraph("HTML Parsing", tc_bold), Paragraph("BeautifulSoup4", tc), Paragraph("Targeted page parsing and fallback DOM text sanitization.", tc)],
        [Paragraph("Validation", tc_bold), Paragraph("Pydantic v2", tc), Paragraph("Strict data validation and schema-compliant JSON enforcement.", tc)],
        [Paragraph("Data Analytics", tc_bold), Paragraph("Pandas", tc), Paragraph("Tabular metric processing, score normalization, and comparison.", tc)],
        [Paragraph("Visualization", tc_bold), Paragraph("Plotly", tc), Paragraph("Interactive polar radar charts and horizontal competitor benchmarks.", tc)],
        [Paragraph("User Interface", tc_bold), Paragraph("Streamlit", tc), Paragraph("Interactive research dashboard with live execution traces.", tc)],
    ]
    tech_table = Table(tech_rows, colWidths=[90, 130, 284])
    tech_table.setStyle(TBL)
    tech_table.setStyle(alt_rows(len(tech_rows)))
    story.append(tech_table)
    story.append(Spacer(1, 4))

    # Primary Data-Source Categories Box (from Synopsis)
    story.append(Paragraph("<b>Primary Public Web Data-Source Categories:</b>", h2))
    story.append(Paragraph(
        "<b>1. Business News:</b> Reuters, Bloomberg, CNBC, TechCrunch, PR Newswire, Business Wire. &nbsp;|&nbsp; "
        "<b>2. Investor Portals:</b> HCLTech, TCS, Infosys, Wipro, Accenture IR repositories. &nbsp;|&nbsp; "
        "<b>3. Regulatory Filings:</b> SEC EDGAR, BSE/NSE Corporate Announcements, UK Companies House. &nbsp;|&nbsp; "
        "<b>4. Industry Benchmarks:</b> Gartner Magic Quadrants, IDC MarketScape, Everest PEAK Matrix. &nbsp;|&nbsp; "
        "<b>5. Cloud Ecosystems:</b> AWS Partner Network, Microsoft Azure Marketplace, Google Cloud Partner Directory.", body))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 5: SYSTEM ARCHITECTURE (FIGURE 2 & HOW TO READ THE DIAGRAM)
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("10. System Architecture", h1))
    story.append(hr())
    story.append(Paragraph(
        "The system architecture strictly separates the user interface, agent orchestration brain, external tool belt, "
        "public web sources, and output deliverables. This modular separation enables independent enhancement of individual "
        "layers (e.g., swapping search providers or updating LLM prompts) without breaking pipeline stability.", body))
    story.append(Spacer(1, 2))

    # FIGURE 2 ARCHITECTURE DIAGRAM
    story.append(make_synopsis_architecture_diagram())
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "<b>Figure 2. High-level system architecture (layered view: interface, agent brain, tool belt, public web, results)</b>", caption))
    story.append(Spacer(1, 4))

    # HOW TO READ THE DIAGRAM (EXACT FROM SYNOPSIS)
    story.append(Paragraph("<b>How to read the diagram:</b>", h2))
    read_steps = [
        [Paragraph("<b>(1)</b>", tc_bold), Paragraph("The user types a research objective (a company, competitor or market question) into the Streamlit dashboard.", tc)],
        [Paragraph("<b>(2)</b>", tc_bold), Paragraph("The Streamlit dashboard passes the objective to the LangGraph/LangChain agent orchestrator.", tc)],
        [Paragraph("<b>(3)</b>", tc_bold), Paragraph("The orchestrator and Gemini 2.5 Flash reason together in an iterative Think, Act, Observe loop.", tc)],
        [Paragraph("<b>(4)</b>", tc_bold), Paragraph("The orchestrator calls specialized tools from its belt: Search, Scrape, Validate, and Analyze.", tc)],
        [Paragraph("<b>(5)</b>", tc_bold), Paragraph("Search and Scrape reach out to public web sources and bring back clean page text without advertisements.", tc)],
        [Paragraph("<b>(6)</b>", tc_bold), Paragraph("Validated and analyzed findings become Plotly interactive charts and HTML / Markdown / JSON reports.", tc)],
        [Paragraph("<b>(7)</b>", tc_bold), Paragraph("Streamlit displays the deliverables in tabbed views and lets the user download complete report bundles.", tc)],
    ]
    read_table = Table(read_steps, colWidths=[24, 480])
    read_table.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 2),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 2),
    ]))
    story.append(read_table)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 6: DETAILED WORKFLOW & USE CASE DIAGRAMS (FIGURES 1 & 3)
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("11. Detailed System Design & Workflows", h1))
    story.append(hr())
    story.append(Paragraph("11.1 Agentic Workflow / Data Flow Diagram (DFD)", h2))
    story.append(Paragraph(
        "The workflow is organized as a state-driven agentic pipeline. A research objective initiates source discovery; "
        "extracted evidence is progressively transformed into structured information. The agent revisits discovery when evidence is insufficient.", body))
    story.append(Spacer(1, 2))

    # FIGURE 1 WORKFLOW DIAGRAM
    story.append(make_synopsis_workflow_diagram())
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "<b>Figure 1. Agentic workflow / flow chart of the proposed system (8 stages, colour-coded by phase, with a feedback loop)</b>", caption))
    story.append(Spacer(1, 6))

    story.append(Paragraph("11.2 Use Case Diagram", h2))
    story.append(Paragraph(
        "The Use Case model defines the functional boundary between the human Analyst/Researcher and the automated agent subsystem.", body))
    story.append(Spacer(1, 2))

    # FIGURE 3 USE CASE DIAGRAM
    story.append(make_usecase_diagram())
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "<b>Figure 3. Use case diagram illustrating core analyst interactions, preset workflows, and automated pipeline execution</b>", caption))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 7: ReAct LOOP & CLASS DIAGRAM (FIGURES 4 & 5)
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("11.3 LangGraph ReAct Agent Loop", h1))
    story.append(hr())
    story.append(Paragraph(
        "The execution engine coordinates reasoning and action through a state-machine loop. When Gemini determines evidence is incomplete, "
        "it dispatches tools (web_search, scrape_webpage) and feeds observations back into memory until sufficiency is achieved.", body))
    story.append(Spacer(1, 2))

    # FIGURE 4 ReAct LOOP
    story.append(make_react_diagram())
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "<b>Figure 4. LangGraph ReAct agent state-machine and feedback loop execution model with tool dispatch and Pydantic validation</b>", caption))
    story.append(Spacer(1, 6))

    story.append(Paragraph("11.4 Class & Pydantic Schema Architecture", h1))
    story.append(hr())
    story.append(Paragraph(
        "The object model couples the orchestration agent with strongly typed Pydantic v2 schemas to ensure end-to-end data integrity.", body))
    story.append(Spacer(1, 2))

    # FIGURE 5 CLASS DIAGRAM
    story.append(make_class_diagram())
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "<b>Figure 5. UML class and Pydantic v2 schema relationship diagram illustrating model composition and orchestration dependencies</b>", caption))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 8: MODULE DESCRIPTION (ALL 9 MODULES FROM SYNOPSIS)
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("12. Module Description (Matching Synopsis Section 10)", h1))
    story.append(hr())
    story.append(Paragraph(
        "The architecture is partitioned into nine discrete functional modules that isolate specific computational concerns:", body))

    modules = [
        ("Module 1: Research Input",
         "Accepts and structures the user's research objective. Supports arbitrary natural-language market queries as well as "
         "pre-configured presets for the five target technology peers (HCL Technologies, TCS, Infosys, Wipro, Accenture). "
         "Sanitizes query strings and passes parameters into the LangGraph state graph."),

        ("Module 2: Search / Discovery",
         "Generates targeted Web and News search queries using DuckDuckGo (DDGS API). Employs boolean modifiers and temporal filters "
         "to identify recent earnings calls, press releases, strategic announcements, and industry commentary without incurring API cost."),

        ("Module 3: Web Scraping",
         "Retrieves and extracts content from accessible public web pages. Utilizes Trafilatura for primary main-text extraction "
         "with automated stripping of headers, footers, navigation, cookie banners, and inline advertising. Uses BeautifulSoup4 as fallback."),

        ("Module 4: Evidence Processing",
         "Cleans, normalizes, and chunks extracted text. Deduplicates overlapping news reports, enforces character window limits "
         "to prevent LLM context-window saturation, and structures page metadata (URL, page title, publish date) for downstream auditing."),

        ("Module 5: Validation",
         "Performs automated checks on source relevance and evidence consistency. Checks that collected articles directly address "
         "the research query. If evidence is thin or irrelevant, signals the orchestrator to trigger secondary discovery queries."),

        ("Module 6: Agentic Synthesis",
         "Employs Google Gemini 2.5 Flash as the core LLM reasoning engine. Guided by a strict synthesis system prompt, converts "
         "unstructured evidence chunks into structured JSON conforming to the MarketIntelligenceReport Pydantic schema."),

        ("Module 7: Strategic Analysis",
         "Produces comparative market-intelligence observations, SWOT matrix categorization (Strengths, Weaknesses, Opportunities, "
         "Threats), strategic theme identification, and quantitative benchmark scoring across AI Readiness, Cloud Momentum, and Global Scale."),

        ("Module 8: Visualization",
         "Constructs interactive data representations using Plotly and Pandas. Renders multi-axis polar radar charts comparing the "
         "five technology companies, horizontal benchmark bar charts, and stylized summary scorecards inside the Streamlit dashboard."),

        ("Module 9: Reporting / Export",
         "Generates exportable research artifacts in three distinct formats: responsive HTML executive briefings with embedded CSS, "
         "GitHub-flavored Markdown dossiers with source hyperlinks, and machine-readable JSON dumps for downstream data pipelines."),
    ]

    mod_rows = [[Paragraph("<b>Module</b>", th), Paragraph("<b>Architectural Responsibility & Implementation Details</b>", th)]]
    for m_title, m_desc in modules:
        mod_rows.append([Paragraph(m_title, tc_bold), Paragraph(m_desc, tc)])

    mod_table = Table(mod_rows, colWidths=[130, 374])
    mod_table.setStyle(TBL)
    mod_table.setStyle(alt_rows(len(mod_rows)))
    story.append(mod_table)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 9: DATABASE DESIGN & TESTING (MATCHING SYNOPSIS SECTION 12)
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("13. Database & Data Storage Design", h1))
    story.append(hr())
    story.append(Paragraph(
        "The system operates on a stateless, memory-efficient real-time streaming model. Extracted web content and intermediate "
        "reasoning traces are maintained in-memory within the LangGraph StateGraph dictionary during execution. "
        "Completed intelligence reports are serialized to disk as structured JSON artifacts under the reports/ directory. "
        "This file-based caching model avoids unnecessary relational database overhead while ensuring report provenance and auditability.", body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("14. Testing & Verification (Matching Synopsis Section 12)", h1))
    story.append(hr())
    story.append(Paragraph(
        "Testing is structured across four rigorous levels to validate isolated components, inter-stage communication, end-to-end "
        "workflow execution, and resilience against hostile web environments:", body))

    test_levels = [
        [Paragraph("<b>Level</b>", th), Paragraph("<b>What is Tested</b>", th), Paragraph("<b>Method & Tooling</b>", th)],
        [Paragraph("Unit Testing", tc_bold),
         Paragraph("Query generation, text cleaning, Pydantic schemas, URL deduplication, export serializers.", tc),
         Paragraph("Automated pytest test suite with static mock inputs.", tc)],
        [Paragraph("Integration Testing", tc_bold),
         Paragraph("Hand-offs between pipeline stages: Search to Scrape, Scrape to Synthesis, Synthesis to Validation.", tc),
         Paragraph("Sequential execution of connected stages on fixed sample data.", tc)],
        [Paragraph("System Testing", tc_bold),
         Paragraph("Complete execution from research objective to HTML/MD/JSON output for the 5 target companies.", tc),
         Paragraph("End-to-end automated and manual runs via Streamlit UI.", tc)],
        [Paragraph("Robustness Testing", tc_bold),
         Paragraph("Paywalled, blocked, or slow pages, empty search results, irrelevant sources, malformed LLM outputs.", tc),
         Paragraph("Injected HTTP failure mocks and edge-case prompt scenarios.", tc)],
    ]
    tl_table = Table(test_levels, colWidths=[95, 235, 174])
    tl_table.setStyle(TBL)
    tl_table.setStyle(alt_rows(len(test_levels)))
    story.append(tl_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Sample Test Cases Matrix (Exact from Synopsis Table 12):</b>", h2))
    test_cases = [
        [Paragraph("<b>ID</b>", th), Paragraph("<b>Test Case Description</b>", th), Paragraph("<b>Expected Verified Result</b>", th)],
        [Paragraph("T1", tc_bold), Paragraph("Enter a valid company research objective.", tc), Paragraph("Relevant Web and News sources are discovered dynamically.", tc)],
        [Paragraph("T2", tc_bold), Paragraph("Scrape a normal news article.", tc), Paragraph("Main text is returned without navigation menus, cookie banners, or ads.", tc)],
        [Paragraph("T3", tc_bold), Paragraph("Scrape a paywalled or blocked web page.", tc), Paragraph("Page is skipped gracefully and logged; system does not hang or bypass controls.", tc)],
        [Paragraph("T4", tc_bold), Paragraph("Search returns duplicate or irrelevant links.", tc), Paragraph("Duplicates are removed and low-relevance domains are filtered out.", tc)],
        [Paragraph("T5", tc_bold), Paragraph("Evidence is too thin for a reliable answer.", tc), Paragraph("Agent returns to discovery stage and generates secondary searches.", tc)],
        [Paragraph("T6", tc_bold), Paragraph("LLM returns output that violates schema.", tc), Paragraph("Pydantic validation rejects response and triggers structured retry.", tc)],
        [Paragraph("T7", tc_bold), Paragraph("Compare all five target technology companies.", tc), Paragraph("Structured comparison table and Plotly radar charts are generated.", tc)],
        [Paragraph("T8", tc_bold), Paragraph("Export the final research briefing.", tc), Paragraph("Valid HTML, Markdown, and JSON files are produced and downloadable.", tc)],
    ]
    tc_table = Table(test_cases, colWidths=[28, 232, 244])
    tc_table.setStyle(TBL)
    tc_table.setStyle(alt_rows(len(test_cases)))
    story.append(tc_table)
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 10: RESULTS, LIMITATIONS, FUTURE SCOPE, REFERENCES & SIGN-OFF
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("15. Results & Evaluation Criteria (Matching Synopsis Table 13)", h1))
    story.append(hr())
    eval_rows = [
        [Paragraph("<b>Evaluation Criterion</b>", th), Paragraph("<b>Verification Method</b>", th), Paragraph("<b>Target Acceptance Standard</b>", th)],
        [Paragraph("Source Relevance", tc_bold), Paragraph("Reviewer evaluates discovered URLs against objective.", tc), Paragraph("Over 85% of discovered sources directly relevant to inquiry.", tc)],
        [Paragraph("Extraction Quality", tc_bold), Paragraph("Inspection of cleaned text samples for advertising clutter.", tc), Paragraph("Zero navigation text, ads, or cookie banners in extracted content.", tc)],
        [Paragraph("Schema Validity", tc_bold), Paragraph("Proportion of LLM outputs passing Pydantic validation.", tc), Paragraph("100% schema compliance; all schema violations caught and retried.", tc)],
        [Paragraph("Evidence Traceability", tc_bold), Paragraph("Audit of findings back to originating web source URL.", tc), Paragraph("100% of reported facts cite verified public source URLs.", tc)],
        [Paragraph("Time Saved", tc_bold), Paragraph("Agent run time vs. human analyst manual search time.", tc), Paragraph("Complete research report in < 90s (90%+ time reduction vs. manual).", tc)],
        [Paragraph("Output Completeness", tc_bold), Paragraph("Integrity of generated HTML, Markdown, and JSON files.", tc), Paragraph("All three file formats generated without corruption or data loss.", tc)],
    ]
    eval_table = Table(eval_rows, colWidths=[100, 220, 184])
    eval_table.setStyle(TBL)
    eval_table.setStyle(alt_rows(len(eval_rows)))
    story.append(eval_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("16. Limitations", h1))
    story.append(hr())
    story.append(Paragraph(
        "&bull; <b>Public Web Availability:</b> Output quality is contingent on content accessible to public search engines.<br/>"
        "&bull; <b>No Authentication Bypass:</b> The system strictly respects paywalls, CAPTCHAs, and corporate intranet firewalls.<br/>"
        "&bull; <b>Inference Latency:</b> Real-time multi-page scraping and LLM synthesis requires 45-90 seconds per run.<br/>"
        "&bull; <b>Human Verification Required:</b> High-stakes investment or strategic decisions should review underlying source URLs.", body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("17. Future Scope (Matching Synopsis Section 14)", h1))
    story.append(hr())
    story.append(Paragraph(
        "&bull; Introduce specialized sub-agents for financial statement analysis, patent auditing, and executive synthesis.<br/>"
        "&bull; Add persistent vector-based memory (ChromaDB / FAISS) for quarter-over-quarter trend analysis and historical tracking.<br/>"
        "&bull; Integrate direct regulatory API connectors for SEC EDGAR, BSE/NSE filings, and UK Companies House.<br/>"
        "&bull; Automate board-ready PowerPoint (PPTX) slide deck generation from synthesized research dossiers.<br/>"
        "&bull; Implement real-time market anomaly alerts and notifications for breaking competitive developments.", body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("18. References (Matching Synopsis Section 15)", h1))
    story.append(hr())
    story.append(Paragraph(
        "1. Yao, S. et al. (2022). <i>ReAct: Synergizing Reasoning and Acting in Language Models</i>. ICLR 2023 / arXiv:2210.03629.<br/>"
        "2. Barbaresi, A. (2021). <i>Trafilatura: A Web Scraping Library and Tool for Text Discovery and Extraction</i>. ACL.<br/>"
        "3. LangChain / LangGraph Official Documentation for Stateful Agentic Workflows (2024).<br/>"
        "4. Google Gemini 2.5 Flash Official Technical Documentation and Structured Outputs Guide (2024).<br/>"
        "5. Pydantic v2 Official Documentation for Robust Schema Validation and Settings Management.<br/>"
        "6. Streamlit & Plotly Official Documentation for Python Interactive Visualization and Dashboards.<br/>"
        "7. IEEE Std 830-1998: <i>IEEE Recommended Practice for Software Requirements Specifications</i>.", body))
    story.append(Spacer(1, 8))

    # Formal Approval / Sign-off Block
    sign_data = [
        [Paragraph("<b>Prepared By:</b>", th), Paragraph("<b>Reviewed & Approved By:</b>", th)],
        [Paragraph("<b>Adarsh Dubey</b><br/>Roll No: 2400320100061<br/>Department of Computer Science & Engineering<br/>ABES Engineering College, Ghaziabad", tc),
         Paragraph("<b>Radhika Singhal</b><br/>Project Guide<br/>Department of Computer Science & Engineering<br/>ABES Engineering College, Ghaziabad", tc)],
        [Paragraph("Signature: ___________________________<br/>Date: 30 September 2026", tc_bold),
         Paragraph("Signature: ___________________________<br/>Date: 30 September 2026", tc_bold)]
    ]
    sign_table = Table(sign_data, colWidths=[252, 252])
    sign_table.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 1.2, C_NAVY),
        ("INNERGRID",     (0, 0), (-1, -1), 0.5, C_GRAY_LITE),
        ("BACKGROUND",    (0, 0), (-1,  0), C_GRAY_PALE),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story.append(sign_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {PDF_FILENAME}")


if __name__ == "__main__":
    build_pdf()
