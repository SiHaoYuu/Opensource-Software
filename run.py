import git
import pandas as pd
from datetime import datetime, timedelta
import os

# 1. 指定本地仓库路径
repo_path = r'D:\code\data_crawler\vscode'

try:
    # 检查路径是否存在
    if not os.path.exists(repo_path):
        print(f"错误：路径不存在 - {repo_path}")
        print("请先克隆仓库：git clone https://github.com/microsoft/vscode.git")
        exit(1)
    
    repo = git.Repo(repo_path)
    print(f"成功打开仓库：{repo_path}")
    
    # 2. 计算5年前的日期
    five_years_ago = datetime.now() - timedelta(days=5*365)
    print(f"提取从 {five_years_ago.strftime('%Y-%m-%d')} 到现在的提交历史")
    
    # 3. 确定正确的主分支名称
    try:
        # 尝试获取当前分支
        current_branch = repo.active_branch.name
        print(f"当前分支：{current_branch}")
        main_branch = 'main' if 'main' in repo.heads else 'master'
    except:
        # 如果无法确定，尝试main，失败则尝试master
        main_branch = 'main' if 'main' in repo.heads else 'master'
    
    print(f"使用分支：{main_branch}")
    
    # 4. 遍历提交历史
    commits_data = []
    commit_count = 0
    
    for commit in repo.iter_commits(main_branch, since=five_years_ago):
        commit_count += 1
        
        # 正确获取修改的文件列表
        try:
            modified_files = list(commit.stats.files.keys())
        except AttributeError:
            # 如果stats.files不可用，尝试其他方法
            modified_files = []
            try:
                if commit.parents:
                    # 比较与父提交的差异
                    diff = commit.parents[0].diff(commit)
                    for diff_item in diff:
                        path = diff_item.a_path if diff_item.a_path else diff_item.b_path
                        if path:
                            modified_files.append(path)
            except:
                modified_files = ["获取失败"]
        
        # 准备提交信息
        commit_info = {
            'commit_hash': commit.hexsha[:10],  # 取前10位，更简洁
            'author': commit.author.name if commit.author else "Unknown",
            'author_email': commit.author.email if commit.author else "Unknown",
            'date': commit.authored_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'message': commit.message.strip().replace('\n', ' ') if commit.message else "",
            'modified_files_count': len(modified_files),
            'modified_files': ', '.join(modified_files[:10]) if modified_files else ""  # 只显示前10个文件
        }
        
        commits_data.append(commit_info)
        
        # 显示进度
        if commit_count % 100 == 0:
            print(f"已处理 {commit_count} 个提交...")
    
    # 5. 转换为DataFrame并保存
    if commits_data:
        df = pd.DataFrame(commits_data)
        
        # 排序：最新的提交在前
        df['date_dt'] = pd.to_datetime(df['date'])
        df = df.sort_values('date_dt', ascending=False)
        df = df.drop('date_dt', axis=1)
        
        # 保存到CSV
        csv_filename = 'vscode_commit_history.csv'
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"成功导出 {len(df)} 条提交记录到 '{csv_filename}'")
        
        # 显示统计信息
        print(f"\n数据统计：")
        print(f"- 时间范围：{five_years_ago.strftime('%Y-%m-%d')} 至 {datetime.now().strftime('%Y-%m-%d')}")
        print(f"- 作者数量：{df['author'].nunique()}")
        print(f"- 平均每次提交修改文件数：{df['modified_files_count'].mean():.1f}")
    else:
        print("没有找到符合条件的提交记录")
        
except git.exc.InvalidGitRepositoryError:
    print(f"错误：{repo_path} 不是有效的Git仓库")
    print("请确保路径正确，或先克隆仓库：git clone https://github.com/microsoft/vscode.git")
except Exception as e:
    print(f"发生错误：{type(e).__name__}: {e}")