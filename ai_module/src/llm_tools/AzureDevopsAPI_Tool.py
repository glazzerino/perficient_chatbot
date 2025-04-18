import jmespath
import argparse
from ..utils.AzureDevops.AzureDevopsAPI import AzureDevopsAPI
from ..utils.AzureDevops.commands import command_list


def _jmespath_filter(data: dict, query: str = None) -> dict:
    return jmespath.search(query, data) if query else data


def _check_args(checks: list[str], args: dict = None):
    if not args:
        raise argparse.ArgumentError(
            "No arguments provided. Use --help for more information."
        )
    for check in checks:
        if check not in args:
            raise argparse.ArgumentError(
                None,
                f"{check} is required for this command. Use --help for more information.",
            )


def get_projects(azure_devops_api, args) -> dict:
    query = args.query if "query" in args else None
    return _jmespath_filter(azure_devops_api.get_projects(), query)


def get_employees(azure_devops_api, args) -> dict:
    return _jmespath_filter(azure_devops_api.get_employees(), args.query)


def update_work_item(azure_devops_api, args) -> dict:
    _check_args(["project", "ids"], args)
    title = args.title or None
    description = args.description or None
    assignedMail = args.assigned or None
    result = azure_devops_api.update_work_item(
        id=args.ids[0],
        project=args.project,
        title=title,
        description=description,
        assignedMail=assignedMail,
    )

    return result


def get_work_items(azure_devops_api, args) -> dict:
    _check_args(["project", "ids"], args)

    result = azure_devops_api.get_work_items(
        project=args.project, ids=args.ids, as_of=args.as_of
    )

    return _jmespath_filter(result, args.query)


def get_project_info(azure_devops_api: AzureDevopsAPI, args: dict) -> dict:
    _check_args(["projectId"], args)
    result = azure_devops_api.get_project_info(args.projectId)
    return _jmespath_filter(result, args.query)


def get_work_item(azure_devops_api, args) -> dict:
    _check_args(["ids", "project"], args)

    result = azure_devops_api.get_work_item(
        project=args.project or None, id=int(args.ids[0])
    )

    return _jmespath_filter(result, args.query)


def create_work_item(azure_devops_api, args) -> dict:
    _check_args(["project", "title", "type", "description"], args)

    return azure_devops_api.create_work_item(
        project=args.project,
        title=args.title.strip('"'),
        type=args.type,
        description=args.description,
        assignedMail=args.assigned or None,
    )


def azure_devops_cli(input_string: str, token: str, org: str):
    azure_devops_api = AzureDevopsAPI(token, org)

    parser = argparse.ArgumentParser(
        description="Azure DevOps CLI", exit_on_error=False
    )
    parser.add_argument(
        "command",
        choices=command_list,
        help="Command to execute",
    )

    parser.add_argument("--project", type=str, help="Project name")
    parser.add_argument("--projectId", type=str, help="Project ID")
    parser.add_argument("--type", type=str, help="Type of the work item")
    parser.add_argument("--title", nargs="+", help="Title of the work item")
    parser.add_argument("--as_of", type=str, help="As of date for work items")
    parser.add_argument("--query", nargs="+", type=str, help="JMESPath query")
    parser.add_argument("--ids", type=int, nargs="+", help="List of work item IDs")
    parser.add_argument(
        "--description", nargs="+", type=str, help="Description of the work item"
    )
    parser.add_argument("--assigned", type=str, help="Assigned person of the work item")

    try:
        print("Input string:" + input_string)
        args = parser.parse_args(input_string.split())
    except Exception as e:
        return parser.format_usage()
    # except SystemExit():
    # return "Invalid command. Use --help for more information."
    args.query = " ".join(args.query) if args.query else None
    args.title = " ".join(args.title) if args.title else None
    args.description = " ".join(args.description) if args.description else None

    return _run_command(args, azure_devops_api)


def _run_command(args: dict, azure_devops_api: AzureDevopsAPI) -> dict:
    if args.command == "get_projects":
        return get_projects(azure_devops_api, args)
    elif args.command == "get_employees":
        return get_employees(azure_devops_api, args)
    elif args.command == "get_work_items":
        return get_work_items(azure_devops_api, args)
    elif args.command == "get_work_item":
        return get_work_item(azure_devops_api, args)
    elif args.command == "create_work_item":
        return create_work_item(azure_devops_api, args)
    elif args.command == "update_work_item":
        return update_work_item(azure_devops_api, args)
    else:
        raise Exception("Command not found")
