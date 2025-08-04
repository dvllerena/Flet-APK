def _create_sample_data(conn, logger):
    """Crea datos de prueba básicos"""
    try:
        logger.info("Creando datos de prueba...")
        
        # Datos de energía de prueba para algunos municipios
        sample_energia = [
            (1, 2024, 1, 150.5, "Datos de prueba enero"),
            (2, 2024, 1, 120.3, "Datos de prueba enero"),
            (3, 2024, 1, 98.7, "Datos de prueba enero"),
            (1, 2024, 2, 145.2, "Datos de prueba febrero"),
            (2, 2024, 2, 118.9, "Datos de prueba febrero")
        ]
        
        for energia in sample_energia:
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO energia_barra 
                    (municipio_id, año, mes, energia_mwh, observaciones, usuario_id)
                    VALUES (?, ?, ?, ?, ?, 1)
                """, energia)
            except Exception as e:
                logger.warning(f"Error insertando energía: {e}")
        
        # Datos de facturación de prueba
        sample_facturacion = [
            (1, 2024, 1, 80.2, 45.3, 125.5, "Facturación enero"),
            (2, 2024, 1, 70.1, 38.9, 109.0, "Facturación enero"),
            (3, 2024, 1, 55.4, 32.1, 87.5, "Facturación enero")
        ]
        
        for fact in sample_facturacion:
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO facturacion 
                    (municipio_id, año, mes, facturacion_mayor, facturacion_menor, facturacion_total, observaciones, usuario_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                """, fact)
            except Exception as e:
                logger.warning(f"Error insertando facturación: {e}")
        
        conn.commit()
        logger.info("Datos de prueba creados exitosamente")
        
    except Exception as e:
        logger.error(f"Error creando datos de prueba: {e}")
        raise
