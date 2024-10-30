from sumitomo_f70 import SumitomoF70

with SumitomoF70(com_port='COM11') as f70:
    # Insert commands here (full list in docs)
    # For example:
    print("Attempting command")
    t1, t2, t3, t4 = f70.read_all_temperatures()
    print("Temperatures:")
    #He,H20 Out, H20 In, Inactive
    print(t1,t2,t3,t4)
    a,b=f70.read_all_pressures()
    print("Pressures:")
    print(a,b)
    c=f70.read_id()
    print("id:")
    print(c)
    d,e=f70.read_status_bits()
    print("Status")
    print(d,e)