"""
Seed script to populate MongoDB with consistent Category and Product data.

Usage:
  python seed_data.py
"""

from __future__ import annotations

import os
from typing import Dict, List

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


if __name__ == "__main__":
    run_seed()


