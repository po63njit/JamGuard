from __future__ import annotations

def make_file_signal_source_config(iq_file:str, fs:int, channels_1c:int=8)->str:
    return f"""[GNSS-SDR]\nGNSS-SDR.internal_fs_sps={fs}\nSignalSource.implementation=File_Signal_Source\nSignalSource.filename={iq_file}\nSignalSource.item_type=gr_complex\nSignalSource.sampling_frequency={fs}\nChannels_1C.count={channels_1c}\nChannels.in_acquisition={channels_1c}\n"""

def replace_signal_source_filename(config_text:str,new_filename:str)->str:
    lines=[]
    replaced=False
    for ln in config_text.splitlines():
        if ln.startswith("SignalSource.filename="):
            lines.append(f"SignalSource.filename={new_filename}")
            replaced=True
        else:
            lines.append(ln)
    if not replaced:
        lines.append(f"SignalSource.filename={new_filename}")
    return "\n".join(lines)+"\n"
