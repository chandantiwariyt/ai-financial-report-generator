from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

def build_pdf(ticker, stock_info, analysis, ai_content, output_path='report_output.pdf'):
    doc    = SimpleDocTemplate(output_path, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    story  = []

    # Custom Styles
    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                  fontSize=24, textColor=colors.HexColor('#003366'),
                                  spaceAfter=6, alignment=TA_CENTER)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading1'],
                                    fontSize=14, textColor=colors.HexColor('#003366'),
                                    spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'],
                                 fontSize=10, spaceAfter=8, leading=14)
    metric_label = ParagraphStyle('MetricLabel', parent=styles['Normal'],
                                   fontSize=9, textColor=colors.grey)

    # Header
    story.append(Paragraph(stock_info['name'], title_style))
    story.append(Paragraph(f"Financial Analysis Report — {ticker}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#003366')))
    story.append(Spacer(1, 0.2*inch))

    # Key Metrics Table
    story.append(Paragraph("Key Metrics", heading_style))
    metrics = analysis['metrics']
    data = [
        ['Metric', 'Value', 'Metric', 'Value'],
        ['Current Price',   f"₹{stock_info['current_price']:,.2f}",  'P/E Ratio',      f"{stock_info['pe_ratio']}"],
        ['Market Cap',      f"₹{stock_info['market_cap']/1e9:.1f}B", 'Beta',           f"{stock_info['beta']}"],
        ['Profit Margin',   f"{metrics['profit_margin']*100:.1f}%",  'Sharpe Ratio',   f"{metrics['sharpe_ratio']}"],
        ['Annual Return',   f"{metrics['annual_return']}%",          'Max Drawdown',   f"{metrics['max_drawdown']}%"],
        ['ROE',             f"{metrics['roe']*100:.1f}%",            'Current Ratio',  f"{metrics['current_ratio']}"],
    ]
    table = Table(data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND',  (0,0), (-1,0), colors.HexColor('#003366')),
        ('TEXTCOLOR',   (0,0), (-1,0), colors.white),
        ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',    (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f0f4f8'), colors.white]),
        ('GRID',        (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING',     (0,0), (-1,-1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.2*inch))

    # Executive Summary
    story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(ai_content['executive_summary'], body_style))
    story.append(Spacer(1, 0.1*inch))

    # Risk Assessment
    story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
    story.append(Paragraph("Risk Assessment", heading_style))
    story.append(Paragraph(ai_content['risk_assessment'], body_style))
    story.append(Spacer(1, 0.1*inch))

    # Investment Thesis
    story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
    story.append(Paragraph("Investment Thesis", heading_style))
    story.append(Paragraph(ai_content['investment_thesis'], body_style))
    story.append(Spacer(1, 0.2*inch))

    # Footer
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#003366')))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("This report is AI-generated for educational purposes only. Not financial advice.",
                            ParagraphStyle('Footer', parent=styles['Normal'],
                                           fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))

    doc.build(story)
    return output_path