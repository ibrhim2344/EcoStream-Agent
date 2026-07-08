# config.py
import os
from dotenv import load_dotenv

# شحن المتغيرات البيئية من ملف .env
load_dotenv()

class Config:
    """
    EcoStream-Agent المركزية لمشروع Configuration إدارة واجهة الإعدادات
    """
    # إعدادات نموذج الميثان والذكاء الاصطناعي
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"
    
    # الثوابت البيئية والمالية لحسابات الانبعاثات
    METHANE_GWP = 28  # (Global Warming Potential) المعامل العالمي للاحتباس الحراري للميثان مقارنة بـ CO2
    CARBON_TAX_PER_TONNE = 85.0  # قيمة الضريبة الكربونية بالدولار لكل طن مكافئ كربوني
    METHANE_PRICE_PER_KG = 0.08   # القيمة التجارية للغاز المفقود (دولار لكل كيلوجرام)
    
    # المعرفات الافتراضية للموقع والمعدات
    DEFAULT_VALVE_ID = "V-102"
    DEFAULT_PIPELINE_ID = "PL-07"
    
    # بيانات فني الصيانة الميداني الافتراضي للاستدعاء الطارئ
    TECH_NAME = "Engineer Khalid"
    TECH_CONTACT = "+966 55-XXX-XXXX"