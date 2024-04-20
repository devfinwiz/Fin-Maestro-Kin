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


def process_shareholding_pattern_data(data):
    stock_name = data.get('symbol', '')
    shareholding_pattern = data.get('shareholding_pattern', [])
    formatted_reports = {}
    for report in shareholding_pattern:
        label = report.get("")
        if label:
            formatted_label = label.replace('+', '').strip()
            formatted_reports[formatted_label] = {key: value for key, value in report.items() if key != ""}
    return {'symbol': stock_name, 'shareholding_pattern': formatted_reports}


def process_cash_flow_data(data):
    stock_name = data.get('symbol', '')
    cash_flow = data.get('cash_flow_statement', [])
    formatted_reports = {}
    for report in cash_flow:
        label = report.get("")
        if label:
            formatted_label = label.replace('+', '').strip()
            formatted_reports[formatted_label] = {key: value for key, value in report.items() if key != ""}
    return {'symbol': stock_name, 'cash_flow_statement': formatted_reports}


def process_balance_sheet_data(data):
    stock_name = data.get('symbol', '')
    cash_flow = data.get('balance_sheet', [])
    formatted_reports = {}
    for report in cash_flow:
        label = report.get("")
        if label:
            formatted_label = label.replace('+', '').strip()
            formatted_reports[formatted_label] = {key: value for key, value in report.items() if key != ""}
    return {'symbol': stock_name, 'balance_sheet': formatted_reports}


def process_profit_loss_data(data):
    stock_name = data.get('symbol', '')
    profit_loss_statement = data.get('profit_loss_statement', [])
    formatted_reports = {}
    for report in profit_loss_statement:
        label = report.get("")
        if label:
            formatted_label = label.replace('+', '').strip()
            formatted_reports[formatted_label] = {key: value for key, value in report.items() if key != ""}
    return {'symbol': stock_name, 'profit_loss_statement': formatted_reports}


def process_ratios_data(data):
    stock_name = data.get('symbol', '')
    ratios = data.get('ratios', [])
    formatted_reports = {}
    for report in ratios:
        label = report.get("")
        if label:
            formatted_label = label.replace('+', '').strip()
            formatted_reports[formatted_label] = {key: value for key, value in report.items() if key != ""}
    return {'symbol': stock_name, 'ratios': formatted_reports}


def process_key_metrics_data(value):
    return value.replace('\n', '').replace('\u20b9', '').replace('          ', '').replace('         ', '').replace('       ','').replace(' ','').replace(',','').replace('Cr.','Cr')