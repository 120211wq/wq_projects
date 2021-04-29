import sqlite3


class SQLManager():
    def __init__(self):
        self.conn = sqlite3.connect("../test.db",timeout=60)
        self.c = self.conn.cursor()

    def sel_db(self):
        self.c.execute("select name from sqlite_master where type='table' order by name")
        table_list = self.c.fetchall()
        return table_list

    def del_sql(self):
        try:

            self.c.execute('drop table plc_send_history')
            self.c.execute('drop table power_send_history')
            self.c.execute('drop table abnormal_record')
            self.c.execute('drop table box_state')
            self.c.execute('drop table running_box')
        except Exception as a:
            print(a)
            pass

    def create_sql(self):
        try:
            self.c.execute(
                "CREATE TABLE plc_send_history (id integer primary key,box_id INTEGER,plc_data TEXT,is_special INTEGER,box_plc_count INTEGER,plc_count INTEGER,send_time DATE   )")
            self.c.execute(
                "CREATE TABLE power_send_history (id integer primary key,box_id INTEGER,plc_data TEXT,is_special INTEGER,box_power_count INTEGER,power_count INTEGER,send_time DATE   )")
            self.c.execute(
                "CREATE TABLE abnormal_record (id integer primary key,box_id INTEGER,record_reason TEXT,record_time DATE)")
            self.c.execute(
                "CREATE TABLE box_state (id integer primary key,normal_box INTEGER,abnormal_box INTEGER,abnormal_box_list TEXT,record_time DATE)")
            self.c.execute(
                "CREATE TABLE running_box (id integer primary key,box_number INTEGER,box_count INTEGER,runnning_type TEXT,box_type INTEGER,thread_ident TEXT,record_time DATE)")
            self.conn.commit()
            print("已创建数据表")
        except Exception as a:
            print(a)
            pass

    def box_state_sql(self, normal_box, abnormal_box, abnormal_box_list):
        self.c.execute(
            "INSERT INTO box_state (normal_box,abnormal_box,abnormal_box_list,record_time) VALUES (?,?,?,DATETIME('now', 'localtime'))",
            (normal_box, abnormal_box, abnormal_box_list))
        self.conn.commit()

    def record_sql(self, box_id, record_reason):
        self.c.execute(
            "INSERT INTO abnormal_record (box_id,record_reason,record_time) VALUES (?,?,DATETIME('now', 'localtime'))",
            (box_id, record_reason))
        self.conn.commit()

    def qlc_sql(self, box_id, plc_data, is_special, box_plc_count, plc_count):
        self.c.execute(
            "INSERT INTO plc_send_history (box_id,plc_data,is_special,box_plc_count,plc_count,send_time) VALUES (?,?,?,?,?,DATETIME('now', 'localtime'))",
            (box_id, plc_data, is_special, box_plc_count, plc_count))
        self.conn.commit()

    def power_sql(self, box_id, plc_data, is_special, box_power_count, power_count):
        self.c.execute(
            "INSERT INTO power_send_history (box_id,plc_data,is_special,box_power_count,power_count,send_time) VALUES (?,?,?,?,?,DATETIME('now', 'localtime'))",
            (box_id, plc_data, is_special, box_power_count, power_count))
        self.conn.commit()

    def register_sql(self, box_id, ip_addres, ip_port):
        self.c.execute(
            "INSERT INTO register(box_id,ip_addres,ip_port) VALUES (?,?,?)",
            (box_id, ip_addres, ip_port))
        self.conn.commit()

    def create_register_sql(self):
        self.c.execute(
            "CREATE TABLE register(id integer primary key,box_id INTEGER,ip_addres TEXT,ip_port INTEGER)")
        self.conn.commit()

    def sel_box(self, sel_value):
        print(sel_value)
        try:
            self.c.execute(
                sel_value)
            values = self.c.fetchall()
            return values
        except Exception as e:
            return e

    def insert_spl(self,sel_value):
        self.c.execute(
            sel_value)
        self.conn.commit()


if __name__ == '__main__':
    c = SQLManager()
    box_num = 23412323
    ident = 21434
    sql = "select box_id from register where box_id = " + "23412323"
    # c.register_sql(box_num, '106.75.148.235', '8765')
    value = c.sel_box(sql)
    print(len(value))