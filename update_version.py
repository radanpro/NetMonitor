import json
import os

# استخراج رقم الإصدار من GitHub (من متغير البيئة GITHUB_REF)
version = os.getenv("GITHUB_REF").split("/")[-1] 

# محتوى ملف latest_version.json
version_info = {
    "version": version,
    "commit": "1ccbf50"  # يمكن إضافة commit hash هنا إذا رغبت
}

# كتابة البيانات في ملف latest_version.json
with open("latest_version.json", "w") as json_file:
    json.dump(version_info, json_file, indent=4)

print("تم تحديث latest_version.json بنجاح.")
