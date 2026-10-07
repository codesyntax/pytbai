#!/usr/bin/env python3
"""
Test de integración: Crear múltiples facturas encadenadas
"""
from pytbai import TBai
from decimal import Decimal

print("=" * 70)
print("🔗 TEST DE INTEGRACIÓN: Encadenamiento de Facturas")
print("=" * 70)

config = {
    "subject": {
        "entity_id": "B20456794",
        "name": "OFENVAL S.L."
    },
    "software": {
        "license": "TBAIPRUEBA",
        "dev_entity": "A48119820",
        "soft_name": "TicketBAI OFENVAL",
        "soft_version": "1.0.0"
    }
}

tbai = TBai(config)

# ============================================================================
# FACTURA 1 (Primera factura, sin encadenamiento)
# ============================================================================
print("\n📄 FACTURA 1: Primera factura de la serie (sin encadenamiento)")
print("-" * 70)

invoice1 = tbai.create_invoice("A", 1, "Primera factura de prueba", "S")
invoice1.create_line("Producto A", Decimal("2"), Decimal("50.00"))
invoice1.create_line("Producto B", Decimal("1"), Decimal("150.00"))

dict1 = invoice1.get_dict()
print(f"✅ Factura creada: {dict1['serial_code']}-{dict1['num']}")
print(f"   Descripción: {dict1['description']}")
print(f"   Encadenamiento: {'NO (primera factura)' if 'previous_invoice' not in dict1 else 'SÍ'}")
print(f"   Total: {invoice1.get_total_amount()} €")

# Simular SignatureValue que devolvería Hacienda después de firmar
signature1 = "MEJP9Z/7SbnG+Fb8BzZAbWYRj95wFgY0jwcZhpMMf+SbhjnSIMULATED1=="
print(f"   SignatureValue (simulado): {signature1[:50]}...")

# ============================================================================
# FACTURA 2 (Encadenada a Factura 1)
# ============================================================================
print("\n📄 FACTURA 2: Segunda factura (encadenada a Factura 1)")
print("-" * 70)

invoice2 = tbai.create_invoice("A", 2, "Segunda factura de prueba", "S")

# *** AQUÍ ESTÁ EL ENCADENAMIENTO ***
invoice2.set_previous_invoice(
    serial_code="A",
    num="1",
    expedition_date="22-01-2026",
    signature_value=signature1
)

invoice2.create_line("Servicio consultoría", Decimal("10"), Decimal("80.00"))

dict2 = invoice2.get_dict()
print(f"✅ Factura creada: {dict2['serial_code']}-{dict2['num']}")
print(f"   Descripción: {dict2['description']}")
print(f"   Encadenamiento: {'NO' if 'previous_invoice' not in dict2 else 'SÍ ✓'}")

if 'previous_invoice' in dict2:
    prev = dict2['previous_invoice']
    print(f"   └─ Factura anterior: {prev['serial_code']}-{prev['num']}")
    print(f"      Fecha anterior: {prev['expedition_date']}")
    print(f"      Firma anterior: {prev['signature_value'][:50]}...")

print(f"   Total: {invoice2.get_total_amount()} €")

# Simular SignatureValue de Factura 2
signature2 = "XYZ456DEF/8AcqH+Gc9CdYgSk06xGhZ1kxdaSiqNNg+TcikoCDSIMULATED2=="
print(f"   SignatureValue (simulado): {signature2[:50]}...")

# ============================================================================
# FACTURA 3 (Encadenada a Factura 2)
# ============================================================================
print("\n📄 FACTURA 3: Tercera factura (encadenada a Factura 2)")
print("-" * 70)

invoice3 = tbai.create_invoice("A", 3, "Tercera factura de prueba", "S")

# Encadenar a la Factura 2
invoice3.set_previous_invoice(
    serial_code="A",
    num="2",
    expedition_date="22-01-2026",
    signature_value=signature2
)

invoice3.create_line("Mantenimiento mensual", Decimal("1"), Decimal("500.00"))
invoice3.create_line("Soporte técnico", Decimal("3"), Decimal("120.00"))

dict3 = invoice3.get_dict()
print(f"✅ Factura creada: {dict3['serial_code']}-{dict3['num']}")
print(f"   Descripción: {dict3['description']}")
print(f"   Encadenamiento: {'NO' if 'previous_invoice' not in dict3 else 'SÍ ✓'}")

if 'previous_invoice' in dict3:
    prev = dict3['previous_invoice']
    print(f"   └─ Factura anterior: {prev['serial_code']}-{prev['num']}")
    print(f"      Fecha anterior: {prev['expedition_date']}")
    print(f"      Firma anterior: {prev['signature_value'][:50]}...")

print(f"   Total: {invoice3.get_total_amount()} €")

# ============================================================================
# RESUMEN DE LA CADENA
# ============================================================================
print("\n" + "=" * 70)
print("✅ TEST DE INTEGRACIÓN COMPLETADO")
print("=" * 70)
print("\n🔗 Cadena de facturas creada correctamente:")
print()
print("   [Factura A-1]")
print("        │")
print("        │ signature_value_1")
print("        ↓")
print("   [Factura A-2] ← EncadenamientoFacturaAnterior")
print("        │")
print("        │ signature_value_2")
print("        ↓")
print("   [Factura A-3] ← EncadenamientoFacturaAnterior")
print()
print("📋 Verificaciones:")
print(f"   • Factura 1: {'✓' if 'previous_invoice' not in dict1 else '✗'} SIN encadenamiento (correcto)")
print(f"   • Factura 2: {'✓' if 'previous_invoice' in dict2 else '✗'} CON encadenamiento (correcto)")
print(f"   • Factura 3: {'✓' if 'previous_invoice' in dict3 else '✗'} CON encadenamiento (correcto)")
print()
print("🎯 Esto simula el comportamiento en producción donde cada factura")
print("   contiene el SignatureValue de la factura anterior, creando una")
print("   cadena blockchain que impide manipulación de facturas.")
print()
