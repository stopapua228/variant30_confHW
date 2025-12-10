import argparse,sys,os
from .parser import compile_to_value,ParseError
from .lexer import LexError
from .yaml_emit import emit_yaml

def main(argv=None):
    ap=argparse.ArgumentParser(prog="conf2yaml",description="Учебный конфигурационный язык → YAML")
    ap.add_argument("-i","--input",required=True,help="Путь к входному файлу")
    ap.add_argument("-o","--output",required=True,help="Путь к выходному YAML файлу")
    args=ap.parse_args(argv)

    if not os.path.isfile(args.input):
        print(f"Input file not found: {args.input}",file=sys.stderr)
        return 2

    out_dir=os.path.dirname(os.path.abspath(args.output)) or "."
    try:
        os.makedirs(out_dir,exist_ok=True)
    except Exception as e:
        print(f"Cannot create output directory: {e}",file=sys.stderr)
        return 2

    try:
        with open(args.input,"r",encoding="utf-8") as f:
            src=f.read()
        value=compile_to_value(src)
        y=emit_yaml(value)
        with open(args.output,"w",encoding="utf-8") as f:
            f.write(y+"\n")
        return 0
    except (LexError,ParseError) as e:
        print(str(e),file=sys.stderr)
        return 3
    except Exception as e:
        print(f"Unexpected error: {e}",file=sys.stderr)
        return 1
