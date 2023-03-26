import os
import subprocess
import shlex
import json
import math
import sys

REPOPATH = "./kitchen_garden-main"
INDEXPATH = "./inverted_index.json"

inverted_index = {}


def tokenize_file(file_path):
    command = f"pygmentize -f raw {file_path}"
    args = shlex.split(command)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        raise Exception(f"Error while tokenizing file {file_path}: {error.decode('utf-8')}")
    return output.decode("utf-8").split('\n')


def get_text(token):
    return token.split('\t')[1].replace("'", "")


def create_inverted_index(repo_path):
    inverted_index = {}
    for root, dirs, files in os.walk(repo_path):
        for file_name in files:
            if file_name.endswith(".cpp") or file_name.endswith(".h"):  # other file extensions can be used
                file_path = os.path.join(root, file_name)
                tokens = set(tokenize_file(file_path))
                for token in tokens:
                    if token.startswith("Token.Name"):
                        text = get_text(token)
                        if text not in inverted_index:
                            inverted_index[text] = set()
                        inverted_index[text].add(file_path)
    for token in inverted_index.keys():
        inverted_index[token] = list(inverted_index[token])
    return inverted_index


def get_set_of_tokens(query_tokens):
    res = set(map(lambda token: get_text(token), filter(lambda token: token.startswith("Token.Name"), query_tokens)))
    return res


def check_file_similarity(file_path, inverted_index):
    query_tokens = list(tokenize_file(file_path))
    query_tokens = get_set_of_tokens(query_tokens)
    min_num_tokens = math.ceil(len(query_tokens) * 0.85)

    for repo_name, repo_tokens in inverted_index.items():
        matching_files = set()
        for token in query_tokens:
            if token in repo_tokens:
                matching_files.update(repo_tokens[token])
        for file_name in matching_files:
            file_tokens = set()
            for token in query_tokens:
                if token in repo_tokens and file_name in repo_tokens[token]:
                    file_tokens.add(token)
            if len(file_tokens) >= min_num_tokens:
                return f"The code has {len(file_tokens) / len(query_tokens):.{2}} similarity with {file_name}"
    return "OK"


def save_inverted_index():
    with open(INDEXPATH, "w") as f:
        json.dump(inverted_index, f)


def load_inverted_index():
    with open(INDEXPATH, "r") as f:
        inverted_index = json.load(f)


for repo_name in os.listdir(REPOPATH):
    repo_full_path = os.path.join(REPOPATH, repo_name)
    if os.path.isdir(repo_full_path):
        inverted_index[repo_name] = create_inverted_index(repo_full_path)
save_inverted_index()

code_to_check = []
for line in sys.stdin:
    code_to_check.append(line)
code_to_check = "\n".join(code_to_check)
os.system(f'echo "{code_to_check}" > file_to_check.cpp')

similarity = check_file_similarity("file_to_check.cpp", inverted_index)
print(similarity)
