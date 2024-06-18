import logging
import os
import subprocess

import gitlab
import litellm
from gitlab.const import SearchScope

from moatless import Workspace, AgenticLoop
from moatless.benchmark.utils import trace_metadata
from moatless.edit.clarify import _get_pre_start_line, _get_post_end_line_index
from moatless.edit.edit import EditCode
from moatless.transitions import code_transitions, edit_code_transitions
from moatless.utils.repo import (
    maybe_clone,
    pull_latest,
    clean_and_reset_state,
    get_diff,
    stage_all_files,
    create_and_checkout_branch,
    commit_changes,
    push_branch,
    setup_repo,
    clean_and_reset_repo,
)

gl = gitlab.Gitlab(url="https://gitlab.com/", private_token=os.environ["GITLAB_TOKEN"])

excluded = {"doktor24/frontends/ground-control"}

logging.basicConfig(level=logging.INFO)

logging.getLogger("LiteLLM").setLevel(logging.WARN)
litellm.success_callback = ["langfuse"]
litellm.failure_callback = ["langfuse"]


def list_groups():
    groups = gl.groups.list(iterator=True)
    for group in groups:
        print(f"{group.id} - {group.name}")


extensions = "-extension:md"

# frontend = 5785047
# services 5784926
# p24 5648780
group = gl.groups.get(5784926)


def find_git_repos(directory):
    git_repos = []
    for root, dirs, files in os.walk(directory):
        if ".git" in dirs:
            relative_path = os.path.relpath(root, directory)
            git_repos.append(relative_path)
            dirs.remove(".git")
    return git_repos


ignored_dirs = ["target", "node_modules"]


def find_name_in_files(repo_path, name):
    occurrences = []

    full_repo_path = f"{base_path}/{repo_path}"

    for root, dirs, files in os.walk(full_repo_path):
        for file in files:
            if any(dir in root for dir in ignored_dirs):
                continue
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line_number, line in enumerate(f, start=1):
                            if name.lower() in line.lower():
                                relative_path = os.path.relpath(
                                    file_path, full_repo_path
                                )
                                occurrences.append(
                                    (
                                        relative_path,
                                        line_number,
                                        line.strip(),
                                    )
                                )
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}")

    return occurrences


def display_occurrences(occurrences):
    if not occurrences:
        print("No occurrences found.")
    else:
        for file_path, line_number, line in occurrences:
            print(f"File: {file_path}, Line: {line_number}, Text: {line}")


def save_occurrences_to_file(occurrences, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for repo_path, relative_path, line_number, line in occurrences:
            f.write(f"{repo_path},{relative_path},{line_number},{line}\n")


base_path = "/home/albert/repos/p24"


def create_workspace(repo_dir, search_results):
    workspace = Workspace.from_dirs(repo_dir=repo_dir)

    for search_result in search_results:
        print(f"\nFound {search_result['path']} {search_result['startline']}")

        start_line = max(0, search_result["startline"] - 3)
        end_line = start_line + len(search_result["data"].split("\n"))

        workspace.file_context.add_line_span_to_context(
            search_result["path"], start_line, end_line
        )

    return workspace


def create_agent(workspace, session_id, trace_id):
    metadata = trace_metadata(
        instance_id=trace_id,
        session_id=session_id,
        trace_name="remove_code",
    )

    return AgenticLoop(
        edit_code_transitions(
            global_params={},
            state_params={
                EditCode: {"show_file_context": False, "lint_updated_code": False}
            },
        ),
        workspace=workspace,
        metadata=metadata,
    )


def create_branch_name(ticket_id, variable):
    return f"feature/{ticket_id}-remove-{variable}"


def remove_usage_of_variable(ticket_id, variable, repo_path):
    occurrences = find_name_in_files(repo_path, name)
    if not occurrences:
        return

    print(f'Found {len(occurrences)} occurrences of "{variable}" in {repo_path}')

    repo_dir = f"{base_path}/{repo_path}"
    repo_name = repo_path.split("/")[-1]
    clean_and_reset_repo(repo_dir)

    branch_name = create_branch_name(ticket_id, variable)

    project_path = f"doktor24/{repo_path}"
    print(project_path)

    project = gl.projects.get(project_path)

    existing_mrs = project.mergerequests.list(state="opened", source_branch=branch_name)
    if existing_mrs:
        print(f"MR already exists for {repo_dir}")
        # continue

    input(f"Press Enter to update {repo_path}...")
    create_and_checkout_branch(repo_dir, branch_name)

    print(f"Created branch {branch_name} for {repo_dir}")

    expected_changes = "\nExpected changes:"

    display_occurrences(occurrences)
    for file_path, line_number, line in occurrences:
        workspace = Workspace.from_dirs(repo_dir=repo_dir)
        content = workspace.file_repo.get_file(file_path).content
        if variable.lower() not in line.lower():
            continue

        if variable.lower() not in content.lower():
            continue

        print(f"\nFound {file_path} {line_number}")

        start_line = max(0, line_number - 3)
        end_line = start_line + 3

        content_lines = content.split("\n")
        ctx_start_line = max(0, start_line - 25)
        ctx_end_line = min(len(content_lines), end_line + 25)

        workspace.file_context.add_line_span_to_context(
            file_path, ctx_start_line, ctx_end_line
        )

        start_line = _get_pre_start_line(start_line, 1, content_lines)
        end_line = _get_post_end_line_index(end_line, len(content_lines), content_lines)
        expected_changes += f"\n* {file_path}:{line_number}"

        file_name = file_path.split("/")[-1].replace(".", "_")
        trace_id = f"{repo_name}_{file_name}_{line_number}"
        agent = create_agent(workspace, f"remove_{variable}_from_{repo_name}", trace_id)

        instructions = f"Remove the {variable} variable from {file_path}"

        response = agent.run(
            input_data={
                "start_line": start_line,
                "end_line": end_line,
                "file_path": file_path,
                "instructions": instructions,
            },
        )

        print(f"Response:\n {response.message}")
        workspace.save()

    print(expected_changes)

    diff = get_diff(repo_dir)
    print("\nDiff")
    print(diff)

    occurrences_left = find_name_in_files(repo_path, name)
    if occurrences_left:
        print(f"Found {len(occurrences_left)} occurrences left in {repo_path}")
        display_occurrences(occurrences_left)

    input("Files updated. Committing changes. Press Enter to continue...")

    print("Pushing and creating MR....")
    stage_all_files(repo_dir=repo_dir)
    commit_message = f"{ticket_id}: Remove the {variable} variable"
    commit_changes(repo_dir, commit_message)
    print(f"Committed changes: {commit_message}")
    push_branch(repo_dir, branch_name)

    if not existing_mrs:
        mr = project.mergerequests.create(
            {
                "source_branch": branch_name,
                "target_branch": "master",
                "title": commit_message,
                "description": commit_message,
            }
        )

        print(f"Created MR {mr.web_url}")


if __name__ == "__main__":
    name = "practitionerUrl"  # input("Enter the name to search for in .java files: ")
    git_repos = find_git_repos(base_path)
    print(f"Found {len(git_repos)} git repos in {base_path}")

    for repo_path in git_repos:
        remove_usage_of_variable("AX-47815", name, repo_path)
