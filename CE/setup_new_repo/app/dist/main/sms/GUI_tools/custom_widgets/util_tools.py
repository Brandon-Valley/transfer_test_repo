# self.duration: 72 --> '1:12'
def sec_to_min_str(total_sec):
    minutes = int(total_sec / 60)
    seconds = int(total_sec % 60)
    sec_str = str(seconds)
    if len(sec_str) < 2:
        sec_str = '0' + sec_str
    return str(minutes) + ':' + sec_str