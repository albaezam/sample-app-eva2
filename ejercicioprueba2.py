import requests
import urllib.parse

# Consumo estimado de combustible promedio (ejemplo: 12 km por litro)
KM_PER_LITER = 12.0

# 1. ACTUALIZACIÓN DE URLS (Agregamos el perfil /car/ en OSRM)
OSM_GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
OSRM_ROUTE_URL = "http://router.project-osrm.org/route/v1/car/"  # <-- Cambiado a /car/

HEADERS = {
    "User-Agent": "Evaluacion2_DRY7122_StudentProject/1.0"
}

def obtener_coordenadas(ciudad):
    """Convierte el nombre de una ciudad en coordenadas usando OpenStreetMap limitado a Chile"""
    params = {
        "q": ciudad,
        "format": "json",
        "limit": 1,
        "countrycodes": "cl"  # <-- IMPORTANTE: Esto fuerza la búsqueda solo en Chile
    }
    try:
        response = requests.get(OSM_GEOCODE_URL, params=params, headers=HEADERS)
        data = response.json()
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            display_name = data[0]["display_name"].split(",")[0]
            return lon, lat, display_name
        return None
    except Exception as e:
        print(f"Error al buscar la ciudad '{ciudad}': {e}")
        return None

print("====================================================")
print("  Sistema de Planificación de Viajes (OSM & OSRM)   ")
print("====================================================")

while True:
    print("\n--- Nueva Consulta (Presiona 'q' para salir) ---")
    
    origen_input = input("Ciudad de Origen: ").strip()
    if origen_input.lower() == 'q':
        break
        
    destino_input = input("Ciudad de Destino: ").strip()
    if destino_input.lower() == 'q':
        break

    if not origen_input or not destino_input:
        print("Error: El origen y el destino no pueden estar vacíos.")
        continue

    print("Buscando ciudades en OpenStreetMap...")
    
    origen_geo = obtener_coordenadas(origen_input)
    destino_geo = obtener_coordenadas(destino_input)
    
    if not origen_geo or not destino_geo:
        print("Error: No se pudo encontrar una o ambas ciudades en Chile.")
        continue
        
    lon1, lat1, nombre_origen = origen_geo
    lon2, lat2, nombre_destino = destino_geo

    # Construir la URL para OSRM con pasos de narrativa habilitados
    url_osrm = f"{OSRM_ROUTE_URL}{lon1},{lat1};{lon2},{lat2}?overview=full&steps=true"

    try:
        response = requests.get(url_osrm)
        data = response.json()
        
        if data.get("code") == "Ok":
            route = data["routes"][0]
            
            # A. Distancia en KM (de metros a km)
            distancia_km = route["distance"] / 1000.0
            
            # B. Tiempo de viaje desglosado
            tiempo_segundos = int(route["duration"])
            horas = tiempo_segundos // 3600
            minutos = (tiempo_segundos % 3600) // 60
            segundos = tiempo_segundos % 60
            
            # C. Combustible
            combustible_litros = distancia_km / KM_PER_LITER
            
            print("\n================ RESULTADOS DEL VIAJE ================")
            print(f"Ruta: {nombre_origen} -> {nombre_destino}")
            print(f"Distancia: {distancia_km:.2f} km")
            print(f"Duración: {horas} horas, {minutos} minutos y {segundos} segundos")
            print(f"Combustible requerido: {combustible_litros:.2f} litros")
            print("------------------------------------------------------")
            
            # D. Narrativa del viaje
            print("Narrativa del viaje:")
            paso_n = 1
            legs = route.get("legs", [])
            for leg in legs:
                for step in leg.get("steps", []):
                    maneuver = step.get("maneuver", {}).get("type", "Conducir")
                    modifier = step.get("maneuver", {}).get("modifier", "")
                    street = step.get("name", "")
                    
                    # Traducir maniobras comunes de OSRM para cumplir con la narrativa
                    maneuver_es = maneuver.replace("turn", "Girar").replace("depart", "Salir").replace("arrive", "Llegar")
                    
                    instruccion = f"{maneuver_es.title()} {modifier}"
                    if street:
                        instruccion += f" por {street}"
                        
                    if street or modifier:
                        print(f"  {paso_n}. {instruccion}")
                        paso_n += 1
                        
            print("======================================================")
        else:
            print(f"OSRM no pudo calcular la ruta. Motivo: {data.get('code')}")
            
    except Exception as e:
        print(f"Error al conectar con el servidor de rutas: {e}")

print("Saliendo del programa. ¡Buen viaje!")