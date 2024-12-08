from weasyprint import HTML, CSS
from flask import url_for
import logging
import os
from urllib.parse import urljoin

def generate_pdf_from_html(html_content, css_files=None, base_url=None):
    """
    Generate PDF from HTML content
    Args:
        html_content (str): HTML content to convert
        css_files (list): List of CSS file paths
        base_url (str): Base URL for resolving relative URLs
    Returns:
        bytes: Generated PDF content
    """
    try:
        # Create WeasyPrint HTML object with base URL
        html = HTML(string=html_content, base_url=base_url)
        
        # Collect CSS styles
        styles = []
        if css_files:
            for css_file in css_files:
                if os.path.exists(css_file):
                    styles.append(CSS(filename=css_file))
                    
        # Add custom PDF styles
        pdf_styles = CSS(string='''
            @page {
                size: letter;
                margin: 2cm;
            }
            img {
                max-width: 100%;
                height: auto;
            }
            .grid-item, .portfolio-item {
                break-inside: avoid;
                page-break-inside: avoid;
                margin-bottom: 20px;
            }
            .zine-layout, .newsletter-layout, .portfolio-layout {
                display: block;
            }
            .card {
                break-inside: avoid;
                page-break-inside: avoid;
                margin-bottom: 20px;
                border: 1px solid #ddd;
                padding: 10px;
            }
        ''')
        styles.append(pdf_styles)
        
        # Generate PDF
        return html.write_pdf(stylesheets=styles)
    except Exception as e:
        logging.error(f"PDF generation error: {str(e)}")
        raise
