# tests/test_graph.py
import pytest
from agents.graph import app_graph

def test_graph_baseline_safe_flow():
    """اختبار تدفق الوكلاء في الحالة الطبيعية المستقرة (بدون تسريبات)"""
    # 1. إعداد المدخلات الآمنة للبئر
    initial_state = {
        "leak_rate": 0.0,
        "pressure": 450.0,
        "image_bytes": None,
        "anomaly_detected": False,
        "telemetry_status": "",
        "visual_analysis_summary": "",
        "gas_lost_cost_hourly": 0.0,
        "carbon_penalty_hourly": 0.0,
        "co2_equivalent_rate": 0.0,
        "esg_risk_level": "Low",
        "scada_signal_sent": False,
        "scada_log": "",
        "inventory_available": False,
        "dispatch_status": "",
        "generated_runbook": "",
        "current_agent": "Monitor",
        "logs": []
    }
    
    # 2. تشغيل الـ LangGraph Pipeline بالكامل
    final_state = app_graph.invoke(initial_state)
    
    # 3. التحقق من صحة قرارات الوكلاء المشتركة
    assert final_state["anomaly_detected"] is False
    assert final_state["esg_risk_level"] == "Low"
    assert final_state["scada_signal_sent"] is False
    assert "healthy" in final_state["generated_runbook"].lower() or "baseline" in final_state["generated_runbook"].lower()

def test_graph_critical_leak_flow():
    """اختبار استجابة شبكة الوكلاء وتفعيل بروتوكولات الأتمتة عند حدوث تسريب ميثان حرج"""
    # 1. مدخلات تسريب حرج وضغط مرتفع
    initial_state = {
        "leak_rate": 65.0,  # قيمة تسريب عالية تسبب تصنيف خطر مرتفع
        "pressure": 850.0,
        "image_bytes": None,
        "anomaly_detected": False,
        "telemetry_status": "",
        "visual_analysis_summary": "",
        "gas_lost_cost_hourly": 0.0,
        "carbon_penalty_hourly": 0.0,
        "co2_equivalent_rate": 0.0,
        "esg_risk_level": "Low",
        "scada_signal_sent": False,
        "scada_log": "",
        "inventory_available": False,
        "dispatch_status": "",
        "generated_runbook": "",
        "current_agent": "Monitor",
        "logs": []
    }
    
    # 2. تشغيل الـ LangGraph Pipeline
    final_state = app_graph.invoke(initial_state)
    
    # 3. التحقق من القرارات الحرجة للوكلاء
    assert final_state["anomaly_detected"] is True
    assert final_state["esg_risk_level"] == "High"  # يجب أن يرفع وكيل المخاطر مستوى التقييم
    assert final_state["scada_signal_sent"] is True  # يجب أن يأمر وكيل التنفيذ بغلق الصمام فوراً
    assert final_state["inventory_available"] is True
    assert len(final_state["generated_runbook"]) > 0  # يجب توليد دليل الصيانة بالـ AI