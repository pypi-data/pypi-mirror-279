import sympy as sp
import os
import re

def eq_to_code(eq, rep_dict, tmp_var_counter):
    """
    Convert a symbolic equation to a string of code, handling Piecewise expressions and Mod.
    """
    tmp_vars = []

    if not isinstance(eq, int) and eq.has(sp.Mod):
        # Handle Mod case
        mod_eqs = eq.atoms(sp.Mod)
        for mod_eq in mod_eqs:
            a, b = mod_eq.args
            a_code, tmp_vars_a = eq_to_code(a, rep_dict, tmp_var_counter)
            b_code, tmp_vars_b = eq_to_code(b, rep_dict, tmp_var_counter)
            mod_code = f"(({a_code}) % ({b_code}))"
            tmp_var_name = f"tmp_mod_{tmp_var_counter[0]}"
            tmp_var_counter[0] += 1
            tmp_vars.extend(tmp_vars_a + tmp_vars_b + [(tmp_var_name, mod_code)])
            eq = eq.subs(mod_eq, sp.Symbol(tmp_var_name))

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

def generate_numba_functions(sym_models, model_param, name, path="."):
    # variable information extraction
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
    # get max var_num in param:
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

    tmp_var_counter = [0]

    # ode equation
    x, y, u, p, symbolic_eqs = sym_models["ode"]

    func_str += "@jit(nopython=True)\ndef " + name[0:3] + "_ode(x, y, u, p):\n"
    if symbolic_eqs == sp.Symbol("Empty"):
        func_str += f"    return np.full((1, ), np.nan, dtype=np.float64)\n\n"
    else:
        func_str += "    f = np.zeros({})\n".format(len(symbolic_eqs))
        for i, eq in enumerate(symbolic_eqs):
            eq_code, tmp_vars = eq_to_code(eq, combined_rep_dict, tmp_var_counter)
            for tmp_var in tmp_vars:
                if isinstance(tmp_var[1], list):
                    for line in tmp_var[1]:
                        func_str += f"    {line}\n"
                else:
                    func_str += f"    {tmp_var[0]} = {tmp_var[1]}\n"
            func_str += "    f[{}] = {}\n".format(i, eq_code)
        # Finalize the function string with a return statement
        func_str += "    return f\n\n\n"

    # abe equation
    x, y, u, p, symbolic_eqs = sym_models["abe"]
    func_str += "@jit(nopython=True)\ndef " + name[0:3] + "_ae(x, y, u, p):\n"
    if symbolic_eqs == sp.Symbol("Empty"):
        func_str += f"    return np.full((1, ), np.nan, dtype=np.float64)\n\n"
    else:
        func_str += "    f = np.zeros({})\n".format(len(symbolic_eqs))
        for i, eq in enumerate(symbolic_eqs):
            eq_code, tmp_vars = eq_to_code(eq, combined_rep_dict, tmp_var_counter)
            for tmp_var in tmp_vars:
                if isinstance(tmp_var[1], list):
                    for line in tmp_var[1]:
                        func_str += f"    {line}\n"
                else:
                    func_str += f"    {tmp_var[0]} = {tmp_var[1]}\n"
            func_str += "    f[{}] = {}\n".format(i, eq_code)
        func_str += "    return f\n\n"

    # exe equation
    x, y, u, p, symbolic_eqs = sym_models["exe"]
    func_str += "@jit(nopython=True)\ndef " + name[0:3] + "_exe(x, y, u, p):\n"
    if symbolic_eqs == sp.Symbol("Empty"):
        func_str += f"    return np.full((1, ), np.nan, dtype=np.float64)\n\n"
    else:
        func_str += "    f = np.zeros({})\n".format(len(symbolic_eqs))
        for i, eq in enumerate(symbolic_eqs):
            eq_code, tmp_vars = eq_to_code(eq, combined_rep_dict, tmp_var_counter)
            for tmp_var in tmp_vars:
                if isinstance(tmp_var[1], list):
                    for line in tmp_var[1]:
                        func_str += f"    {line}\n"
                else:
                    func_str += f"    {tmp_var[0]} = {tmp_var[1]}\n"
            func_str += "    f[{}] = {}\n".format(i, eq_code)
        func_str += "    return f\n\n"

    with open(path, "w") as file:
        file.write(func_str)
        