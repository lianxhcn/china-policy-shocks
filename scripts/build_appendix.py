# -*- coding: utf-8 -*-
"""
从 Excel 政策冲击库自动生成 CSV 和 Markdown 附录。

日常维护方式：
    只修改 data/policy_shock_library_v0_1.xlsx

自动生成：
    data/policy_shock_library_v0_1.csv
    appendix_policy_list.md
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


# =========================
# 1. 路径设置
# =========================

ROOT = Path(__file__).resolve().parents[1]

XLSX_PATH = ROOT / "data" / "policy_shock_library_v0_1.xlsx"
CSV_PATH = ROOT / "data" / "policy_shock_library_v0_1.csv"
OUT_MD_PATH = ROOT / "appendix_policy_list.md"

PREFERRED_SHEET = "Policy_Shocks_v0.1"


# =========================
# 2. 字段别名
# =========================

COLUMN_ALIASES: Dict[str, List[str]] = {
    "policy_name": ["政策名称", "policy_name", "Policy Name", "name"],
    "domain": ["领域", "所属领域", "研究领域", "domain", "Domain"],
    "year": ["年份", "政策年份", "year", "Year"],
    "policy_object": ["政策对象", "policy_object", "Policy Object"],
    "treatment_group": ["处理组定义", "处理组", "treatment_group", "Treatment Group"],
    "control_group": ["对照组定义", "对照组", "control_group", "Control Group"],
    "shock_time": ["冲击时间", "实施时间", "政策冲击时间", "shock_time", "Shock Time"],
    "merge_key": ["数据合并键", "合并键", "merge_key", "Merge Key"],
    "method": ["推荐方法", "识别方法", "method", "Method"],
    "identification_risk": ["识别风险类型", "识别风险", "identification_risk", "Identification Risk"],
    "data_source": ["数据源", "可用数据源", "data_source", "Data Source"],
    "rating": ["推荐等级", "rating", "Rating"],
    "official_source": ["官方来源 URL", "官方来源", "official_source", "Official Source"],
    "notes": ["备注", "notes", "Notes"],
}


FIELD_LABELS: Dict[str, str] = {
    "year": "年份",
    "rating": "推荐等级",
    "policy_object": "政策对象",
    "treatment_group": "处理组",
    "control_group": "对照组",
    "shock_time": "冲击时间",
    "merge_key": "合并键",
    "method": "推荐方法",
    "identification_risk": "识别风险",
    "data_source": "数据源",
    "notes": "备注",
}


SHOW_FIELDS: List[str] = [
    "year",
    "rating",
    "policy_object",
    "treatment_group",
    "control_group",
    "shock_time",
    "merge_key",
    "method",
    "identification_risk",
    "data_source",
    "notes",
]


DOMAIN_ORDER: List[str] = [
    "国际贸易与对外开放",
    "金融市场与公司治理",
    "银行、影子银行与金融监管",
    "财税政策与政府激励",
    "绿色低碳与环境治理",
    "数字经济、数据与平台治理",
    "产业政策与创新政策",
    "城市、土地与房地产政策",
    "民生、劳动、教育与医疗",
]


# =========================
# 3. 工具函数
# =========================

def read_policy_excel(path: Path) -> pd.DataFrame:
    """读取政策冲击库 Excel。优先读取指定 sheet，失败则读取第一个 sheet。"""
    if not path.exists():
        raise FileNotFoundError(f"找不到 Excel 文件：{path}")

    xls = pd.ExcelFile(path)

    if PREFERRED_SHEET in xls.sheet_names:
        sheet_name = PREFERRED_SHEET
    else:
        sheet_name = xls.sheet_names[0]

    return pd.read_excel(path, sheet_name=sheet_name)


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """清理列名中的空格和换行。"""
    df = df.copy()
    df.columns = [str(c).strip().replace("\n", " ") for c in df.columns]
    return df


def find_column(df: pd.DataFrame, aliases: List[str]) -> Optional[str]:
    """根据别名列表寻找实际列名。"""
    existing = set(df.columns)

    for name in aliases:
        if name in existing:
            return name

    lower_map = {str(c).strip().lower(): c for c in df.columns}
    for name in aliases:
        key = name.strip().lower()
        if key in lower_map:
            return lower_map[key]

    return None


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """把 Excel 中的各种列名统一为脚本内部字段名。"""
    df = clean_columns(df)

    normalized = pd.DataFrame()

    for internal_name, aliases in COLUMN_ALIASES.items():
        actual_col = find_column(df, aliases)
        if actual_col is not None:
            normalized[internal_name] = df[actual_col]
        else:
            normalized[internal_name] = ""

    normalized = normalized.fillna("")

    for col in normalized.columns:
        normalized[col] = normalized[col].astype(str).str.strip()

    normalized = normalized[normalized["policy_name"].str.len() > 0].copy()

    if normalized.empty:
        raise ValueError("Excel 中没有识别到有效政策记录。请检查是否存在「政策名称」列。")

    return normalized


def safe_text(value: object) -> str:
    """清理 Markdown 输出文本。"""
    text = "" if value is None else str(value).strip()

    if text.lower() in {"nan", "none"}:
        return ""

    text = text.replace("\r\n", "；")
    text = text.replace("\n", "；")
    text = text.replace("\r", "；")

    return text


def make_link(url: object) -> str:
    """把 URL 转成 Markdown 链接。多个 URL 用分号分隔时，逐个生成链接。"""
    text = safe_text(url)

    if not text:
        return ""

    parts = [p.strip() for p in text.replace("；", ";").split(";") if p.strip()]

    links = []
    for idx, part in enumerate(parts, start=1):
        if part.startswith("http://") or part.startswith("https://"):
            label = "Link" if len(parts) == 1 else f"Link {idx}"
            links.append(f"[{label}]({part})")
        else:
            links.append(part)

    return "；".join(links)


def sort_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """按领域、推荐等级、年份、政策名称排序。"""
    df = df.copy()

    domain_rank = {name: i for i, name in enumerate(DOMAIN_ORDER)}
    rating_rank = {"A": 1, "B": 2, "C": 3}

    df["_domain_rank"] = df["domain"].map(domain_rank).fillna(999)
    df["_rating_rank"] = df["rating"].map(rating_rank).fillna(999)

    df["_year_sort"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})", expand=False)
        .fillna("9999")
        .astype(int)
    )

    df = df.sort_values(
        ["_domain_rank", "domain", "_rating_rank", "_year_sort", "policy_name"],
        kind="stable",
    )

    return df.drop(columns=["_domain_rank", "_rating_rank", "_year_sort"])


# =========================
# 4. 生成 Markdown 附录
# =========================

def build_markdown_appendix(df: pd.DataFrame) -> str:
    """生成分组列表格式的 Markdown 附录。"""
    lines: List[str] = []

    lines.extend(
        [
            "---",
            'title: "附录：中国政策冲击汇编"',
            "format:",
            "  html:",
            "    toc: true",
            "    toc-depth: 3",
            "    number-sections: true",
            "---",
            "",
            "# 附录：中国政策冲击汇编",
            "",
            "本附录由 `data/policy_shock_library_v0_1.xlsx` 自动生成，用于在线浏览和页内检索。",
            "读者可以使用浏览器的 `Ctrl + F` 搜索政策名称、研究领域、识别方法、数据层级或关键词。",
            "",
            "下载数据：",
            "",
            "- [Excel 版](data/policy_shock_library_v0_1.xlsx)",
            "- [CSV 版](data/policy_shock_library_v0_1.csv)",
            "",
            "说明：本页面是浏览版，不替代 Excel / CSV。若需排序、筛选或批量处理，请下载数据文件。",
            "",
        ]
    )

    df = df.copy()
    df["domain"] = df["domain"].replace("", "未分类")

    for domain, g in df.groupby("domain", sort=False):
        lines.append(f"## {domain}")
        lines.append("")

        for _, row in g.iterrows():
            policy_name = safe_text(row.get("policy_name", "未命名政策"))
            lines.append(f"### {policy_name}")
            lines.append("")

            for field in SHOW_FIELDS:
                label = FIELD_LABELS[field]
                value = safe_text(row.get(field, ""))

                if value:
                    lines.append(f"- **{label}**：{value}")

            official_source = make_link(row.get("official_source", ""))
            if official_source:
                lines.append(f"- **官方来源**：{official_source}")

            lines.append("")

    return "\n".join(lines)


# =========================
# 5. 主程序
# =========================

def main() -> None:
    raw_df = read_policy_excel(XLSX_PATH)
    df = normalize_dataframe(raw_df)
    df = sort_dataframe(df)

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")

    md_text = build_markdown_appendix(df)
    OUT_MD_PATH.write_text(md_text, encoding="utf-8")

    print(f"已读取：{XLSX_PATH}")
    print(f"已生成：{CSV_PATH}")
    print(f"已生成：{OUT_MD_PATH}")
    print(f"政策记录数：{len(df)}")


if __name__ == "__main__":
    main()