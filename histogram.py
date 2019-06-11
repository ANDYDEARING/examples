def create_histogram(file, band_number):
    """takes a file and a desired number of bands, prints
    the histogram, and returns nothing"""
    nums = get_nums_from_file(file)
    bands = get_bands(nums, band_number)
    print_histogram(bands)


def get_nums_from_file(file):
    """reads numbers from a passed file and returns a list
    of stripped strings converted to floats"""
    nums = []
    with open(file) as fh:
        for line in fh.readlines():
            nums.append(float(line.strip()))
    return nums


def get_bands(nums, band_number):
    """accepts a list of floats and a desired number of bands,
    returning a dictionary of bands and their frequencies. To 
    maximize even data representation, both the maximum and 
    minimum values are included as endpoints"""
    bands = {}
    min_num = min(nums)
    max_num = max(nums)
    band_size = (max_num - min_num) / band_number
    for index in range(band_number):
        bands[(index * band_size) + min_num] = 0
    for num in nums:
        band = num // band_size * band_size + min_num

        # accounts for the special case of the max number to include it
        # in the highest data bucket as the upper limit
        if (band not in bands) and (band - band_size in bands):
            bands[band-band_size] += 1
        else:
            bands[band] += 1
    return bands


def print_histogram(bands):
    for band in sorted(bands.keys()):
        print(f"{str(band).rjust(5)} | {'*' * bands[band]}")


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Create a histogram')
    parser.add_argument('-b', '--band-number', default=10, type=int)
    parser.add_argument('file', help='file to read')
    args = parser.parse_args()

    file = Path(args.file)

    if file.is_file():
        create_histogram(file, args.band_number)
    else:
        print(f"{file} does not exist!")
        exit(1)
