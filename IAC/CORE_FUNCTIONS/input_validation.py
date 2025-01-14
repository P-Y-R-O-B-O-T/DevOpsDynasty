def a_zA_z0_9(inp) -> bool :
    if len(inp) > 53 :
        return False
    for _ in inp :
        if _ not in "qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP1234567890_" :
            return False
    return True
