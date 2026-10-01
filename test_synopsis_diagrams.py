"""
Test script to verify exact synopsis diagrams rendering via ReportLab.
"""
from reportlab.graphics.shapes import (
    Drawing, Rect, String, Line, Group, Polygon, Circle, Ellipse
)
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter

# ── Color Palette matching Synopsis ──────────────────────────────────────────
C_BLUE         = colors.HexColor("#2563EB")
C_BLUE_LIGHT   = colors.HexColor("#EFF6FF")
C_BLUE_BORDER  = colors.HexColor("#BFDBFE")

C_TEAL         = colors.HexColor("#0D9488")
C_TEAL_LIGHT   = colors.HexColor("#F0FDFA")
C_TEAL_BORDER  = colors.HexColor("#99F6E4")

C_PURPLE       = colors.HexColor("#7C3AED")
C_PURPLE_LIGHT = colors.HexColor("#FAF5FF")
C_PURPLE_BORDER= colors.HexColor("#DDD6FE")

C_GREEN        = colors.HexColor("#16A34A")
C_GREEN_LIGHT  = colors.HexColor("#F0FDF4")
C_GREEN_BORDER = colors.HexColor("#BBF7D0")

C_AMBER        = colors.HexColor("#D97706")
C_AMBER_LIGHT  = colors.HexColor("#FFFBEB")
C_AMBER_BORDER = colors.HexColor("#FDE68A")

C_NAVY         = colors.HexColor("#1E293B")
C_GRAY_HVY     = colors.HexColor("#334155")
C_GRAY_MED     = colors.HexColor("#64748B")
C_GRAY_LITE    = colors.HexColor("#E2E8F0")
C_WHITE        = colors.white

# ── Vector Icon Helpers ──────────────────────────────────────────────────────
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

# ── 1. FIGURE 2: HIGH-LEVEL SYSTEM ARCHITECTURE (Exact Synopsis Reference) ───
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
        lx += 62
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
    d.add(Rect(32, l1_y + 6, 88, l1_h - 12, rx=4, ry=4, fillColor=C_WHITE, strokeColor=C_BLUE, strokeWidth=1.2))
    draw_user_icon(d, 50, l1_y + 32, C_BLUE)
    d.add(String(64, l1_y + 34, "USER", fontName="Helvetica-Bold", fontSize=8, fillColor=C_NAVY))
    d.add(String(64, l1_y + 24, "Analyst asks a", fontName="Helvetica", fontSize=6, fillColor=C_GRAY_MED))
    d.add(String(64, l1_y + 15, "research question", fontName="Helvetica", fontSize=6, fillColor=C_GRAY_MED))

    # Arrow User -> Streamlit (Badge 1)
    d.add(Line(120, l1_y + 32, 160, l1_y + 32, strokeColor=C_BLUE, strokeWidth=1.5))
    d.add(Polygon([160, l1_y + 32, 154, l1_y + 35, 154, l1_y + 29], fillColor=C_BLUE, strokeColor=C_BLUE, strokeWidth=0))
    draw_numbered_badge(d, 140, l1_y + 32, 1, col=C_BLUE, r=6.5)

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

    # Flow 2 (Streamlit -> Agent Orchestrator)
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


