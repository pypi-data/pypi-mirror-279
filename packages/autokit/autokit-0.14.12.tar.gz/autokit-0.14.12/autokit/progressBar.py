def print_progress_bar(context, filename, bytes_downloaded, total_size_in_bytes):
    """
    Prints the download progress.
    """

    try:
        import tqdm
    except ImportError:
        tqdm = None

    if tqdm:

        # Create a tqdm progress bar if it doesn't exist
        if not hasattr(context, "pbar"):
            context.pbar = tqdm.tqdm(desc=filename, unit='B', unit_scale=True, unit_divisor=1024, total=total_size_in_bytes, leave=False, dynamic_ncols=True)

        # Update the progress bar
        context.pbar.update(bytes_downloaded - context.pbar.n)

        # Close the progress bar if download is complete
        if bytes_downloaded >= total_size_in_bytes:
            context.pbar.close()

    else:
        print(f"Downloading {filename}: {bytes_downloaded / 1024:.2f}KB / {total_size_in_bytes / 1024:.2f}KB", end='\r')
