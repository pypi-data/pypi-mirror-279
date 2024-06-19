
"""
Bulk Hasher

Python bindings for bulk hashing of files

Author: Alex Murkoff
"""

def hash_file(filename: str) -> str:
    """
    Hash the contents of the file specified

    Arguments:
        - filename: str - File to hash

    Returns: str - SHA256 hexadecimal representation of hash of the file
    """
    ...

def get_hash_from_file(file_to_hash: str, sha_file: str) -> str:
    """
    Get the stored SHA256 hash of the file specified in the sha_file

    Arguments:
        - file_to_hash: str - File to get the hash of
        - sha_file: str - File containing SHA256 hashes

    Returns: str - SHA256 hash of the file
    """
    ...

def check_hashes_against_file(hash_list_filename: str) -> int:
    """
    Open the file specified and check all files in the file against re-calculated SHA256 hashes, returns the number of mismatched hashes

    Arguments:
        - hash_list_filename: str - File containing SHA256 hashes

    Returns: int - Number of mismatched hashes
    """
    ...

def regenerate_hashes(path: str, out_file: str) -> None:
    """
    Regenerate SHA256 hashes recursively for all files in the directory specified, writing the results to the specified file

    Arguments:
        - path: str - Path to recursively check the files of
        - out_file: str - File to write the hashes of the files to
    
    Returns: None
    """
    ...


def version() -> str:
    """
    Get the version of the program

    Returns: str - Version of the program
    """
    ...
