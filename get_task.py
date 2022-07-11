import json
from todoist_api_python.api import TodoistAPI

token = "cdd2805fb37f7cde2343f764b94b534d0c6f2f25"
api = TodoistAPI(token)


def main():
    tasks = api.get_tasks()
    records = {
        task.id: {"content": task.content, "project_id": task.project_id}
        for task in tasks
    }
    write("tasks.json", records)

    projects = api.get_projects()
    records = {project.id: project.name for project in projects}
    write("projects.json", records)


def write(file, records):
    with open(file, "w", encoding="utf-8") as fp:
        json.dump(records, fp, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
