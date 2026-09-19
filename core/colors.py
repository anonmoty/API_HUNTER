import sys

class C:
    # Standard colors
    R = '\033[91m'
    G = '\033[92m'
    Y = '\033[93m'
    B = '\033[94m'
    M = '\033[95m'
    CY = '\033[96m'
    W = '\033[97m'
    D = '\033[2m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    # Extended palette (Dark Green + Red)
    DG = '\033[38;5;22m'
    LG = '\033[38;5;46m'
    DR = '\033[38;5;124m'
    MR = '\033[38;5;196m'

    @staticmethod
    def ok(t):
        return C.LG + "[+]" + C.RESET + " " + t

    @staticmethod
    def fail(t):
        return C.MR + "[-]" + C.RESET + " " + t

    @staticmethod
    def warn(t):
        return C.Y + "[!]" + C.RESET + " " + t

    @staticmethod
    def info(t):
        return C.CY + "[*]" + C.RESET + " " + t

    @staticmethod
    def api(t):
        return C.LG + "[API]" + C.RESET + " " + t

    @staticmethod
    def vuln(t):
        return C.MR + C.BOLD + "[!]" + C.RESET + " " + t

    @staticmethod
    def bar(cur, tot, label=""):
        ln = 30
        fl = int(ln * cur / tot) if tot > 0 else 0
        blk = C.LG + chr(9608) * fl + C.RESET + C.DG + chr(9617) * (ln - fl) + C.RESET
        pct = int(100 * cur / tot) if tot > 0 else 0
        sys.stdout.write("\r  " + C.DR + "[" + C.RESET + blk + C.DR + "]" + C.RESET + " " + C.LG + str(pct) + "%" + C.RESET + " " + C.D + label + C.RESET)
        sys.stdout.flush()
        if cur == tot:
            sys.stdout.write("\n")
