import os
import re
from pathlib import Path

def fix_dialogs_in_file(file_path):
    """Corrige los diálogos en un archivo"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f" Error leyendo {file_path}: {e}")
        return False
    
    original_content = content
    changes_made = []
    
    # Patrón 1: self.page.dialog = dialog \n dialog.open = True \n self.page.update()
    pattern1 = r'(\s*)self\.page\.dialog = (dialog)\s*\n\s*\2\.open = True\s*\n\s*self\.page\.update\(\)'
    replacement1 = r'\1self.page.show_dialog(\2)'
    
    new_content = re.sub(pattern1, replacement1, content, flags=re.MULTILINE)
    if new_content != content:
        changes_made.append("Convertido page.dialog a show_dialog")
        content = new_content
    
    # Patrón 2: dialog.open = False \n self.page.update()
    pattern2 = r'(\s*)dialog\.open = False\s*\n\s*self\.page\.update\(\)'
    replacement2 = r'''\1if self.page.dialog:
\1    self.page.dialog.open = False
\1    self.page.update()'''
    
    new_content = re.sub(pattern2, replacement2, content, flags=re.MULTILINE)
    if new_content != content:
        changes_made.append("Mejorado cierre de diálogo")
        content = new_content
    
    # Patrón 3: Variante con variable dialog diferente
    pattern3 = r'(\s*)self\.page\.dialog = ([a-zA-Z_][a-zA-Z0-9_]*)\s*\n\s*\2\.open = True\s*\n\s*self\.page\.update\(\)'
    replacement3 = r'\1self.page.show_dialog(\2)'
    
    new_content = re.sub(pattern3, replacement3, content, flags=re.MULTILINE)
    if new_content != content:
        changes_made.append("Convertido page.dialog con variable personalizada")
        content = new_content
    
    # Patrón 4: Cerrar con variable personalizada
    pattern4 = r'(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\.open = False\s*\n\s*self\.page\.update\(\)'
    replacement4 = r'''\1if self.page.dialog:
\1    self.page.dialog.open = False
\1    self.page.update()'''
    
    new_content = re.sub(pattern4, replacement4, content, flags=re.MULTILINE)
    if new_content != content:
        changes_made.append("Mejorado cierre con variable personalizada")
        content = new_content
    
    # Solo escribir si hubo cambios
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f" Corregido: {file_path}")
            for change in changes_made:
                print(f"   - {change}")
            return True
        except Exception as e:
            print(f" Error escribiendo {file_path}: {e}")
            return False
    else:
        print(f"  Sin cambios: {file_path}")
        return False

def backup_files(files_to_backup):
    """Crea backup de los archivos antes de modificar"""
    backup_dir = Path("backup_dialogs")
    backup_dir.mkdir(exist_ok=True)
    
    for file_path in files_to_backup:
        try:
            backup_path = backup_dir / file_path.name
            backup_path.write_text(file_path.read_text(encoding='utf-8'), encoding='utf-8')
            print(f" Backup creado: {backup_path}")
        except Exception as e:
            print(f"  Error creando backup de {file_path}: {e}")

def find_dialog_files(root_dir):
    """Encuentra archivos que contienen diálogos"""
    python_files = list(Path(root_dir).rglob("*.py"))
    dialog_files = []
    
    for file_path in python_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            if 'page.dialog' in content or 'AlertDialog' in content:
                dialog_files.append(file_path)
        except Exception as e:
            print(f"  Error leyendo {file_path}: {e}")
    
    return dialog_files

def main():
    """Corrige todos los archivos Python con diálogos"""
    
    print(" Iniciando corrección de diálogos...")
    print("=" * 50)
    
    root_dir = "perdidas_matanzas_app"
    
    if not Path(root_dir).exists():
        print(f" Directorio {root_dir} no encontrado")
        return
    
    # Encontrar archivos con diálogos
    print(" Buscando archivos con diálogos...")
    dialog_files = find_dialog_files(root_dir)
    
    if not dialog_files:
        print("ℹ  No se encontraron archivos con diálogos")
        return
    
    print(f" Encontrados {len(dialog_files)} archivos con diálogos:")
    for file_path in dialog_files:
        print(f"   - {file_path}")
    
    # Crear backup
    print("\n Creando backup de archivos...")
    backup_files(dialog_files)
    
    # Procesar archivos
    print("\n  Procesando archivos...")
    print("-" * 30)
    
    fixed_count = 0
    
    for file_path in dialog_files:
        if fix_dialogs_in_file(file_path):
            fixed_count += 1
    
    print("\n" + "=" * 50)
    print(f" Proceso completado:")
    print(f"   - Archivos procesados: {len(dialog_files)}")
    print(f"   - Archivos corregidos: {fixed_count}")
    print(f"   - Backup creado en: ./backup_dialogs/")
    
    if fixed_count > 0:
        print("\n Recomendaciones:")
        print("   1. Prueba la aplicación para verificar que los diálogos funcionan")
        print("   2. Si hay problemas, restaura desde el backup")
        print("   3. Elimina la carpeta backup_dialogs cuando todo funcione bien")

if __name__ == "__main__":
    main()
