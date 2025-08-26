"""
Seed script to populate MongoDB with consistent Category and Product data.

Usage:
  python seed_data.py
"""

from __future__ import annotations

import os
from typing import Dict, List, Tuple, Optional
import sys
import json
import re

from mongoengine import connect, DoesNotExist

from config import Config
from models import Category, Product


def ensure_connection() -> None:
    connect(
        db=Config.MONGODB_SETTINGS["db"],
        host=Config.MONGODB_SETTINGS["host"],
        port=Config.MONGODB_SETTINGS["port"],
    )


def upsert_category(data: Dict) -> Category:
    try:
        cat = Category.objects.get(slug=data["slug"])  # type: ignore[index]
    except DoesNotExist:
        cat = Category(**data)  # type: ignore[arg-type]
        cat.save()
        return cat

    # Update existing fields to keep data fresh
    for key, value in data.items():
        setattr(cat, key, value)
    cat.save()
    return cat


def upsert_product(data: Dict) -> Product:
    # De-dup by sku
    prod = Product.objects(sku=data["sku"]).first()
    if prod is None:
        prod = Product(**data)  # type: ignore[arg-type]
        prod.save()
        return prod

    for key, value in data.items():
        setattr(prod, key, value)
    prod.save()
    return prod


def run_seed() -> None:
    ensure_connection()

    categories_seed: List[Dict] = [
        {
            "name": "อิเล็กทรอนิกส์",
            "description": "แกดเจ็ตและอุปกรณ์อิเล็กทรอนิกส์ยอดนิยม",
            "image_url": "https://picsum.photos/seed/electronics/800/600",
            "slug": "electronics",
            "is_active": True,
        },
        {
            "name": "แฟชั่น",
            "description": "เสื้อผ้าและเครื่องแต่งกายสไตล์โมเดิร์น",
            "image_url": "https://picsum.photos/seed/fashion/800/600",
            "slug": "fashion",
            "is_active": True,
        },
        {
            "name": "บ้านและไลฟ์สไตล์",
            "description": "ของใช้ภายในบ้านและของตกแต่ง",
            "image_url": "https://picsum.photos/seed/home/800/600",
            "slug": "home-lifestyle",
            "is_active": True,
        },
        {
            "name": "กีฬาและสุขภาพ",
            "description": "อุปกรณ์กีฬาและของเพื่อสุขภาพ",
            "image_url": "https://picsum.photos/seed/sports/800/600",
            "slug": "sports-health",
            "is_active": True,
        },
    ]

    categories = {c_data["slug"]: upsert_category(c_data) for c_data in categories_seed}

    products_seed: List[Dict] = [
        {
            "name": "หูฟังไร้สาย Pro X",
            "description": "ระบบตัดเสียงรบกวน อึดนาน 30 ชั่วโมง",
            "price": 3990.0,
            "original_price": 4590.0,
            "category": categories["electronics"],
            "images": ["https://picsum.photos/seed/headphones/1200/800"],
            "stock_quantity": 120,
            "sku": "ELEC-HP-PROX",
            "brand": "SoundMax",
            "tags": ["wireless", "noise-cancelling"],
            "is_featured": True,
            "is_active": True,
            "rating": 4.6,
            "review_count": 842,
        },
        {
            "name": "สมาร์ทวอทช์ Fit 2",
            "description": "กันน้ำ วัดชีพจร ติดตามการนอน",
            "price": 2790.0,
            "original_price": 3290.0,
            "category": categories["electronics"],
            "images": ["https://picsum.photos/seed/watch/1200/800"],
            "stock_quantity": 85,
            "sku": "ELEC-WATCH-FIT2",
            "brand": "Fitio",
            "tags": ["smartwatch", "fitness"],
            "is_featured": True,
            "is_active": True,
            "rating": 4.4,
            "review_count": 523,
        },
        {
            "name": "เสื้อยืด Cotton Premium",
            "description": "ผ้านุ่ม ระบายอากาศดี ใส่สบาย",
            "price": 290.0,
            "original_price": 350.0,
            "category": categories["fashion"],
            "images": ["https://picsum.photos/seed/tshirt/1200/800"],
            "stock_quantity": 300,
            "sku": "FASH-TSHIRT-CTNPREM",
            "brand": "Wearly",
            "tags": ["tshirt", "cotton"],
            "is_featured": True,
            "is_active": True,
            "rating": 4.2,
            "review_count": 211,
        },
        {
            "name": "หมอนหนุน Memory Foam",
            "description": "รองรับสรีระ ลดปวดคอ หลับสบาย",
            "price": 690.0,
            "original_price": 890.0,
            "category": categories["home-lifestyle"],
            "images": ["https://picsum.photos/seed/pillow/1200/800"],
            "stock_quantity": 160,
            "sku": "HOME-PILLOW-MEMFOAM",
            "brand": "Sleeplux",
            "tags": ["pillow", "sleep"],
            "is_featured": False,
            "is_active": True,
            "rating": 4.5,
            "review_count": 129,
        },
        {
            "name": "ดัมเบลปรับน้ำหนัก 20kg",
            "description": "ปรับได้ทีละ 2.5kg ประหยัดพื้นที่",
            "price": 3590.0,
            "original_price": 4290.0,
            "category": categories["sports-health"],
            "images": ["https://picsum.photos/seed/dumbbell/1200/800"],
            "stock_quantity": 40,
            "sku": "SPORT-DUMB-20KG",
            "brand": "StrongPro",
            "tags": ["gym", "homeworkout"],
            "is_featured": True,
            "is_active": True,
            "rating": 4.7,
            "review_count": 301,
        },
        {
            "name": "รองเท้าวิ่ง AirFlow",
            "description": "ระบายอากาศดี น้ำหนักเบา ซัพพอร์ตข้อเท้า",
            "price": 1990.0,
            "original_price": 2490.0,
            "category": categories["sports-health"],
            "images": ["https://picsum.photos/seed/runningshoes/1200/800"],
            "stock_quantity": 95,
            "sku": "SPORT-SHOE-AIRFLOW",
            "brand": "FleetRun",
            "tags": ["running", "shoes"],
            "is_featured": False,
            "is_active": True,
            "rating": 4.3,
            "review_count": 188,
        },
    ]

    for pdata in products_seed:
        upsert_product(pdata)

    print(
        {
            "categories": Category.objects.count(),
            "products": Product.objects.count(),
            "featured_products": Product.objects(is_featured=True, is_active=True).count(),
        }
    )


