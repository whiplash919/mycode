# Obsidian Vault 清理脚本

## clean-circled-chars.py — 清除圈字母/圈数字

把 AI 生成内容里常见的装饰 unicode 字符还原成普通字符：

| 原字符 | 清理后 |
|---|---|
| `Ⓐ Ⓑ ... Ⓩ` | `A B ... Z` |
| `ⓐ ⓑ ... ⓩ` | `a b ... z` |
| `① ② ... ⑳` | `1 2 ... 20` |
| `⓪` | `0` |
| `❶-❿  ➀-➉  ➊-➓` | `1-10` |
| `㉑-㊿` | `21-50` |
| `🅐-🅩  🅰-🆉` | `A-Z` |
| `⊕ ⊖ ⊗ ⊘ ⊙` | `+ - * / .` |

**不动**：中文、中文标点、普通 emoji、英文、标准 ASCII。

### 使用步骤

```bash
# 1. clone 或下载本仓库到本地
git clone https://github.com/whiplash919/mycode.git
cd mycode/obsidian/scripts

# 2. 先 dry-run，看会改哪些文件（不实际写入）
python3 clean-circled-chars.py --dry-run /path/to/your/obsidian/vault

# 3. 确认无误后实际清理
python3 clean-circled-chars.py /path/to/your/obsidian/vault

# 或只清理单个文件
python3 clean-circled-chars.py /path/to/note.md
```

### 安全说明

- **强烈建议先 `--dry-run`**，确认要改的文件清单
- **建议先备份 vault 或先 commit 一遍**（如果 vault 在 git 里）：
  ```bash
  cd /path/to/your/vault
  git add -A && git commit -m "before circled-chars cleanup"
  ```
- 脚本会跳过 `.obsidian/`、`.trash/`、`.git/` 等隐藏目录
- 脚本**只动**上表列出的字符，不会改动其它任何字节

### 为什么会有这些字符

某些 AI（特别是早期模型或某些前端渲染器）生成内容时，会把英文字母和数字"美化"成圈字符作为装饰。这些字符：

- **看起来像加粗或大号字**——但实际是不同的 unicode 码位
- **不能被搜索匹配**——搜 "ARM" 找不到 "ⒶⓇⓂ"
- **不能被 Dataview 索引**——`Ⓟ/Ⓔ` 不是 `P/E`
- **复制粘贴时会保留**——污染从一个文档传播到另一个

这就是为什么必须批量清理。

### 预防

捕获外部内容到 INBOX 时养成习惯：
1. 粘贴后立即跑一遍 `clean-circled-chars.py` 处理 INBOX
2. 或者在系统级输入法/剪贴板工具里设规则自动转换

如果你的 INBOX 文件夹路径固定，可以设个 cron 或 fswatch 自动跑：

```bash
# 每小时清理 INBOX
0 * * * * python3 /path/to/clean-circled-chars.py /path/to/vault/00\ -\ INBOX/
```
