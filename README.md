# Alpha 月度利润计算器

## 简介

图形化 Alpha 月度利润计算器，支持 macOS 和 Windows 平台。界面美观，参数灵活，适合积分、余额、过期积分等多种场景的月度利润测算。
![image.png|200](https://pub-c7c3a09e8d7b4cd3bff5014134cfa3a0.r2.dev/20250602112602.png)
## 功能
- 支持输入日交易量档位、余额积分、每次领取预期收益、交易损耗率等参数
- 支持 15 天内积分滚动过期和领取扣除逻辑
- 自动计算真实交易量、余额档位、余额金额
- 结果一键显示，界面自适应，支持深色/浅色 mac 风格
- 支持 X（推特）和 GitHub 主页跳转
- **🌐 网页版**: 支持在浏览器中直接使用，无需安装
- **🔒 输入验证**: 防止数值溢出，提供友好的错误提示
- **📱 响应式设计**: 网页版支持桌面和移动设备

## 运行方法

### 桌面版（Tkinter）

1. 安装 Python 3（推荐 3.8 及以上，需自带 Tkinter）
2. 进入项目目录，运行：

```bash
python alpha_profit_calculator_tkinter.py
```

无需额外依赖。

### 网页版

1. 构建网页版：

```bash
python build_wasm.py
```

2. 部署到GitHub Pages：

将 `dist/webpage` 目录下的所有文件上传到GitHub仓库，然后在仓库设置中启用GitHub Pages。

3. 本地测试（可选）：

```bash
cd dist/webpage
python -m http.server 8000
```

然后在浏览器中打开 `http://localhost:8000`

## 打包为可执行文件

### macOS

```bash
pip install pyinstaller
pyinstaller --onefile --windowed alpha_profit_calculator_tkinter.py
```

生成的可执行文件在 `dist/` 目录下。

### Windows

请在 Windows 环境下运行：

```bash
pip install pyinstaller
pyinstaller --onefile --windowed alpha_profit_calculator_tkinter.py
```

### 跨平台自动打包（GitHub Actions）

本项目支持 GitHub Actions 自动打包 Windows 版本。参考 `.github/workflows/build-windows.yml`，推送到 main 分支或手动触发即可自动生成 Windows EXE 并下载。

## 网页版特点

- 🌐 **纯网页版**: 无需安装，直接在浏览器中运行
- 🐍 **WASM驱动**: 使用Pyodide将Python代码编译为WebAssembly运行
- 📱 **响应式设计**: 支持桌面和移动设备
- 🎨 **现代化UI**: 美观的渐变背景和流畅的交互动画
- ⚡ **实时计算**: 输入参数时自动更新相关字段
- 🔧 **完全功能**: 与桌面版完全相同的计算逻辑
- 🚀 **GitHub Pages**: 可直接部署到GitHub Pages，无需服务器

### 网页版注意事项

1. **首次加载**: 第一次打开页面时需要下载Pyodide运行环境（约5MB），请耐心等待
2. **网络要求**: 需要网络连接来加载Pyodide，建议在稳定的网络环境下使用
3. **浏览器兼容**: 支持现代浏览器（Chrome, Firefox, Safari, Edge）
4. **GitHub Pages**: 适合部署到GitHub Pages，支持自定义域名

## 主要参数说明
- **Ntl（日交易量档位）**：入账交易量 2^N USD 得 N 分（范围：0-50）
- **Pb（余额积分）**：余额积分，10^N USD 余额得 N-1 分（范围：0-15）
- **Ipdw（每次领取预期收益）**：每次领取的预期收益，默认 100（范围：0-100000）
- **Rdur（交易损耗率）**：默认 0.0002（范围：0-1）
- **T_alpha（门槛）**：默认 200 分（范围：0-10000）

### 输入限制说明
为了防止数值溢出和确保计算精度，系统对所有输入参数都设置了合理的范围限制：
- 当输入超出范围时，会显示友好的错误提示
- 桌面版和网页版都进行了相同的验证
- 这些限制基于实际使用场景设定，满足绝大多数用户需求

## 联系作者
- X: [@tan_maty](https://x.com/tan_maty)
- GitHub: [matyle](https://github.com/matyle)

---

如有建议或需求，欢迎 issue 或 PR！ 