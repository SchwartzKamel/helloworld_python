"""
main.py
==========================================
Core python file that runs the application
"""
import app.modules.api as api

def hello_world(name: str = "World") -> str:
    """Example of Hello World that has a paramater to display for auto-doc

    Args:
        name (str, optional): Name value. Defaults to "World".
    
    Returns:
        str: Returns "Hello World!" or "Hello {name}!" if a `name` is passed
    """
    print(f"Hello {name}!")

def random_name(api_key: str) -> str:
    name = api.GET_page("https://randommer.io/api/Name", api_key=api_key)

    return name

def main():
    """Main function, core logic of the application
    """
    hello_world()


if __name__ == "__main__":
    main()
