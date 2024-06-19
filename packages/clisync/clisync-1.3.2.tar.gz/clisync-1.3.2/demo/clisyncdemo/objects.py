from typing import Optional
import clisync

class Object():

    @staticmethod
    def create(a: int, b: str, c: Optional[float] = 5.0) -> str:
        """This is a docstring for the create method.

        Args:
            a (int): This is an integer
            b (str): This is a string
            c (float): This is a float

        Returns:
            str: This is a string
        """
        print(f"Creating object with a={a}, b={b}, c={c}")
        return "Object created"

    @staticmethod
    def delete(a: int):
        """This is a docstring for the delete method.

        Args:
            a (int): This is an integer

        Returns:
            None
        """
        pass 

class ObjectControlled():

    @staticmethod
    @clisync.include()
    def create(a: int, b: str, c: float) -> str:
        """This is a docstring for the create method.

        Args:
            a (int): This is an integer
            b (str): This is a string
            c (float): This is a float

        Returns:
            str: This is a string
        """
        print(f"Creating object with a={a}, b={b}, c={c}")
        return "Object created"
    
    @staticmethod
    @clisync.include(c=1)
    def create_with_default(a: int, b: str, c: float = 2.0) -> str:
        """This method is included because of the `expose_cli` decorator.

        Args:
            a (int): This is an integer
            b (str): This is a string
            c (float): This is a float

        Returns:
            str: This is a string
        """
        print(f"Creating object with a={a}, b={b}, c={c}. Parameter c has a default value of 1 in the CLI.")
        return "Object created"

    @staticmethod
    def delete(a: int):
        """This method is not included in the cli."""
        pass 