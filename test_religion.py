from analyzer import analyze_message

def test_religion():
    test_cases = [
        "الدين شيء جميل في حياتنا",
        "أنا لا أحترم هذا الدين إطلاقاً (مع شتيمة)",
        "الأنبياء عليهم السلام قدوة لنا",
        "يسخر من أحد الرموز الدينية بطريقة مسيئة"
    ]

    print("--- بدء اختبار محلل الرسائل (قسم الأديان) ---")
    for text in test_cases:
        is_offensive, reason = analyze_message(text)
        status = "❌ مخالف" if is_offensive else "✅ سليم"
        print(f"النص: {text}")
        print(f"النتيجة: {status} | السبب: {reason}")
        print("-" * 30)

if __name__ == "__main__":
    test_religion()
