from lib import CONN, CURSOR


class Employee:
    all = {}

    def __init__(self, name, job_title, department_id, id=None):
        self.id = id
        self.name = name
        self.job_title = job_title
        self.department_id = department_id

    def __repr__(self):
        return f"<Employee {self.id}: {self.name}, {self.job_title}>"

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                job_title TEXT,
                department_id INTEGER
            );
        """)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS employees;")
        CONN.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute(
                "INSERT INTO employees (name, job_title, department_id) VALUES (?, ?, ?);",
                (self.name, self.job_title, self.department_id),
            )
            self.id = CURSOR.lastrowid
            Employee.all[self.id] = self
        else:
            self.update()
        CONN.commit()

    @classmethod
    def create(cls, name, job_title, department_id):
        emp = cls(name, job_title, department_id)
        emp.save()
        return emp

    @classmethod
    def instance_from_db(cls, row):
        emp_id = row[0]
        if emp_id in cls.all:
            return cls.all[emp_id]
        else:
            emp = cls(row[1], row[2], row[3], emp_id)
            cls.all[emp_id] = emp
            return emp

    @classmethod
    def find_by_id(cls, emp_id):
        CURSOR.execute("SELECT * FROM employees WHERE id = ?;", (emp_id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        return None

    def update(self):
        CURSOR.execute(
            "UPDATE employees SET name = ?, job_title = ?, department_id = ? WHERE id = ?;",
            (self.name, self.job_title, self.department_id, self.id),
        )
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM employees WHERE id = ?;", (self.id,))
        CONN.commit()
        if self.id in Employee.all:
            del Employee.all[self.id]
        self.id = None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM employees;")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    def reviews(self):
        from .review import Review
        CURSOR.execute("SELECT * FROM reviews WHERE employee_id = ?;", (self.id,))
        rows = CURSOR.fetchall()
        return [Review.instance_from_db(row) for row in rows]
