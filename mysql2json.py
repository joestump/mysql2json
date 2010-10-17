import sys
import json
import MySQLdb

host = 'localhost'
user = 'damienfir'
pwd = 'inside'
db_name = 'damienfir_tripin'

class mysql:
    def __init__(self):
        self.connect()
        self.tables = {}
        self.json = ''
    
    def connect(self):
        db = MySQLdb.connect(host=host, user=user, passwd=pwd, db=db_name)
        self.c = db.cursor()
    
    def get_tables(self):
        self.c.execute('SHOW TABLES')
        for table in self.c.fetchall():
            self.tables[table[0]] = []
    
    def get_fields(self, table):
        sql = 'DESCRIBE %s'
        self.c.execute(sql % table)
        ret = []
        for row in self.c.fetchall():
            ret.append(row[0])
        return ret
    
    def get_entries(self):
        sql = 'SELECT %s FROM %s'
        for table in self.tables.iterkeys():
            cols = self.get_fields(table)
            self.c.execute(sql % (','.join(cols), table))
            for row in self.c.fetchall():
                item = {}
                for i in range(0,len(cols)):
                    try:
                        item[cols[i]] = str(row[i])
                    except:
                        print row[i]
            self.tables[table].append(item)
    
    def to_json(self):
        try:
            self.json = json.dumps(self.tables)
        except UnicodeDecodeError as e:
            print 'json error:'
            print e
        return self.json
    
    def export(self):
        if not self.c:
            self.connect()
        self.get_tables()
        self.get_entries()
        return self.to_json()

def main():
    sql = mysql()
    print sql.export()

if __name__ == '__main__':
    main()
