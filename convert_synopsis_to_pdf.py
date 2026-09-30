import re
import os
import subprocess
import markdown
import pypdf

workspace_dir = os.path.dirname(os.path.abspath(__file__))
md_path = os.path.join(workspace_dir, "PROJECT_SYNOPSIS.md")
html_path = os.path.join(workspace_dir, "PROJECT_SYNOPSIS.html")
pdf_path = os.path.join(workspace_dir, "PROJECT_SYNOPSIS.pdf")

with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

# Split markdown by <!-- PAGE BREAK -->
pages_md = md_content.split("<!-- PAGE BREAK -->")
print(f"Total sections parsed: {len(pages_md)}")

pages_html = []
for i, p_md in enumerate(pages_md):
    # Convert each page's markdown to HTML
    body = markdown.markdown(
        p_md.strip(),
        extensions=["tables", "fenced_code", "nl2br"]
    )
    # Style pre/code blocks
    body = re.sub(
        r'<pre><code>([\s\S]*?)</code></pre>',
        r'<div class="workflow-box"><pre class="workflow-code">\1</pre></div>',
        body
    )
    is_last = (i == len(pages_md) - 1)
    break_style = "page-break-after: auto;" if is_last else "page-break-after: always;"
    page_wrapper = f"""
    <div class="page-container page-{i+1}" style="{break_style}">
        <div class="page-header">
            <span class="doc-title">Project Synopsis &bull; Autonomous Agentic Market Analyzer</span>
            <span class="page-num">Section {i+1} of {len(pages_md)}</span>
        </div>
        <div class="page-content">
            {body}
        </div>
        <div class="page-footer">
            <span>Market Intelligence & Autonomous Agentic Web Analyzer</span>
            <span>Page {i+1} of {len(pages_md)}</span>
        </div>
    </div>
    """
    pages_html.append(page_wrapper)

full_body = "\n".join(pages_html)

styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Project Synopsis - Autonomous Agentic Market Analyzer</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 9mm 12mm 9mm 12mm;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif;
            font-size: 8.85pt;
            line-height: 1.36;
            color: #1e293b;
            background: #ffffff;
            margin: 0;
            padding: 0;
        }}

        .page-container {{
            width: 100%;
            height: 275mm;
            max-height: 275mm;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
            padding: 2mm 1mm;
        }}

        .page-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1.5px solid #2563eb;
            padding-bottom: 3px;
            font-size: 7.5pt;
            color: #64748b;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}

        .page-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid #cbd5e1;
            padding-top: 3px;
            font-size: 7.5pt;
            color: #94a3b8;
            margin-top: 6px;
        }}

        .page-content {{
            flex: 1;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }}

        h1, h2, h3, h4 {{
            color: #0f172a;
            font-weight: 700;
            margin-top: 0.45em;
            margin-bottom: 0.22em;
            page-break-after: avoid;
        }}

        h1 {{
            font-size: 13pt;
            color: #1e3a8a;
            line-height: 1.15;
            margin-top: 0;
        }}

        h2 {{
            font-size: 10.8pt;
            color: #1e40af;
            border-bottom: 1.2px solid #cbd5e1;
            padding-bottom: 2px;
            margin-top: 0.25em;
        }}

        h3 {{
            font-size: 9.3pt;
            color: #0f172a;
            margin-top: 0.35em;
        }}

        h4 {{
            font-size: 8.6pt;
            color: #334155;
            margin-top: 0.25em;
            margin-bottom: 0.12em;
        }}

        p {{
            margin: 0.28em 0;
            text-align: justify;
        }}

        ul, ol {{
            margin: 0.22em 0;
            padding-left: 17px;
        }}

        li {{
            margin-bottom: 0.12em;
        }}

        strong {{
            color: #0f172a;
        }}

        code {{
            font-family: 'Consolas', monospace;
            font-size: 7.9pt;
            background: #f1f5f9;
            color: #0f172a;
            padding: 1px 3px;
            border-radius: 2px;
            border: 1px solid #e2e8f0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 0.35em 0;
            font-size: 7.6pt;
            page-break-inside: avoid;
        }}

        th, td {{
            border: 1px solid #cbd5e1;
            padding: 3.5px 5.5px;
            text-align: left;
            vertical-align: top;
        }}

        th {{
            background: #f1f5f9;
            color: #0f172a;
            font-weight: 600;
        }}

        tr:nth-child(even) td {{
            background: #f8fafc;
        }}

        hr {{
            border: none;
            border-top: 1px solid #cbd5e1;
            margin: 0.45em 0;
        }}

        .workflow-box {{
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 3px solid #2563eb;
            border-radius: 4px;
            padding: 3.5px 7px;
            margin: 0.35em 0;
            page-break-inside: avoid;
        }}

        .workflow-code {{
            font-family: 'Consolas', monospace;
            font-size: 7.3pt;
            line-height: 1.18;
            color: #0f172a;
            background: transparent;
            margin: 0;
            white-space: pre;
        }}

        @media print {{
            body {{
                font-size: 8.85pt;
                color: #000000;
            }}
            .page-container {{
                height: 275mm;
                max-height: 275mm;
            }}
        }}
    </style>
</head>
<body>
{full_body}
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(styled_html)

print("HTML written to:", html_path)

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

file_uri = "file:///" + html_path.replace("\\", "/")

cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    file_uri
]

res = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    page_count = len(reader.pages)
    print(f"RESULT_PAGE_COUNT: {page_count}")
    for i, p in enumerate(reader.pages):
        print(f"Page {i+1}: {len(p.extract_text())} chars")
else:
    print(f"FAILED_TO_GENERATE: {res.stderr}")
