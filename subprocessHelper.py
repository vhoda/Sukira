from subprocess import DEVNULL, STDOUT, Popen, PIPE, call, run as _run
from traceback import TracebackException

def printEx(e):
    """Imprime una traza de error."""
    print("".join(TracebackException.from_exception(e).format()))

def run(command, **kwargs):
    """Ejecuta un comando y devuelve el resultado."""
    return _run(command, **kwargs)

def returnCode(command, **kwargs):
    """Ejecuta un comando y devuelve su código de retorno."""
    return call(command, **kwargs)

def silent_run(command, **kwargs):
    """Ejecuta un comando sin imprimir salida y maneja errores."""
    command = [str(i) for i in command]
    try:
        return call(command, stdout=DEVNULL, stderr=STDOUT, **kwargs)
    except Exception as ex:
        print(f"Silent_run error:\n", command)
        printEx(ex)

def loud_run(command, **kwargs):
    """Ejecuta un comando y muestra la salida, manejando errores."""
    command = [str(i) for i in command]
    try:
        return call(command, **kwargs)
    except Exception as ex:
        print(f"Loud_run error:\n", command)
        printEx(ex)

def getout(command, **kwargs):
    """Ejecuta un comando y devuelve su salida como texto."""
    result = _run(command, text=True, stdout=PIPE, **kwargs)
    return result.stdout.strip()

def getout_r(command, **kwargs):
    """Ejecuta un comando y devuelve el código de retorno y la salida."""
    result = _run(command, text=True, stdout=PIPE, **kwargs)
    return [result.returncode, result.stdout]