def _parse_objects_from_section(lines: List[str]) -> List[str]:
    """Collect JSON-like object chunks by brace depth from a section of lines."""
    objects: List[str] = []
    buf: List[str] = []
    depth = 0
    for raw in lines:
        line = raw.rstrip()
        # skip empty separators
        if not line and depth == 0:
            continue
        # accumulate and track depth
        buf.append(line)
        depth += line.count("{") - line.count("}")
        if depth == 0 and buf:
            chunk = "\n".join(buf)
            # strip trailing commas/semicolons between objects
            chunk = chunk.strip()
            if chunk.endswith(",") or chunk.endswith(";"):
                chunk = chunk[:-1]
            objects.append(chunk)
            buf = []
    return objects


def _normalize_extended_json(chunk: str) -> str:
    """Transform Mongo Extended JSON snippets like {"$oid": "..."} and {"$date": "..."} into plain strings.

    Use callable replacement to avoid backreference escaping issues.
    """
    def replace_oid(m: re.Match) -> str:
        return '"' + m.group(1) + '"'

    def replace_date(m: re.Match) -> str:
        return '"' + m.group(1) + '"'

    # Replace { "$oid": "..." } with "..."
    chunk = re.sub(r"\{\s*\"\$oid\"\s*:\s*\"([^\"]+)\"\s*\}", replace_oid, chunk)
    # Replace { "$date": "..." } with "..."
    chunk = re.sub(r"\{\s*\"\$date\"\s*:\s*\"([^\"]+)\"\s*\}", replace_date, chunk)
    return chunk


