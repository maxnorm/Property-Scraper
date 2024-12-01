import os


def calculate_directory_size(directory):
    """
    Calculate the total size of all files in a directory.
    :param directory: Path to the directory
    :return: Total size in bytes
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            total_size += os.path.getsize(file_path)
    return total_size


def format_size(size_in_bytes):
    """
    Format size from bytes to a human-readable format (KB, MB, GB).
    :param size_in_bytes: Size in bytes
    :return: Formatted string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
