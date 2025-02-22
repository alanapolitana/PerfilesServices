
""" class BMIChartView(APIView):

    def get(self, request):
        # Generar el DataFrame
        df = generate_bmi_dataframe()

        # Filtrar registros del usuario logueado
        user_data = df[df['User'] == request.user.email]

        if user_data.empty:
            return HttpResponse("No hay datos de IMC para el usuario logueado.", status=404)

        # Asegúrate de que la columna 'Date' sea de tipo datetime
        user_data.loc[:, 'Date'] = pd.to_datetime(user_data['Date'], errors='coerce')
        user_data = user_data.dropna(subset=['Date']).sort_values(by='Date')

        # Definir los colores según el IMC con subcategorías
        def get_bmi_color(bmi):
            if bmi < 18.5:
                return 'red'  # Bajo peso
            elif 18.5 <= bmi < 24.9:
                return 'green'  # Saludable
            elif 25 <= bmi < 27:
                return 'yellow'  # Sobrepeso grado I
            elif 27 <= bmi < 30:
                return 'orange'  # Sobrepeso grado II
            elif 30 <= bmi < 35:
                return 'purple'  # Obesidad grado I
            elif 35 <= bmi < 40:
                return 'darkviolet'  # Obesidad grado II
            else:
                return 'brown'  # Obesidad grado III (Mórbida)

        user_data['Color'] = user_data['BMI'].apply(get_bmi_color)

 
 
        def calculate_ideal_weight(height):
    # Convertir la altura a float si es un decimal
          height = float(height) if isinstance(height, Decimal) else height
          return 21.7 * (height ** 2)
 
        # Suponiendo que la altura del usuario está almacenada en el DataFrame
        user_data['IdealWeight'] = user_data['Height'].apply(calculate_ideal_weight)

        # Crear el gráfico
        plt.figure(figsize=(10, 6))

        # Graficar la línea continua que conecta los puntos
        plt.plot(user_data['Date'], user_data['BMI'], color='gray', linestyle='-', linewidth=1, alpha=0.7)

        # Graficar los puntos de IMC con colores definidos
        scatter = plt.scatter(user_data['Date'], user_data['BMI'], c=user_data['Color'], s=100, edgecolors='k', alpha=0.7)

        # Añadir etiquetas de IMC en cada punto
        for i, row in user_data.iterrows():
            plt.text(row['Date'], row['BMI'], f'{row["BMI"]:.1f}', fontsize=9, ha='right')

        # Graficar la línea del peso ideal (IMC de 21.7)
        plt.plot(user_data['Date'], [21.7] * len(user_data), color='blue', linestyle='--', label='Peso Ideal (IMC = 21.7)')

        # Etiquetas y configuración
        plt.xlabel('Fecha')
        plt.ylabel('IMC')
        plt.title('Evolución del IMC')

        # Añadir leyenda explicativa de colores
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Bajo peso (IMC < 18.5)', markerfacecolor='red', markersize=10, alpha=0.7),
            Line2D([0], [0], marker='o', color='w', label='Saludable (18.5 ≤ IMC < 24.9)', markerfacecolor='green', markersize=10, alpha=0.7),
            Line2D([0], [0], marker='o', color='w', label='Sobrepeso grado I (25 ≤ IMC < 27)', markerfacecolor='yellow', markersize=10, alpha=0.7),
            Line2D([0], [0], marker='o', color='w', label='Sobrepeso grado II (27 ≤ IMC < 30)', markerfacecolor='orange', markersize=10, alpha=0.7),
            Line2D([0], [0], marker='o', color='w', label='Obesidad grado I (30 ≤ IMC < 35)', markerfacecolor='purple', markersize=10, alpha=0.7),
            Line2D([0], [0], marker='o', color='w', label='Obesidad grado II (35 ≤ IMC < 40)', markerfacecolor='darkviolet', markersize=10, alpha=0.7),
            Line2D([0], [0], marker='o', color='w', label='Obesidad grado III (IMC ≥ 40)', markerfacecolor='brown', markersize=10, alpha=0.7),
            Line2D([0], [0], color='blue', linestyle='--', label='Peso Ideal (IMC = 21.7)', markersize=10, alpha=0.7)
        ]
        plt.legend(handles=legend_elements, loc='upper right')

        plt.grid(True)
        plt.tight_layout()

        # Activar el cursor interactivo para mostrar el valor del IMC
        cursor = mplcursors.cursor(scatter, hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(f'IMC: {user_data.iloc[sel.target.index]["BMI"]:.1f}\nPeso: {user_data.iloc[sel.target.index]["Weight"]} kg'))

        # Guardar el gráfico en un buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        # Devolver el gráfico como respuesta HTTP
        return HttpResponse(buf, content_type='image/png') """