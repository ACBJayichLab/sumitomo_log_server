from sumitomo_f70 import SumitomoF70

with SumitomoF70(com_port='COM11') as f70:
    
    f70.set_off()