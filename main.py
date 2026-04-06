from backend.castingTables import CastToCorrectTypes
from backend.parser import startParsing
from backend.complexity import calculateComplexity
from backend.describe import describeTables


def main():
    """
    This executes the command line interface providing a menu to execute all necessary actions.
    """
    while True:
        print("Please select on what you would like to do:")
        print("0 Exit")
        print("1 Parse XML files to parquet files")
        print("2 Describe all tables")
        print("3 Cast tables to correct types (creates new files called [tableName]_typed.parquet)")
        print("4 Calculate complexity of a file")
        
        action = input()
        if(action == "0"):
            return
        elif(action == "1"):
            startParsing()
        elif(action == "2"):
            describeTables()
        elif(action == "3"):
            CastToCorrectTypes()
        if(action == "4"):
            calculateComplexity()
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()