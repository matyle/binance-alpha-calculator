#!/usr/bin/env python3
"""
WASM模块打包脚本
将Python计算逻辑打包成可在浏览器中直接使用的模块
"""

import os
import shutil
import json
from pathlib import Path

# 定义路径
PROJECT_ROOT = Path(__file__).parent
DIST_DIR = PROJECT_ROOT / "dist"
WEBPAGE_DIR = DIST_DIR / "webpage"
CALCULATOR_FILE = PROJECT_ROOT / "alpha_calculator.py"

def create_directories():
    """创建必要的目录"""
    print("创建目录结构...")
    WEBPAGE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ 创建目录: {WEBPAGE_DIR}")

def create_python_module():
    """创建Python模块文件"""
    print("创建Python模块...")
    
    # 复制计算模块
    module_file = WEBPAGE_DIR / "alpha_calculator.py"
    shutil.copy2(CALCULATOR_FILE, module_file)
    print(f"✓ 复制计算模块: {module_file}")
    
    # 创建初始化文件
    init_file = WEBPAGE_DIR / "__init__.py"
    init_file.write_text("# Alpha Calculator Module\n")
    print(f"✓ 创建初始化文件: {init_file}")

def create_setup_py():
    """创建setup.py文件用于打包"""
    setup_content = '''from setuptools import setup, find_packages

setup(
    name="alpha-calculator",
    version="1.0.0",
    description="Alpha Profit Calculator Core Module",
    packages=find_packages(),
    python_requires=">=3.7",
)
'''
    
    setup_file = WEBPAGE_DIR / "setup.py"
    setup_file.write_text(setup_content)
    print(f"✓ 创建setup.py: {setup_file}")

def create_manifest():
    """创建manifest.json文件"""
    manifest = {
        "name": "alpha-calculator",
        "version": "1.0.0",
        "description": "Alpha Profit Calculator Core Module",
        "main": "alpha_calculator.py",
        "functions": [
            "calculate_profit",
            "calculate_auto_fields",
            "validate_inputs"
        ]
    }
    
    manifest_file = WEBPAGE_DIR / "manifest.json"
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"✓ 创建manifest.json: {manifest_file}")

