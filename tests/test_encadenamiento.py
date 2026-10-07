#!/usr/bin/env python3
"""
Test unitario para encadenamiento de facturas en pytbai
"""
import unittest
from pytbai import TBai
from decimal import Decimal


class TestEncadenamiento(unittest.TestCase):
    """Tests para el encadenamiento de facturas"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.config = {
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
        self.tbai = TBai(self.config)
    
    def test_set_previous_invoice(self):
        """Test que se puede establecer una factura anterior"""
        invoice = self.tbai.create_invoice("A", 100, "Test factura", "S")
        
        # Establecer factura anterior
        invoice.set_previous_invoice(
            serial_code="A",
            num="99",
            expedition_date="21-01-2026",
            signature_value="ABC123XYZ789"
        )
        
        # Verificar que se guardó
        prev = invoice.get_previous_invoice()
        self.assertIsNotNone(prev)
        self.assertEqual(prev['serial_code'], 'A')
        self.assertEqual(prev['num'], '99')
        self.assertEqual(prev['expedition_date'], '21-01-2026')
        self.assertEqual(prev['signature_value'], 'ABC123XYZ789')
    
    def test_invoice_without_previous(self):
        """Test que una factura sin anterior devuelve None"""
        invoice = self.tbai.create_invoice("A", 1, "Primera factura", "S")
        
        # No establecer factura anterior
        prev = invoice.get_previous_invoice()
        self.assertIsNone(prev)
    
    def test_get_dict_includes_previous(self):
        """Test que get_dict() incluye la factura anterior"""
        invoice = self.tbai.create_invoice("A", 100, "Test factura", "S")
        invoice.create_line("Producto", Decimal("1"), Decimal("100"))
        
        # Establecer factura anterior
        invoice.set_previous_invoice(
            serial_code="A",
            num="99",
            expedition_date="21-01-2026",
            signature_value="SIGNATURE_VALUE_PREVIOUS"
        )
        
        # Obtener diccionario
        invoice_dict = invoice.get_dict()
        
        # Verificar que incluye previous_invoice
        self.assertIn('previous_invoice', invoice_dict)
        self.assertEqual(invoice_dict['previous_invoice']['serial_code'], 'A')
        self.assertEqual(invoice_dict['previous_invoice']['num'], '99')
    
    def test_get_dict_without_previous(self):
        """Test que get_dict() no incluye previous_invoice si no se estableció"""
        invoice = self.tbai.create_invoice("A", 1, "Primera factura", "S")
        invoice.create_line("Producto", Decimal("1"), Decimal("100"))
        
        # Obtener diccionario
        invoice_dict = invoice.get_dict()
        
        # No debe incluir previous_invoice
        self.assertNotIn('previous_invoice', invoice_dict)
    
    def test_change_previous_invoice(self):
        """Test que se puede cambiar la factura anterior"""
        invoice = self.tbai.create_invoice("A", 100, "Test factura", "S")
        
        # Establecer primera factura anterior
        invoice.set_previous_invoice(
            serial_code="A",
            num="99",
            expedition_date="21-01-2026",
            signature_value="FIRST_SIGNATURE"
        )
        
        # Cambiar a otra factura anterior
        invoice.set_previous_invoice(
            serial_code="A",
            num="98",
            expedition_date="20-01-2026",
            signature_value="SECOND_SIGNATURE"
        )
        
        # Verificar que se actualizó
        prev = invoice.get_previous_invoice()
        self.assertEqual(prev['num'], '98')
        self.assertEqual(prev['signature_value'], 'SECOND_SIGNATURE')
    
    def test_signature_value_truncated_to_100_chars(self):
        """Test que el signature_value se trunca a 100 caracteres"""
        invoice = self.tbai.create_invoice("A", 100, "Test factura", "S")
        
        # Signature value largo (más de 100 caracteres)
        long_signature = "A" * 150
        
        invoice.set_previous_invoice(
            serial_code="A",
            num="99",
            expedition_date="21-01-2026",
            signature_value=long_signature
        )
        
        prev = invoice.get_previous_invoice()
        # Debe estar truncado a 100 caracteres
        self.assertEqual(len(prev['signature_value']), 100)
        self.assertEqual(prev['signature_value'], "A" * 100)


if __name__ == '__main__':
    unittest.main()
