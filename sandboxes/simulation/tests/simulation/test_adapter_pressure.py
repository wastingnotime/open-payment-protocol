from app.simulation.adapter_pressure import build_pressure_report


def test_adapter_pressure_report_preserves_native_resource_and_qr_boundaries():
    report = build_pressure_report()
    assert report["asaas"]["native_shape"] == {"resource": "payment", "qr": "separate_retrieval", "money": "decimal_json_number"}
    assert report["pagbank"]["native_shape"]["resource"] == "order_qr_charge"
    assert report["pagarme"]["native_shape"]["resource"] == "order_charge_transaction"


def test_adapter_pressure_report_does_not_create_shared_status_or_money_fields():
    report = build_pressure_report()
    assert all("status" not in entry for entry in report.values())
    assert len({entry["native_shape"]["money"] for entry in report.values()}) == 4
    assert len({entry["native_shape"]["qr"] for entry in report.values()}) == 5


def test_adapter_pressure_report_is_sourced_from_current_scenario_registries():
    report = build_pressure_report()
    assert {provider: entry["scenario_count"] for provider, entry in report.items()} == {
        "asaas": 19, "iugu": 25, "mercadopago": 18, "pagbank": 17, "pagarme": 14,
    }
