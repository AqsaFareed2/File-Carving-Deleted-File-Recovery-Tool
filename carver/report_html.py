"""
Phase 3 - Task B: HTML report.

Owner:  <assign a teammate>
Tests:  tests/test_report_html.py   (currently RED -- make them pass)

--------------------------------------------------------------------------
WHAT TO DO
--------------------------------------------------------------------------
Implement ``write_html(data, path)`` so it writes a single, self-contained HTML
page (all CSS inline -- no external files) that a forensic analyst can open in a
browser. It should show:

  * a header with the image path/size and the summary counts (recovered,
    duplicates, embedded; optionally the by-format / by-confidence breakdown);
  * a TABLE of the recovered files, one row each, with: #, type, offset
    (offset_hex), size, confidence, sha256 (a short prefix is fine), notes;
  * confidence shown as a colour-coded badge -- e.g. green for "high", amber for
    "medium", red for "low".

``data`` is the canonical summary from ``carver.report.report_data`` (see
carver/report_json.py for its full shape). Use ``html.escape`` on any text that
comes from the image (paths, notes) to avoid breaking the markup. You only edit
THIS file and tests/test_report_html.py.

--------------------------------------------------------------------------
ACCEPTANCE (tests/test_report_html.py)
--------------------------------------------------------------------------
The written file contains a <table>, has one row per recovered file (each
file's offset_hex appears), and shows the confidence values.
"""



import html

def write_html(data: dict, path: str) -> None:
    """
    Write ``data`` to ``path`` as a self-contained HTML report.
    """
    
    # Safely extract header/summary information
    image = data.get('image', {})
    summary = data.get('summary', {})
    image_path = html.escape(str(image.get('path', 'N/A')))
    image_size = html.escape(str(image.get('size', '0')))
    recovered = str(summary.get('recovered', len(data.get('files', []))))
    duplicates = str(summary.get('duplicates', 0))
    embedded = str(summary.get('embedded', 0))

    # Start building the HTML content with internal CSS
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File Carving Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; color: #333; }}
        .header-box {{ background-color: #f4f6f7; padding: 20px; border-radius: 8px; border: 1px solid #bdc3c7; margin-bottom: 20px; }}
        h1 {{ color: #2c3e50; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #dddddd; text-align: left; padding: 10px; }}
        th {{ background-color: #2c3e50; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        
        /* Badge Styling */
        .badge {{ padding: 5px 10px; border-radius: 12px; color: white; font-weight: bold; font-size: 0.85em; text-align: center; display: inline-block; min-width: 60px; }}
        .badge-high {{ background-color: #27ae60; }} /* Green */
        .badge-medium {{ background-color: #f39c12; }} /* Amber */
        .badge-low {{ background-color: #c0392b; }} /* Red */
    </style>
</head>
<body>
    <div class="header-box">
        <h1>Investigation Summary</h1>
        <p><strong>Image Path:</strong> {image_path}</p>
        <p><strong>Image Size:</strong> {image_size} bytes</p>
        <p>
            <strong>Recovered:</strong> {recovered} | 
            <strong>Duplicates:</strong> {duplicates} | 
            <strong>Embedded:</strong> {embedded}
        </p>
    </div>

    <table>
        <thead>
            <tr>
                <th>Number</th>
                <th>Type</th>
                <th>Offset</th>
                <th>Size</th>
                <th>Confidence</th>
                <th>SHA-256</th>
                <th>Notes</th>
            </tr>
        </thead>
        <tbody>
"""

    # Loop through each recovered file
    for f in data.get('files', []):
        f_num = html.escape(str(f.get('index', '')))
        f_type = html.escape(str(f.get('format', '')))

        # Checking for 'offset_hex' as required by the test
        f_offset = html.escape(str(f.get('offset_hex', f.get('offset', ''))))
        f_size = html.escape(str(f.get('size', '')))
        f_notes = html.escape(str(f.get('note', '')))
        
        # Get short prefix of SHA-256
        full_sha = str(f.get('sha256', ''))
        short_sha = html.escape(full_sha[:8]) if full_sha else ''
        
        # Determine confidence level and badge color
        confidence = str(f.get('confidence', 'low')).lower()
        if confidence == 'high':
            badge_class = 'badge-high'
        elif confidence in ['medium', 'amber']:
            badge_class = 'badge-medium'
        else:
            badge_class = 'badge-low'
            
        conf_display = html.escape(confidence.capitalize())
        badge_html = f"<span class='badge {badge_class}'>{conf_display}</span>"

        html_content += f"""
            <tr>
                <td>{f_num}</td>
                <td>{f_type}</td>
                <td>{f_offset}</td>
                <td>{f_size}</td>
                <td>{badge_html}</td>
                <td>{short_sha}</td>
                <td>{f_notes}</td>
            </tr>"""

    html_content += """
        </tbody>
    </table>
</body>
</html>
"""

    # Write the output to the path provided by the test
    with open(path, 'w', encoding='utf-8') as file:
        file.write(html_content)
