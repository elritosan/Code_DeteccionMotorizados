from DataBase.PostgreSQLConnection import ClassPostgreSQLConnection
import psycopg2

class ClassTblMotorizadosPostgreSQL:

    def select_all_from_motorizados(self):
        """Obtiene todos los registros de la tabla 'dsa.motorizados'."""
        query = "SELECT * FROM dsa.motorizados;"
        try:
            ClassPostgreSQLConnection.execute_query(query)
            print("✅ Consulta SELECT ejecutada exitosamente en la tabla 'dsa.motorizados'.")
        except psycopg2.Error as e:
            print(f"❌ Error ejecutando SELECT en la tabla 'dsa.motorizados': {e}")

    def insert_into_motorizados(self, placa, personas, cascos):
        """Inserta un nuevo registro en la tabla 'dsa.motorizados'."""
        query = "INSERT INTO dsa.motorizados (placa, personas, cascos) VALUES (%s, %s, %s);"
        params = (placa, personas, cascos)
        try:
            ClassPostgreSQLConnection.execute_query(query, params)
            print("✅ Consulta INSERT ejecutada exitosamente en la tabla 'dsa.motorizados'.")
        except psycopg2.Error as e:
            print(f"❌ Error ejecutando INSERT en la tabla 'dsa.motorizados': {e}")