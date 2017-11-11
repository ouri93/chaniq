
def build_std_pool_name(vs_env, vs_dnsname, vs_port):
    return vs_env + '_P_' + vs_dnsname + '_' + vs_port

def build_std_vs_name(vs_env, vs_dnsname, vs_port):
    return vs_env + '_VS_' + vs_dnsname + '_' + vs_port
