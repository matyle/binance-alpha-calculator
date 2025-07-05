import tkinter as tk
from tkinter import messagebox
import webbrowser
from alpha_calculator import calculate_profit, calculate_auto_fields

# macOS 风格配色
BG_COLOR = "#ececec"  # 浅灰底
FRAME_BG = "#f7f7f7"  # 更浅的灰色
TITLE_COLOR = "#222222"  # 深色标题
LABEL_COLOR = "#333333"  # 深色标签
RESULT_COLOR = "#007aff"  # mac 蓝色
BUTTON_BG = "#f0f0f0"  # mac 按钮灰
BUTTON_FG = "#222222"
BUTTON_ACTIVE_BG = "#e1e1e1"
SEPARATOR_COLOR = "#d1d1d1"
LINK_X_COLOR = "#007aff"
LINK_GITHUB_COLOR = "#24292f"

class AlphaProfitCalculatorTk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alpha 月度利润计算器")
        self.configure(bg=BG_COLOR)
        self.minsize(520, 600)
        self.create_widgets()

    def create_widgets(self):
        # 标题
        title = tk.Label(self, text="Alpha 月度利润计算器", font=("Helvetica Neue", 20, "bold"), fg=TITLE_COLOR, bg=BG_COLOR)
        title.pack(pady=(18, 6), fill='x')
        subtitle = tk.Label(self, text="基于积分与余额自动计算月利润", font=("Helvetica Neue", 12), fg=LABEL_COLOR, bg=BG_COLOR)
        subtitle.pack(pady=(0, 10), fill='x')

        # 输入区 Frame
        input_frame = tk.LabelFrame(self, text="参数输入", font=("Helvetica Neue", 12, "bold"), fg=TITLE_COLOR, bg=FRAME_BG, bd=1, relief=tk.GROOVE, padx=16, pady=10, labelanchor='n')
        input_frame.pack(padx=18, pady=(0, 10), fill="x")
        self.entries = {}
        params = [
            ("Ntl（日交易量档位）", "Ntl", ""),
            ("Pb（余额积分）", "Pb", ""),
            ("门槛（Tα，默认200分）", "T_alpha", "200"),
            ("Ipdw（每次领取预期收益）", "Ipdw", "100"),
            ("Rdur（交易损耗率）", "Rdur", "0.0002"),
        ]
        input_frame.columnconfigure(1, weight=1)
        for idx, (label_text, key, default) in enumerate(params):
            label = tk.Label(input_frame, text=label_text, font=("Helvetica Neue", 11), bg=FRAME_BG, fg=LABEL_COLOR)
            label.grid(row=idx, column=0, padx=6, pady=8, sticky='e')
            entry = tk.Entry(input_frame, font=("Helvetica Neue", 11), width=16, relief=tk.FLAT, bd=2, bg="white", fg=LABEL_COLOR, insertbackground=LABEL_COLOR)
            entry.grid(row=idx, column=1, padx=6, pady=8, sticky='ew')
            if default:
                entry.insert(0, default)
            self.entries[key] = entry

        # 固定参数和自动计算区
        auto_frame = tk.Frame(self, bg=BG_COLOR)
        auto_frame.pack(padx=18, pady=(0, 10), fill="x")
        for i in range(4):
            auto_frame.grid_columnconfigure(i, weight=1)
        self.vactual_var = tk.StringVar()
        self.vactual_var.set("Vactual（真实交易量）：-")
        self.vactual_label = tk.Label(auto_frame, textvariable=self.vactual_var, font=("Helvetica Neue", 11), bg=BG_COLOR, fg=LABEL_COLOR)
        self.vactual_label.grid(row=1, column=0, sticky='w', pady=2)
        self.nbal_var = tk.StringVar()
        self.nbal_var.set("Nbal（余额档位）：-")
        self.nbal_label = tk.Label(auto_frame, textvariable=self.nbal_var, font=("Helvetica Neue", 11), bg=BG_COLOR, fg=LABEL_COLOR)
        self.nbal_label.grid(row=2, column=0, sticky='w', pady=2)
        self.balance_var = tk.StringVar()
        self.balance_var.set("余额（USD）：-")
        self.balance_label = tk.Label(auto_frame, textvariable=self.balance_var, font=("Helvetica Neue", 11), bg=BG_COLOR, fg=LABEL_COLOR)
        self.balance_label.grid(row=3, column=0, sticky='w', pady=2)

        # 分割线
        sep = tk.Frame(self, height=2, bd=0, bg=SEPARATOR_COLOR)
        sep.pack(fill="x", padx=18, pady=8)

        # 结果区 Frame
        result_frame = tk.LabelFrame(self, text="计算结果", font=("Helvetica Neue", 12, "bold"), fg=TITLE_COLOR, bg=FRAME_BG, bd=1, relief=tk.GROOVE, padx=16, pady=16, labelanchor='n')
        result_frame.pack(padx=18, pady=(0, 18), fill="x")
        self.result_var = tk.StringVar()
        self.result_var.set("月利润：")
        result_label = tk.Label(result_frame, textvariable=self.result_var, font=("Helvetica Neue", 16, "bold"), fg=RESULT_COLOR, bg=FRAME_BG)
        result_label.pack(pady=8, fill='x')

        # 计算按钮
        calc_btn = tk.Button(
            self, text="计 算",
            font=("Helvetica Neue", 13, "bold"),
            bg=BUTTON_BG, fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_FG,
            command=self.on_calculate, relief=tk.RAISED, bd=1, height=2, width=12,
            highlightbackground=SEPARATOR_COLOR
        )
        calc_btn.pack(pady=(0, 16), fill='x', padx=80)

        # Ntl、Pb 输入时自动更新 Vactual、Nbal、余额
        self.entries["Ntl"].bind('<KeyRelease>', self.update_auto_fields)
        self.entries["Pb"].bind('<KeyRelease>', self.update_auto_fields)

        # 作者链接区
        link_frame = tk.Frame(self, bg=BG_COLOR)
        link_frame.pack(side="bottom", pady=(0, 16), fill='x')
        x_link = tk.Label(link_frame, text="X: @tan_maty", font=("Helvetica Neue", 10, "underline"), fg=LINK_X_COLOR, bg=BG_COLOR, cursor="hand2")
        x_link.pack(side="left", padx=10)
        x_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://x.com/tan_maty"))
        github_link = tk.Label(link_frame, text="GitHub: matyle", font=("Helvetica Neue", 10, "underline"), fg=LINK_GITHUB_COLOR, bg=BG_COLOR, cursor="hand2")
        github_link.pack(side="left", padx=10)
        github_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/matyle"))

    def update_auto_fields(self, event=None):
        try:
            Ntl = float(self.entries["Ntl"].get())
            Pb = float(self.entries["Pb"].get())
            Vactual, Nbal, balance = calculate_auto_fields(Ntl, Pb)
            self.vactual_var.set(f"Vactual（真实交易量）：{Vactual:.2f}")
            self.nbal_var.set(f"Nbal（余额档位）：{Nbal:.0f}")
            self.balance_var.set(f"余额（USD）：{balance:.0f}")
        except ValueError as e:
            self.vactual_var.set("Vactual（真实交易量）：错误")
            self.nbal_var.set("Nbal（余额档位）：错误")
            self.balance_var.set("余额（USD）：错误")
        except Exception:
            self.vactual_var.set("Vactual（真实交易量）：-")
            self.nbal_var.set("Nbal（余额档位）：-")
            self.balance_var.set("余额（USD）：-")

    def on_calculate(self):
        try:
            Ntl = float(self.entries["Ntl"].get())
            Pb = float(self.entries["Pb"].get())
            T_alpha = float(self.entries["T_alpha"].get()) if self.entries["T_alpha"].get() else 200
            Ipdw = float(self.entries["Ipdw"].get()) if self.entries["Ipdw"].get() else 100
            Rdur = float(self.entries["Rdur"].get()) if self.entries["Rdur"].get() else 0.0002
            profit, Vactual, Nbal, balance = calculate_profit(Ntl, Pb, T_alpha, Ipdw, Rdur)
            self.result_var.set(f"月利润：{profit:.2f} USD")
            self.vactual_var.set(f"Vactual（真实交易量）：{Vactual:.2f}")
            self.nbal_var.set(f"Nbal（余额档位）：{Nbal:.0f}")
            self.balance_var.set(f"余额（USD）：{balance:.0f}")
        except ValueError as e:
            messagebox.showwarning("输入错误", str(e))
        except Exception as e:
            messagebox.showwarning("输入错误", f"请检查输入：{e}")

if __name__ == "__main__":
    app = AlphaProfitCalculatorTk()
    app.mainloop() 