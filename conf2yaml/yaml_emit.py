def emit_yaml(value):
    lines=[]
    def emit_seq(seq,indent):
        prefix="  "*indent
        if not seq:
            return [prefix+"[]"] if indent==0 else [prefix+"[]"]
        out=[]
        for item in seq:
            if isinstance(item,list):
                if not item:
                    out.append(prefix+"- []")
                else:
                    out.append(prefix+"-")
                    out.extend(emit_seq(item,indent+1))
            else:
                out.append(prefix+"- "+str(item))
        return out

    if isinstance(value,list):
        lines=emit_seq(value,0)
    else:
        lines=[str(value)]
    return "\n".join(lines)
