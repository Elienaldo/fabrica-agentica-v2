"""Aviso da V2 ao Bootstrapper: bloqueio na checagem inicial da destruição.

SEM USO desde 17/11/2026: o Bootstrapper passou a rodar `destruir-secao-api.py` e lê o resultado
direto, então o script não chama mais este módulo (evita o Bootstrapper avisar a si mesmo).
Mantido só como módulo testado, sem chamador.

Uma tentativa, sem retry e sem redirecionamento; nada acontece na importação.
Configuração: ambiente do processo e, se faltar, variáveis User do Windows.
"""
import json
import os
import re
import urllib.error
import urllib.request

URL_ENV = 'FABRICA_V2_WEBHOOK_URL'
KEY_ENV = 'FABRICA_V2_WEBHOOK_KEY'
URL_PATTERN = r'https://api2\.cursor\.sh/automations/webhook/[A-Za-z0-9_-]+'
SCRIPT = 'destruir-secao-api.py'


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
    request = urllib.request.Request(
        url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json',
                 'Authorization': 'Bearer ' + key, 'X-Automation-Key': key}, method='POST')
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        with opener.open(request, timeout=timeout) as response:
            return response.status
    except urllib.error.HTTPError as error:
        code = error.code
        error.close()
        return code


def _clean(text, secrets):
    text = str(text)
    for secret in secrets:
        if secret:
            text = text.replace(secret, '[redigido]')
    return ''.join(c for c in text if c >= ' ' or c == '\n')[:2000]


def notify_bloqueio_inicial(result, exit_code, execution_id, *, env=None, user_env_reader=None, transport=None):
    """Só envia no bloqueio da checagem inicial (exit 2, stage preflight).

    Uma tentativa por objeto de resultado; nunca altera exit nem erro originais.
    """
    if exit_code != 2 or result.get('stage') != 'preflight':
        return None
    if 'notification' in result:
        return result['notification']
    notice = {'status': 'not_configured', 'execution_id': execution_id,
              'delivery_confirmed': False, 'attempt_count': 0}
    result['notification'] = notice
    env = os.environ if env is None else env
    reader = _user_env if user_env_reader is None else user_env_reader
    url = env.get(URL_ENV) or reader(URL_ENV) or ''
    key = env.get(KEY_ENV) or reader(KEY_ENV) or ''
    if not url or not key:
        return notice
    if not re.fullmatch(URL_PATTERN, url) or any(c in key for c in '\r\n'):
        notice['status'] = 'invalid_configuration'
        return notice
    secrets = (key, url)
    secao = result.get('secao') if isinstance(result.get('secao'), dict) else {}
    motivos = result.get('motivos_aviso_humano') or []
    payload = {'execution_id': execution_id, 'script': SCRIPT,
               'feature': _clean(secao.get('nome') or '', secrets),
               'exit': 2,
               'erro': _clean(result.get('erro') or 'Bloqueio na checagem inicial.', secrets),
               'motivos_aviso_humano': [_clean(m, secrets) for m in motivos if isinstance(m, str)],
               'status': 'aguardando_humano'}
    notice['attempt_count'] = 1
    try:
        code = (transport or _post)(url, payload, key, timeout=8)
        notice['http_status'] = int(code)
        notice['status'] = 'http_accepted' if code == 200 else 'http_rejected'
    except Exception as failure:
        notice['status'] = 'send_failed'
        notice['error_type'] = type(failure).__name__
    return notice