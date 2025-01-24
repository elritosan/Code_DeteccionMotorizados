import psycopg2

class ClassPostgreSQLConnection:

    @classmethod
    def execute_query(cls, query, params=None):
        """Abre la conexión, ejecuta la consulta y la cierra automáticamente"""
        try:
            # Abre la conexión en cada ejecución
            conn = psycopg2.connect(
                dbname="BD_DeteccionMotorizados",
                user="postgres",
                password="admin",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()

            # Ejecuta la consulta
            cur.execute(query, params)
            conn.commit()

        except psycopg2.Error as e:
            if conn:
                conn.rollback()  # Asegura que el rollback solo se hace si la conexión sigue abierta
            print(f"Error en la ejecución de la consulta: {e}")

        finally:
            # Cierra el cursor y la conexión correctamente
            if cur:
                cur.close()
            if conn:
                conn.close()