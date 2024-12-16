def a_zA_z0_9(inp) -> bool :
    for _ in inp :
        if _ not in "qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP1234567890_" :
            return False
    return True
