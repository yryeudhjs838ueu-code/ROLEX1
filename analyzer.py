import os
import json
from openai import OpenAI

# إعداد العميل باستخدام متغيرات البيئة المجهزة مسبقاً في Manus
client = OpenAI()

def analyze_message(text):
    """
    تحليل النص لمعرفة ما إذا كان يحتوي على شتائم، إهانات، أو إساءة للأديان.
    يعيد True إذا كان النص مخالفاً، و False خلاف ذلك.
    """
    if not text or len(text.strip()) < 2:
        return False

    prompt = f"""
قم بتحليل النص التالي الوارد من مجموعة تيليجرام وحدد ما إذا كان يحتوي على أي من الفئات التالية:
1.  **شتائم أو ألفاظ نابية**: كلمات بذيئة، سباب، أو تعابير فاحشة.
2.  **إهانات شخصية**: توجيه إهانات أو هجوم شخصي على أي فرد.
3.  **إساءة للأديان أو المعتقدات**: أي محتوى يسيء إلى الأديان، الرموز الدينية، أو المعتقدات الشخصية، بما في ذلك السخرية أو التجديف.

يجب أن يكون التحليل دقيقاً ويأخذ في الاعتبار السياق العربي. إذا كان النص يحتوي على أي من هذه الفئات، فاعتبره مسيئاً.

النص: "{text}"

يجب أن يكون الرد بتنسيق JSON فقط كالتالي:
{{
  "is_offensive": true/false,
  "reason": "سبب قصير باللغة العربية"
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "أنت خبير في الإشراف على المحتوى العربي وتحديد الإساءات والشتائم."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_schema", "json_schema": {
                "name": "analysis_result",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "is_offensive": {"type": "boolean"},
                        "reason": {"type": "string"}
                    },
                    "required": ["is_offensive", "reason"],
                    "additionalProperties": False
                }
            }}
        )
        
        content = response.choices[0].message.content
        if not content:
            return False, ""
        result = json.loads(content)
        return result.get("is_offensive", False), result.get("reason", "")
    except Exception as e:
        print(f"Error analyzing message: {e}")
        return False, "حدث خطأ أثناء تحليل الرسالة"
