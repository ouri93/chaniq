
def build_std_pool_name(env, poolName, vs_port):
    return env + '_P_' + poolName + '_' + vs_port
def build_std_mon_name(env, monName):
    return env + '_MON_' + monName
def build_std_vs_name(env, vs_dnsname, vs_port):
    return env + '_VS_' + vs_dnsname + '_' + vs_port

def build_std_ir_name(ir_env, irdg_name, ir_type):
    if ir_type == 'iRule':
        return ir_env + '_IR_' + irdg_name
    elif ir_type == 'Data Group':
        return ir_env + '_DG_' + irdg_name