def _load_from_data_txt(path: str) -> Tuple[List[Dict], List[Dict]]:
    """Parse root data.txt into (products, categories) lists of dicts.

    The file uses two sections labeled 'Product :' and 'Categories :', followed by
    multiple object literals separated by commas/semicolons.
    """
    with open(path, "r", encoding="utf-8") as f:
        all_lines = f.read().splitlines()

    # Find section indices
    prod_start = None
    cat_start = None
    for idx, line in enumerate(all_lines):
        if prod_start is None and line.strip().startswith("Product :"):
            prod_start = idx + 1
            continue
        if line.strip().startswith("Categories :"):
            cat_start = idx + 1
            break

    if prod_start is None or cat_start is None:
        raise RuntimeError("data.txt missing required sections 'Product :' and 'Categories :'")

    product_lines = all_lines[prod_start:cat_start - 1]
    category_lines = all_lines[cat_start:]

    product_chunks = _parse_objects_from_section(product_lines)
    category_chunks = _parse_objects_from_section(category_lines)

    def to_dict_list(chunks: List[str]) -> List[Dict]:
        results: List[Dict] = []
        for ch in chunks:
            norm = _normalize_extended_json(ch)
            try:
                data = json.loads(norm)
                results.append(data)
            except json.JSONDecodeError as e:
                # Provide context to help debugging malformed blocks
                raise RuntimeError(f"Failed to parse block as JSON: {e}\nBlock:\n{norm}") from e
        return results

    products_raw = to_dict_list(product_chunks)
    categories_raw = to_dict_list(category_chunks)

    return products_raw, categories_raw


def run_seed_from_file(path: str) -> None:
    ensure_connection()

    products_raw, categories_raw = _load_from_data_txt(path)

    # Upsert categories first and build mapping from original _id to saved Category
    original_id_to_category: Dict[str, Category] = {}

    for c in categories_raw:
        original_id: Optional[str] = None
        if isinstance(c.get("_id"), dict):
            # Already normalized by _normalize_extended_json, so should be string
            pass
        # normalize fields allowed by model
        original_id = str(c.get("_id")) if c.get("_id") is not None else None
        # Prepare payload
        c_payload: Dict = {
            "name": c.get("name"),
            "description": c.get("description"),
            "image_url": c.get("image_url"),
            "slug": c.get("slug"),
            "is_active": bool(c.get("is_active", True)),
        }
        saved = upsert_category(c_payload)
        if original_id:
            original_id_to_category[original_id] = saved

    # Upsert products, resolving category by original id reference
    for p in products_raw:
        # Resolve category
        category_ref = p.get("category")
        resolved_category = None
        if isinstance(category_ref, dict):
            # after normalization it should be a string, but handle both
            category_original_id = category_ref.get("$oid")
            if category_original_id:
                resolved_category = original_id_to_category.get(category_original_id)
        elif isinstance(category_ref, str):
            resolved_category = original_id_to_category.get(category_ref)

        if resolved_category is None:
            # Skip products with unknown category mapping
            continue

        p_payload: Dict = {
            "name": p.get("name"),
            "description": p.get("description"),
            "price": float(p.get("price", 0.0)),
            "original_price": float(p.get("original_price", 0.0)) if p.get("original_price") is not None else None,
            "category": resolved_category,
            "images": list(p.get("images") or []),
            "stock_quantity": int(p.get("stock_quantity", 0)),
            "sku": p.get("sku"),
            "brand": p.get("brand"),
            "tags": list(p.get("tags") or []),
            "is_featured": bool(p.get("is_featured", False)),
            "is_active": bool(p.get("is_active", True)),
            "rating": float(p.get("rating", 0.0)),
            "review_count": int(p.get("review_count", 0)),
        }
        upsert_product(p_payload)

    print(
        {
            "categories": Category.objects.count(),
            "products": Product.objects.count(),
            "from_file": True,
        }
    )


if __name__ == "__main__":
    # Usage:
    #   python seed_data.py                -> seed with built-in data
    #   python seed_data.py --file ../data.txt  -> import from external data file
    if len(sys.argv) >= 3 and sys.argv[1] == "--file":
        run_seed_from_file(sys.argv[2])
    else:
        run_seed()


