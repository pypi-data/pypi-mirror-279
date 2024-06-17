import argparse
from cxcli.cx_caller import CxCaller
from cxcli.users.list_users import list_users


def usage():
    print ("Available commands: list")


def create_parser():
    parser = argparse.ArgumentParser(description="Users")
    parser.add_argument("cmd", choices=["list"])
    parser.add_argument("params", nargs="*")
    return parser



def users_cmd(cx: CxCaller, args):
    parsed_args = create_parser().parse_args(args=args)
    cmd = parsed_args.cmd
    if cmd=="list":
        list_users(cx, parsed_args)
