
def build_std_pool_name(vs_env, vs_dnsname, vs_port):
    return vs_env + '_P_' + vs_dnsname + '_' + vs_port
def build_std_mon_name(vs_env, vs_dnsname, vs_port):
    return vs_env + '_MON_' + vs_dnsname + '_' + vs_port
def build_std_vs_name(vs_env, vs_dnsname, vs_port):
    return vs_env + '_VS_' + vs_dnsname + '_' + vs_port
def build_std_ir_name(vs_env, vs_dnsname, vs_port, ir_type):
    if ir_type == 'iRule':
        return vs_env + '_IR_' + vs_dnsname + '_' + vs_port
    elif ir_type == 'Data Group':
        return vs_env + '_DG_' + vs_dnsname + '_' + vs_port