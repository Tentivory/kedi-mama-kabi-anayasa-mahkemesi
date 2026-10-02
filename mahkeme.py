#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kedi Mama Kabı Anayasa Mahkemesi.

Kase boşaldığında toplanır, gramajdan hüküm çıkarır.
Bağımlılık yok. Patates kabul edilmez.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import datetime


def doluluk(gram: float, kapasite: float) -> float:
    if kapasite <= 0:
        raise ValueError("Kapasite sıfır olamaz; kase yoksa mahkeme de yok.")
    if gram < 0:
        raise ValueError("Negatif mama, fizik ihlalidir. Dava dusurulur.")
    return max(0.0, min(100.0, (gram / kapasite) * 100.0))


def hukum(oran: float, aciliyet: str) -> tuple[str, str]:
    gece = aciliyet == "gece"
    if oran <= 0:
        madde = "Md. 0 — Mutlak boşluk"
        metin = (
            "Kase anayasal boşluk halindedir. Derhal infaz: bir poşet açılır. "
            + ("Gece ise ışık açılmaz, fısıltıyla dökülür. " if gece else "")
            + "Temyiz yok."
        )
    elif oran <= 25:
        madde = "Md. 7 — Açlık ihbarı"
        metin = "İhlal sabittir. Kedi haklı, insan sanıktır. Bir avuç yetmez, iki avuç."
    elif oran <= 60:
        madde = "Md. 19 — İhtiyati tedbir"
        metin = "Dava esastan görülürken kabın üstü tamamlanır. Kedi izler, sen utanırsın."
    elif oran < 90:
        madde = "Md. 42 — Ret"
        metin = "Dava reddedildi. Kedi yine de küsebilir; bu anayasal haktır, sınırlanamaz."
    else:
        madde = "Md. 90 — Doygunluk"
        metin = "İhlal yok. Yine de kedi drama yaparsa seyret, karışma. Bu da içtihattır."
    return madde, metin


def esas_no(kedi: str, gram: float) -> str:
    ham = f"{kedi}|{gram}|{datetime.now().strftime('%Y%m%d')}"
    ozet = hashlib.sha256(ham.encode("utf-8")).hexdigest()[:6].upper()
    return f"2026/MAMA-{ozet}"


def itiraz_notu(itiraz: str | None) -> str:
    if not itiraz:
        return "Sanık beyanda bulunmadı. Kedi bunu itiraf saydı."
    if "yeni koydum" in itiraz.lower():
        return f"İtiraz ({itiraz!r}) dinlendi ve 'klasik savunma' diye dosyaya işlendi. Red."
    return f"İtiraz ({itiraz!r}) tutanağa geçti. Mahkeme etkilenmedi, kedi etkilendi."


def karar_metni(kedi: str, gram: float, kapasite: float, aciliyet: str, itiraz: str | None) -> str:
    oran = doluluk(gram, kapasite)
    madde, metin = hukum(oran, aciliyet)
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    satirlar = [
        "=" * 62,
        "KEDİ MAMA KABI ANAYASA MAHKEMESİ",
        "Bağlayıcı karar  |  Mamaştay Büyük Daire",
        "=" * 62,
        f"Esas no     : {esas_no(kedi, gram)}",
        f"Tarih       : {simdi}",
        f"Başvuran    : {kedi} (pati ile)",
        f"Sanık       : kabı doldurması gereken kişi",
        f"Gram        : {gram:.1f} / {kapasite:.1f}  ({oran:.1f}%)",
        f"Aciliyet    : {aciliyet}",
        "-" * 62,
        f"Hüküm       : {madde}",
        metin,
        itiraz_notu(itiraz),
        "-" * 62,
        "Kesinleşme  : bu çıktının ekranda görünmesiyle.",
        "İnfaz       : poşet. Gerekirse ikinci poşet.",
        "Muhalefet   : yok. Kedi oybirliği sayılır.",
        "=" * 62,
    ]
    return "\n".join(satirlar)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Kedi mama kabı için anayasal hüküm üretir.")
    p.add_argument("--kedi", default="İsimsiz Pati", help="Başvuran kedinin adı")
    p.add_argument("--gram", type=float, required=True, help="Kaptaki mevcut mama (gram)")
    p.add_argument("--kapasite", type=float, default=80.0, help="Kabın kapasitesi (gram)")
    p.add_argument("--aciliyet", choices=["normal", "gece", "misafir"], default="normal")
    p.add_argument("--itiraz", default=None, help="Sanığın beyhude savunması")
    args = p.parse_args(argv)
    try:
        print(karar_metni(args.kedi, args.gram, args.kapasite, args.aciliyet, args.itiraz))
    except ValueError as exc:
        print(f"Usulden ret: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
