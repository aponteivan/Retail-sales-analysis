import numpy as np

def cargar_datos(ruta_archivo):
    # Cargar las columnas numéricas (Age, Quantity, Price per Unit, Total Amount)
    datos_numericos = np.genfromtxt(ruta_archivo, delimiter=',', skip_header=1, usecols=(4, 6, 7, 8))
    
    # Cargar columnas de texto (Transaction ID, Date, Customer ID, Gender, Product Category)
    datos_texto = np.genfromtxt(ruta_archivo, delimiter=',', skip_header=1, usecols=(0, 1, 2, 3, 5), dtype=str)
    
    return datos_numericos, datos_texto

def calcular_ventas_por_categoria(datos_numericos, datos_texto):
    # Obtener categorías únicas (Product Category está en la columna 4 de datos_texto)
    categorias_unicas = np.unique(datos_texto[:, 4])

    # Calcular el total de ventas por categoría
    ventas_por_categoria = np.zeros_like(categorias_unicas, dtype=float)
    for i, categoria in enumerate(categorias_unicas):
        # Filtrar por categoría de producto
        indices_categoria = datos_texto[:, 4] == categoria
        # Multiplica Quantity (columna 1) por Price per Unit (columna 2) para obtener las ventas
        ventas_por_categoria[i] = np.sum(datos_numericos[indices_categoria, 1] * datos_numericos[indices_categoria, 2])

    # Identificar categoría con mayores y menores ventas
    indice_max = np.argmax(ventas_por_categoria)
    indice_min = np.argmin(ventas_por_categoria)
    categoria_mas_vendida = categorias_unicas[indice_max]
    categoria_menos_vendida = categorias_unicas[indice_min]

    print("Categoría con mayores ventas:", categoria_mas_vendida)
    print("Categoría con menores ventas:", categoria_menos_vendida)

    return categorias_unicas, ventas_por_categoria

def calcular_promedio_ventas_diarias(datos_numericos, datos_texto):
    # Convertir la columna de fechas (columna 1 de datos_texto) a formato de fechas NumPy (np.datetime64)
    fechas = np.array([np.datetime64(fecha, 'D') for fecha in datos_texto[:, 1]])

    # Extraer categorías únicas
    categorias_unicas = np.unique(datos_texto[:, 4])

    # Crear un diccionario para almacenar ventas diarias por categoría
    ventas_diarias_por_categoria = {categoria: [] for categoria in categorias_unicas}
    
    # Obtener días únicos
    dias_unicos = np.unique(fechas)

    # Recorrer cada día único y sumar ventas por categoría en ese día
    for dia in dias_unicos:
        indices_dia = fechas == dia
        for categoria in categorias_unicas:
            indices_categoria = datos_texto[:, 4] == categoria
            indices_validos = indices_dia & indices_categoria
            # Multiplica Price per Unit (columna 2) por Quantity (columna 1) para obtener ventas
            ventas_dia = np.sum(datos_numericos[indices_validos, 2] * datos_numericos[indices_validos, 1])  
            ventas_diarias_por_categoria[categoria].append(ventas_dia)

    # Calcular el promedio de ventas diarias por categoría
    promedio_ventas_diarias = {}
    for categoria in categorias_unicas:
        ventas_diarias = ventas_diarias_por_categoria[categoria]
        promedio_ventas_diarias[categoria] = np.mean(ventas_diarias) if len(ventas_diarias) > 0 else 0

    return promedio_ventas_diarias

if __name__ == "__main__":
    ruta_archivo = 'C:/Users/ivan_/Documents/bootcamp/GIT/Retail-sales-analysis/retail_sales_dataset.csv'
    
    # Cargar los datos
    datos_numericos, datos_texto = cargar_datos(ruta_archivo)
    print(datos_numericos)
    print(datos_numericos.shape)

    # 2. Exploración de Datos: Calcular ventas por categoría
    categorias_unicas, ventas_por_categoria = calcular_ventas_por_categoria(datos_numericos, datos_texto)
    
    # 3. Calcular promedio de ventas diarias por categoría
    promedio_ventas_diarias = calcular_promedio_ventas_diarias(datos_numericos, datos_texto)
    
    # Mostrar el promedio de ventas diarias por categoría
    print("\nPromedio de ventas diarias por categoría:")
    for categoria, promedio in promedio_ventas_diarias.items():
        print(f"Categoría {categoria}: Promedio de ventas diarias: {promedio}")

    # 4. Manipulación de Datos: Filtrar por categoría específica (ejemplo: categoría 'Electronics')
    categoria_especifica = 'Electronics'
    datos_filtrados = datos_numericos[datos_texto[:, 4] == categoria_especifica]

    if datos_filtrados.size > 0:  # Verificar si hay datos filtrados
        # - Suma: Cantidad total vendida
        cantidad_total = np.sum(datos_filtrados[:, 1])  # Columna 1 es 'Quantity'
        print(f"\nCantidad total vendida de la categoría {categoria_especifica}: {cantidad_total}")

        # - Resta: Diferencia entre la cantidad máxima y mínima vendida
        cantidad_maxima = np.max(datos_filtrados[:, 1])  # Columna 1 es 'Quantity'
        cantidad_minima = np.min(datos_filtrados[:, 1])  # Columna 1 es 'Quantity'
        diferencia_cantidades = cantidad_maxima - cantidad_minima
        print(f"Diferencia entre la cantidad máxima y mínima: {diferencia_cantidades}")

        # - Multiplicación: Ingreso total por categoría
        ingreso_total = np.sum(datos_filtrados[:, 1] * datos_filtrados[:, 2])  # Cantidad * Precio por unidad
        print(f"Ingreso total de la categoría {categoria_especifica}: {ingreso_total}")

        # - División: Promedio de precio unitario
        precio_promedio = np.mean(datos_filtrados[:, 2])  # Columna 2 es 'Price per Unit'
        print(f"Precio promedio de la categoría {categoria_especifica}: {precio_promedio}")
    else:
        print(f"\nNo se encontraron datos para la categoría {categoria_especifica}.")
