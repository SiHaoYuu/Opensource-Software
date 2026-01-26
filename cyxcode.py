import requests
import json
import time
from typing import Dict, List, Optional, Any
import pandas as pd
from datetime import datetime
import csv
import os


class MaxDataVSCodeCrawler:
    """
    修复版VS Code大数据爬虫
    专门修复NoneType错误
    """

    def __init__(self, github_token: str = None):
        """
        初始化爬虫

        Args:
            github_token: GitHub Personal Access Token（必须！）
        """
        if not github_token or github_token == "ghp_your_token_here":
            print("⚠️  警告：获取大量数据必须使用GitHub Token！")
            print("请先在 https://github.com/settings/tokens 创建token")
            print("并替换代码中的 GITHUB_TOKEN 变量")
            raise ValueError("需要GitHub Token")

        self.github_token = github_token
        self.base_url = "https://api.github.com/repos/microsoft/vscode"
        self.session = requests.Session()

        # 设置请求头
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Mozilla/5.0 (compatible; VSCodeMaxCrawler/1.0)"
        }

        self.session.headers.update(self.headers)
        self.max_per_page = 100  # GitHub每页最大100条

        # 配置获取的最大数量（更保守的设置）
        self.config = {
            'contributors': 300,  # 贡献者：300条
            'commits': 500,  # 提交：500条
            'issues': 200,  # 问题：200条
            'prs': 200,  # PR：200条
            'releases': 50,  # 发布：50条
            'branches': 30,  # 分支：30条
            'stargazers': 300,  # Star用户：300条
            'forks': 100,  # Fork仓库：100条
        }

    def _make_request_safe(self, url: str, params: Dict = None) -> Optional[Any]:
        """
        安全的API请求，增加重试机制
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params, timeout=30)

                # 显示API限制
                remaining = response.headers.get('X-RateLimit-Remaining', 'N/A')
                limit = response.headers.get('X-RateLimit-Limit', 'N/A')
                print(f"📊 API剩余: {remaining}/{limit}")

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 403:
                    reset_time = response.headers.get('X-RateLimit-Reset')
                    if reset_time:
                        reset_time = datetime.fromtimestamp(int(reset_time))
                        wait_seconds = max(10, (reset_time - datetime.now()).total_seconds())
                        print(f"⏰ API限制，等待 {wait_seconds:.0f} 秒...")
                        time.sleep(wait_seconds + 2)
                        continue
                    else:
                        print("❌ 未知的403错误")
                        return None
                elif response.status_code in [404, 422]:
                    print(f"❌ {response.status_code}: {response.text[:100]}")
                    return None
                else:
                    print(f"❌ 错误 {response.status_code}")
                    return None

            except requests.exceptions.Timeout:
                print(f"⏱️  请求超时，尝试 {attempt + 1}/{max_retries}")
                time.sleep(5)
            except Exception as e:
                print(f"❌ 请求异常: {e}")
                time.sleep(3)

        print(f"⚠️  请求失败，已重试{max_retries}次")
        return None

    def _safe_len(self, obj) -> int:
        """安全的获取长度，处理None值"""
        if obj is None:
            return 0
        try:
            return len(obj)
        except:
            return 0

    def _safe_get(self, data: Dict, key: str, default: Any = ''):
        """安全获取字典值"""
        if not isinstance(data, dict):
            return default

        value = data.get(key, default)
        if value is None:
            return default
        return value

    def get_massive_contributors(self) -> List[Dict]:
        """
        获取大量贡献者数据
        """
        print(f"🔍 获取贡献者数据（目标: {self.config['contributors']}条）...")

        contributors = []
        page = 1

        while len(contributors) < self.config['contributors']:
            print(f"  获取第{page}页贡献者...")

            params = {
                "per_page": min(self.max_per_page, self.config['contributors'] - len(contributors)),
                "page": page,
            }

            url = f"{self.base_url}/contributors"
            data = self._make_request_safe(url, params)

            if data is None or not isinstance(data, list):
                print("  ⚠️  获取数据失败或格式错误")
                break

            if len(data) == 0:
                print(f"  ✅ 已获取所有数据，共 {len(contributors)} 条")
                break

            for item in data:
                if not isinstance(item, dict):
                    continue

                contributors.append({
                    "序号": len(contributors) + 1,
                    "用户名": self._safe_get(item, 'login', '未知'),
                    "贡献次数": self._safe_get(item, 'contributions', 0),
                    "用户ID": self._safe_get(item, 'id', ''),
                    "头像URL": self._safe_get(item, 'avatar_url', ''),
                    "主页": self._safe_get(item, 'html_url', ''),
                    "类型": self._safe_get(item, 'type', 'User'),
                    "管理员": self._safe_get(item, 'site_admin', False),
                    "获取时间": datetime.now().isoformat(),
                    "页码": page
                })

            if len(data) < params["per_page"]:
                print(f"  ✅ 已获取所有数据，共 {len(contributors)} 条")
                break

            time.sleep(0.8)
            page += 1

            if len(contributors) >= self.config['contributors']:
                print(f"  ✅ 已达到目标数量: {len(contributors)} 条")
                break

        print(f"✅ 最终获取到 {len(contributors)} 条贡献者数据")
        return contributors

    def get_massive_commits(self, since_date: str = "2023-01-01") -> List[Dict]:
        """
        获取大量提交记录
        """
        print(f"🔍 获取提交记录（目标: {self.config['commits']}条）...")

        commits = []
        page = 1

        while len(commits) < self.config['commits']:
            print(f"  获取第{page}页提交记录...")

            params = {
                "per_page": min(self.max_per_page, self.config['commits'] - len(commits)),
                "page": page,
                "since": since_date
            }

            url = f"{self.base_url}/commits"
            data = self._make_request_safe(url, params)

            if data is None or not isinstance(data, list):
                print("  ⚠️  获取数据失败或格式错误")
                break

            if len(data) == 0:
                print(f"  ✅ 已获取所有数据，共 {len(commits)} 条")
                break

            for commit in data:
                if not isinstance(commit, dict):
                    continue

                commit_info = self._safe_get(commit, 'commit', {})
                author_info = self._safe_get(commit_info, 'author', {})

                commits.append({
                    "序号": len(commits) + 1,
                    "SHA": self._safe_get(commit, 'sha', ''),
                    "短SHA": self._safe_get(commit, 'sha', '')[:8],
                    "提交信息": self._safe_get(commit_info, 'message', '')[:200],
                    "作者": self._safe_get(author_info, 'name', ''),
                    "作者邮箱": self._safe_get(author_info, 'email', ''),
                    "提交时间": self._safe_get(author_info, 'date', ''),
                    "GitHub用户": self._safe_get(self._safe_get(commit, 'author', {}), 'login', ''),
                    "URL": self._safe_get(commit, 'html_url', ''),
                    "获取时间": datetime.now().isoformat(),
                    "页码": page
                })

            if len(data) < params["per_page"]:
                print(f"  ✅ 已获取所有数据，共 {len(commits)} 条")
                break

            time.sleep(0.8)
            page += 1

            if len(commits) >= self.config['commits']:
                print(f"  ✅ 已达到目标数量: {len(commits)} 条")
                break

        print(f"✅ 最终获取到 {len(commits)} 条提交记录")
        return commits

    def get_massive_issues_safe(self, state: str = "all", issue_type: str = "issues") -> List[Dict]:
        """
        修复版：获取大量问题/PR数据（修复NoneType错误）
        """
        max_items = self.config['issues'] if issue_type == "issues" else self.config['prs']
        type_name = "问题" if issue_type == "issues" else "PR"

        print(f"🔍 获取{state}{type_name}（目标: {max_items}条）...")

        items = []
        page = 1
        endpoint = "/issues" if issue_type == "issues" else "/pulls"

        while len(items) < max_items:
            print(f"  获取第{page}页{type_name}...")

            params = {
                "per_page": min(self.max_per_page, max_items - len(items)),
                "page": page,
                "state": state,
            }

            url = f"{self.base_url}{endpoint}"
            data = self._make_request_safe(url, params)

            if data is None or not isinstance(data, list):
                print("  ⚠️  获取数据失败或格式错误")
                break

            if len(data) == 0:
                print(f"  ✅ 已获取所有数据，共 {len(items)} 条")
                break

            for item in data:
                if not isinstance(item, dict):
                    continue

                # 对于issues端点，需要过滤掉PR
                if endpoint == "/issues" and 'pull_request' in item:
                    continue

                # 安全获取所有字段
                body = self._safe_get(item, 'body', '')
                labels = self._safe_get(item, 'labels', [])
                user_info = self._safe_get(item, 'user', {})

                # 处理标签
                label_names = []
                if isinstance(labels, list):
                    for label in labels:
                        if isinstance(label, dict):
                            name = self._safe_get(label, 'name', '')
                            if name:
                                label_names.append(name)

                items.append({
                    "序号": len(items) + 1,
                    "编号": self._safe_get(item, 'number', 0),
                    "标题": self._safe_get(item, 'title', ''),
                    "类型": "PR" if 'pull_request' in item else "Issue",
                    "状态": self._safe_get(item, 'state', ''),
                    "创建者": self._safe_get(user_info, 'login', ''),
                    "创建时间": self._safe_get(item, 'created_at', ''),
                    "更新时间": self._safe_get(item, 'updated_at', ''),
                    "关闭时间": self._safe_get(item, 'closed_at', ''),
                    "标签数": len(label_names),
                    "标签": ', '.join(label_names[:3]),  # 只取前3个标签
                    "评论数": self._safe_get(item, 'comments', 0),
                    "正文长度": self._safe_len(body),  # 使用安全长度函数
                    "正文预览": body[:100] + "..." if body else '',
                    "URL": self._safe_get(item, 'html_url', ''),
                    "获取时间": datetime.now().isoformat(),
                    "页码": page
                })

            print(f"  本页获取: {len(data)} 条，累计: {len(items)} 条")

            if len(data) < params["per_page"]:
                print(f"  ✅ 已获取所有数据，共 {len(items)} 条")
                break

            time.sleep(1.2)  # Issues API限制较严格
            page += 1

            if len(items) >= max_items:
                print(f"  ✅ 已达到目标数量: {len(items)} 条")
                break

        print(f"✅ 最终获取到 {len(items)} 条{type_name}数据")
        return items

    def get_massive_stargazers(self) -> List[Dict]:
        """
        获取大量star用户
        """
        print(f"🔍 获取Star用户（目标: {self.config['stargazers']}条）...")

        stargazers = []
        page = 1

        while len(stargazers) < self.config['stargazers']:
            print(f"  获取第{page}页Star用户...")

            params = {
                "per_page": min(self.max_per_page, self.config['stargazers'] - len(stargazers)),
                "page": page
            }

            url = f"{self.base_url}/stargazers"
            data = self._make_request_safe(url, params)

            if data is None or not isinstance(data, list):
                print("  ⚠️  获取数据失败或格式错误")
                break

            if len(data) == 0:
                print(f"  ✅ 已获取所有数据，共 {len(stargazers)} 条")
                break

            for user in data:
                if not isinstance(user, dict):
                    continue

                stargazers.append({
                    "序号": len(stargazers) + 1,
                    "用户名": self._safe_get(user, 'login', '未知'),
                    "用户ID": self._safe_get(user, 'id', ''),
                    "头像URL": self._safe_get(user, 'avatar_url', ''),
                    "主页": self._safe_get(user, 'html_url', ''),
                    "类型": self._safe_get(user, 'type', 'User'),
                    "管理员": self._safe_get(user, 'site_admin', False),
                    "获取时间": datetime.now().isoformat(),
                    "页码": page
                })

            if len(data) < params["per_page"]:
                print(f"  ✅ 已获取所有数据，共 {len(stargazers)} 条")
                break

            time.sleep(1.0)
            page += 1

            if len(stargazers) >= self.config['stargazers']:
                print(f"  ✅ 已达到目标数量: {len(stargazers)} 条")
                break

        print(f"✅ 最终获取到 {len(stargazers)} 条Star用户数据")
        return stargazers

    def get_massive_forks(self) -> List[Dict]:
        """
        获取大量fork信息
        """
        print(f"🔍 获取Fork仓库（目标: {self.config['forks']}条）...")

        forks = []
        page = 1

        while len(forks) < self.config['forks']:
            print(f"  获取第{page}页Fork...")

            params = {
                "per_page": min(self.max_per_page, self.config['forks'] - len(forks)),
                "page": page,
            }

            url = f"{self.base_url}/forks"
            data = self._make_request_safe(url, params)

            if data is None or not isinstance(data, list):
                print("  ⚠️  获取数据失败或格式错误")
                break

            if len(data) == 0:
                print(f"  ✅ 已获取所有数据，共 {len(forks)} 条")
                break

            for fork in data:
                if not isinstance(fork, dict):
                    continue

                owner_info = self._safe_get(fork, 'owner', {})
                description = self._safe_get(fork, 'description', '')

                forks.append({
                    "序号": len(forks) + 1,
                    "仓库名": self._safe_get(fork, 'full_name', ''),
                    "所有者": self._safe_get(owner_info, 'login', ''),
                    "是否私有": self._safe_get(fork, 'private', False),
                    "描述": description[:150] if description else '',
                    "Fork时间": self._safe_get(fork, 'created_at', ''),
                    "更新时间": self._safe_get(fork, 'updated_at', ''),
                    "推送时间": self._safe_get(fork, 'pushed_at', ''),
                    "Stars数": self._safe_get(fork, 'stargazers_count', 0),
                    "语言": self._safe_get(fork, 'language', ''),
                    "主页": self._safe_get(fork, 'html_url', ''),
                    "获取时间": datetime.now().isoformat(),
                    "页码": page
                })

            if len(data) < params["per_page"]:
                print(f"  ✅ 已获取所有数据，共 {len(forks)} 条")
                break

            time.sleep(0.8)
            page += 1

            if len(forks) >= self.config['forks']:
                print(f"  ✅ 已达到目标数量: {len(forks)} 条")
                break

        print(f"✅ 最终获取到 {len(forks)} 条Fork数据")
        return forks

    def get_massive_branches(self) -> List[Dict]:
        """
        获取所有分支
        """
        print(f"🔍 获取分支列表（目标: {self.config['branches']}条）...")

        branches = []
        page = 1

        while len(branches) < self.config['branches']:
            print(f"  获取第{page}页分支...")

            params = {
                "per_page": min(self.max_per_page, self.config['branches'] - len(branches)),
                "page": page
            }

            url = f"{self.base_url}/branches"
            data = self._make_request_safe(url, params)

            if data is None or not isinstance(data, list):
                print("  ⚠️  获取数据失败或格式错误")
                break

            if len(data) == 0:
                print(f"  ✅ 已获取所有数据，共 {len(branches)} 条")
                break

            for branch in data:
                if not isinstance(branch, dict):
                    continue

                commit_info = self._safe_get(branch, 'commit', {})

                branches.append({
                    "序号": len(branches) + 1,
                    "分支名": self._safe_get(branch, 'name', ''),
                    "是否受保护": self._safe_get(branch, 'protected', False),
                    "提交SHA": self._safe_get(commit_info, 'sha', ''),
                    "获取时间": datetime.now().isoformat(),
                    "页码": page
                })

            if len(data) < params["per_page"]:
                print(f"  ✅ 已获取所有数据，共 {len(branches)} 条")
                break

            time.sleep(0.5)
            page += 1

            if len(branches) >= self.config['branches']:
                print(f"  ✅ 已达到目标数量: {len(branches)} 条")
                break

        print(f"✅ 最终获取到 {len(branches)} 条分支数据")
        return branches

    def get_massive_releases(self) -> List[Dict]:
        """
        获取所有发布版本
        """
        print(f"🔍 获取发布版本（目标: {self.config['releases']}条）...")

        releases = []
        page = 1

        while len(releases) < self.config['releases']:
            print(f"  获取第{page}页发布版本...")

            params = {
                "per_page": min(self.max_per_page, self.config['releases'] - len(releases)),
                "page": page
            }

            url = f"{self.base_url}/releases"
            data = self._make_request_safe(url, params)

            if data is None or not isinstance(data, list):
                print("  ⚠️  获取数据失败或格式错误")
                break

            if len(data) == 0:
                print(f"  ✅ 已获取所有数据，共 {len(releases)} 条")
                break

            for release in data:
                if not isinstance(release, dict):
                    continue

                body = self._safe_get(release, 'body', '')
                author_info = self._safe_get(release, 'author', {})
                assets = self._safe_get(release, 'assets', [])

                # 计算总下载量
                total_downloads = 0
                if isinstance(assets, list):
                    for asset in assets:
                        if isinstance(asset, dict):
                            total_downloads += self._safe_get(asset, 'download_count', 0)

                releases.append({
                    "序号": len(releases) + 1,
                    "版本号": self._safe_get(release, 'tag_name', ''),
                    "版本名称": self._safe_get(release, 'name', ''),
                    "发布者": self._safe_get(author_info, 'login', ''),
                    "发布日期": self._safe_get(release, 'published_at', ''),
                    "预发布": self._safe_get(release, 'prerelease', False),
                    "草稿": self._safe_get(release, 'draft', False),
                    "发布说明长度": self._safe_len(body),
                    "发布说明预览": body[:120] + "..." if body else '',
                    "资产数量": len(assets) if isinstance(assets, list) else 0,
                    "总下载量": total_downloads,
                    "URL": self._safe_get(release, 'html_url', ''),
                    "获取时间": datetime.now().isoformat(),
                    "页码": page
                })

            if len(data) < params["per_page"]:
                print(f"  ✅ 已获取所有数据，共 {len(releases)} 条")
                break

            time.sleep(0.8)
            page += 1

            if len(releases) >= self.config['releases']:
                print(f"  ✅ 已达到目标数量: {len(releases)} 条")
                break

        print(f"✅ 最终获取到 {len(releases)} 条发布数据")
        return releases

    def get_repository_stats(self) -> Dict[str, Any]:
        """获取仓库统计信息"""
        print("🔍 获取仓库统计信息...")

        url = f"{self.base_url}"
        data = self._make_request_safe(url)

        if isinstance(data, dict):
            license_info = self._safe_get(data, 'license', {})

            return {
                "总Stars": self._safe_get(data, 'stargazers_count', 0),
                "总Forks": self._safe_get(data, 'forks_count', 0),
                "总Watchers": self._safe_get(data, 'watchers_count', 0),
                "开放问题": self._safe_get(data, 'open_issues_count', 0),
                "仓库大小": self._safe_get(data, 'size', 0),
                "创建时间": self._safe_get(data, 'created_at', ''),
                "最后更新": self._safe_get(data, 'updated_at', ''),
                "最后推送": self._safe_get(data, 'pushed_at', ''),
                "默认分支": self._safe_get(data, 'default_branch', 'main'),
                "语言": self._safe_get(data, 'language', ''),
                "License": self._safe_get(license_info, 'name', ''),
                "获取时间": datetime.now().isoformat()
            }
        return {}

    def export_massive_data_safely(self, export_dir: str = "vscode_massive_data"):
        """
        安全的导出大量数据（修复版）
        """
        os.makedirs(export_dir, exist_ok=True)
        print(f"📂 数据将导出到: {os.path.abspath(export_dir)}/")

        total_items = 0
        failed_apis = []

        try:
            # 1. 贡献者
            print(f"\n{'=' * 60}")
            print("1. 获取贡献者数据...")
            contributors = self.get_massive_contributors()
            if contributors:
                success = self._export_to_csv_safe(contributors, f"{export_dir}/1_contributors.csv")
                if success:
                    total_items += len(contributors)
                else:
                    failed_apis.append("contributors")
            else:
                print("  ⚠️  未获取到贡献者数据")
                failed_apis.append("contributors")

            # 2. 提交记录
            print(f"\n{'=' * 60}")
            print("2. 获取提交记录...")
            commits = self.get_massive_commits()
            if commits:
                success = self._export_to_csv_safe(commits, f"{export_dir}/2_commits.csv")
                if success:
                    total_items += len(commits)
                else:
                    failed_apis.append("commits")
            else:
                print("  ⚠️  未获取到提交记录")
                failed_apis.append("commits")

            # 3. 问题
            print(f"\n{'=' * 60}")
            print("3. 获取问题数据...")
            issues = self.get_massive_issues_safe(state="open", issue_type="issues")
            if issues:
                success = self._export_to_csv_safe(issues, f"{export_dir}/3_issues_open.csv")
                if success:
                    total_items += len(issues)
                else:
                    failed_apis.append("issues")
            else:
                print("  ⚠️  未获取到问题数据")
                failed_apis.append("issues")

            # 4. PR
            print(f"\n{'=' * 60}")
            print("4. 获取PR数据...")
            prs = self.get_massive_issues_safe(state="open", issue_type="pulls")
            if prs:
                success = self._export_to_csv_safe(prs, f"{export_dir}/4_prs_open.csv")
                if success:
                    total_items += len(prs)
                else:
                    failed_apis.append("prs")
            else:
                print("  ⚠️  未获取到PR数据")
                failed_apis.append("prs")

            # 5. Star用户
            print(f"\n{'=' * 60}")
            print("5. 获取Star用户数据...")
            stargazers = self.get_massive_stargazers()
            if stargazers:
                success = self._export_to_csv_safe(stargazers, f"{export_dir}/5_stargazers.csv")
                if success:
                    total_items += len(stargazers)
                else:
                    failed_apis.append("stargazers")
            else:
                print("  ⚠️  未获取到Star用户数据")
                failed_apis.append("stargazers")

            # 6. Fork仓库
            print(f"\n{'=' * 60}")
            print("6. 获取Fork仓库数据...")
            forks = self.get_massive_forks()
            if forks:
                success = self._export_to_csv_safe(forks, f"{export_dir}/6_forks.csv")
                if success:
                    total_items += len(forks)
                else:
                    failed_apis.append("forks")
            else:
                print("  ⚠️  未获取到Fork数据")
                failed_apis.append("forks")

            # 7. 发布版本
            print(f"\n{'=' * 60}")
            print("7. 获取发布版本数据...")
            releases = self.get_massive_releases()
            if releases:
                success = self._export_to_csv_safe(releases, f"{export_dir}/7_releases.csv")
                if success:
                    total_items += len(releases)
                else:
                    failed_apis.append("releases")
            else:
                print("  ⚠️  未获取到发布数据")
                failed_apis.append("releases")

            # 8. 分支
            print(f"\n{'=' * 60}")
            print("8. 获取分支数据...")
            branches = self.get_massive_branches()
            if branches:
                success = self._export_to_csv_safe(branches, f"{export_dir}/8_branches.csv")
                if success:
                    total_items += len(branches)
                else:
                    failed_apis.append("branches")
            else:
                print("  ⚠️  未获取到分支数据")
                failed_apis.append("branches")

            # 9. 仓库统计
            print(f"\n{'=' * 60}")
            print("9. 获取仓库统计信息...")
            stats = self.get_repository_stats()
            if stats:
                self._export_to_csv_safe([stats], f"{export_dir}/9_repository_stats.csv")

            # 显示总结
            print(f"\n{'=' * 60}")
            print("📊 数据获取总结")
            print("=" * 60)
            print(f"✅ 成功获取总数据条数: {total_items:,}")

            if failed_apis:
                print(f"⚠️  以下API获取失败: {', '.join(failed_apis)}")

            print(f"\n📁 保存目录: {os.path.abspath(export_dir)}/")

            # 显示文件列表
            print(f"\n📄 生成的文件:")
            csv_files = [f for f in os.listdir(export_dir) if f.endswith('.csv')]
            for file in sorted(csv_files):
                filepath = f"{export_dir}/{file}"
                try:
                    # 简单统计行数
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        count = len(lines) - 1 if len(lines) > 0 else 0
                    print(f"  {file}: {count:,} 条")
                except Exception as e:
                    print(f"  {file}: 读取失败 ({e})")

        except Exception as e:
            print(f"\n❌ 导出过程中出错: {e}")
            import traceback
            traceback.print_exc()

    def _export_to_csv_safe(self, data: Any, filename: str) -> bool:
        """
        安全的导出数据到CSV，返回是否成功
        """
        try:
            # 检查数据是否为空
            if data is None:
                print(f"  ⚠️  数据为空: {filename}")
                return False

            # 如果是字典，转为列表
            if isinstance(data, dict):
                data = [data]

            # 检查是否为列表
            if not isinstance(data, list):
                print(f"  ❌ 数据不是列表: {type(data)}")
                return False

            # 检查列表是否为空
            if len(data) == 0:
                print(f"  ⚠️  数据列表为空: {filename}")
                return False

            # 检查列表中的元素
            valid_data = []
            for i, item in enumerate(data):
                if item is None:
                    continue
                if not isinstance(item, dict):
                    continue
                valid_data.append(item)

            if not valid_data:
                print(f"  ⚠️  无有效数据: {filename}")
                return False

            # 获取所有字段
            all_fields = set()
            for item in valid_data:
                if isinstance(item, dict):
                    all_fields.update(item.keys())

            if not all_fields:
                print(f"  ⚠️  无有效字段: {filename}")
                return False

            # 导出CSV
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=sorted(all_fields))
                writer.writeheader()
                writer.writerows(valid_data)

            print(f"  ✅ 已导出: {filename} ({len(valid_data):,} 条)")
            return True

        except Exception as e:
            print(f"  ❌ 导出失败 {filename}: {e}")
            return False

    def show_config(self):
        """显示当前配置"""
        print("\n" + "=" * 60)
        print("📋 数据获取配置")
        print("=" * 60)

        total_target = sum(self.config.values())
        print(f"🎯 目标总数据条数: {total_target:,}")
        print("\n各数据类型目标:")
        for key, value in self.config.items():
            print(f"  • {key}: {value:,} 条")

        print(f"\n💡 提示:")
        print(f"  1. 当前配置较为保守，避免触发API限制")
        print(f"  2. 如需修改数量，可直接编辑config字典")
        print(f"  3. 所有数据获取都经过安全处理")


def main():
    """主函数"""
    print("🚀 VS Code GitHub仓库大数据爬虫（安全修复版）")
    print("=" * 60)
    print("✅ 专门修复NoneType错误和API限制问题")
    print("=" * 60)

    # 必须设置你的GitHub Token
    GITHUB_TOKEN = "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1"  # 必须替换！

    try:
        # 创建爬虫实例
        crawler = MaxDataVSCodeCrawler(github_token=GITHUB_TOKEN)

        # 显示配置
        crawler.show_config()

        print("\n请选择操作:")
        print("1. 导出所有数据（推荐）")
        print("2. 只测试单个API")
        print("3. 自定义配置")

        choice = input("\n请输入选择 (1-3): ").strip()

        if choice == "1":
            export_dir = input("输入导出目录名 (默认: vscode_massive_data): ").strip()
            if not export_dir:
                export_dir = "vscode_massive_data"

            confirm = input(f"将导出到 {export_dir}/，确认开始？(y/n): ").strip().lower()
            if confirm == 'y':
                print(f"\n🚀 开始获取数据，请耐心等待...")
                print("程序会自动处理API限制，可能需要较长时间")
                print("-" * 60)
                crawler.export_massive_data_safely(export_dir)
            else:
                print("操作已取消")

        elif choice == "2":
            print("\n可选测试的API:")
            print("1. 贡献者 API")
            print("2. 提交记录 API")
            print("3. 问题 API")
            print("4. PR API")

            api_choice = input("选择要测试的API (1-4): ").strip()

            if api_choice == "1":
                print("\n测试贡献者API...")
                data = crawler.get_massive_contributors()
                print(f"获取到 {len(data) if data else 0} 条数据")

            elif api_choice == "2":
                print("\n测试提交记录API...")
                data = crawler.get_massive_commits()
                print(f"获取到 {len(data) if data else 0} 条数据")

            elif api_choice == "3":
                print("\n测试问题API...")
                data = crawler.get_massive_issues_safe(state="open", issue_type="issues")
                print(f"获取到 {len(data) if data else 0} 条数据")

            elif api_choice == "4":
                print("\n测试PR API...")
                data = crawler.get_massive_issues_safe(state="open", issue_type="pulls")
                print(f"获取到 {len(data) if data else 0} 条数据")

        elif choice == "3":
            print("\n当前配置:")
            for i, (key, value) in enumerate(crawler.config.items(), 1):
                print(f"{i}. {key}: {value:,}")

            config_idx = input("\n输入要修改的配置编号 (或按Enter跳过): ").strip()
            if config_idx:
                try:
                    idx = int(config_idx) - 1
                    keys = list(crawler.config.keys())
                    if 0 <= idx < len(keys):
                        key = keys[idx]
                        new_value = input(f"请输入新的 {key} 数量 (当前: {crawler.config[key]:,}): ").strip()
                        if new_value:
                            crawler.config[key] = int(new_value)
                            print(f"✅ {key} 已更新为 {crawler.config[key]:,}")
                except Exception as e:
                    print(f"❌ 修改失败: {e}")

            export_dir = "vscode_custom_data"
            confirm = input(f"使用新配置导出到 {export_dir}/？(y/n): ").strip().lower()
            if confirm == 'y':
                crawler.export_massive_data_safely(export_dir)

    except ValueError as e:
        print(f"❌ {e}")
        print("请确保已设置正确的GitHub Token")
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 安装依赖: pip install requests pandas
    main()