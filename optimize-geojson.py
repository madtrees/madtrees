#!/usr/bin/env python3
"""
Script para optimizar el archivo GeoJSON de árboles de Madrid.
Reduce el tamaño eliminando campos innecesarios y opcionalmente reduciendo el número de árboles.
"""

import json
import sys
import os
from pathlib import Path

def optimize_geojson(input_file, output_file, keep_ratio=1.0, keep_fields=None):
    """
    Optimiza un archivo GeoJSON.
    
    Args:
        input_file: Ruta al archivo GeoJSON original
        output_file: Ruta al archivo GeoJSON optimizado
        keep_ratio: Ratio de árboles a mantener (1.0 = todos, 0.25 = 25%)
        keep_fields: Lista de campos a mantener en properties (None = campos esenciales)
    """
    print(f"📖 Leyendo {input_file}...")
    
    if not os.path.exists(input_file):
        print(f"❌ Error: No se encuentra el archivo {input_file}")
        return False
    
    # Mostrar tamaño original
    original_size = os.path.getsize(input_file) / (1024 * 1024)
    print(f"📦 Tamaño original: {original_size:.2f} MB")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    if 'features' not in data or not isinstance(data['features'], list):
        print("❌ Error: Formato de GeoJSON inválido")
        return False
    
    original_count = len(data['features'])
    print(f"🌳 Total de árboles: {original_count:,}")
    
    # Campos esenciales por defecto
    if keep_fields is None:
        keep_fields = ['species', 'common_name', 'diameter', 'height', 'NBRE_DTO', 'NBRE_BARRI', 'CODIGO_ESP']
    
    # Procesar features
    optimized_features = []
    
    for i, feature in enumerate(data['features']):
        # Filtrar por ratio (por ejemplo, mantener 1 de cada 4)
        if keep_ratio < 1.0:
            if i % int(1 / keep_ratio) != 0:
                continue
        
        # Crear feature optimizado
        optimized_feature = {
            'type': feature['type'],
            'geometry': feature['geometry']
        }
        
        # Mantener solo campos especificados
        if 'properties' in feature:
            optimized_props = {}
            for field in keep_fields:
                if field in feature['properties']:
                    optimized_props[field] = feature['properties'][field]
            optimized_feature['properties'] = optimized_props
        
        optimized_features.append(optimized_feature)
    
    # Crear GeoJSON optimizado
    optimized_data = {
        'type': 'FeatureCollection',
        'features': optimized_features
    }
    
    print(f"✂️  Árboles después de optimización: {len(optimized_features):,}")
    print(f"📝 Escribiendo {output_file}...")
    
    # Guardar archivo optimizado
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(optimized_data, f, ensure_ascii=False, separators=(',', ':'))
    except Exception as e:
        print(f"❌ Error al escribir el archivo: {e}")
        return False
    
    # Mostrar estadísticas
    optimized_size = os.path.getsize(output_file) / (1024 * 1024)
    reduction = ((original_size - optimized_size) / original_size) * 100
    
    print(f"\n✅ Optimización completada!")
    print(f"📦 Tamaño nuevo: {optimized_size:.2f} MB")
    print(f"📉 Reducción: {reduction:.1f}%")
    print(f"🌳 Árboles: {len(optimized_features):,} ({(len(optimized_features)/original_count)*100:.1f}% del original)")
    
    # Advertencia si aún es muy grande
    if optimized_size > 100:
        print(f"\n⚠️  ADVERTENCIA: El archivo aún es muy grande para GitHub ({optimized_size:.2f} MB > 100 MB)")
        print(f"💡 Considera reducir el número de árboles con: --keep-ratio 0.25")
    elif optimized_size > 50:
        print(f"\n⚠️  El archivo ({optimized_size:.2f} MB) funcionará pero la carga será lenta.")
        print(f"💡 Para mejor rendimiento, considera --keep-ratio 0.5")
    
    return True

def main():
    # Argumentos por defecto
    input_file = 'trees.geojson'
    output_file = 'trees-data.geojson'
    keep_ratio = 1.0
    
    # Procesar argumentos de línea de comandos
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--input' and i + 1 < len(args):
            input_file = args[i + 1]
            i += 2
        elif args[i] == '--output' and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] == '--keep-ratio' and i + 1 < len(args):
            try:
                keep_ratio = float(args[i + 1])
                if not 0 < keep_ratio <= 1.0:
                    print("❌ Error: --keep-ratio debe estar entre 0 y 1.0")
                    return
            except ValueError:
                print("❌ Error: --keep-ratio debe ser un número")
                return
            i += 2
        elif args[i] in ['--help', '-h']:
            print_help()
            return
        else:
            print(f"❌ Argumento desconocido: {args[i]}")
            print_help()
            return
    
    # Ejecutar optimización
    optimize_geojson(input_file, output_file, keep_ratio)

def print_help():
    print("""
🌳 Optimizador de GeoJSON para Madtrees

Uso:
    python optimize-geojson.py [opciones]

Opciones:
    --input <archivo>       Archivo GeoJSON de entrada (default: trees.geojson)
    --output <archivo>      Archivo GeoJSON de salida (default: trees-data.geojson)
    --keep-ratio <ratio>    Ratio de árboles a mantener (default: 1.0)
                            Ejemplos: 1.0 (todos), 0.5 (50%), 0.25 (25%)
    --help, -h              Mostrar esta ayuda

Ejemplos:
    # Optimizar manteniendo todos los árboles (solo reduce campos)
    python optimize-geojson.py
    
    # Mantener 50% de los árboles
    python optimize-geojson.py --keep-ratio 0.5
    
    # Mantener 25% de los árboles
    python optimize-geojson.py --keep-ratio 0.25 --output trees-reduced.geojson
    """)

if __name__ == '__main__':
    main()
