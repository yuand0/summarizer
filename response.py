def success(data=None,message="ok"):
    return {"code": 0, "data":data,"message":message}

def error(code,message):
    return {"code":code,"data":None,"message":message}
    
        
