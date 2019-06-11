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

    # uses the midpoint method to include both minimum and maximum
    # dividing by band number - 1 because half a range is appended to each end
    if band_number != 1:
        band_size = (max_num - min_num) / (band_number - 1)
    else:
        band_size = 0

    # make the histogram with ranges
    for index in range(band_number):
        # bands[(index * band_size) + min_num] = 0
        min_of_band = (index*band_size) + min_num - (band_size/2)
        max_of_band = (index*band_size) + min_num + (band_size/2)
        bands[(min_of_band,max_of_band)] = 0
    
    # add the numbers to the histogram
    for num in nums:
        if find_band(num, bands) is None:
            breakpoint()
        bands[find_band(num, bands)] += 1
        
    return bands

def find_band(num, ranges_dict):
    """accepts a dictionary with tuple keys of potential ranges and 
    returns the key where the num belongs, returning None if not 
    found"""

    for range_tuple in ranges_dict:
        if range_tuple[0] <= num < range_tuple[1]:
            # if the range is found, exit funcion
            correct_range_tuple = range_tuple
            return correct_range_tuple

    # if the range isn't found, return none
    return None

def print_histogram(bands):
    for band in sorted(bands.keys()):
        # limits decimal places to 1
        band_range = f"{round(band[0],1)}-{round(band[1],1)}"
        print(f"{band_range.rjust(15)} | {'*' * bands[band]}")


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
