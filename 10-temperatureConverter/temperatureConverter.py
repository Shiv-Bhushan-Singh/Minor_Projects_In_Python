def convert():
    value = float(input("Temperature: "))
    unit = input("From (C/F/K): ").upper()
    if unit == "C":
        print(f"F: {value*9/5+32}, K: {value+273.15}")
    elif unit == "F":
        c = (value-32)*5/9
        print(f"C: {c}, K: {c+273.15}")
    elif unit == "K":
        c = value - 273.15
        print(f"C: {c}, F: {c*9/5+32}")

convert()