# vlan_check.py
def validar_vlan(numero):
    if 1 <= numero <= 1005:
        return "Normal"
    elif 1006 <= numero <= 4094:
        return "Extendido"
    else:
        return "Fuera de rango (debe ser entre 1 y 4094)"

if __name__ == "__main__":
    try:
        vlan = int(input("Ingrese el número de VLAN: "))
        rango = validar_vlan(vlan)
        print(f"La VLAN {vlan} pertenece al rango {rango}.")
    except ValueError:
        print("Por favor, ingrese un número válido.")
