"""Aviso da V2 ao Bootstrapper ao terminar a criação de seção (sucesso ou falha).

Uma tentativa, sem retry e sem redirecionamento; configuração process/User; nada acontece na importação.
"""
import json
import os
import re
import unicodedata
import urllib.request
import urllib.error

URL_ENV = 'FABRICA_V2_CRIACAO_WEBHOOK_URL'
KEY_ENV = 'FABRICA_V2_CRIACAO_WEBHOOK_KEY'
URL_PATTERN = r'https://api2\.cursor\.sh/automations/webhook/[A-Za-z0-9_-]+'

def _user_env(name):
    if name not in (URL_ENV, KEY_ENV) or os.name != 'nt':
        return ''
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as handle:
            value, kind = winreg.QueryValueEx(handle, name)
            return value if isinstance(value, str) else ''
    except OSError:
        return ''

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def _post(url, payload, key, *, timeout):
    request = urllib.request.Request(url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type':'application/json', 'Authorization':'Bearer '+key, 'X-Automation-Key':key}, method='POST')
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        with opener.open(request, timeout=timeout) as response:
            return response.status
    except urllib.error.HTTPError as failure:
        code = failure.code
        failure.close()
        return code

def notify_creation(report, exit_code, execution_id, *, env=None, user_env_reader=None, transport=None):
    if 'notification' in report:
        return report['notification']
    notice = {'status':'not_configured', 'execution_id':execution_id,
              'delivery_confirmed':False, 'attempt_count':0}
    report['notification'] = notice
    section = report.get('section_name', '')
    if not isinstance(section, str) or not section.strip() or any(unicodedata.category(c) in {'Cc','Cf','Cs'} for c in section):
        notice['status'] = 'not_sent_invalid_section'
        return notice
    env = os.environ if env is None else env
    reader = _user_env if user_env_reader is None else user_env_reader
    url = env.get(URL_ENV) or reader(URL_ENV)
    key = env.get(KEY_ENV) or reader(KEY_ENV)
    if not url or not key:
        return notice
    if not re.fullmatch(URL_PATTERN, url) or any(c in key for c in '\r\n'):
        notice['status'] = 'invalid_configuration'
        return notice
    error = '' if exit_code == 0 else str(report.get('message') or 'Operação de criação interrompida; conferir estado antes de repetir.')
    for secret in (key, url):
        error = error.replace(secret, '[redigido]')
    error = ''.join(c for c in error if c >= ' ' or c == '\n')[:2000]
    payload = {'execution_id':execution_id, 'script':'criar-secao-feature.py', 'secao':section,
               'status':'sucesso' if exit_code == 0 else 'falha', 'exit':int(exit_code), 'erro':error}
    notice['attempt_count'] = 1
    try:
        code = (transport or _post)(url, payload, key, timeout=8)
        notice['http_status'] = int(code)
        notice['status'] = 'http_accepted' if code == 200 else 'http_rejected'
    except Exception as failure:
        notice['status'] = 'send_failed'
        notice['error_type'] = type(failure).__name__
    return notice