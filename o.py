# -*- coding: utf-8 -*-
import csv
import git
import datetime
import os
import json
import codecs

#encoding=utf8  
import sys


reload(sys) 
sys.setdefaultencoding('utf-8')

# CSV文件路径，替换为实际的路径
csv_file_path = "files.csv"
with open(csv_file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    # 跳过标题行（如果有）
    next(reader)
    today = datetime.date.today()
    # start_time = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    # end_time = datetime.datetime(today.year, today.month, today.day, 23, 59, 59)
    start_time = today - datetime.timedelta(days=7)
    start_time = datetime.datetime(start_time.year, start_time.month, start_time.day, 0, 0, 0)
    end_time = datetime.datetime.now()
    print("Checking commits between {} and {}".format(start_time, end_time))  # 添加调试信息

    results = {}

    for row in reader:
        project_name = row[0]
        project_type = row[1]
        project_path = os.path.abspath(row[2])  # 获取绝对路径
        repo_path = os.path.join(project_path, ".git")
        print("Checking repository at path: {}".format(repo_path))  # 添加调试信息
        try:
            repo = git.Repo(repo_path, search_parent_directories=True)
            print("Repository found: {}".format(repo_path))  # 添加调试信息
            project_commits = []
            for commit in repo.iter_commits(since=start_time, until=end_time):
                if commit.author.name == 'sunjianxiang':
                    commit_info = {
                        "branch": repo.active_branch.name,
                        "commit": commit.message.encode('utf-8', 'ignore').decode('utf-8'),
                        "commit_date": datetime.datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')
                    }
                    project_commits.append(commit_info)
                    print("Project Name: {}, Project Path: {}, Commit Hash: {}, Message: {}".format(project_name, project_path, commit.hexsha, commit.message.encode('utf-8', 'ignore').decode('utf-8')))
            if project_commits:
                results[project_name] = {
                    "date": datetime.date.today().strftime('%Y-%m-%d'),
                    "type": project_type,
                    "records": project_commits,
                    "created_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                print("No commits found for today in repository: {}".format(repo_path))  # 添加调试信息
        except git.exc.InvalidGitRepositoryError:
            print("Invalid Git repository at path: {}".format(repo_path))  # 添加调试信息
            continue
        except git.exc.NoSuchPathError:
            print("No such path: {}".format(repo_path))  # 添加调试信息
            continue

    # 将结果写入output.json文件
    with codecs.open('output.json', 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile, ensure_ascii=False, indent=4)

    print("Results have been written to output.json")