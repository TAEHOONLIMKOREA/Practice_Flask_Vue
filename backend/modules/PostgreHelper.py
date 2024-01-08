import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from psycopg2 import sql, extensions

db_host = 'keties.iptime.org'
db_port = '55432'
db_name = 'dx_3dp'
db_user = 'keti_superuser'
db_password = 'madcoder'
db_schema = 'hbnu'


class PostgreClient(object):
    def __init__(self):
        # PostgreSQL 연결 정보 저장
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        # PostgreSQL에 연결
        self.conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password)

    def create_schema(self, schema_name):
        self.db_schema = schema_name
        # PostgreSQL에 연결하고 스키마 ff
        try:
            # PostgreSQL에 연결
            with self.conn as conn:
                with conn.cursor() as cursor:
                    # 스키마 생성 쿼리 실행
                    create_schema_query = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
                    cursor.execute(create_schema_query)

                    print(f"스키마 '{schema_name}'가 성공적으로 생성되었습니다.")
        except Exception as e:
            print(f"스키마 생성 중 오류 발생: {e}")

    def create_initial_table(self):
        cur = self.conn.cursor()

        # exceptions handling
        query = f"SELECT 1 FROM information_schema.tables WHERE table_name='{self.db_schema}.machine'"
        cur.execute(query)
        result = cur.fetchone()
        if result is None:
            # Create Machine Table
            cur.execute(f"""
                CREATE TABLE {self.db_schema}.machine(
                    machine_id varchar PRIMARY KEY,
                    machine_type varchar,
                    machine_product varchar, 
                    machine_manufacturer varchar, 
                    machine_printing_size varchar,
                    machine_material varchar,
                    bp_table_name varchar
                    )
                """)

        # exceptions handling
        query = f"SELECT 1 FROM information_schema.tables WHERE table_name='{self.db_schema}.material_master'"
        cur.execute(query)
        result = cur.fetchone()
        if result is None:
            # Create Material Table
            cur.execute(f"""
                CREATE TABLE {self.db_schema}.material_master(
                    material_name varchar PRIMARY KEY,
                    material_lot_table_name varchar,
                    material_use_table_name varchar
                    )
                """)

        # exceptions handling
        query = f"SELECT 1 FROM information_schema.tables WHERE table_name='{self.db_schema}.material_product'"
        cur.execute(query)
        result = cur.fetchone()
        if result is None:
            # Create Material Table
            cur.execute(f"""
                   CREATE TABLE {self.db_schema}.material_product(
                       material_product_id serial PRIMARY KEY,
                       material_name varchar REFERENCES {self.db_schema}.material_master(material_name),
                       material_manufacturer varchar, 
                       material_product_name varchar
                       )
                   """)

            # exceptions handling
        query = f"SELECT 1 FROM information_schema.tables WHERE table_name='{self.db_schema}.material_measurement'"
        cur.execute(query)
        result = cur.fetchone()
        if result is None:
            # Create Material Table
            cur.execute(f"""
                       CREATE TABLE {self.db_schema}.material_measurement(
                           material_measurement_id serial PRIMARY KEY,
                           material_product_id integer REFERENCES {self.db_schema}.material_product(material_product_id),
                           material_measurement_date varchar
                           )
                       """)

        # exceptions handling
        query = f"SELECT 1 FROM information_schema.tables WHERE table_name='{self.db_schema}.design'"
        cur.execute(query)
        result = cur.fetchone()
        if result is None:
            # Create Design Table
            cur.execute(f"""
                CREATE TABLE {self.db_schema}.design(
                    design_id serial PRIMARY KEY,
                    design_date varchar,
                    design_model varchar,
                    design_purpose varchar,
                    design_customer varchar
                    )
                """)
            cur.execute(f"""
                INSERT INTO {self.db_schema}.design (
                    design_date, design_model, design_purpose, design_customer
                    ) VALUES (
                        'Unknown', 'Unknown', 'Unknown', 'Unknown'
                    )
                """)
        # exceptions handling
        query = f"SELECT 1 FROM information_schema.tables WHERE table_name='{self.db_schema}.build_strategy'"
        cur.execute(query)
        result = cur.fetchone()
        if result is None:
            # Create Build Strategy Table
            cur.execute(f"""
                CREATE TABLE {self.db_schema}.build_strategy(
                    bs_id serial PRIMARY KEY,
                    bs_create_date varchar,
                    bs_name varchar,
                    design_ids integer[]
                    )
                """)
            cur.execute(f"""
                INSERT INTO {self.db_schema}.build_strategy (
                    bs_create_date, bs_name
                    ) VALUES (
                        'Unknown', 'Unknown'
                    )
                """)

        self.conn.commit()

    def create_machine_sub_table(self, machine_id):
        cur = self.conn.cursor()

        bp_table_name = "machine_" + machine_id + "_build_process"
        # exceptions handling
        cur.execute(f"SELECT 1 FROM information_schema.tables WHERE table_name='{self.db_schema}.{bp_table_name}'")
        result = cur.fetchone()
        if result is None:
            # Create Build Process Table
            cur.execute(f"""
                CREATE TABLE {self.db_schema}.{bp_table_name}(
                    bp_id serial PRIMARY KEY, 
                    build_date varchar,
                    bs_id integer REFERENCES {self.db_schema}.build_strategy(bs_id),
                    material_name varchar REFERENCES {self.db_schema}.material_master(material_name)
                    )
                """)

        cali_table_name = "machine_" + machine_id + "_cali"
        # exceptions handling
        query = f"SELECT 1 FROM information_schema.tables WHERE table_name='{self.db_schema}.{cali_table_name}'"
        cur.execute(query)
        result = cur.fetchone()
        if result is None:
            # Create Cali Table
            cur.execute(f"""
                CREATE TABLE {self.db_schema}.{cali_table_name}(
                    id serial PRIMARY KEY,
                    cali_date varchar,
                    machine_id varchar REFERENCES {self.db_schema}.machine(machine_id)
                    )
                """)

        self.conn.commit()

    def create_material_sub_table(self, material_name):
        cur = self.conn.cursor()

        material_lot_table_name = material_name + "_lot"
        # exceptions handling
        query = f"SELECT 1 FROM information_schema.tables WHERE table_name='{self.db_schema}.{material_lot_table_name}'"
        cur.execute(query)
        result = cur.fetchone()
        if result is None:
            # Create Material Lot Number Table
            cur.execute(f"""
                CREATE TABLE {self.db_schema}.{material_lot_table_name}(
                    material_lot_id serial PRIMARY KEY,
                    lot_number varchar,
                    purchase_date varchar,
                    Sieving bool,
                    material_manufacturer varchar
                    )
                """)

        material_use_table_name = material_name + "_use"
        # exceptions handling
        query = f"SELECT 1 FROM information_schema.tables WHERE table_name='{self.db_schema}.{material_use_table_name}'"
        cur.execute(query)
        result = cur.fetchone()
        if result is None:
            # Create Material Use Table
            cur.execute(f"""
                CREATE TABLE {self.db_schema}.{material_use_table_name}(
                    date_time varchar,
                    consumption integer,
                    material_lot_id integer REFERENCES {self.db_schema}.{material_lot_table_name}(material_lot_id),
                    machine_id varchar REFERENCES {self.db_schema}.machine(machine_id)
                    )
                """)
        self.conn.commit()

    def InsertOne_MachineMeta(self, machine_id, machine_type, machine_product, machine_manufacturer,
                              machine_printing_size, machine_material):
        cur = self.conn.cursor()
        # Exceptions
        query_id = sql.SQL("SELECT * FROM {}.machine WHERE {} = {}").format(
            sql.Identifier(self.db_schema),
            sql.Identifier("machine_id"),
            sql.Literal(machine_id)
        )
        cur.execute(query_id)
        result = cur.fetchone()
        if result:  # id값이 일치하는 로우가 하나라도 있다면
            return
        # 데이터 삽입 쿼리
        query = f"""
            INSERT INTO {self.db_schema}.machine (
                machine_id, machine_type, machine_product, machine_manufacturer,
                machine_printing_size, machine_material
            ) VALUES (
                '{machine_id}', '{machine_type}', '{machine_product}', '{machine_manufacturer}',
                '{machine_printing_size}', '{machine_material}'
            )
            """
        cur.execute(query)
        self.conn.commit()
        # machine table에 raw가 추가되면 계층구조로 연결된 테이블을 생성
        self.create_machine_sub_table(machine_id)

    def InsertMany_MachineDataWithDF(self):
        # 데이터프레임 생성 (가상의 데이터 사용)
        data = {
            "machine_id": ["id1", "id2", "id3", "id4"],
            "machine_type": ["PBF", "PBF", "PBF", "SLA"],
            "machine_product": ["M160", "M160", "M120", "CMET"],
            "machine_manufacturer": ["Velts", "Velts", "Velts", "Lincsolution"],
            "machine_printing_size": ["size1", "size2", "size3", "size4"],
            "machine_material": ["material1", "material2", "material3", "material4"]
        }
        df = pd.DataFrame(data)
        # 테이블 이름
        table_name = 'machine'
        # SQLAlchemy 엔진 생성
        engine = create_engine(
            f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        # 데이터프레임을 PostgreSQL에g 저장
        df.to_sql(name=table_name, con=engine, schema=self.db_schema, if_exists='append', index=False)
        self.conn.commit()

    def InsertOne_BS_Data(self, bs_create_date, bs_name, design_ids=[]):
        # 데이터 삽입 쿼리
        query = f"""
            INSERT INTO {self.db_schema}.build_strategy (
                bs_create_date, bs_name, design_ids
            ) VALUES (
                '{bs_create_date}', '{bs_name}', ARRAY{design_ids}::integer[]
            )
        """
        self.conn.cursor().execute(query)
        self.conn.commit()

    def InsertOne_BP_Data(self, machine_id, build_date, material_id, bs_id=1):

        # 데이터 삽입 쿼리
        query = f"""
            INSERT INTO {self.db_schema}.machine_{machine_id}_build_process (
                build_date, bs_id, material_id
            ) VALUES (
                '{build_date}', '{bs_id}',  '{material_id}'
            )
        """
        self.conn.cursor().execute(query)
        self.conn.commit()

    def InsertOne_MaterialData(self, material_name, material_manufacturer, material_product):
        material_lot_table_name = material_name + "_lot"
        material_use_table_name = material_name + "_use"
        # 데이터 삽입 쿼리
        query = f"""
            INSERT INTO {self.db_schema}.material_master (
                material_name, material_lot_table_name, material_use_table_name
            ) VALUES (
                '{material_name}', '{material_lot_table_name}', '{material_use_table_name}'
            )
            """

        # TODO: material_name 중복체크
        self.conn.cursor().execute(query)
        self.conn.commit()
        self.create_material_sub_table(material_name)

        # material product 데이터 삽입
        query_insert = f"""
            INSERT INTO {self.db_schema}.material_product (
            material_name, material_manufacturer, material_product_name
            ) VALUES (
            '{material_name}', '{material_manufacturer}', '{material_product}'
            )
            """
        self.conn.cursor().execute(query_insert)
        self.conn.commit()

    def get_material_type(self):
        cur = self.conn.cursor()
        try:
            # 쿼리 생성
            query = sql.SQL("SELECT {} FROM {}.{}").format(
                sql.Identifier("material_name"),
                sql.Identifier(self.db_schema),
                sql.Identifier("material_master")
            )
            # 쿼리 실행
            cur.execute(query)
            # 결과 가져오기
            distinct_values = cur.fetchall()
            result = []
            # 결과 출력
            for value in distinct_values:
                result.append(value)
            return result
        except Exception:
            self.conn.rollback()
            return None

    def get_material_manufacturer(self):
        cur = self.conn.cursor()
        try:
            # 쿼리 생성
            query = sql.SQL("SELECT DISTINCT {} FROM {}.{}").format(
                sql.Identifier("material_manufacturer"),
                sql.Identifier(self.db_schema),
                sql.Identifier("material_product")
            )
            # 쿼리 실행
            cur.execute(query)
            # 결과 가져오기
            distinct_values = cur.fetchall()
            result = []
            # 결과 출력
            for value in distinct_values:
                result.append(value)
            return result
        except Exception:
            self.conn.rollback()
            return None

    def get_machine_type(self):
        cur = self.conn.cursor()
        try:
            # 쿼리 생성
            query = sql.SQL("SELECT DISTINCT {} FROM {}.{}").format(
                sql.Identifier("machine_type"),
                sql.Identifier(self.db_schema),
                sql.Identifier("machine")
            )
            # 쿼리 실행
            cur.execute(query)
            # 결과 가져오기
            distinct_values = cur.fetchall()
            result = []
            # 결과 출력
            for value in distinct_values:
                result.append(value)
            return result
        except Exception:
            self.conn.rollback()
            return None

    def get_machine_product_list(self, machine_type):
        cur = self.conn.cursor()
        try:
            # 쿼리 생성
            query = sql.SQL("SELECT * FROM {}.machine WHERE {} = {}").format(
                sql.Identifier(self.db_schema),
                sql.Identifier("machine_type"),
                sql.Literal(machine_type)
            )
            # 쿼리 실행
            cur.execute(query)
            # 결과 가져오기
            values = cur.fetchall()
            result = []
            # 결과 배열 변환
            for value in values:
                result.append(value[2])
            result = list(set(result))
            return result
        except Exception:
            self.conn.rollback()
            return None

    def get_machine_id(self, machine_type, machine_product):
        cur = self.conn.cursor()
        try:
            # 쿼리 생성
            query = sql.SQL("SELECT * FROM {}.machine WHERE {} = {} AND {} = {}").format(
                sql.Identifier(self.db_schema),
                sql.Identifier("machine_type"),
                sql.Literal(machine_type),
                sql.Identifier("machine_product"),
                sql.Literal(machine_product)
            )
            # 쿼리 실행
            cur.execute(query)
            # 결과 가져오기
            values = cur.fetchall()
            result = []
            # 결과 출력
            for value in values:
                result.append(value[0])

            return result
        except Exception:
            self.conn.rollback()
            return None

    def get_machine_id_list(self):
        cur = self.conn.cursor()
        try:
            # 쿼리 생성
            query = sql.SQL("SELECT * FROM {}.machine").format(
                sql.Identifier(self.db_schema),
            )
            # 쿼리 실행
            cur.execute(query)
            # 결과 가져오기
            values = cur.fetchall()
            result = []
            # 결과 출력
            for value in values:
                result.append(value[0])
            return result
        except Exception:
            self.conn.rollback()
            return None

    def get_material_id(self, material_name, material_manufacturer):
        cur = self.conn.cursor()
        try:
            # 쿼리 생성
            query = sql.SQL("SELECT * FROM {}.material WHERE {} = {} AND {} = {}").format(
                sql.Identifier(self.db_schema),
                sql.Identifier("material_name"),
                sql.Literal(material_name),
                sql.Identifier("material_manufacturer"),
                sql.Literal(material_manufacturer)
            )
            # 쿼리 실행
            cur.execute(query)
            # 결과 가져오기
            values = cur.fetchall()
            if (len(values) == 0):
                # id값 1은 Unknown임
                return 1
            else:
                return values[0][0]
        except Exception:
            self.conn.rollback()
            return None

    def get_material_list(self):
        cur = self.conn.cursor()
        try:
            query = sql.SQL("SELECT * FROM {}.material_master").format(
                sql.Identifier(self.db_schema)
            )
            cur.execute(query)
            values = cur.fetchall()
            return values
        except Exception:
            self.conn.rollback()
            return None

    def get_BS_id(self, bs_create_date, bs_name):

        cur = self.conn.cursor()
        bs_table_name = "build_strategy"
        try:
            # 쿼리 생성
            query = sql.SQL("SELECT * FROM {}.{} WHERE {} = {} AND {} = {}").format(
                sql.Identifier(self.db_schema),
                sql.Identifier(bs_table_name),
                sql.Identifier("bs_create_date"),
                sql.Literal(bs_create_date),
                sql.Identifier("bs_name"),
                sql.Literal(bs_name)
            )
            # 쿼리 실행
            cur.execute(query)
            # 결과 가져오기
            values = cur.fetchall()
            if (len(values) == 0):
                # id값 1은 Unknown임
                return 1
            else:
                return values[0][0]
        except Exception:
            self.conn.rollback()
            return None

    def get_bs_list(self):
        try:
            cur = self.conn.cursor()
            query = sql.SQL("SELECT * FROM {}.build_strategy").format(
                sql.Identifier(self.db_schema)
            )
            cur.execute(query)
            values = cur.fetchall()
            return values
        except Exception as e:
            self.conn.rollback()
            return None


    def get_BP_datetime_list(self, machine_id):
        cur = self.conn.cursor()

        table_name = "machine_" + machine_id + "_build_process"

        try:
            # 쿼리 생성
            query = sql.SQL("SELECT * FROM {}.{}").format(
                sql.Identifier(self.db_schema),
                sql.Identifier(table_name)
            )
            # 쿼리 실행
            cur.execute(query)
            # 결과 가져오기
            values = cur.fetchall()
            result = []
            # 결과 출력
            for value in values:
                result.append(value[1])
            return result
        except:
            self.conn.rollback()
            return None