def create_optimized_html():
    """创建优化的HTML文件"""
    html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alpha 月度利润计算器</title>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            width: 100%;
            max-width: 500px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .title {
            color: #2c3e50;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .subtitle {
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 10px;
        }

        .loading {
            color: #3498db;
            font-size: 12px;
            font-style: italic;
        }

        .input-section {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .input-group {
            margin-bottom: 15px;
        }

        .input-group:last-child {
            margin-bottom: 0;
        }

        .input-label {
            display: block;
            color: #34495e;
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 5px;
        }

        .input-field {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 14px;
            background: white;
            transition: border-color 0.3s;
        }

        .input-field:focus {
            outline: none;
            border-color: #3498db;
        }

        .auto-fields {
            display: grid;
            gap: 10px;
            margin-bottom: 20px;
        }

        .auto-field {
            background: #e8f4f8;
            padding: 12px 16px;
            border-radius: 10px;
            color: #2c3e50;
            font-size: 14px;
        }

        .result-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            text-align: center;
            color: white;
        }

        .result-value {
            font-size: 24px;
            font-weight: 700;
        }

        .calculate-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
            margin-bottom: 20px;
        }

        .calculate-btn:hover {
            transform: translateY(-2px);
        }

        .calculate-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .footer {
            text-align: center;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
        }

        .footer-link {
            color: #3498db;
            text-decoration: none;
            margin: 0 10px;
        }

        .message {
            padding: 10px 15px;
            border-radius: 8px;
            margin: 10px 0;
            font-size: 14px;
        }

        .message.error {
            background: #fee;
            color: #c62828;
            border: 1px solid #fdd;
        }

        .message.success {
            background: #efffef;
            color: #2e7d32;
            border: 1px solid #c8e6c9;
        }

        @media (max-width: 600px) {
            .container {
                padding: 20px;
                margin: 10px;
            }
            .title {
                font-size: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">Alpha 月度利润计算器</h1>
            <p class="subtitle">基于积分与余额自动计算月利润</p>
            <p class="loading" id="loadingText">正在初始化计算模块...</p>
        </div>

        <div class="input-section">
                         <div class="input-group">
                 <label class="input-label" for="ntl">Ntl（日交易量档位，范围：0-50）</label>
                 <input type="number" id="ntl" class="input-field" step="0.1" min="0" max="50" oninput="updateAutoFields()">
             </div>
 
             <div class="input-group">
                 <label class="input-label" for="pb">Pb（余额积分，范围：0-15）</label>
                 <input type="number" id="pb" class="input-field" step="0.1" min="0" max="15" oninput="updateAutoFields()">
             </div>
 
             <div class="input-group">
                 <label class="input-label" for="talpha">门槛（Tα，默认200分，范围：0-10000）</label>
                 <input type="number" id="talpha" class="input-field" value="200" step="1" min="0" max="10000">
             </div>
 
             <div class="input-group">
                 <label class="input-label" for="ipdw">Ipdw（每次领取预期收益，范围：0-100000）</label>
                 <input type="number" id="ipdw" class="input-field" value="100" step="1" min="0" max="100000">
             </div>
 
             <div class="input-group">
                 <label class="input-label" for="rdur">Rdur（交易损耗率，范围：0-1）</label>
                 <input type="number" id="rdur" class="input-field" value="0.0002" step="0.0001" min="0" max="1">
             </div>
        </div>

        <div class="auto-fields">
            <div class="auto-field" id="vactual">Vactual（真实交易量）：-</div>
            <div class="auto-field" id="nbal">Nbal（余额档位）：-</div>
            <div class="auto-field" id="balance">余额（USD）：-</div>
        </div>

        <div class="result-section">
            <div class="result-value" id="resultValue">月利润：-</div>
        </div>

        <button class="calculate-btn" onclick="calculateProfit()" id="calculateBtn" disabled>
            计算
        </button>

        <div id="messageArea"></div>

        <div class="footer">
            <a href="https://x.com/tan_maty" class="footer-link" target="_blank">X: @tan_maty</a>
            <a href="https://github.com/matyle" class="footer-link" target="_blank">GitHub: matyle</a>
        </div>
    </div>

    <script>
        let pyodide;
        let calculator;

        async function initializePyodide() {
            try {
                // 加载Pyodide
                pyodide = await loadPyodide();
                
                // 直接执行计算模块代码
                const calculatorCode = await fetch('./alpha_calculator.py').then(r => r.text());
                pyodide.runPython(calculatorCode);
                
                // 获取计算函数
                calculator = {
                    calculate_profit: pyodide.globals.get('calculate_profit'),
                    calculate_auto_fields: pyodide.globals.get('calculate_auto_fields'),
                    validate_inputs: pyodide.globals.get('validate_inputs')
                };
                
                // 更新UI状态
                document.getElementById('loadingText').style.display = 'none';
                document.getElementById('calculateBtn').disabled = false;
                
                showMessage('计算模块已加载完成！', 'success');
                
            } catch (error) {
                console.error('初始化失败:', error);
                showMessage('初始化失败：' + error.message, 'error');
            }
        }

                 function updateAutoFields() {
             if (!calculator) return;
             
             const ntl = document.getElementById('ntl').value;
             const pb = document.getElementById('pb').value;
             
             if (!ntl || !pb) {
                 document.getElementById('vactual').textContent = 'Vactual（真实交易量）：-';
                 document.getElementById('nbal').textContent = 'Nbal（余额档位）：-';
                 document.getElementById('balance').textContent = '余额（USD）：-';
                 return;
             }

             try {
                 const result = calculator.calculate_auto_fields(parseFloat(ntl), parseFloat(pb));
                 const [vactual, nbal, balance] = result.toJs();
                 
                 document.getElementById('vactual').textContent = `Vactual（真实交易量）：${vactual.toFixed(2)}`;
                 document.getElementById('nbal').textContent = `Nbal（余额档位）：${nbal.toFixed(0)}`;
                 document.getElementById('balance').textContent = `余额（USD）：${balance.toFixed(0)}`;
             } catch (error) {
                 console.error('更新自动字段失败:', error);
                 
                 // 显示错误信息
                 let errorMessage = '计算错误';
                 if (error.message && error.message.includes('ValueError')) {
                     const match = error.message.match(/ValueError: (.+)/);
                     if (match) {
                         errorMessage = match[1];
                     }
                 }
                 
                 document.getElementById('vactual').textContent = 'Vactual（真实交易量）：错误';
                 document.getElementById('nbal').textContent = 'Nbal（余额档位）：错误';
                 document.getElementById('balance').textContent = '余额（USD）：错误';
                 
                 showMessage(errorMessage, 'error');
             }
         }

                 function calculateProfit() {
             if (!calculator) {
                 showMessage('计算模块未加载完成', 'error');
                 return;
             }

             const ntl = document.getElementById('ntl').value;
             const pb = document.getElementById('pb').value;
             const talpha = document.getElementById('talpha').value || 200;
             const ipdw = document.getElementById('ipdw').value || 100;
             const rdur = document.getElementById('rdur').value || 0.0002;

             if (!ntl || !pb) {
                 showMessage('请输入必要的参数：Ntl 和 Pb', 'error');
                 return;
             }

             try {
                 const result = calculator.calculate_profit(
                     parseFloat(ntl), 
                     parseFloat(pb), 
                     parseFloat(talpha), 
                     parseFloat(ipdw), 
                     parseFloat(rdur)
                 );
                 
                 const [profit, vactual, nbal, balance] = result.toJs();
                 
                 document.getElementById('resultValue').textContent = `月利润：${profit.toFixed(2)} USD`;
                 document.getElementById('vactual').textContent = `Vactual（真实交易量）：${vactual.toFixed(2)}`;
                 document.getElementById('nbal').textContent = `Nbal（余额档位）：${nbal.toFixed(0)}`;
                 document.getElementById('balance').textContent = `余额（USD）：${balance.toFixed(0)}`;
                 
                 showMessage('计算完成！', 'success');
                 
             } catch (error) {
                 console.error('计算失败:', error);
                 
                 // 解析错误信息
                 let errorMessage = '计算失败';
                 if (error.message && error.message.includes('ValueError')) {
                     const match = error.message.match(/ValueError: (.+)/);
                     if (match) {
                         errorMessage = match[1];
                     }
                 } else if (error.message) {
                     errorMessage = error.message;
                 }
                 
                 showMessage(errorMessage, 'error');
             }
         }

        function showMessage(message, type) {
            const messageArea = document.getElementById('messageArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            messageDiv.textContent = message;
            
            messageArea.innerHTML = '';
            messageArea.appendChild(messageDiv);
            
            setTimeout(() => {
                messageDiv.remove();
            }, 3000);
        }

        // 页面加载时初始化
        window.addEventListener('load', initializePyodide);
    </script>
</body>
</html>'''
    
    html_file = WEBPAGE_DIR / "index.html"
    html_file.write_text(html_content, encoding='utf-8')
    print(f"✓ 创建优化的HTML文件: {html_file}")

def create_github_pages_config():
    """创建GitHub Pages配置文件"""
    # 创建.nojekyll文件
    nojekyll_file = WEBPAGE_DIR / ".nojekyll"
    nojekyll_file.write_text("")
    print(f"✓ 创建.nojekyll文件: {nojekyll_file}")

def create_deployment_readme():
    """创建部署说明文档"""
    readme_content = '''# Alpha 月度利润计算器 - 网页版

## 部署到 GitHub Pages

### 方法1: 直接上传到GitHub仓库
1. 将此目录下的所有文件上传到GitHub仓库的根目录
2. 在仓库设置中启用GitHub Pages
3. 选择从主分支部署

### 方法2: 使用GitHub Actions自动部署
创建`.github/workflows/deploy.yml`文件：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    
    - name: Build web version
      run: python build_wasm.py
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./dist/webpage
```

## 功能特点

- 🌐 **纯网页版**: 无需安装，直接在浏览器中运行
- 🐍 **WASM驱动**: 使用Pyodide将Python代码编译为WebAssembly
- 📱 **响应式设计**: 支持桌面和移动设备
- 🚀 **快速加载**: 优化的模块加载机制
- 🔧 **完整功能**: 与桌面版完全相同的计算逻辑

## 技术栈

- **前端**: HTML5, CSS3, JavaScript
- **计算引擎**: Python + Pyodide (WebAssembly)
- **部署**: GitHub Pages

## 使用说明

1. 输入日交易量档位（Ntl）和余额积分（Pb）
2. 调整其他参数（可选）
3. 点击"计算"按钮获取结果
4. 系统会自动计算真实交易量、余额档位和月利润

## 注意事项

- 首次访问需要加载Pyodide运行环境（约5MB）
- 建议使用现代浏览器（Chrome, Firefox, Safari, Edge）
- 需要网络连接来加载必要的资源

## 开发者

- X: [@tan_maty](https://x.com/tan_maty)
- GitHub: [matyle](https://github.com/matyle)
'''
    
    readme_file = WEBPAGE_DIR / "README.md"
    readme_file.write_text(readme_content, encoding='utf-8')
    print(f"✓ 创建部署说明: {readme_file}")

def main():
    """主函数"""
    print("🚀 开始构建WASM版本的Alpha计算器...")
    print("=" * 50)
    
    # 创建目录结构
    create_directories()
    
    # 创建Python模块
    create_python_module()
    
    # 创建打包配置
    create_setup_py()
    create_manifest()
    
    # 创建优化的HTML
    create_optimized_html()
    
    # 创建GitHub Pages配置
    create_github_pages_config()
    
    # 创建部署说明
    create_deployment_readme()
    
    print("=" * 50)
    print("✅ WASM版本构建完成！")
    print(f"📁 输出目录: {WEBPAGE_DIR}")
    print("\n🎯 部署到GitHub Pages:")
    print("1. 将dist/webpage目录下的所有文件上传到GitHub仓库")
    print("2. 在仓库设置中启用GitHub Pages")
    print("3. 选择从主分支部署")
    print("\n🌐 本地测试:")
    print(f"   cd {WEBPAGE_DIR}")
    print("   python -m http.server 8000")
    print("   然后访问 http://localhost:8000")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 