# pylint:disable=C0111,C0103

def detailed_orders(db):
    '''return a list of all orders (order_id, customer.contact_name,
    employee.firstname) ordered by order_id'''
    query = "SELECT o.OrderID, c.ContactName, e.FirstName  \
            FROM Customers c \
            JOIN Orders o ON o.CustomerID = c.CustomerID \
            JOIN Employees e ON e.EmployeeID = o.EmployeeID \
            GROUP BY o.OrderID \
            ORDER BY o.OrderID ASC"
    db.execute(query)
    results = db.fetchall()
    return results

def spent_per_customer(db):
    query = '''SELECT c.ContactName , \
                SUM(SUM(od.UnitPrice * od.Quantity)) OVER ( \
                    PARTITION BY od.OrderID   \
                    ORDER BY od.OrderDetailID  \
                ) AS total_amount_spent \
                FROM OrderDetails od \
                JOIN Orders o ON o.OrderID = od.OrderID \
                JOIN Customers c ON c.CustomerID = o.CustomerID \
                GROUP BY o.CustomerID  \
                ORDER BY total_amount_spent ASC'''
    db.execute(query)
    results = db.fetchall()
    return results

def best_employee(db):
    '''Implement the best_employee method to determine who’s the best employee!
    By “best employee”, we mean the one who sells the most.
    We expect the function to return a tuple like: ('FirstName', 'LastName',
    6000 (the sum of all purchase)). The order of the information is irrelevant
    '''
    query = "SELECT e.FirstName , e.LastName,\
            SUM(SUM(od.UnitPrice * od.Quantity)) OVER (\
                PARTITION BY od.OrderID   \
                ORDER BY od.ProductID  \
            ) AS total_amount_sold\
            FROM Employees e \
            JOIN Orders o ON o.EmployeeID = e.EmployeeID \
            JOIN OrderDetails od ON od.OrderID = o.OrderID  \
            GROUP BY e.EmployeeID ORDER BY total_amount_sold DESC"
    db.execute(query)
    results = db.fetchall()
    return results[0]

def orders_per_customer(db):
    '''Return a list of tuples where each tuple contains the contactName
    of the customer and the number of orders they made (contactName,
    number_of_orders). Order the list by ascending number of orders'''
    query = "SELECT c.ContactName, COUNT((o.OrderID)) AS sold_count \
            FROM Customers c  \
            LEFT JOIN Orders o ON o.CustomerID = c.CustomerID \
            GROUP BY c.ContactName \
            ORDER BY sold_count ASC"
    db.execute(query)
    results = db.fetchall()
    return results
