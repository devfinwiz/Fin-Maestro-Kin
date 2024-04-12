def process_quarterly_reports_data(data):
    stock_name = data.get('symbol', '')
    quarterly_reports = data.get('quarterly_reports', [])

    formatted_reports = {}
    for report in quarterly_reports:
        label = report.get('')
        if label:
            formatted_label = label.replace('+', '').strip()
            formatted_reports[formatted_label] = {key: value for key, value in report.items() if key != ''}
    
    return {'symbol': stock_name, 'quarterly_reports': formatted_reports}
