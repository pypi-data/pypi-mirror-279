import re
import sympy as sp
import os

def eq_to_code(eq, rep_dict, tmp_var_counter):
    """
    Convert a symbolic equation to a string of code, handling Piecewise expressions.
    """
    tmp_vars = []

    if not isinstance(eq, int) and eq.has(sp.Piecewise):
        # Handle Piecewise case
        piece_eqs = eq.atoms(sp.Piecewise)
        for piece_eq in piece_eqs:
            pieces = piece_eq.args
            piece_code_lines = []
            tmp_piecewise_name = f"tmp_piecewise_{tmp_var_counter[0]}"
            tmp_var_counter[0] += 1
            for i, (expr, cond) in enumerate(pieces):
                expr_code, tmp_vars_expr = eq_to_code(expr, rep_dict, tmp_var_counter)
                cond_code, tmp_vars_cond = eq_to_code(cond, rep_dict, tmp_var_counter)
                if i == 0:
                    piece_code_lines.append(f"if {cond_code}:")
                elif cond_code == "True":
                    piece_code_lines.append(f"else:")
                else:
                    piece_code_lines.append(f"elif {cond_code}:")
                piece_code_lines.append(f"    {tmp_piecewise_name} = {expr_code}")
                tmp_vars.extend(tmp_vars_expr + tmp_vars_cond)
            # piece_code_lines.append(f"else:")
            # piece_code_lines.append(f"    {tmp_piecewise_name} = 0")
            tmp_vars.append((tmp_piecewise_name, piece_code_lines))
            eq = eq.subs(piece_eq, sp.Symbol(tmp_piecewise_name))

    # Convert the final expression to string and replace variables
    code_str = str(eq)
    for key, value in rep_dict.items():
        code_str = code_str.replace(key, value)
    # code_str = code_str.replace("pi", "np.pi")
    code_str = re.sub(r'\bpi\b', 'np.pi', code_str)

    return code_str, tmp_vars

def preprocess_mod(eq, rep_dict):
    """
    Preprocess the equation to replace Mod(x, y) with x if y is not a variable.
    """
    if not isinstance(eq, int) and eq.has(sp.Mod):
        mod_eqs = eq.atoms(sp.Mod)
        for mod_eq in mod_eqs:
            a, b = mod_eq.args
            b_code = str(b)
            for key, value in rep_dict.items():
                b_code = b_code.replace(key, value)
            if b_code not in rep_dict.values():
                eq = eq.subs(mod_eq, a)
    return eq

def sym2num(sym_model, model_param, name, path="."):
    # Variable information extraction
    ss_var = model_param['state_variable']
    ab_var = model_param['algebraic_variable']
    ex_var = model_param['extern_variable']
    param = model_param['parameter']
    x_dim, y_dim, u_dim, p_dim = len(ss_var), len(ab_var), len(ex_var), len(param)
    i = 0
    ss_rep_dict = {}
    for key, value in ss_var.items():
        x_rep = f"x[{i}]"
        ss_rep_dict.update({f"x{i}": x_rep})
        i += 1
    i = 0
    ab_rep_dict = {}
    for key, value in ab_var.items():
        y_rep = f"y[{i}]"
        ab_rep_dict.update({f"y{i}": y_rep})
        i += 1
    i = 0
    ex_rep_dict = {}
    for key, value in ex_var.items():
        ex_rep = f"u[{i}][0]"
        if value['var_num'] == 1:
            ex_rep = f"u[{i}][0]"
        else:
            ex_rep = f"u[{i}]"
        ex_rep_dict.update({f"u{i}": ex_rep})
        i += 1
    i = 0
    param_rep_dict = {}
    all_var_num_one = all(p['var_num'] == 1 for p in param.values())
    for key, value in param.items():
        p_rep = f"p[{i}][0][0]"
        if all_var_num_one:
            p_rep = f"p[{i}][0]"
            param_rep_dict.update({f"p{i}": p_rep})
        elif isinstance(value['var_num'], int):
            if value['var_num'] == 1:  # Number
                p_rep = f"p[{i}][0][0]"
                param_rep_dict.update({f"p{i}": p_rep})
            else:  # vector
                p_rep = f"p[{i}][0]"
                param_rep_dict.update({f"p{i}": p_rep})
        elif len(value['var_num']) == 2:  # matrix
            p_rep = f"p[{i}]"
            param_rep_dict.update({f"p{i}": p_rep})
            for j in range(value['var_num'][0]):
                for k in range(value['var_num'][1]):
                    p_ele_rep = f"p[{i}][{j}][{k}]"
                    param_rep_dict.update({f"p_{i}_{j}{k}": p_ele_rep})
        else:
            print(f"wrong var_num of parameter {i}")
        i += 1

    # Begin constructing the function as a string
    func_str = "import numpy as np\nfrom numba import jit\n\n"

    combined_rep_dict = {**param_rep_dict, **ss_rep_dict, **ab_rep_dict, **ex_rep_dict}

    # Generate Jacobian functions
    jacobian_funcs = [
        ("dfx", "x"),
        ("dfy", "y"),
        ("dfu", "u"),
        ("dgx", "x"),
        ("dgy", "y"),
        ("dgu", "u")
    ]

    for jac_name, var_name in jacobian_funcs:
        if jac_name.startswith("df"):
            x, y, u, p, symbolic_eqs = sym_model["ode"]
            if var_name == "x":
                var_symbols = sp.symbols(f'x:{x_dim}')
            elif var_name == "y":
                var_symbols = sp.symbols(f'y:{y_dim}')
            elif var_name == "u":
                var_symbols = sp.symbols(f'u:{u_dim}')
        else:
            x, y, u, p, symbolic_eqs = sym_model["abe"]
            if var_name == "x":
                var_symbols = sp.symbols(f'x:{x_dim}')
            elif var_name == "y":
                var_symbols = sp.symbols(f'y:{y_dim}')
            elif var_name == "u":
                var_symbols = sp.symbols(f'u:{u_dim}')
        
        # Preprocess equations to handle Mod case
        symbolic_eqs = [preprocess_mod(eq, combined_rep_dict) for eq in symbolic_eqs]

        jac_eqs = sp.Matrix(symbolic_eqs).jacobian(var_symbols)

        func_str += f"@jit(nopython=True)\ndef {name[:3]}_{jac_name}(x, y, u, p):\n"
        if jac_eqs.shape == (0, 0):
            func_str += f"    return np.full((1, 1), np.nan, dtype=np.float64)\n\n"
        else:
            func_str += f"    jac = np.zeros(({jac_eqs.shape[0]}, {jac_eqs.shape[1]}))\n"
            for i, row in enumerate(jac_eqs.tolist()):
                for j, eq in enumerate(row):
                    if eq != 0:
                        eq_code, tmp_vars = eq_to_code(eq, combined_rep_dict, [0])
                        for tmp_var, tmp_code in tmp_vars:
                            if isinstance(tmp_code, list):
                                for line in tmp_code:
                                    func_str += f"    {line}\n"    
                            else:        
                                func_str += f"    {tmp_var} = {tmp_code}\n"
                        func_str += f"    jac[{i}, {j}] = {eq_code}\n"
            func_str += "    return jac\n\n"

    # Write the function string to a Python file
    with open(path, "w") as file:
        file.write(func_str)
