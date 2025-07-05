# Alpha 月度利润计算器 - 网页版

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
