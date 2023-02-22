

def formatMktCap(mktCap):
    
    if mktCap >=1**12:
        mktCap = round(mktCap / 1**12,2)
        return f'{mktCap}T'
    elif mktCap >=1**9:
        mktCap = round(mktCap / 1**9,2)
        return f'{mktCap}B'
    elif mktCap >=1**6:
        mktCap = round(mktCap / 1**6,2)
        return f'{mktCap}M'
    else:
        
        return str(round(mktCap,2))