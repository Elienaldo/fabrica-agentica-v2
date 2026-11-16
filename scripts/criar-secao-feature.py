"""Launcher local: não usa API do app; o companion executa UIA Windows."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import unicodedata
import uuid
from notificacao_criacao_v2 import notify_creation


def feature_name(value: str) -> str:
    if any(unicodedata.category(c) in {"Cc", "Cf", "Cs"} for c in value):
        raise ValueError("Nome contém controle, formato invisível ou surrogate inválido.")
    name = unicodedata.normalize("NFC", value.replace("/", "-").replace("\\", "-").strip())
    if not name or name.casefold() in {"fábrica agêntica", "fábrica agêntica v2", "âncora v2", "nova seção"}:
        raise ValueError("Nome vazio ou reservado para origem/Âncora V2/nome temporário.")
    return name


def read_report(path: Path) -> dict:
    if not path.is_file() or path.stat().st_size > 65536:
        return {}
    try:
        result = json.loads(path.read_text(encoding="utf-8-sig"))
        return result if isinstance(result, dict) else {}
    except (OSError, ValueError):
        return {}


class CommandLineError(ValueError):
    pass

class CreationParser(argparse.ArgumentParser):
    def error(self, message):
        raise CommandLineError(message)


def finish(report: dict, code: int, execution_id: str, root: Path) -> int:
    report['execution_id'] = execution_id
    report['exit_code'] = code
    try:
        notice = notify_creation(report, code, execution_id)
    except Exception as error:
        notice = {'status':'notifier_error', 'delivery_confirmed':False, 'error_type':type(error).__name__}
        report['notification'] = notice
    report['needs_human_notification'] = code != 0 or notice.get('status') != 'http_accepted'
    try:
        logs = root/'logs'
        logs.mkdir(exist_ok=True)
        path = logs/(execution_id+'-final.json')
        report['final_report_path'] = str(path)
        path.write_text(json.dumps(report, ensure_ascii=False), encoding='utf-8')
    except OSError:
        report['final_report_saved'] = False
    print(json.dumps(report, ensure_ascii=False))
    return code


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    root = Path(__file__).resolve().parent
    execution_id = 'criar-secao-'+uuid.uuid4().hex
    report: dict = {'status':'ABORTADO', 'stage':'precheck', 'section_id':None}
    parser = CreationParser(description='Cria seção via Âncora V2 e devolve somente Âncora V2; sem exclusões.')
    parser.add_argument('nome_feature')
    parser.add_argument('--selectors', type=Path, help='Legado: configuração antiga não é compatível; opção será rejeitada antes da UI.')
    try:
        args = parser.parse_args(argv)
        report['section_name'] = unicodedata.normalize('NFC', args.nome_feature.replace('/', '-').replace('\\', '-').strip())
        name = feature_name(args.nome_feature)
        report['section_name'] = name
        if args.selectors is not None:
            raise ValueError('--selectors legado não é usado. Execute somente com nome_feature; nenhum arquivo de config será lido.')
        if sys.platform != 'win32':
            raise RuntimeError('Somente Windows; não inicia o app.')
        companion = root/'criar-secao-feature.ps1'
        powershell = Path(os.environ.get('SystemRoot', r'C:\Windows'))/'System32/WindowsPowerShell/v1.0/powershell.exe'
        if not companion.is_file() or not powershell.is_file():
            raise RuntimeError('Companion .ps1 ou Windows PowerShell ausente.')
        logs = root/'logs'
        logs.mkdir(exist_ok=True)
        result_path = logs/(execution_id+'.json')
        command = [str(powershell), '-NoLogo', '-NoProfile', '-NonInteractive', '-File', str(companion), '-FeatureName', name, '-ResultPath', str(result_path)]
        try:
            completed = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=90, check=False)
        except subprocess.TimeoutExpired:
            report.update(read_report(result_path))
            report.update(status='ABORTADO_TIMEOUT', position_current_uncertain=True,
                          message='Companion de diagnóstico encerrado após 90s; app não é terminado. Conferir UI, não repetir automaticamente.', result_path=str(result_path))
            return finish(report, 124, execution_id, root)
        except KeyboardInterrupt:
            report.update(read_report(result_path))
            report.update(status='INTERROMPIDO', position_current_uncertain=True,
                          message='Interrupção humana; companion encerrado pelo subprocess, sem rollback. Conferir UI antes de repetir.', result_path=str(result_path))
            return finish(report, 130, execution_id, root)
        saved = read_report(result_path)
        if not saved:
            raise RuntimeError('Companion não produziu relatório válido; possível policy bloqueada. Não usar ExecutionPolicy Bypass. stderr: '+completed.stderr[-1600:])
        report.update(saved)
        report['result_path'] = str(result_path)
        if completed.returncode != 0 or report.get('status') != 'CONCLUIDO':
            if report.get('status') == 'CONCLUIDO':
                report['companion_status'] = 'CONCLUIDO'
                report['status'] = 'ABORTADO_COMPANION'
            if not report.get('message'):
                report['message'] = 'Companion retornou código '+str(completed.returncode)+'; resultado não confirmado como concluído.'
            return finish(report, 3, execution_id, root)
        return finish(report, 0, execution_id, root)
    except CommandLineError as error:
        report.update(status='ABORTADO_ARGUMENTOS', message=str(error))
        return finish(report, 2, execution_id, root)
    except Exception as error:
        report.update(status='ABORTADO', message=str(error))
        return finish(report, 3, execution_id, root)


if __name__ == '__main__':
    raise SystemExit(main())