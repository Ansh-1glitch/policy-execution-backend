"""
PDF Generator Module - Converts NLP JSON data to formatted PDF
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime


def generate_policy_pdf(nlp_data: dict, file_name: str = "policy.pdf") -> BytesIO:
    """
    Generate a formatted PDF from NLP policy data
    
    Args:
        nlp_data: Dictionary containing policy data with rules
        file_name: Name of the original policy file
    
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E3192'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2E3192'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph("Policy Execution Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Metadata Section
    policy_id = nlp_data.get('policy_id', 'N/A')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    metadata = [
        ['Policy ID:', policy_id],
        ['Source File:', file_name],
        ['Generated:', timestamp],
        ['Total Rules:', str(len(nlp_data.get('rules', [])))]
    ]
    
    metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8E8E8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(metadata_table)
    elements.append(Spacer(1, 20))
    
    # Rules Section
    rules_heading = Paragraph("Extracted Rules & Tasks", heading_style)
    elements.append(rules_heading)
    elements.append(Spacer(1, 12))
    
    rules = nlp_data.get('rules', [])
    
    if rules:
        # Rules table header
        rules_data = [['Rule ID', 'Action', 'Role', 'Deadline']]
        
        # Add each rule with Paragraph for text wrapping
        for rule in rules:
            # Use Paragraph for action text to enable wrapping
            action_text = rule.get('action', 'N/A')
            action_para = Paragraph(action_text, styles['Normal'])
            
            rules_data.append([
                Paragraph(rule.get('rule_id', 'N/A'), styles['Normal']),
                action_para,  # Wrapped text
                Paragraph(rule.get('responsible_role', 'N/A'), styles['Normal']),
                Paragraph(rule.get('deadline', 'Not specified'), styles['Normal'])
            ])
        
        # Adjusted column widths to prevent text overlap
        rules_table = Table(rules_data, colWidths=[0.8*inch, 3.2*inch, 1.2*inch, 1.3*inch])
        rules_table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E3192')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Body styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(rules_table)
    else:
        no_rules = Paragraph("No rules found in this policy.", styles['Normal'])
        elements.append(no_rules)
    
    elements.append(Spacer(1, 20))
    
    # Statistics Section
    stats_heading = Paragraph("Statistics Summary", heading_style)
    elements.append(stats_heading)
    elements.append(Spacer(1, 12))
    
    # Count tasks by role
    role_counts = {}
    for rule in rules:
        role = rule.get('responsible_role', 'Unknown')
        role_counts[role] = role_counts.get(role, 0) + 1
    
    stats_data = [['Metric', 'Value']]
    stats_data.append(['Total Rules Extracted', str(len(rules))])
    
    for role, count in role_counts.items():
        stats_data.append([f'{role} Tasks', str(count)])
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E3192')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ]))
    
    elements.append(stats_table)
    
    # Footer
    elements.append(Spacer(1, 30))
    footer_text = "Generated by PolicyVision3.0 - Policy Execution Engine"
    footer = Paragraph(footer_text, ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    ))
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF data
    buffer.seek(0)
    return buffer


def generate_simple_pdf(data: dict) -> BytesIO:
    """
    Generate a simple PDF for testing
    
    Args:
        data: Dictionary with any data
    
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title = Paragraph("Policy Data Export", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Add data as text
    import json
    data_text = json.dumps(data, indent=2)
    content = Paragraph(f"<pre>{data_text}</pre>", styles['Code'])
    elements.append(content)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
