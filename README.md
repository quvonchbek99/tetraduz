# ТЕТРАДЬ — rus tili onlayn

Rus tili o'qituvchisining sayti va mustaqil mashq uchun bepul darsxona.

| Sahifa | Nima bor |
|---|---|
| `index.html` | Bosh sahifa: ustoz, 3 oylik dastur, bog'lanish (UZ / RU) |
| `darslar.html` | 6 daraja, 32 mavzu (A0 → C1): qoida, jadval, misollar, dialog, ovoz, 320 ta mashq |
| `lugat.html` | Kunlik 50 so'z (hozir 500 so'z): ro'yxat, kartochkalar, test |
| `mashqlar.html` | Aralash test, olmoshlar bo'yicha 40 mashq, so'zlashuv iboralari |
| `kitoblar.html` | 5 asosiy darslik, A0–C1 yo'l xaritasi, mavzular xaritasi, 12 haftalik reja |

A0–B1 mavzular tartibi quyidagi darsliklarga tayanadi (matn va mashqlar yangidan yozilgan):
«Дорога в Россию», «Поехали!», «Жили-были… 28 уроков», «Русский язык в упражнениях», «The New Penguin Russian Course».

## Tuzilishi

```
assets/tetrad.css        umumiy uslublar (yorug' / qorong'i rejim)
assets/tetrad.js         menyu, ovoz (ru-RU), saqlash, mashq dvigateli
assets/darslar-data.js   A0–B1 (18 dars)
assets/darslar-yuqori.js B1–C1 (14 dars)
assets/lugat-data.js     kunlik so'zlar — yangi kun qo'shish uchun TETRAD_DAYS boshiga yozing
assets/mashq-data.js     olmosh mashqlari va iboralar
```

Yangi so'zlar qo'shish: `assets/lugat-data.js` faylida `TETRAD_DAYS` ro'yxatining boshiga yangi kun qo'shing, har qator `ruscha|transliteratsiya|o'zbekcha`.

O'quvchi natijalari (o'tilgan darslar, o'rganilgan so'zlar) faqat uning brauzerida saqlanadi.
