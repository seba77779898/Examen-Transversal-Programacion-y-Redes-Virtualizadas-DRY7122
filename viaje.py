# viaje.py
import math
import time

# Diccionario de ciudades con sus coordenadas (Lat, Lon)
ciudades = {
    "santiago": (-33.4489, -70.6693),
    "valparaiso": (-33.0472, -71.6127),
    "concepcion": (-36.8201, -73.0444),
    "mendoza": (-32.8895, -68.8458),
    "buenos aires": (-34.6037, -58.3816),
    "cordoba": (-31.4201, -64.1888),
    "rosario": (-32.9595, -60.6615),
}

# Velocidades promedio en km/h
transportes = {
    "auto": 80,
    "bus": 60,
    "tren": 50,
    "avion": 800
}

def haversine(coord1, coord2):
    """Calcula la distancia en kilometros entre dos puntos geograficos."""
    R = 6371  # Radio de la Tierra en km
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def normalizar(texto):
    return texto.strip().lower()

def main():
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE CALCULO DE DISTANCIAS CHILE - ARGENTINA")
        print("="*50)
        
        origen = input("Ingrese Ciudad de Origen (Ej: Santiago, Mendoza): ")
        destino = input("Ingrese Ciudad de Destino (Ej: Buenos Aires, Valparaiso): ")
        
        origen_norm = normalizar(origen)
        destino_norm = normalizar(destino)
        
        if origen_norm not in ciudades or destino_norm not in ciudades:
            print("Error: Una de las ciudades no esta en la base de datos.")
            print("Ciudades disponibles:", ", ".join(ciudades.keys()))
            continue
        
        if origen_norm == destino_norm:
            print("El origen y destino no pueden ser iguales.")
            continue
        
        # Calcular distancia
        coord_origen = ciudades[origen_norm]
        coord_destino = ciudades[destino_norm]
        distancia_km = haversine(coord_origen, coord_destino)
        distancia_millas = distancia_km * 0.621371
        
        # Elegir transporte
        print("\nMedios de transporte disponibles:")
        for idx, (tipo, vel) in enumerate(transportes.items(), 1):
            print(f"  {idx}. {tipo.capitalize()} ({vel} km/h)")
        print("  s. Salir")
        
        opcion = input("Seleccione el numero del transporte o 's' para salir: ").lower()
        
        if opcion == 's':
            print("Saliendo del programa...")
            break
        
        try:
            idx_transporte = int(opcion) - 1
            tipo_transporte = list(transportes.keys())[idx_transporte]
            velocidad = transportes[tipo_transporte]
        except (ValueError, IndexError):
            print("Opcion no valida. Intente de nuevo.")
            continue
        
        # Calcular tiempo
        horas = distancia_km / velocidad
        minutos = horas * 60
        
        # Narrativa del viaje (sin emojis)
        narrativa = f"""
        Ruta: {origen.capitalize()} -> {destino.capitalize()}
        Medio: {tipo_transporte.capitalize()}
        Distancia: {distancia_km:.2f} kilometros | {distancia_millas:.2f} millas
        Duracion estimada: {int(horas)} horas y {int((horas % 1) * 60)} minutos
        Consejo: Lleva tus documentos y disfruta el paisaje.
        """
        print(narrativa)
        
        # Preguntar si quiere hacer otro calculo
        continuar = input("\nDesea calcular otro viaje? (Presione Enter para continuar, 's' para salir): ").lower()
        if continuar == 's':
            print("Hasta luego!")
            break

if __name__ == "__main__":
    main()
