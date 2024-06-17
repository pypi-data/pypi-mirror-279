import argparse
import warnings

from cxcli import users
from cxcli.cx_caller import CxCaller
from cxcli.cx_token import get_token
from urllib3.exceptions import InsecureRequestWarning




def create_parser():
    parser = argparse.ArgumentParser(
        description="ConnectX CLI", epilog="Copyright Amdocs"
    )
    parser.add_argument("--t", "--tenant", help="Tenant name", required=True)
    parser.add_argument(
        "--u", "--user", help="ConnectX username (email in most cases)"
    )
    parser.add_argument("--p", "--passw", help="ConnectX password")
    parser.add_argument(
        "--e",
        "--env",
        help="dev, ppe, or prod",
        choices=["dev", "ppe", "prod"],
        required=True,
    )
    parser.add_argument("command", choices=["users"])
    parser.add_argument("params", nargs="*")
    # parser.add_argument(
    #     "--format", default="json", choices=["json", "csv"], type=str.lower
    # )
    return parser


def main():
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)
    args = create_parser().parse_args()
    domain_name = get_domain_nane(args.e)
    token = get_token(args.u,args.p,args.t,domain_name)
    cx = CxCaller(domain_name=domain_name,token=token)
    if args.command == "users":
        users.users_cmd(cx,args.params)
    # print(token)


def get_domain_nane(env):
    if env == "dev":
        return "dev.amdocs-dbs.cloud"
    if env == "ppe":
        return "ppe.amdocs-dbs.cloud"
    if env == "prod":
        return "amdocs-dbs.com"
    raise Exception(f"Unknown enviroment {env}")