# ── 2. FIGURE 1: 8-STAGE AGENTIC WORKFLOW WITH FEEDBACK LOOP (Exact Synopsis) ──
def make_synopsis_workflow_diagram():
    W, H = 504, 255
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, rx=6, ry=6, fillColor=C_WHITE, strokeColor=C_GRAY_LITE, strokeWidth=1))

    # Stages data
    # Row 1:
    r1 = [
        (1, "INPUT",      draw_chat_icon,    "Research objective",   "in plain English",        C_BLUE,   C_BLUE_LIGHT,   C_BLUE_BORDER),
        (2, "SEARCH",     draw_search_icon,  "DuckDuckGo Web +",     "News discovery",          C_BLUE,   C_BLUE_LIGHT,   C_BLUE_BORDER),
        (3, "SCRAPE",     draw_doc_icon,     "Trafilatura + BS4",    "clean page text",         C_TEAL,   C_TEAL_LIGHT,   C_TEAL_BORDER),
        (4, "SYNTHESIZE", draw_sparkle_icon, "Gemini 2.5 Flash",     "structured findings",     C_PURPLE, C_PURPLE_LIGHT, C_PURPLE_BORDER),
    ]

    # Row 2:
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
        # Card outline
        d.add(Rect(cx, y_r1, card_w, card_h, rx=5, ry=5, fillColor=C_WHITE, strokeColor=col, strokeWidth=1.3))
        # Top header pill
        d.add(Rect(cx, y_r1 + card_h - 18, card_w, 18, rx=5, ry=5, fillColor=col, strokeColor=col, strokeWidth=0))
        d.add(Rect(cx, y_r1 + card_h - 18, card_w, 6, rx=0, ry=0, fillColor=col, strokeColor=col, strokeWidth=0))
        # Number badge & title
        d.add(Circle(cx + 12, y_r1 + card_h - 9, 6.5, fillColor=C_WHITE, strokeColor=C_WHITE, strokeWidth=0))
        d.add(String(cx + 12, y_r1 + card_h - 12, str(num), fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=col))
        d.add(String(cx + 24, y_r1 + card_h - 12, name, fontName="Helvetica-Bold", fontSize=7.5, fillColor=C_WHITE))

        # Icon inside
        icon_fn(d, cx + card_w/2, y_r1 + card_h - 32, col)

        # 2 description lines
        d.add(String(cx + card_w/2, y_r1 + 18, l1, fontName="Helvetica-Bold", fontSize=6.5, textAnchor="middle", fillColor=C_NAVY))
        d.add(String(cx + card_w/2, y_r1 + 8,  l2, fontName="Helvetica", fontSize=6, textAnchor="middle", fillColor=C_GRAY_MED))

        # Horizontal connecting arrow to next card
        if i < 3:
            ax1 = cx + card_w + 1
            ax2 = ax1 + gap_x - 3
            ay = y_r1 + card_h/2
            d.add(Line(ax1, ay, ax2, ay, strokeColor=C_NAVY, strokeWidth=1.2))
            d.add(Polygon([ax2, ay, ax2 - 4, ay + 3, ax2 - 4, ay - 3], fillColor=C_NAVY, strokeColor=C_NAVY, strokeWidth=0))

    # Draw Row 2
    for i, (num, name, icon_fn, l1, l2, col, bg, border) in enumerate(r2):
        cx = start_x + i * (card_w + gap_x)
        # Card outline
        d.add(Rect(cx, y_r2, card_w, card_h, rx=5, ry=5, fillColor=C_WHITE, strokeColor=col, strokeWidth=1.3))
        # Top header pill
        d.add(Rect(cx, y_r2 + card_h - 18, card_w, 18, rx=5, ry=5, fillColor=col, strokeColor=col, strokeWidth=0))
        d.add(Rect(cx, y_r2 + card_h - 18, card_w, 6, rx=0, ry=0, fillColor=col, strokeColor=col, strokeWidth=0))
        # Number badge & title
        d.add(Circle(cx + 12, y_r2 + card_h - 9, 6.5, fillColor=C_WHITE, strokeColor=C_WHITE, strokeWidth=0))
        d.add(String(cx + 12, y_r2 + card_h - 12, str(num), fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=col))
        d.add(String(cx + 24, y_r2 + card_h - 12, name, fontName="Helvetica-Bold", fontSize=7.5, fillColor=C_WHITE))

        # Icon inside
        icon_fn(d, cx + card_w/2, y_r2 + card_h - 32, col)

        # 2 description lines
        d.add(String(cx + card_w/2, y_r2 + 18, l1, fontName="Helvetica-Bold", fontSize=6.5, textAnchor="middle", fillColor=C_NAVY))
        d.add(String(cx + card_w/2, y_r2 + 8,  l2, fontName="Helvetica", fontSize=6, textAnchor="middle", fillColor=C_GRAY_MED))

        # Horizontal connecting arrow to next card
        if i < 3:
            ax1 = cx + card_w + 1
            ax2 = ax1 + gap_x - 3
            ay = y_r2 + card_h/2
            d.add(Line(ax1, ay, ax2, ay, strokeColor=C_NAVY, strokeWidth=1.2))
            d.add(Polygon([ax2, ay, ax2 - 4, ay + 3, ax2 - 4, ay - 3], fillColor=C_NAVY, strokeColor=C_NAVY, strokeWidth=0))

    # Connecting Flow from Row 1 Stage 4 to Row 2 Stage 5
    # Goes down from bottom of Stage 4 (cx=388+54=442, y=150) to y=134, left to x=64, down to y=116 into Stage 5
    d.add(Line(442, y_r1, 442, 134, strokeColor=C_PURPLE, strokeWidth=1.3))
    d.add(Line(442, 134, 64, 134, strokeColor=C_PURPLE, strokeWidth=1.3))
    d.add(Line(64, 134, 64, y_r2 + card_h, strokeColor=C_PURPLE, strokeWidth=1.3))
    d.add(Polygon([64, y_r2 + card_h, 61, y_r2 + card_h + 4, 67, y_r2 + card_h + 4],
                  fillColor=C_PURPLE, strokeColor=C_PURPLE, strokeWidth=0))
    d.add(String(253, 137, "findings move on to checking",
                 fontName="Helvetica-Oblique", fontSize=6.5, textAnchor="middle", fillColor=C_PURPLE))

    # Feedback Loop: From top of Stage 5 curving back up to bottom of Stage 2 (SEARCH)
    # Dashed amber arrow
    fb_x1 = start_x + card_w/2 + 20   # from stage 5 top
    fb_x2 = start_x + (card_w + gap_x) + card_w/2  # into stage 2 bottom
    d.add(Line(fb_x1, y_r2 + card_h, fb_x1, 126, strokeColor=C_AMBER, strokeWidth=1.4, strokeDashArray=[4, 2]))
    d.add(Line(fb_x1, 126, fb_x2, 126, strokeColor=C_AMBER, strokeWidth=1.4, strokeDashArray=[4, 2]))
    d.add(Line(fb_x2, 126, fb_x2, y_r1, strokeColor=C_AMBER, strokeWidth=1.4, strokeDashArray=[4, 2]))
    d.add(Polygon([fb_x2, y_r1, fb_x2 - 3, y_r1 - 5, fb_x2 + 3, y_r1 - 5],
                  fillColor=C_AMBER, strokeColor=C_AMBER, strokeWidth=0))

    # Amber badge on the feedback loop
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

print("make_synopsis_workflow_diagram defined successfully")
