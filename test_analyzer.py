from analyzer import analyze_message

def test():
    test_cases = [
        "مرحباً كيف حالكم؟",
        "هذا الشخص غبي جداً ولا يفهم",
        "يا ابن الـ ... (شتيمة افتراضية)",
        "أنا أحب البرمجة",
        "تباً لك ولعائلتك"
    ]

    print("--- بدء اختبار محلل الرسائل ---")
    for text in test_cases:
        is_offensive, reason = analyze_message(text)
        status = "❌ مخالف" if is_offensive else "✅ سليم"
        print(f"النص: {text}")
        print(f"النتيجة: {status} | السبب: {reason}")
        print("-" * 30)

if __name__ == "__main__":
    test()
