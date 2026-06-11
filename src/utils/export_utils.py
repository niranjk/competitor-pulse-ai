"""Export utilities for CSV, PDF, and JSON formats."""
import csv
import json
from io import BytesIO, StringIO
from datetime import datetime
from typing import Optional, List, Dict, Any
from src.core.state import StructuredGTMModel


def generate_csv_export(results: List[Dict[str, Any]]) -> str:
    """Generate CSV export from research results."""
    output = StringIO()
    if not results:
        return ""
    
    fieldnames = [
        "Competitor",
        "URL",
        "Pricing Changed",
        "Detected Tiers",
        "Pricing Metrics",
        "Hiring Signals",
        "Research Date",
        "Status"
    ]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for result in results:
        intel = result.get("intelligence")
        writer.writerow({
            "Competitor": result.get("competitor_name", ""),
            "URL": result.get("target_url", ""),
            "Pricing Changed": intel.has_pricing_changed if intel else "",
            "Detected Tiers": " | ".join(intel.detected_tiers) if intel else "",
            "Pricing Metrics": " | ".join(intel.pricing_metrics) if intel else "",
            "Hiring Signals": " | ".join(intel.hiring_signals) if intel else "",
            "Research Date": result.get("research_date", datetime.now().isoformat()),
            "Status": "✓ Valid" if result.get("guardrail_passed") else "✗ Flagged"
        })
    
    return output.getvalue()


def generate_json_export(results: List[Dict[str, Any]]) -> str:
    """Generate JSON export from research results."""
    export_data = {
        "export_date": datetime.now().isoformat(),
        "total_competitors": len(results),
        "results": []
    }
    
    for result in results:
        intel = result.get("intelligence")
        export_data["results"].append({
            "competitor_name": result.get("competitor_name"),
            "target_url": result.get("target_url"),
            "research_date": result.get("research_date"),
            "guardrail_validation": result.get("guardrail_passed"),
            "intelligence": intel.model_dump() if intel else None,
            "outreach_sequence": result.get("outreach_sequence", ""),
            "mcp_enabled": result.get("mcp_enabled", False)
        })
    
    return json.dumps(export_data, indent=2)


def generate_pdf_report(results: List[Dict[str, Any]]) -> bytes:
    """Generate professional PDF report (HTML-based fallback)."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.5*inch, leftMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#0066cc'),
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Title
        elements.append(Paragraph("CompetitorPulseAI Research Report", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Results for each competitor
        for i, result in enumerate(results):
            if i > 0:
                elements.append(PageBreak())
            
            intel = result.get("intelligence")
            comp_name = result.get("competitor_name", "Unknown")
            
            # Competitor section
            elements.append(Paragraph(f"<b>{i+1}. {comp_name}</b>", styles['Heading2']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Basic info table
            info_data = [
                ["URL", result.get("target_url", "N/A")],
                ["Status", "✓ Valid" if result.get("guardrail_passed") else "✗ Flagged"],
                ["MCP Enabled", "Yes" if result.get("mcp_enabled") else "No"],
            ]
            
            info_table = Table(info_data, colWidths=[1.2*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1e293b')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
            ]))
            
            elements.append(info_table)
            elements.append(Spacer(1, 0.15*inch))
            
            # Intelligence findings
            if intel:
                elements.append(Paragraph("<b>Key Findings:</b>", styles['Heading3']))
                
                findings_data = [
                    ["Pricing Changed", "Yes" if intel.has_pricing_changed else "No"],
                    ["Tiers", ", ".join(intel.detected_tiers[:3]) if intel.detected_tiers else "N/A"],
                    ["Hiring Signals", str(len(intel.hiring_signals)) if intel.hiring_signals else "0"],
                ]
                
                findings_table = Table(findings_data, colWidths=[1.2*inch, 4*inch])
                findings_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1e293b')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#334155')),
                ]))
                
                elements.append(findings_table)
                elements.append(Spacer(1, 0.1*inch))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    except Exception as e:
        # Fallback: generate simple HTML PDF
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial; background: #0f172a; color: #f8fafc; margin: 20px; }}
                h1 {{ color: #0066cc; border-bottom: 2px solid #0066cc; }}
                h2 {{ color: #00d4ff; margin-top: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th, td {{ padding: 10px; text-align: left; border: 1px solid #334155; }}
                th {{ background: #1e293b; color: #0066cc; font-weight: bold; }}
                tr:nth-child(even) {{ background: #0f172a; }}
                .status-valid {{ color: #10b981; }}
                .status-invalid {{ color: #ef4444; }}
            </style>
        </head>
        <body>
            <h1>CompetitorPulseAI Research Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Total Competitors: {len(results)}</p>
            
            <h2>Results Summary</h2>
            <table>
                <tr>
                    <th>Competitor</th>
                    <th>Status</th>
                    <th>Pricing Changed</th>
                    <th>Tiers</th>
                    <th>Hiring Signals</th>
                </tr>
        """
        
        for result in results:
            intel = result.get("intelligence")
            status = "✓ Valid" if result.get("guardrail_passed") else "✗ Flagged"
            pricing = "Yes" if intel and intel.has_pricing_changed else "No" if intel else "N/A"
            tiers = len(intel.detected_tiers) if intel and intel.detected_tiers else 0
            signals = len(intel.hiring_signals) if intel and intel.hiring_signals else 0
            
            html_content += f"""
                <tr>
                    <td>{result.get('competitor_name', 'Unknown')}</td>
                    <td class="{'status-valid' if result.get('guardrail_passed') else 'status-invalid'}">{status}</td>
                    <td>{pricing}</td>
                    <td>{tiers}</td>
                    <td>{signals}</td>
                </tr>
            """
        
        html_content += """
            </table>
        </body>
        </html>
        """
        
        try:
            import pdfkit
            return pdfkit.from_string(html_content, False, options={'quiet': ''})
        except:
            # Last resort: return as bytes with warning
            return html_content.encode('utf-8')


def parse_batch_competitors(batch_input: str) -> List[tuple]:
    """Parse comma-separated competitor list into (name, url) tuples."""
    competitors = []
    lines = batch_input.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Handle "Company, https://url.com" format
        if ',' in line:
            parts = [p.strip() for p in line.split(',', 1)]
            name = parts[0]
            url = parts[1] if len(parts) > 1 else f"https://{name.lower().replace(' ', '')}.com"
        else:
            # Just company name - infer URL
            name = line
            url = f"https://{name.lower().replace(' ', '')}.com"
        
        competitors.append((name, url))
    
    return competitors
