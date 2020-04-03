import sqlite3
import os.path
import sys
from objects import *

class Database:

    def __init__(self, path="./static/data/map.db"):
        """
        Constructor for DB object. Connects to the sqlite3 database specified by path.
        
        Arguments:
            path -- a String representing the path to the sqlite3 database
        """
        if not os.path.isfile(path):
            print ("Path to sqlite3 database not found in the specified path. Will exit now.")
            sys.exit()
        try:
            self.conn = sqlite3.connect(path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            
        except sqlite3.Error as e:
            print(e)
            sys.exit()
    

    def insert_one(self, sql, data) -> None:
        """
        Insert a row into the sqlite3 database.
        
        Arguments:
            sql  -- a String representing SQL query in the form of a prepared statement
            data -- a dict containing data to be inserted
            
        Returns:
            None
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, data)
        self.conn.commit()
        
    def insert_many(self, sql, data) -> None:
        """
        Insert multiple rows into the sqlite3 database.

        Arguments:
            sql  -- a String representing SQL query in the form of a prepared statement
            data -- list of dict containing data to be inserted

        Returns:
            None
        """
        cursor = self.conn.cursor()
        cursor.executemany(sql, data)
        self.conn.commit()
        
    def select_many(self, sql) -> list:
        """
        Query a list of data from the sqlite3 database.

        Arguments:
            sql  -- a String representing the SQL SELECT query to execute

        Returns:
            List of dict of data for each row, empty list if sqlite3 returns 0 rows
        """
        c = self.conn.cursor()
        result = c.execute(sql).fetchall()
        return [dict(row) for row in result]

    def select_one(self, sql) -> dict:
        """
        Query a singular row from the sqlite3 database.

        Arguments:
            sql  -- a String representing the SQL SELECT query to execute

        Returns:
            Dict representing the row returned, none if sqlite3 returns 0 rows
        """
        c = self.conn.cursor()
        result = c.execute(sql).fetchone()
        return dict(result) if result is not None else None
    
    
    def select_node(self, id=None, name=None, sql=None) -> Node:
        """
        Query a single Node object from the sqlite3 database.

        Arguments:
            id   -- string or int representing the id of the node to search for
            name -- string representing the name of the node to search for
            sql  -- a String representing the SQL SELECT query to execute

        Returns:
            Node object representing the row returned from the SQL query
            None if sqlite3 returns 0 rows
        """
        if (id is not None):
            sql = "SELECT * FROM nodes WHERE id = '{}'".format(id)
            
        elif (name is not None):
            sql = "SELECT * FROM nodes WHERE name = '{}'".format(name)
                    
        result = self.select_one(sql)
        return Node(data=result) if result is not None else None
    
    
    def select_adj_list(self) -> dict:
        """
        Query the edge table in the database and return the data in the form of an adjacency list.
        Note that edges with source/destination that do not exist in the Nodes table will be ommited

        Returns:
            Graph object representing the adjacency list
        """
        c = self.conn.cursor()
        result = self.select_many('''SELECT 
                                        edge.source as source_id,
                                        nodes.name as source_name,
                                        nodes.lat as source_lat,
                                        nodes.long as source_long,
                                        nodes.type as source_type,
                                        nodes.description as source_description,
                                        edge.destination as destination_id,
                                        n2.name as destination_name,
                                        n2.lat as destination_lat,
                                        n2.long as destination_long,
                                        n2.type as destination_type,
                                        n2.description as destination_description,
                                        edge.distance as distance,
                                        edge.bus_service as bus_service,
                                        edge.type as edge_type
                                    FROM nodes
                                    JOIN edge on nodes.id = edge.source
                                    JOIN nodes n2 on n2.id = edge.destination''')
        
        return result