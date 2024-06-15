import importlib
import os
from . import sym_2_func, non_numba_func as nnb, sym_2_Jac

def converter(folder_name, num_output_folder, jac_output_folder, to_generate):
    os.makedirs(num_output_folder, exist_ok=True)
    os.makedirs(jac_output_folder, exist_ok=True)
    files = [file for file in os.listdir(folder_name) if 'model_info' not in file and 'sym' in file]

    for file_name in files:
        module_path = f"{folder_name}.{file_name.split('.')[0]}"

        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            print(f"Failed to import module {module_path}: {e}")
            continue

        prefix = file_name.split('_')[0][:3]
        init_function_name = f"{prefix}_init"

        try:
            sym_models = {
                "ode": getattr(module, f"symbolic_{prefix}_ode")(),
                "abe": getattr(module, f"symbolic_{prefix}_ae")(),
                "exe": getattr(module, f"symbolic_{prefix}_exe")()
            }
        except AttributeError as e:
            print(f"Failed to get symbolic functions from {module_path}: {e}")
            continue

        file_name_split = file_name.split('.')[0].split('_')
        model_name = '_'.join(file_name_split[1:-1])
        file_name_prefix = '_'.join(file_name_split[:-1])
        num_file_path = os.path.join(num_output_folder, f'{file_name_prefix}_num.py')
        jac_file_path = os.path.join(jac_output_folder, f'{file_name_prefix}_jac.py')

        model_info_module_path = f'{folder_name}.{file_name_split[0]}_model_info'

        try:
            model_info_module = importlib.import_module(model_info_module_path)
            model_metadata = getattr(model_info_module, 'model_metadata', None)
        except ImportError as e:
            print(f"Failed to import model info module {model_info_module_path}: {e}")
            continue
        except AttributeError as e:
            print(f"Failed to get model_metadata from {model_info_module_path}: {e}")
            continue

        if model_metadata:
            for i, metadata in model_metadata.items():
                if metadata['name'] == model_name:
                    break
            try:
                if to_generate == 'num':
                    sym_2_func.generate_numba_functions(sym_models, model_metadata[i], file_name, num_file_path)
                elif to_generate == 'jac':
                    sym_2_Jac.sym2num(sym_models, model_metadata[i], file_name, jac_file_path)
            except Exception as e:
                print(f"Failed to generate functions or Jacobians for {file_name}: {e}")
                continue

        if to_generate == 'num':
            try:
                function_lines = nnb.extract_function(os.path.join(folder_name, file_name), init_function_name)
                nnb.update_or_append_function(num_file_path, function_lines, init_function_name)
            except Exception as e:
                print(f"Failed to extract or update functions for {file_name}: {e}")

        print(f"Processing complete for: {file_name}")

def to_num(folder_name, num_output_folder):
    converter(folder_name, num_output_folder, num_output_folder, 'num')

def to_jac(folder_name, jac_output_folder):
    converter(folder_name, jac_output_folder, jac_output_folder, 'jac')
