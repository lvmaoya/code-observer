# -*- coding: utf-8 -*-
import csv
import git
import datetime
import os

# CSV文件路径，替换为实际的路径
csv_file_path = "p.csv"
with open(csv_file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    # 跳过标题行（如果有）
    next(reader)
    today = datetime.date.today()
    start_time = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    end_time = datetime.datetime(today.year, today.month, today.day, 23, 59, 59)
    print("Checking commits between {} and {}".format(start_time, end_time))  # 添加调试信息
    for row in reader:
        project_name = row[0]
        project_path = os.path.abspath(row[1])  # 获取绝对路径
        repo_path = os.path.join(project_path, ".git")
        print("Checking repository at path: {}".format(repo_path))  # 添加调试信息
        try:
            repo = git.Repo(repo_path, search_parent_directories=True)
            print("Repository found: {}".format(repo_path))  # 添加调试信息
            commits_found = False
            for commit in repo.iter_commits(since=start_time, until=end_time):
                commits_found = True
                print("Project Name: {}, Project Path: {}, Commit Hash: {}, Message: {}".format(project_name, project_path, commit.hexsha, commit.message))
            if not commits_found:
                print("No commits found for today in repository: {}".format(repo_path))  # 添加调试信息
        except git.exc.InvalidGitRepositoryError:
            print("Invalid Git repository at path: {}".format(repo_path))  # 添加调试信息
            continue
        except git.exc.NoSuchPathError:
            print("No such path: {}".format(repo_path))  # 添加调试信息
            continue