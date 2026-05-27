#!/usr/bin/env python3
"""
清理 Obsidian vault 里的圈字母/圈数字 unicode 字符。

把 AI 生成内容里常见的装饰符号还原成普通 ASCII：
  Ⓐ Ⓑ Ⓒ ... Ⓩ  → A B C ... Z
  ⓐ ⓑ ⓒ ... ⓩ  → a b c ... z
  ① ② ③ ... ⑳   → 1 2 3 ... 20
  ⓪              → 0
  ❶ ❷ ❸ ... ❿   → 1 2 3 ... 10 (negative circled)
  ➀ ➁ ➂ ... ➉   → 1 2 3 ... 10 (sans-serif)
  ➊ ➋ ➌ ... ➓   → 1 2 3 ... 10 (negative sans-serif)
  ㉑ ㉒ ... ㊿    → 21 22 ... 50
  ⊕ ⊖ ⊗ ⊘ ⊙    → + - * / .

中文、中文标点、普通 emoji 不动。

用法：
  # 试运行（不改文件，只打印会改什么）
  python3 clean-circled-chars.py --dry-run /path/to/vault

  # 实际清理
  python3 clean-circled-chars.py /path/to/vault

  # 清理单个文件
  python3 clean-circled-chars.py /path/to/note.md
"""
import argparse
import os
import sys
from pathlib import Path


def build_translation_table():
    """构建 unicode 翻译表：圈字符 → 普通字符。"""
    m = {}

    # 圈数字 ① - ⑳ → 1 - 20
    for i in range(20):
        m[chr(0x2460 + i)] = str(i + 1)
    # 圈零 ⓪ → 0
    m[chr(0x24EA)] = '0'

    # 圈数字 21-35 (㉑-㉟)
    for i in range(15):
        m[chr(0x3251 + i)] = str(i + 21)
    # 圈数字 36-50 (㊱-㊿)
    for i in range(15):
        m[chr(0x3280 + i)] = str(i + 36)

    # 圈大写字母 Ⓐ - Ⓩ → A - Z
    for i in range(26):
        m[chr(0x24B6 + i)] = chr(0x41 + i)
    # 圈小写字母 ⓐ - ⓩ → a - z
    for i in range(26):
        m[chr(0x24D0 + i)] = chr(0x61 + i)

    # 黑底白字圈数字 ❶ - ❿ → 1 - 10
    for i in range(10):
        m[chr(0x2776 + i)] = str(i + 1)
    # Sans-serif 圈数字 ➀ - ➉ → 1 - 10
    for i in range(10):
        m[chr(0x2780 + i)] = str(i + 1)
    # 黑底 sans-serif 圈数字 ➊ - ➓ → 1 - 10
    for i in range(10):
        m[chr(0x278A + i)] = str(i + 1)

    # Negative circled Latin (🅐-🅩, U+1F150-U+1F169) → A-Z
    for i in range(26):
        m[chr(0x1F150 + i)] = chr(0x41 + i)
    # Negative squared Latin (🅰-🆉, U+1F170-U+1F189) → A-Z
    for i in range(26):
        m[chr(0x1F170 + i)] = chr(0x41 + i)

    # 圈运算符
    m['⊕'] = '+'
    m['⊖'] = '-'
    m['⊗'] = '*'
    m['⊘'] = '/'
    m['⊙'] = '.'
    # 圈百分号、加号等其它常见
    m['⊞'] = '+'

    return str.maketrans(m)


TABLE = build_translation_table()


def clean_text(text: str) -> str:
    return text.translate(TABLE)


def process_file(path: Path, dry_run: bool) -> bool:
    """处理单个 .md 文件。返回是否有改动。"""
    try:
        original = path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, PermissionError) as e:
        print(f'  跳过 {path}: {e}', file=sys.stderr)
        return False

    cleaned = clean_text(original)
    if cleaned == original:
        return False

    # 统计改了多少字符
    diff_count = sum(1 for a, b in zip(original, cleaned) if a != b)
    diff_count += abs(len(original) - len(cleaned))

    if dry_run:
        print(f'  [dry-run] 会修改 {path} ({diff_count} 处)')
    else:
        path.write_text(cleaned, encoding='utf-8')
        print(f'  清理 {path} ({diff_count} 处)')
    return True


def walk_and_clean(target: Path, dry_run: bool):
    if target.is_file():
        files = [target]
    else:
        files = sorted(target.rglob('*.md'))

    print(f'扫描 {len(files)} 个 .md 文件…\n')

    changed = 0
    for f in files:
        # 跳过 .obsidian、.trash、.git 等隐藏目录
        if any(part.startswith('.') for part in f.parts):
            continue
        if process_file(f, dry_run):
            changed += 1

    print()
    if dry_run:
        print(f'[dry-run] {changed} 个文件会被修改（未实际写入）')
    else:
        print(f'已清理 {changed} 个文件')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('target', type=Path, help='vault 目录或单个 .md 文件路径')
    p.add_argument('--dry-run', action='store_true', help='只打印会改什么，不实际写入')
    args = p.parse_args()

    if not args.target.exists():
        print(f'路径不存在: {args.target}', file=sys.stderr)
        sys.exit(1)

    walk_and_clean(args.target, args.dry_run)


if __name__ == '__main__':
    main()
