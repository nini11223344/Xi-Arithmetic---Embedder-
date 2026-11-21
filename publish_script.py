#!/usr/bin/env python3
"""
项目发布脚本
支持 GitHub、PyPI 发布
"""

import os
import sys
import subprocess
import json

class ProjectPublisher:
    def __init__(self):
        self.project_name = "Xi-Arithmetic-Embedder"
        self.repo_name = "Xi-Arithmetic-Embedder"
        
    def check_dependencies(self):
        """检查发布工具依赖"""
        import shutil
        
        missing = []
        tools = {'git', 'twine', 'gh', 'yarn'}
        
        for tool in tools:
            if not shutil.which(tool):
                missing.append(tool)
                
        if missing:
            print("❌ 以下工具未安装:")
            for tool in missing:
                print(f"  - {tool}")
            print("\n请使用以下命令安装:")
            print("  pip install twine")
            print("  brew install git  # macOS")
            print("  brew install gh   # GitHub CLI")
            sys.exit(1)
            
    def publish_github(self, token):
        """发布到 GitHub"""
        print("\n" + "="*60)
        print("📦 GitHub 发布")
        print("="*60)
        
        # 获取远程仓库 URL
        try:
            subprocess.check_output(['git', 'remote', '-v'], cwd='.', stderr=subprocess.DEVNULL)
            remote_url = subprocess.check_output(['git', 'config', 'remote.origin.url'], cwd='.', stderr=subprocess.DEVNULL).decode().strip()
        except subprocess.CalledProcessError:
            print("❌ 没有找到远程仓库配置")
            print("请先创建 GitHub 仓库:")
            print("  https://github.com/new")
            print("  或者手动添加远程仓库:")
            print(f"  git remote add origin https://github.com/{os.environ.get('GITHUB_USER', 'yourusername')}/{self.repo_name}.git")
            return False
            
        # 添加并推送
        try:
            subprocess.run(['git', 'add', '.'], cwd='.', check=True)
            subprocess.run(['git', 'commit', '-m', 'Release: v0.1.0'], cwd='.', check=True)
            print("✅ 准备推送")
            
            # 本地测试
            print("\n尝试推送到 GitHub...")
            result = subprocess.run(['git', 'push', 'origin', 'master'], cwd='.', capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 推送到 GitHub 成功!")
                print(f"🌐 仓库地址: {remote_url}")
                return True
            else:
                print("❌ 推送失败:", result.stderr)
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ 命令执行失败: {e}")
            return False
            
    def publish_pypi(self, token):
        """发布到 PyPI"""
        print("\n" + "="*60)
        print("📦 PyPI 发布")
        print("="*60)
        
        # 构建包
        print("🔨 构建项目包...")
        result = subprocess.run(['python', 'setup.py', 'sdist', 'bdist_wheel'], cwd='.', capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ 构建失败:")
            print(result.stderr)
            return False
            
        print("✅ 构建成功")
        
        # 上传
        print("🚀 上传到 PyPI...")
        result = subprocess.run(['twine', 'upload', 'dist/*'], cwd='.', input=token, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 上传到 PyPI 成功!")
            print("🔗 项目地址: https://pypi.org/project/xi-arithmetic-embedder/")
            return True
        else:
            print("❌ 上传失败:")
            print(result.stderr)
            return False
            
    def generate_github_command(self, token):
        """生成 GitHub CLI 命令"""
        commands = []
        
        # 创建仓库
        user = os.environ.get('GITHUB_USER', 'yourusername')
        commands.append(f'gh repo create {user}/{self.repo_name} --public --clone --description="Xi-Arithmetic-Embedder" --no-wait')
        commands.append(f'git remote set-url origin https://{token}@github.com/{user}/{self.repo_name}.git')
        commands.append(f'git push -u origin master')
        
        print("\n" + "="*60)
        print("GitHub 创建与发布命令")
        print("="*60)
        for i, cmd in enumerate(commands, 1):
            print(f"{i}. {cmd}")
            
        return commands

def main():
    """主函数"""
    print(f"🎯 项目发布助手 - {ProjectPublisher().project_name}")
    print("="*60)
    
    publisher = ProjectPublisher()
    publisher.check_dependencies()
    
    # 显示发布选项
    print("\n请选择发布目标:")
    print("1. GitHub 仓库")
    print("2. PyPI")
    print("3. 发布到所有目标")
    print("4. 手动操作指南")
    print("5. 仅生成 GitHub 命令")
    print("0. 退出")
    
    choice = input("\n请输入选择 (0-5): ").strip()
    
    if choice == "0":
        print("❌ 发布已取消")
        return
        
    # GitHub Token 检查
    github_token = os.environ.get('GITHUB_TOKEN')
    pypi_token = os.environ.get('PYPI_TOKEN')
    
    if not github_token:
        print("❌ 未设置 GITHUB_TOKEN")
        print("请设置环境变量:")
        print("  macOS/Linux: export GITHUB_TOKEN='你的GitHub Token'")
        print("  Windows: set GITHUB_TOKEN='你的GitHub Token'")
        
    if not pypi_token:
        print("❌ 未设置 PYPI_TOKEN")
        print("请设置环境变量:")
        print("  macOS/Linux: export PYPI_TOKEN='你的PyPI Token'")
        print("  Windows: set PYPI_TOKEN='你的PyPI Token'")
        
    # 执行发布
    try:
        if choice == "1":
            if github_token:
                publisher.publish_github(github_token)
            else:
                print("❌ 需要 GITHUB_TOKEN 环境变量")
                
        elif choice == "2":
            if pypi_token:
                publisher.publish_pypi(pypi_token)
            else:
                print("❌ 需要 PYPI_TOKEN 环境变量")
                
        elif choice == "3":
            success = True
            if github_token:
                if not publisher.publish_github(github_token):
                    success = False
            else:
                print("⚠️ 缺少 GITHUB_TOKEN，跳过 GitHub 发布")
                
            if pypi_token:
                if not publisher.publish_pypi(pypi_token):
                    success = False
            else:
                print("⚠️ 缺少 PYPI_TOKEN，跳过 PyPI 发布")
                
        elif choice == "4":
            # 显示手动操作指南
            print("\n" + "="*60)
            print("📋 发布操作指南")
            print("="*60)
            
            github_instructions = f"""
# GitHub 发布步骤

1. 创建 GitHub 仓库
    
    # 方式一: 手动创建
    - 访问 https://github.com/new
    - 输入仓库名: {publisher.repo_name}
    - 选择私有或公开
    - 不要初始化 README

    # 方式二: 使用 GitHub CLI
    {user} = os.environ.get('GITHUB_USER', 'yourusername')
    gh repo create {user}/{publisher.repo_name} --public --clone --no-wait
    
2. 配置 Git 远程仓库

    cd {os.path.abspath('.')}
    git remote add origin https://github.com/{user}/{publisher.repo_name}.git
    git branch -M main
    git push -u origin main
    
3. 测试上传

    # 确保有正确的远程仓库
    git remote -v
    
    # 推送
    git push origin main
    
4. 完成

    可以在浏览器中查看你的仓库:
    https://github.com/{user}/{publisher.repo_name}
"""
            print(github_instructions)
            
            pypi_instructions = """
# PyPI 发布步骤

## 1. 获取 PyPI 令牌

- 访问 https://pypi.org/account/
- 点击右上角用户名 > Your API token
- 点击 "Add API token"
- 命名令牌
- 复制生成的令牌

## 2. 安装构建工具

```bash
pip install twine build
```

## 3. 构建包

```bash
python setup.py sdist bdist_wheel
# 或者
python -m build
```

## 4. 发布到 PyPI

```bash
twine upload dist/*
```

## 5. 验证

访问: https://pypi.org/project/xi-arithmetic-embedder/
"""
            print(pypi_instructions)
            
        elif choice == "5":
            # 生成 GitHub 命令
            if github_token:
                commands = publisher.generate_github_command(github_token)
            else:
                print("❌ 需要 GITHUB_TOKEN 环境变量")
        else:
            print("❌ 无效选项")
            
    except KeyboardInterrupt:
        print("\n❌ 操作被中断")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()